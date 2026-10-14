import opensim as osim
import sys

model_filename = "gait9dof18musc_Thelen_BigSpheres_20160914.osim"

model = osim.Model(model_filename)

state = model.initSystem()
model.setUseVisualizer(True)

init_state = [0.0, 2.0, 3.5, 0.0, 1.5, 0, 0, 0, 0, 0]

editableCoordSet = model.updCoordinateSet()
for i in range(0, editableCoordSet.getSize()):
    editableCoordSet.get(i).setValue(state, init_state[i])

manager = osim.Manager(model)
finalTime = 1
dt =0.001
integrator = osim.SemiExplicitEuler2Integrator(model.getSystem())
integrator.setFixedStepSize(dt)


manager.setIntegratorAccuracy(1e-10) #more accurate
manager = osim.Manager(model, integrator)
manager.initialize(state)
manager.integrate(finalTime)

statesDegrees = manager.getStateStorage()
states_table = manager.getStatesTable()
osim.STOFileAdapter.write(states_table, "forwardSimulation.sto")
