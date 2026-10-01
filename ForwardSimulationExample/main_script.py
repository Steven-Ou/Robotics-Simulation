import opensim as osim
import sys

model_filename = "gait9dof18musc_Thelen_BigSpheres_20160914.osim"

model = osim.Model(model_filename)

state = model.initSystem()
model.setUseVisualizer(True)

init_state = [0.0, 0.0, 0.7, 1.2, -1.5, 0.0, 1.2, -1.5, 0.0, 0.0]

editableCoordSet = model.updCoordinateSet()

for i in range(0, editableCoordSet.getSize()):
    editableCoordSet.get(i).setValue(state, init_state[i])

manager = osim.Manager(model)
finalTime = 1.0
manager.initialize(state)
manager.integrate(finalTime)

statesTable = manager.getStatesTable()
osim.STOFileAdapter.write(statesTable, "forwardSimulation.sto")
