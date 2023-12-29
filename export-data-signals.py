#------------------------------------------------------------
#                                       
# Mobility Lab                            
#                 
# caleb@mobilitylab.co.nz
# 2023
#                    
#------------------------------------------------------------

# This scripts exports the control plan junctions and control plan signals for the selected scenario

#------------------------------------------------------------
# DISCLAIMER
#------------------------------------------------------------
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os

# Define the scenario
scenario = target

filePathCPJ = os.path.join(os.path.dirname(str(model.getDocumentFileName())), 'DYNAMEQ-Aimsun-Files', 'cp_junctions.csv')
filePathCPS = os.path.join(os.path.dirname(str(model.getDocumentFileName())), 'DYNAMEQ-Aimsun-Files', 'cp_signals.csv')

# Export the control plan junctions to a csv
with open(filePathCPJ, 'w') as f:
	# write the heading
	f.write(f'CP_ID,CP_Name,CP_EID,CP_InitialTime,Node_ID,CPJ_Type,CPJ_CycleTime,CPJ_OffsetTime,CPJ_GreenToRedTime,CPJ_RedPercentage,CPP_PhasesIndex,CPP_PhasesDuration,CPP_PhasesInterphase,CPP_PhaseSignals\n')
	# for the control plans used in the scenario
	mcp = scenario.getMasterControlPlan()
	schedule_cp = mcp.getSchedule()
	objType = model.getType("GKControlPlan")
	for schedule in schedule_cp:
		CP = schedule.getControlPlan()
		for NodeId in CP.getControlJunctions():
			CPJ = CP.getControlJunctions()[NodeId]
			for CPP in CPJ.sortPhases():
				# format phase signal into a string list
				signalList = []
				for CPS in CPP.getSignals():
					signalList.append(int(CPS.getSignal().getId()))
				signalListString = str(signalList).replace(',',';').replace("u'","'")
				interphase = CPP.getInterphase()
				if interphase == "FALSE":
					interphase = 0
				elif interphase == "TRUE":
					interphase = 1
				f.write(
						f"{CP.getId()},"
						f"{CP.getName().replace(',', '').strip()},"
						f"{CP.getExternalId().replace(',', '').strip()},"
						f"{QTime.fromMSecsSinceStartOfDay(CP.getOffset()*1000).toString('HH:mm:ss')},"
						f"{str(NodeId)},"
						f"{CPJ.getControlJunctionType()},"
						f"{CPJ.getCycle()},"
						f"{CPJ.getOffset()},"
						f"{CPJ.getYellowTime()},"
						f"{CPJ.getRedPercentageInYellowTime()},"
						f"{CPJ.getPhaseIndex(CPP)+1},"
						f"{CPP.getDuration()},"
						f"{interphase},"
						f"{signalListString}\n"
					)


# Export the control plan signals to CSV
with open(filePathCPS, 'w') as f:
	# write the heading
	f.write(f'CPS_ID,CPS_Node_ID,CPS_Turnings\n')
	# for all the Control Plans Signals in the model
	objType = model.getType("GKControlPlanSignal")
	for CPS in GK.GetObjectsOfType(objType):
		# format turn ids into a string list
		turnList = []
		for turning in CPS.getTurnings():
			turnList.append(int(turning.getId()))
		turnListString = str(turnList).replace(',',';').replace("u'","'")
		# get vehicle class id
		vehClass = CPS.getVehicleClass()
		if vehClass is None:
			vehClassId = 0
		else:
			vehClassId = vehClass.getId()
		f.write(f"{CPS.getId()},{CPS.getNode().getId()},{turnListString}\n")

print('Finished Exporting Signal Data')