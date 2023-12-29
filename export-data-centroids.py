#------------------------------------------------------------
#                                       
# Mobility Lab                            
#                 
# caleb@mobilitylab.co.nz
# 2023
#                    
#------------------------------------------------------------

# This scripts exports the centroids in the model - a set of demand in the scenario must be defined

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

folderPath = os.path.join(os.path.dirname(str(model.getDocumentFileName())), 'DYNAMEQ-Aimsun-Files', 'centroids.csv')

centroidType = model.getType("GKCentroid")
with open(folderPath, 'w') as f:
	f.write('id,name,geometry\n')

	# get the traffic demand from the scenario and then the related centroid configuration
	demand = scenario.getDemand()
	cent_config = demand.getCentroidConfigurations()[0]

	for centroid in cent_config.getCentroids():
		if centroid.exists(scenario):
			# id
			id = centroid.getId()
			name = centroid.getName()
			point = centroid.getPosition()
			point_wkt = f'"POINT ({point.x} {point.y})"'

			f.write(f"{id},{name},{point_wkt}\n")

print('Finished Exporting Centroids')