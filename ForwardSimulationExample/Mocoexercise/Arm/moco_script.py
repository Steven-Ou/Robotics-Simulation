import opensim as osim
import sys
import os
import numpy as np
import helpers

model = helpers.getTorqueDrivenModel()

study = osim.MocoStudy()
problem = study.updProblem()
problem.setModel(model)

problem.setTimeBounds(0, 1)

problem.setStateInfo("/jointset/shoulder0/elv_angle/value", [-1.5, 2.0], 0, 0)
problem.setStateInfo("/jointset/shoulder1/shoulder_elv/value", [0, 3.5], 0, 0)
problem.setStateInfo("/jointset/shoulder2/shoulder_rot/value", [0, 2.5], 0, 0)
problem.setStateInfo("/jointset/elbow/elbow_flexion/value", [0.0, 3.14159], 0, 0)
problem.setStateInfo(
    "/jointset/radioulnar/pro_sup/value", [-3.14159, 3.14159], 0, -3.14159
)
problem.setStateInfoPattern("/jointset/.*/flexion/value", [-1.5708, 1.5708], 0, 1.5708)
problem.setStateInfoPattern("/jointset/.*/deviation/value", [-0.5, 0.5], 0, 0.5)

problem.setStateInfoPattern("/jointset/.*/speed", [], 0, 0)
problem.setStateInfoPattern("/forceset/.*/activation", [0, 1], 0)
problem.setControlInfoPattern("/forceset/.*", [0, 1])

problem.addGoal(osim.MocoControlGoal("myeffort", 1))
solver = study.initCasADiSolver()
solver.set_num_mesh_intervals(30)
solver.set_optim_convergence_tolerance(10)
solver.set_optim_constraint_tolerance(10)
solver.set_optim_max_iterations(1000)


if not os.path.isfile("predictSolution.sto"):
    predictSolution = study.solve()
    solutionUnsealed = predictSolution.unseal()
    solutionUnsealed.write("solutionUnsealed.sto")
    # study.visualize(solutionUnsealed)
