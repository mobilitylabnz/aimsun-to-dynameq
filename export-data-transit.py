#------------------------------------------------------------
#                                       
# Mobility Lab                            
#                 
# caleb@mobilitylab.co.nz
# 2023
#                    
#------------------------------------------------------------

# This scripts exports the pt line data and timings

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

filePathPTLines = os.path.join(os.path.dirname(str(model.getDocumentFileName())), 'DYNAMEQ-Aimsun-Files', 'pt_lines.csv')
filePathPTTimings = os.path.join(os.path.dirname(str(model.getDocumentFileName())), 'DYNAMEQ-Aimsun-Files', 'pt_timings.csv')

# this function write the Bus line paramters to CSV

with open(filePathPTLines, 'w') as f:
	# write the heading
	f.write('PTLine_ID,PTLine_Name,PTLine_EID,PTLine_SubNet,PTLine_Route,PTLine_Stops,PTLine_StopDists,PTLine_TimeTables\n')
	
	# get the public transport plan related to this scenario
	pt_plan = scenario.getPublicLinePlan()
	time_tables = pt_plan.getTimeTables()
	ptline_lst = []
	for timetable in time_tables:
		ptline = timetable.getPublicLine()
		if ptline not in ptline_lst:
			ptline_lst.append(ptline)

	# for all the Public Transport Line in the model
	objType = model.getType("GKPublicLine")
	for PTLine in ptline_lst:
		#print(PTLine.getId())
		PTLineName = PTLine.getName()
		# replacing some special characters...
		PTLineName = PTLineName.replace(u"\u2013","-")
		PTLineName = PTLineName.replace(u"\u0101","a")
		PTLineName = PTLineName.replace(u"\u014c","O")
		PTLineName = PTLineName.replace(u"\u012b","i")
		PTLineName = PTLineName.replace(u"\u2019","")
		PTLineName = PTLineName.replace(u"\u016b","u")
		#PTLineName = PTLineName.encode('utf-8')
		PTLineName = str(PTLineName)
		#PTLineName = re.sub(u"\xe2\x80\x92",' ',PTLineName)
		#print('exporting %s' % PTLine.getName())
		# format route into a string list
		routeList = []
		for section in PTLine.getRoute():
			routeList.append(str(section.getId()))
		routeStringListString = str(routeList).replace(',',';').replace("u'","'")
		# format stop into a string list
		stopList = []
		for stop in PTLine.getStops():
			if stop is not None:
				stopList.append(str(stop.getId()))
		stopStringListString = str(stopList).replace(',',';').replace("u'","'")
		# get the stop to stop distance and store in a list
		stopDistList = []
		for ptSectionData in PTLine.getPTSectionData():
			stopDistList.append(str(ptSectionData.getDistance()))
		stopDistListString = str(stopDistList).replace(',',';').replace("u'","'")
		# format timetable into a string list
		timeTableList = []
		for tb in PTLine.getTimeTables():
			timeTableList.append(str(tb.getId()))
		tbStringListString = str(timeTableList).replace(',',';').replace("u'","'")
		# get the subnetwork if exists
		if PTLine.getProblemNet() is None:
			subNetString = 'None'
		else:
			subNetString = PTLine.getProblemNet().getName()
		
		try:
			#outfile.write(str(PTLine.getId())+','+PTLineName+','+str(PTLine.getExternalId())+','+str(subNetString)+','+str(routeStringListString)+','+str(stopStringListString)+','+str(stopDistListString)+','+str(tbStringListString)+'\n')
			f.write(f"{PTLine.getId()},{PTLineName},{PTLine.getExternalId()},{subNetString},{routeStringListString},{stopStringListString},{stopDistListString},{tbStringListString}\n")
		except UnicodeEncodeError:
			#print(PTLine.getId())
			modelLog.addError('Unicode error encountered at this PT line', PTLine)

# this function write the Bus timetable and schedule paramters to CSV
	with open(filePathPTTimings, 'w') as f:
		# write the headings
		f.write(f'PTLine_ID,PTTimeTable_ID,PTTimeTable_Name,PTSchedule_ID,PTSchedule_InitTime,PTSchedule_Duration,PTSchedule_Type,PTDepartureList,PTStopList\n')

		# get the public transport plan related to this scenario
		pt_plan = scenario.getPublicLinePlan()
		time_tables = pt_plan.getTimeTables()
		for timeTable in time_tables:
			PTLine = timeTable.getPublicLine()
			timetableName = timeTable.getName()
			# replacings some special characters...
			timetableName = timetableName.replace(u"\u2013","-")
			timetableName = timetableName.replace(u"\u0101","a")
			timetableName = timetableName.replace(u"\u014c","O")
			timetableName = timetableName.replace(u"\u012b","i")
			timetableName = timetableName.replace(u"\u2019","")
			timetableName = timetableName.replace(u"\u016b","u")
			#PTLineName = PTLineName.encode('utf-8')
			timetableName = str(timetableName)	
			for schedule in timeTable.getSchedules():
				scheduleInitTime = schedule.getTime().toString('HH:mm:ss')
				scheduleDuration = schedule.getDuration().toString()
				scheduleDepartureType = schedule.getDepartureType()
				departureList = []
				for departure in schedule.getDepartureTimes():
					departureVeh = departure.getVehicle().getName()
					departureTime = departure.getDepartureTime().toString('HH:mm:ss')
					departureDev = departure.getDeviationTime().toString()
					thisDepartureList = [departureVeh, departureTime, departureDev]
					departureList.append(thisDepartureList)
				departureListString = str(departureList).replace(',',';').replace("u'","'")
				# get the stop list associated with each section along the route of the PT lines
				stopList = PTLine.getStops()
				# remove all the Nones - sections with no stops
				stopList = [x for x in stopList if x != None]
				# go through each stop and get the timings
				scheduleStopList = []
				if len(stopList) > 0:
					stopDict = {}
					for stop in stopList:
						if len(stopDict) == 0:
							stopDict[stop.getId()] = [stop]
						elif stop.getId() not in stopDict.keys():
							stopDict[stop.getId()] = [stop]
						else:
							stopDict[stop.getId()].append(stop)
						stopTiming = schedule.getStopTime(stop, len(stopDict[stop.getId()]))
						stopDwellMean = stopTiming.mean
						stopDwellDev = stopTiming.deviation
						stopDwellOffset = stopTiming.offset
						thisStopList = [stop.getId(), stop.getExternalId(), len(stopDict[stop.getId()]), stopDwellMean, stopDwellDev, stopDwellOffset]
						scheduleStopList.append(thisStopList)
				stopListString = str(scheduleStopList).replace(',',';').replace("u'","'")
				f.write(
						f"{PTLine.getId()},{timeTable.getId()},{timetableName},{schedule.getId()},"
						f"{scheduleInitTime},{scheduleDuration},{scheduleDepartureType},"
						f"{departureListString},{stopListString}\n"
					)

print("Finished Exporting PT Lines and Timings")