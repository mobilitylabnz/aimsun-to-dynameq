#------------------------------------------------------------
#                                       
# Mobility Lab                            
#                 
# caleb@mobilitylab.co.nz
# 2023
#                    
#------------------------------------------------------------

# This scripts exports data for the sections in the scenario selected

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

filePathf = os.path.join(os.path.dirname(str(model.getDocumentFileName())), 'DYNAMEQ-Aimsun-Files', 'sections.csv')
filePathg = os.path.join(os.path.dirname(str(model.getDocumentFileName())), 'DYNAMEQ-Aimsun-Files', 'lane_width.csv')
filePathh = os.path.join(os.path.dirname(str(model.getDocumentFileName())), 'DYNAMEQ-Aimsun-Files', 'section_lanes.csv')
filePathi = os.path.join(os.path.dirname(str(model.getDocumentFileName())), 'DYNAMEQ-Aimsun-Files', 'reserved_lanes.csv')

sectionType = model.getType("GKSection")
with open(filePathf, 'w') as f, open(filePathg, 'w') as g, open(filePathh, 'w') as h, open(filePathi, 'w') as i:
	f.write('id,fnode,tnode,nb_lanes,speed,name,capacity,rd_type,func_class,geometry\n')
	g.write('id,lane_width\n')
	h.write('Section_ID,Section_Lane_Index,Section_Lane_Length,Section_Lane_Type\n')
	i.write('Section_ID,Lane,Lanetype,Time_Range\n')
	for section in model.getCatalog().getObjectsByType( sectionType ).values():
		if section.exists(scenario):
			# id
			id = section.getId()
			# fnode
			try:
				fnode = section.getOrigin().getId()
			except:
				fnode = ""
			# tnode
			try:
				tnode = section.getDestination().getId()
			except:
				tnode = ""

			if fnode != tnode:
				# nb_lanes
				nb_lanes = len(section.getLanes())
				# speed
				speed = section.getSpeed()
				# Name
				name = section.getName()
				# capacity
				capacity = section.getCapacity()
				# rd_type
				rd_type = section.getRoadType().getId()
				# func_class
				func_class = section.getDataValueInt(sectionType.getColumn("GKSection::functionalClassAtt",0))

				# write out the linestring for conversion to a shapefile
				# get the points along the polyline
				points = section.getPoints()
				line_wkt = f'"LINESTRING ({", ".join([f"{p.x} {p.y}" for p in points])})"'

				f.write(f"{id},{fnode},{tnode},{nb_lanes},{speed},{name},{capacity},{rd_type},{func_class},{line_wkt}\n")

				# lane_width
				lane_width = section.getLaneWidth()
				g.write(f"{id},{lane_width}\n")

				for n, lane in enumerate(section.getLanes()):
					if lane.isFullLane():
						laneType = 'Full'
						lane_len = section.length2D()
					elif lane.isAnEntryLateral():
						laneType = 'Short_Entry'
						lane_len = lane.getSideLaneLength2D()
					elif lane.isAnExitLateral():
						laneType = 'Short_Exit'
						lane_len = lane.getSideLaneLength2D()
					h.write(f"{id},{n},{lane_len},{laneType}\n")
					
					if lane.getLaneType() != None:
						reserved_type = lane.getLaneType().getId()
						i.write(f"{id},{n+1},{reserved_type},00:00-24:00\n")
					

print('Finished Exporting Section Data')