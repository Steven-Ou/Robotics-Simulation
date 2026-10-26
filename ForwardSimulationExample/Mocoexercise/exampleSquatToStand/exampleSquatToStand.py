## Part 0: Load the Moco libraries and pre-configured Models.
# These models are provided for you (i.e., they are not part of Moco).
import opensim as osim
import exampleSquatToStand_helpers as helpers
import mocoPlotTrajectory as plot
import os
import numpy as np
torqueDrivenModel = helpers.getTorqueDrivenModel()
muscleDrivenModel = helpers.getMuscleDrivenModel()

## Part 1: Torque-driven Predictive Problem
# Part 1a: Create a new MocoStudy.
study = osim.MocoStudy()

# Part 1b: Initialize the problem and set the model.
problem = study.updProblem()
problem.setModel(torqueDrivenModel)

# Part 1c: Set bounds on the problem.
#
# problem.setTimeBounds(initial_bounds, final_bounds)
# problem.setStateInfo(path, trajectory_bounds, inital_bounds, final_bounds)
#
# All *_bounds arguments can be set to a range, [lower upper], or to a
# single value (equal lower and upper bounds). Empty brackets, [], indicate
# using default bounds (if they exist). You may set multiple state infos at
# once using setStateInfoPattern():
#
# problem.setStateInfoPattern(pattern, trajectory_bounds, inital_bounds, ...
#       final_bounds)
#
# This function supports regular expressions in the 'pattern' argument;
# use '.*' to match any substring of the state/control path
# For example, the following will set all coordinate value state infos:
#
# problem.setStateInfoPattern('/path/to/states/.*/value', ...)

# Time bounds
problem.setTimeBounds(0, 1)

# Position bounds: the model should start in a squat and finish 
# standing up.
problem.setStateInfo('/jointset/hip_r/hip_flexion_r/value', 
    [-2, 0.5], -2, 0)
problem.setStateInfo('/jointset/knee_r/knee_angle_r/value', 
    [-2, 0], -2, 0)
problem.setStateInfo('/jointset/ankle_r/ankle_angle_r/value', 
    [-0.5, 0.7], -0.5, 0)

# Velocity bounds: all model coordinates should start and end at rest.
problem.setStateInfoPattern('/jointset/.*/speed', [], 0, 0)

# Part 1d: Add a MocoControlCost to the problem.
problem.addGoal(osim.MocoControlGoal('myeffort'))

# Part 1e: Configure the solver.
solver = study.initCasADiSolver()
solver.set_num_mesh_intervals(25)
solver.set_optim_convergence_tolerance(1e-4)
solver.set_optim_constraint_tolerance(1e-4)

if not os.path.isfile('predictSolution.sto'):
    # Part 1f: Solve! Write the solution to file, and visualize.
    predictSolution = study.solve()
    predictSolution.write('predictSolution.sto')
    study.visualize(predictSolution)
