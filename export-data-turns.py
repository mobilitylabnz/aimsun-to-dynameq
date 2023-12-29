#------------------------------------------------------------
#                                       
# Mobility Lab                            
#                 
# caleb@mobilitylab.co.nz
# 2023
#                    
#------------------------------------------------------------

# This scripts exports the turn data for the scenario selected

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

filePath = os.path.join(os.path.dirname(str(model.getDocumentFileName())), 'DYNAMEQ-Aimsun-Files', 'turnings.csv')

turnType = model.getType("GKTurning")
with open(filePath, 'w') as f:
	f.write('id,id_node,speed,fsection,tsection,flaneA,flaneB,tlaneA,tlaneB,sign,geometry\n')
	for turn in model.getCatalog().getObjectsByType( turnType ).values():
		if turn.exists(scenario):
			# id
			id = turn.getId()
			# get the node id
			id_node = turn.getNode().getId()
			# speed
			speed = turn.getSpeed()
			# from section
			fsection = turn.getOrigin().getId()
			# to section
			tsection = turn.getDestination().getId()
			#from lanes
			flaneA = turn.getOriginFromLane()
			flaneB = turn.getOriginToLane()
			# to lanes
			tlaneA = turn.getDestinationFromLane()
			tlaneB = turn.getDestinationToLane()
			# sign
			sign = turn.getWarningIndicator()
			# write out the linestring for conversion to a shapefile
			# get the points along the polyline
			points = turn.getPoints()
			start_point = points[0]
			end_point = points[-1]
			line_wkt = f'"LINESTRING ({start_point.x} {start_point.y}, {end_point.x} {end_point.y})"'

			f.write(f"{id},{id_node},{speed},{fsection},{tsection},{flaneA},{flaneB},{tlaneA},{tlaneB},{sign},{line_wkt}\n")


print('Finished Exporting Turn File')