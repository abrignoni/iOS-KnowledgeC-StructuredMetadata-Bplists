import sys
import ccl_bplist
import plistlib
import io
import sqlite3
import datetime
import os
import glob

#create directories
time = str(int(datetime.datetime.now().timestamp()))

path = os.getcwd()
try:  
	outpath = path + "/" + time
	os.mkdir(outpath)
	os.mkdir(outpath+"/clean")
	os.mkdir(outpath+"/dirty")
except OSError:  
	print("Error making directories")

#connect sqlite databases
db = sqlite3.connect('knowledgeC.db')
cursor = db.cursor()

#variable initializations
dirtcount = 0
cleancount = 0
intentc = {}
intentv = {}

cursor.execute('''
SELECT
Z_PK,
Z_DKINTENTMETADATAKEY__SERIALIZEDINTERACTION,
Z_DKINTENTMETADATAKEY__INTENTCLASS,
Z_DKINTENTMETADATAKEY__INTENTVERB
FROM ZSTRUCTUREDMETADATA
WHERE Z_DKINTENTMETADATAKEY__SERIALIZEDINTERACTION is not null
''')
all_rows = cursor.fetchall()

for row in all_rows:
	pkv = str(row[0])
	f = row[1]
	intentclass = str(row[2])
	intententverb = str(row[3])
	output_file = open('./'+time+'/dirty/D_Z_PK'+pkv+'.bplist', 'wb')#export dirty from DB
	output_file.write(f)
	output_file.close()	

	g = open('./'+time+'/dirty/D_Z_PK'+pkv+'.bplist', 'rb')
	plistg = ccl_bplist.load(g)
	ns_keyed_archiver_obj = ccl_bplist.deserialise_NsKeyedArchiver(plistg)
	dirtcount = dirtcount+1
	
	binfile = open('./'+time+'/clean/C_Z_PK'+pkv+'.bplist', 'wb')#write to clean
	binfile.write(ns_keyed_archiver_obj)
	binfile.close()
	#add to dictionaries
	intentc['C_Z_PK'+pkv+'.bplist'] = intentclass
	intentv['C_Z_PK'+pkv+'.bplist'] = intententverb
	
	cleancount = cleancount+1

h = open('./'+time+'/Report.html', 'w')	
h.write('<html><body>')
h.write('<h2>iOS 11 - KnowledgeC ZSTRUCTUREDMETADATA bplist report</h2>')
h.write ('<style> table, th, td {border: 1px solid black; border-collapse: collapse;}</style>')
h.write('<br />')

for filename in glob.glob('./'+time+'/clean/*.bplist'):	
	p = open(filename, 'rb')
	cfilename = os.path.basename(filename)
	plist = ccl_bplist.load(p)
	ns_keyed_archiver_obj = ccl_bplist.deserialise_NsKeyedArchiver(plist, parse_whole_structure=True)#deserialize clean
	#Get dictionary values
	A = intentc.get(cfilename)
	B = intentv.get(cfilename)
	
	if A is None:
		A = 'No value'
	if B is None:
		A = 'No value'
	
	#print some values from clean bplist
	NSdata = (ns_keyed_archiver_obj["root"]["intent"]["backingStore"]["data"]["NS.data"])
	
	NSstartDate = ccl_bplist.convert_NSDate((ns_keyed_archiver_obj["root"]["dateInterval"]["NS.startDate"]))
	NSendDate = ccl_bplist.convert_NSDate((ns_keyed_archiver_obj["root"]["dateInterval"]["NS.endDate"]))
	NSduration = ns_keyed_archiver_obj["root"]["dateInterval"]["NS.duration"]
	
	h.write(cfilename)
	h.write('<br />')
	h.write('Intent Class: '+str(A))
	h.write('<br />')
	h.write('Intent Verb: '+str(B))
	h.write('<br />')
	h.write('<table>')
	
	
	h.write('<tr>')
	h.write('<th>Data type</th>')
	h.write('<th>Value</th>')
	h.write('</tr>')
	
	#NSstartDate
	h.write('<tr>')
	h.write('<td>NSstartDate</td>')
	h.write('<td>'+str(NSstartDate)+' Z</td>')
	h.write('</tr>')
	
	#NSsendDate
	h.write('<tr>')
	h.write('<td>NSendDate</td>')
	h.write('<td>'+str(NSendDate)+' Z</td>')
	h.write('</tr>')
	
	#NSduration
	h.write('<tr>')
	h.write('<td>NSduration</td>')
	h.write('<td>'+str(NSduration)+'</td>')
	h.write('</tr>')
	
	#NSdata
	h.write('<tr>')
	h.write('<td>NSdata</td>')
	h.write('<td>'+str(NSdata)+'</td>')
	h.write('</tr>')
	
	h.write('<table>')
	h.write('<br />')
	
	#print(NSstartDate)
	#print(NSendDate)
	#print(NSduration)
	#print(NSdata)
	#print('')


print("")	
print("iOS 11 - KnowledgeC ZSTRUCTUREDMETADATA bplist extractor")
print("By: @phillmoore & @AlexisBrignoni")
print("thinkdfir.com & abrignoni.com")
print("")
print("Bplists from the Z_DKINTENTMETADATAKEY__SERIALIZEDINTERACTION field.")
print("Exported bplists (dirty): "+str(dirtcount))
print("Exported bplists (clean): "+str(cleancount))
print("")
print("Triage report completed. See Reports.html.")
