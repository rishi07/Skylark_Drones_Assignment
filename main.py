'''
Author: 
		Saptarshi Dey
		National Institute of Technology, Durgapur
		07saptarshidey@gmail.com

Time Complexity Analysis: 	
		Let, n = Number of time-stamps in .SRT file (Queries)
		Let, m = Number of geo-tagged locations (Search-space) in .KML file
		Complexity: O(n*m)
'''
'''


DEPENDENCIES: BeautifulSoup with XML parser
$ apt-get install python3-bs4
$ apt-get install python-lxml
'''

from bs4 import BeautifulSoup
from math import sin,cos,sqrt,atan2,radians


'''
Function to calculate distance between two given coordinates.
The function takes in two geo-coordinates as arguments and returns the distance in metres between them.

Elavation is not taken into account as the image location captured by the drone is at the ground. The elavation is due to
the position of the drone which is redundant. We are considering 2-D distance (ground to ground).
 
'''
def distance(latitude_1 , latitude_2 , longitude_1 , longitude_2):							
	latitude_1 = radians(latitude_1)
	latitude_2 = radians(latitude_2)
	longitude_1 = radians(longitude_1)
	longitude_2 = radians(longitude_2)
	delta_longitude = longitude_2-longitude_1
	delta_latitude = latitude_2-latitude_1
	temp = sin(delta_latitude/2)**2 + cos(latitude_1)*cos(latitude_2)*sin(delta_longitude/2)**2
	temp_2 = 2*atan2(sqrt(temp),sqrt(1-temp))
	Radius = 6373.0
	dis = Radius*temp_2
	return dis*1000


#The .csv output file
output_file=open("output.csv","w")				
output_file.write("    TIME_START     ,    TIME_END    ,    IMAGES     "+"\n")

#parsing and reading the .kml file using BeautifulSoup - XML parser
myfile=("./software_dev/images/doc.kml")
latitude=[]
longitude=[]
name=[]
with open(myfile,'r') as f:
	all_data=BeautifulSoup(f,'lxml')
	names=all_data.findAll("description")
	for data in names:
		name.append(data.text)
	coordinates=all_data.findAll("coordinates")
	for data in coordinates:
		line=str(data.text)
		values=line.split(",")
		latitude.append(float(values[0]))
		longitude.append(float(values[1]))

#This value can be changed accordingly. Currently set to 35m as per requirement.
query_radius=35.0000 

#Reading the .SRT file which containes time based geo-coordinates 
srtfile=("./software_dev/videos/DJI_0301.SRT")
with open(srtfile,'r') as srt:
	cnt=0			
	for entries in srt:
		cnt=cnt+1	#count variable
		'''
		Data of each time-stamp contains 4 lines:
		Line1 : 1
		Line 2: 00:00:00,100 --> 00:00:00,200
		Line 3: 73.00135763743417,19.149798647687,0
		Line 4:
		The useful lines are line two and three the modulo 4 of which greater than 2
		'''
		if(cnt%4<=1):	
		 	continue	#not useful lines

		entries=str(entries)
		values=entries.split()
		if(cnt%4==2):
			'''
			Since I was using .csv output format, I need to change comma separated time-stamp to some other standard format
			That is, 00:00:00,300 is changed to 00:00:00:300
			'''
			time_left=str(values[0])
			time_left=time_left.replace(",",":")
			time_right=str(values[2])
			time_right=time_right.replace(",",":")
			output_file.write(time_left+","+time_right+"\n")
		else:
			newlist=[]
			for word in values:
				word=word.split(",")
				newlist.extend(word)
			latitude_2=float(newlist[0])
			longitude_2=float(newlist[1])
			n=len(latitude)
			'''
			Now traverseing all the given geo-coordinates in the .kml file and calculating the distance for each of them from
			the current position.
			'''
			for i in range(n):
				latitude_1=latitude[i]
				longitude_1=longitude[i]
				dis=distance(latitude_1,latitude_2,longitude_1,longitude_2)
				if(dis<=query_radius):
					output_file.write(",,"+name[i])
					output_file.write("\n")
output_file.close()

output_assets=open("output_assets.csv","w")
output_assets.write("    ASSET_NAME    ,    IMAGES    \n")


'''
Value of query_radius now changed to 50 as per requirement.
'''
query_radius=50.00		
assets_file=("./software_dev/assets.csv")

with open(assets_file,'r') as assets:
	cnt=0
	for data in assets:
		cnt=cnt+1
		'''
		Ignoring the first line because no data is present there.
		'''
		if(cnt==1):
			continue
		line=str(data)
		line=line.split(",")
		longitude_2=float(line[2])
		latitude_2=float(line[1])
		output_assets.write(line[0]+"\n")
		'''
			Now traverseing all the given geo-coordinates in the .kml file and calculating the distance for each of them from
			the current position.
		'''
		for i in range(n):
			latitude_1=latitude[i]
			longitude_1=longitude[i]
			dis=distance(latitude_1,latitude_2,longitude_1,longitude_2)		
			if(dis<=query_radius):
				output_assets.write(","+name[i])
				output_assets.write("\n")

output_assets.close()




