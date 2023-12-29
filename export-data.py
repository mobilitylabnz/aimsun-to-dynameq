#------------------------------------------------------------
#                                       
# Mobility Lab                            
#                 
# caleb@mobilitylab.co.nz
# 2023
#                    
#------------------------------------------------------------

# This script exports the necessary files required for the DYNAMEQ Aimsun import tool. Files exported include:
# - bus stops
# - centroids
# - centroid connections
# - nodes
# - sections
# - signals
# - transit lines
# - turns

# Note:
# This script will split merged nodes into individual nodes. If centroids are connected to nodes, this may delete them - the script to split nodes is run after centroid and centroid connection data is exported
# A scenario id is required as the input into the script and only sections, nodes etc. contained within that scenario are exported.
# Files are exported into a folder called 'DYNAMEQ-Aimsun-Files'

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

# Select the scenario
def getScenario():
	genericScenarioType = model.getType("GKGenericScenario")

	dialog = GAnyObjectChooserEditor()
	chooser = dialog.getChooser()
	chooser.setType(genericScenarioType, GAnyObjectChooser.ChooserMode.eOneObject)
	dialog.setShowNoObjectsMessage(True)
	acceptedRejected = dialog.execDialog()
	if acceptedRejected:
		return chooser.getObject()
	print ("no scenario selected")
	return

scenario = getScenario()

# set the export location and create the folder if it doesn't exist
folderPath = os.path.join(os.path.dirname(str(model.getDocumentFileName())), 'DYNAMEQ-Aimsun-Files')
# Check if the folder exists
if not os.path.exists(folderPath):
	# If not, create the folder
	os.makedirs(folderPath)
	print(f"Folder '{folderPath}' created.")
else:
	print(f"Folder '{folderPath}' already exists.")

# run the scripts for individual file exports
model.getCatalog().findByName('export-data-centroids', model.getType('GKScript')).execute(scenario)
model.getCatalog().findByName('export-data-centroid-connections', model.getType('GKScript')).execute(scenario)
model.getCatalog().findByName('split-nodes', model.getType('GKScript')).execute(scenario)
model.getCatalog().findByName('export-data-nodes', model.getType('GKScript')).execute(scenario)
model.getCatalog().findByName('export-data-sections', model.getType('GKScript')).execute(scenario)
model.getCatalog().findByName('export-data-signals', model.getType('GKScript')).execute(scenario)
model.getCatalog().findByName('export-data-transit', model.getType('GKScript')).execute(scenario)
model.getCatalog().findByName('export-data-turns', model.getType('GKScript')).execute(scenario)


print('Finished Exporting All Files')