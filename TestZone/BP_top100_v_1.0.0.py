#This program is supposed to fetch the top 100 list from Beatport and compare it to the previously
#saved list, then present the difference, hence the new entries.

#Dependencies. It is written in Python 2.7 on Windows and it uses BeautifulSoup4

####Version log##################
##################################################
# v. 1.0.0 Released on 3 December 2012 at 23:31
#
#Basic functionality. First working release.

import urllib
import codecs
import os
import time
from bs4 import BeautifulSoup

oldList='old.txt'
newList='new.txt'
trackListFile='tracks.txt'
newEntries='NewTracks.txt'
folderName='Data'
PATH=os.path.join(os.getcwd(),folderName)
VERSION='1.0.0'


def GetNewTrackList():
	#Returns the list of new tracks

	global PATH, folderName, trackListFile

	fullPath=os.path.join(PATH,trackListFile)

	if os.path.exists(fullPath):
		oldData=ReadData(fullPath)

		newData=DownloadTrackList()
		return ComapreLists(oldData,newData)

	else:
		try:
			os.mkdir(folderName)
			print "The program is run for the first time.\n The directory and the initial list with 100 tracks will be created!"
		except:
			print 'The folder already exists!!'
		
		newData=DownloadTrackList()
		return ReadData(fullPath)


def DownloadTrackList():
	#writes the data to the file returns the set of top 100 tracks from Beatport

	URL="http://www.beatport.com/top-100"
	html=urllib.urlopen(URL).read()
	soup=BeautifulSoup(html)

	data=''

	#skip the first element because it's the name of the column in the table
	trackList=soup.find_all('td',{'class':'secondColumn'})[1:]

	for element in trackList:
		data= data+codecs.encode(element.text,'utf-8')+'\n'

	#Get rid of the last NewLine element
	data=data[:-1]
	

	WriteData(trackListFile,data)
	data=data.split('\n')

	return data

def ReadData(filePath):
	#reads the list of tracks

	toRead=open(filePath,'r')
	data=toRead.read()
	data=data.split('\n')

	toRead.close()

	return data

def WriteData(fileName,data):
	#Write the list of tracks to a file
	global PATH

	toWrite=open(os.path.join(PATH,fileName),'w')
	toWrite.write(data)
	toWrite.close()


def ComapreLists(oldL,newL):
	#will return the list of new entries to the top-100. If any.

	global newEntries

	t=time.localtime()
	locTime='Date: '+str(t[2])+'.'+str(t[1])+'.'+str(t[0])+'. Time:  '+str(str(t[3])+'hrs '+str(t[4])+'mins '+str(t[5])+'s')

	NewTracksList=[]
	for track in newL:
		if track not in oldL:
			NewTracksList.append(track)

	prettyResult=locTime+'\n\n\n'

	if len(NewTracksList)==0:
		NewTracksList.append("No New Entries Yet!!")
	#fromat the result before writing/printing
	for element in NewTracksList:
		prettyResult=prettyResult+element+'\n'

	WriteData(newEntries, prettyResult)

	return prettyResult

if __name__=="__main__":

	print 'Hello! I am Beatport verifier version '+VERSION+'\nI am already downloading the updated tracklist. Please be patient...\n\n'

	result= GetNewTrackList()
	if not raw_input("Print the list of new tracks? (ENTER - yes/ any character, then ENTER - no)    "):
		print '\n\n'+result		

raw_input('Execution has finished. Press any key...')