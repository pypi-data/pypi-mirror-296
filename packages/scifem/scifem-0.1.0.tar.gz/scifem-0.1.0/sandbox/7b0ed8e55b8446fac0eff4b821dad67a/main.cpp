// Hand coded Real space
// Author: Jørgen S. Dokken
// SPDX Licence: MIT

#include <basix/finite-element.h>
#include <cmath>
#include <concepts>
#include <cstdlib>
#include <dolfinx/common/IndexMap.h>
#include <dolfinx/common/log.h>
#include <dolfinx/fem/DofMap.h>
#include <dolfinx/fem/ElementDofLayout.h>
#include <dolfinx/fem/FiniteElement.h>
#include <dolfinx/fem/Form.h>
#include <dolfinx/fem/FunctionSpace.h>
#include <dolfinx/fem/petsc.h>
#include <dolfinx/fem/utils.h>
#include <dolfinx/io/ADIOS2Writers.h>
#include <dolfinx/la/MatrixCSR.h>
#include <dolfinx/la/petsc.h>
#include <dolfinx/mesh/Mesh.h>
#include <dolfinx/mesh/cell_types.h>
#include <dolfinx/mesh/generation.h>
#include <dolfinx/mesh/utils.h>
#include <filesystem>
#include <mpi.h>
#include <numbers>
#include <poisson.h>

using namespace dolfinx;

