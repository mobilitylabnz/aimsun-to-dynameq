#------------------------------------------------------------
#                                       
# Mobility Lab                            
#                 
# caleb@mobilitylab.co.nz
# 2023
#                    
#------------------------------------------------------------

# This scripts exports the nodes in the scenario selected

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

folderPath = os.path.join(os.path.dirname(str(model.getDocumentFileName())), 'DYNAMEQ-Aimsun-Files', 'nodes.csv')

nodeType = model.getType("GKNode")
with open(folderPath, 'w') as f:
	f.write('id,name,geometry\n')

	for node in model.getCatalog().getObjectsByType( nodeType ).values():
		if node.exists(scenario):
			# id
			id = node.getId()
			name = node.getName()
			point = node.getPosition()
			point_wkt = f'"POINT ({point.x} {point.y})"'

			f.write(f"{id},{name},{point_wkt}\n")

print('Finished Exporting Nodes')