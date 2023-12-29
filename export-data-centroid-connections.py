#------------------------------------------------------------
#                                       
# Mobility Lab                            
#                 
# caleb@mobilitylab.co.nz
# 2023
#                    
#------------------------------------------------------------

# This scripts exports the centroid connections in the model - a set of demand in the scenario must be defined

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

filePath = os.path.join(os.path.dirname(str(model.getDocumentFileName())), 'DYNAMEQ-Aimsun-Files', 'centroid_connections.csv')

centroidType = model.getType("GKCentroid")
with open(filePath, 'w') as f:
	f.write('id_cent,id_object,obj_type,direction,geometry\n')

	# get the traffic demand from the scenario and then the related centroid configuration
	demand = scenario.getDemand()
	cent_config = demand.getCentroidConfigurations()[0]

	for centroid in cent_config.getCentroids():
		# id
		id = centroid.getId()
		print(id)
		connections = centroid.getConnections()
		for connection in connections:
			conn_obj = connection.getConnectionObject()
			if conn_obj.exists(scenario):
				id_object = conn_obj.getId()
				obj_type = conn_obj.getType().getName()
				if obj_type == "GKSection":
					obj_type = "section"
				elif obj_type == "GKNode":
					obj_type = "node"
				conn_type = connection.getConnectionType()
				if conn_type == 1:
					direction = "from"
				elif conn_type == 2:
					direction = "to"
				
				
				points = connection.getPoints()
				line_wkt = f'"LINESTRING ({", ".join([f"{p.x} {p.y}" for p in points])})"'



				f.write(f"{id},{id_object},{obj_type},{direction},{line_wkt}\n")

print('Finished Exporting Centroid Connections')