/// @brief This program shows how to create finite element spaces without FFCx
/// generated code.
int main(int argc, char* argv[])
{
  dolfinx::init_logging(argc, argv);
  PetscInitialize(&argc, &argv, nullptr, nullptr);

  // The main body of the function is scoped to ensure that all objects
  // that depend on an MPI communicator are destroyed before MPI is
  // finalised at the end of this function.
  {
    if (argc < 2)
    {
      std::cerr << "Usage: ./demo_real_space N" << std::endl;
      return 1;
    }

    std::int64_t N = atoi(argv[1]);

    // Create mesh using double for geometry coordinates
    auto mesh0
        = std::make_shared<mesh::Mesh<double>>(mesh::create_rectangle<double>(
            MPI_COMM_WORLD, {{{0.0, 0.0}, {1, 1}}}, {N, N},
            mesh::CellType::triangle,
            mesh::create_cell_partitioner(mesh::GhostMode::none)));
    std::shared_ptr<const dolfinx::fem::FunctionSpace<double>> Q = nullptr;
    {
      basix::FiniteElement e_v = basix::create_element<double>(
          basix::element::family::P,
          mesh::cell_type_to_basix_type(mesh::CellType::triangle), 0,
          basix::element::lagrange_variant::unset,
          basix::element::dpc_variant::unset, true);

      // NOTE: Optimize input source/dest later as we know this a priori
      std::int32_t num_dofs = (dolfinx::MPI::rank(MPI_COMM_WORLD) == 0) ? 1 : 0;
      std::int32_t num_ghosts
          = (dolfinx::MPI::rank(MPI_COMM_WORLD) != 0) ? 1 : 0;
      std::vector<std::int64_t> ghosts(num_ghosts, 0);
      ghosts.reserve(1);
      std::vector<int> owners(num_ghosts, 0);
      owners.reserve(1);
      std::shared_ptr<const dolfinx::common::IndexMap> imap
          = std::make_shared<const dolfinx::common::IndexMap>(
              MPI_COMM_WORLD, num_dofs, ghosts, owners);
      int index_map_bs = 1;
      int bs = 1;
      // Element dof layout
      fem::ElementDofLayout dof_layout(1, e_v.entity_dofs(),
                                       e_v.entity_closure_dofs(), {}, {});
      std::size_t num_cells_on_process
          = mesh0->topology()->index_map(mesh0->topology()->dim())->size_local()
            + mesh0->topology()
                  ->index_map(mesh0->topology()->dim())
                  ->num_ghosts();

      std::vector<std::int32_t> dofmap(num_cells_on_process, 0);
      dofmap.reserve(1);
      std::shared_ptr<const dolfinx::fem::DofMap> real_dofmap
          = std::make_shared<const dolfinx::fem::DofMap>(
              dof_layout, imap, index_map_bs, dofmap, bs);
      std::vector<std::size_t> value_shape(0);

      std::shared_ptr<const dolfinx::fem::FiniteElement<double>> d_el
          = std::make_shared<const dolfinx::fem::FiniteElement<double>>(e_v, 1,
                                                                        false);

      Q = std::make_shared<const dolfinx::fem::FunctionSpace<double>>(
          mesh0, d_el, real_dofmap, value_shape);
    }

    auto e_u = basix::create_element<double>(
        basix::element::family::P, basix::cell::type::triangle, 1,
        basix::element::lagrange_variant::unset,
        basix::element::dpc_variant::unset, false);
    auto V = std::make_shared<const fem::FunctionSpace<double>>(
        fem::create_functionspace(mesh0, e_u));

    // Define variational forms
    auto a00 = std::make_shared<fem::Form<double>>(
        fem::create_form<double>(*form_poisson_a00, {V, V}, {}, {{}}, {}, {}));
    auto a01 = std::make_shared<fem::Form<double>>(
        fem::create_form<double>(*form_poisson_a01, {V, Q}, {}, {{}}, {}, {}));
    auto a10 = std::make_shared<fem::Form<double>>(
        fem::create_form<double>(*form_poisson_a10, {Q, V}, {}, {{}}, {}, {}));

    std::vector<std::vector<const dolfinx::fem::Form<double, double>*>> as;
    std::vector<const dolfinx::fem::Form<double, double>*> a0
        = {a00.get(), a01.get()};
    as.push_back(a0);
    std::vector<const dolfinx::fem::Form<double, double>*> a1
        = {a10.get(), nullptr};
    as.push_back(a1);
    Mat A = dolfinx::fem::petsc::create_matrix_block(as);
    std::vector<std::pair<std::reference_wrapper<const common::IndexMap>, int>>
        maps;
    maps.push_back({*V->dofmap()->index_map, V->dofmap()->index_map_bs()});
    maps.push_back({*Q->dofmap()->index_map, Q->dofmap()->index_map_bs()});
    std::vector<IS> index_sets = dolfinx::la::petsc::create_index_sets(maps);
    MatZeroEntries(A);
    for (std::size_t i = 0; i < as.size(); ++i)
    {
      for (std::size_t j = 0; j < as[i].size(); ++j)
      {
        if (as[i][j])
        {
          Mat Asub;
          MatGetLocalSubMatrix(A, index_sets[i], index_sets[j], &Asub);
          fem::assemble_matrix(
              la::petsc::Matrix::set_block_fn(Asub, ADD_VALUES), *as[i][j], {});
          MatRestoreLocalSubMatrix(A, index_sets[i], index_sets[j], &Asub);
          MatDestroy(&Asub);
        }
      }
    }

    MatAssemblyBegin(A, MAT_FINAL_ASSEMBLY);
    MatAssemblyEnd(A, MAT_FINAL_ASSEMBLY);

    // Create vectors
    Vec b = dolfinx::fem::petsc::create_vector_block(maps);
    VecZeroEntries(b);
    std::vector<std::vector<PetscScalar>> local_vecs
        = dolfinx::la::petsc::get_local_vectors(b, maps);
    auto L = std::make_shared<fem::Form<double>>(
        fem::create_form<double>(*form_poisson_L, {V}, {}, {{}}, {}, {}));
    fem::assemble_vector(std::span(local_vecs[0].data(), local_vecs[0].size()),
                         *L);

    std::vector<std::span<const double>> lv;
    lv.reserve(2);
    for (auto& l : local_vecs)
      lv.push_back(std::span<const double>(l.data(), l.size()));
    dolfinx::la::petsc::scatter_local_vectors(b, lv, maps);
    VecGhostUpdateBegin(b, ADD_VALUES, SCATTER_REVERSE);
    VecGhostUpdateEnd(b, ADD_VALUES, SCATTER_REVERSE);

    la::petsc::KrylovSolver lu(MPI_COMM_WORLD);
    la::petsc::options::set("ksp_type", "preonly");
    la::petsc::options::set("pc_type", "lu");
    la::petsc::options::set("pc_factor_mat_solver_type", "mumps");
    lu.set_from_options();

    lu.set_operator(A);
    Vec _u = dolfinx::fem::petsc::create_vector_block(maps);

    lu.solve(_u, b);

    std::vector<std::vector<PetscScalar>> local_out
        = dolfinx::la::petsc::get_local_vectors(_u, maps);
    std::shared_ptr<dolfinx::fem::Function<double>> u
        = std::make_shared<dolfinx::fem::Function<double>>(V);
    std::span<double> u_arr = u->x()->mutable_array();
    std::copy(local_out[0].begin(), local_out[0].end(), u_arr.begin());
    u->x()->scatter_fwd();

    auto J = std::make_shared<fem::Form<double>>(fem::create_form<double>(
        *form_poisson_J, {}, {{"uh", u}}, {{}}, {}, {}, V->mesh()));

    double error_local = fem::assemble_scalar(*J);
    double error_global;

    MPI_Allreduce(&error_local, &error_global, 1, MPI_DOUBLE, MPI_SUM,
                  MPI_COMM_WORLD);
    if (dolfinx::MPI::rank(MPI_COMM_WORLD) == 0)
      std::cout << "N" << N << " Error: " << std::sqrt(error_global)
                << std::endl;

    io::VTXWriter<double> file(MPI_COMM_WORLD, "u.bp", {u}, "BP5");
    file.write(0.0);
    file.close();
    VecDestroy(&b);
    MatDestroy(&A);
  }
  return 0;

  PetscFinalize();
}