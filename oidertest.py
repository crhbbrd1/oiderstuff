#!/usr/bin/python
#
# Vignette vgnextoid legacyUID redirector - oider
# JRS -  3/23/2015 - 1.0 - created from slinger
# JRS -  5/12/2015 - 1.1 - handle common entry errors, support multiple legacyUIDs 
#

#####
import sys
import traceback
import urllib2
import types


try:
    import json
except ImportError:
    import simplejson as json

#####
def get_iterable(iterable):
    if isinstance(iterable, basestring):
        iterable = [iterable]
    try:
        iter(iterable)
    except TypeError:
        iterable = [iterable]
    return iterable
	
############################################################
def isIncluded(string, min, max, inclusionString):		   
	inclusionList = list(inclusionString)	
	stringLength= len(string)
	alphaNum = string.isalnum()

	
	if(stringLength>=min and stringLength<=max): 
		for c in string:
			if c not in inclusionList:
				#print("isIncluded: Invalid")
				return ("Invalid Character: "+ "'"+c+"'")
			
		#print("True")
		return ("True")
	else:
		#print("IsIncluded: Invalid Size")
		return ("Invalid Size"+"("+str(stringLength)+")")
######################################################		
	
	
#####
targethost = sys.argv[1]
targetport = sys.argv[2]

def openurl():
	#####
	try: 
		#	response = urllib2.urlopen('https://'+targethost+':'+targetport+'/bin/querybuilder.json?1_property=legacyUid&1_property.operation=like&1_property.value=%25gn%25&p.hits=selective&p.limit=-1&p.properties=jcr%3apath%20legacyUid%20&path=%2fcontent%2fsites')
		
		# response = urllib2.urlopen('https://pcqp1s1.alsac.stjude.org:3443/bin/querybuilder.json?1_property=legacyUid&1_property.operation=like&1_property.value=%25gn%25&p.hits=selective&p.limit=-1&p.properties=jcr%3apath%20legacyUid%20&path=%2fcontent%2fsites')
		
		response = urllib2.urlopen('https://toybox-s1.alsac.stjude.org/chris/badoiderstring.txt')
		
	except urllib2.HTTPError, e:
		print('Error: HTTPError = ' + str(e.code))
		sys.exit(1)
	except urllib2.URLError, e:
		print('Error: URLError = ' + str(e.reason))
		sys.exit(1)
	except httplib.HTTPException, e:
		print('Error: HTTPException')
		sys.exit(1)
	except Exception:
		print('Error: generic exception ' + traceback.format_exc())
		sys.exit(1)
	return response

response=openurl()

####
try:
	
	responseData = json.load(response)
	
except UnicodeDecodeError as e:
	print "Unicode Decode Error: "+str(e)
	# Need to open url again
	response=openurl()
	myfile=response.readline()
	#replace invalid characters
	myfile =unicode(myfile, errors='replace')
	myfile=myfile.encode('utf-8')
	responseData = json.loads(myfile)	
	pass

hitsResult = responseData['hits']


#####
try:
	sites = set( rs['jcr:path'].split('/')[3] for rs in hitsResult)
except Exception:
	print('Error: jcr:path problem ' + traceback.format_exc())
	sys.exit(1)

if len(sites) > 0:
	print "Site count: "+str(len(sites))
	for site in sites:
		print "Site: "+site
		filename = 'C:/Users/hubbardc/AppData/Local/temp' + site + '.redirect'
		try:
        		fo = open(filename, 'w')
		except Exception:
			print('Error: Opening file for write:' + filename + ' ' + traceback.format_exc())
			sys.exit(1)
        	fo.close()
else:
	print('Error: No sites')
	sys.exit(1)


#####
for rs in hitsResult:
 	path = rs['jcr:path']
	pathCheck = isIncluded(path,1,1000,"ABCDEFGHIJKLMNOPQRSTUVQXWYXabcdefghijklmnopqrstuvwxyz0123456789/,:-_")
	##Write to error file if check fails
	if pathCheck != "True":
		errorFile='C:/Users/hubbardc/AppData/Local/temp/Err.txt'
		try:
			po = open(errorFile, 'a')
			try:										
				#po.write('Error: '+check+'	'+oid+' '+vanityURL+'\n')
				#path=unicode(path, 'utf-8')
				path=path.encode("utf-8")
				pathCheck =pathCheck.encode("utf-8")
				po.write('====================================\n')
				po.write('Error: '+pathCheck+' in\n') 
				po.write('Path:\t'+path+'\n')
				po.write('====================================\n')
				po.write('\n')
			except Exception:
				print('Error: Writing data:' + errorFile + ' ' + traceback.format_exc())
				sys.exit(1)
			po.close()
		except Exception:
			print('Error: Opening file for append:' + errorFile + ' ' + traceback.format_exc())
			sys.exit(1)
			
	pathParts = path.split('/')
	vanityURL = path.replace('/jcr:content','.html')
	vanityURL = vanityURL.split('/home', 1)[-1]

	
	for vp in get_iterable(rs['legacyUid']):
		vanityPath = vp.split('=', 1)[-1]
		vanityPath = vanityPath.split('&', 1)[-1]
		vanityPath = vanityPath.replace(' ','')
		UIDs = vanityPath.split(',')
		
		# if len(UIDs) > 1:
			# print "UID multiple count: ",len(UIDs)
			
		for oid in get_iterable(UIDs):
			#check oid
			oidCheck = isIncluded(oid,1,40,"ABCDEFGHIJKLMNOPQRSTUVQXWYXabcdefghijklmnopqrstuvwxyz0123456789")
			if oidCheck == "True":
				##filename = './tmp/' + pathParts[3] + '-' + pathParts[4] + '.redirect'
				filename = 'C:/Users/hubbardc/AppData/Local/temp/blah.txt'	
				try:
					fo = open(filename, 'a')
					try:
						oid=oid.encode("utf-8")
						#vanityURL=vanityURL.encode("utf-8")
						fo.write(oid+' '+vanityURL+'\n')
					except Exception:
						print('Error: Writing data:' + filename + ' ' + traceback.format_exc())
						sys.exit(1)
					fo.close()

				except Exception:
						print('Error: Opening file for append:' + filename + ' ' + traceback.format_exc())
						sys.exit(1)
						
			else:			
				#Write error file here.
				errorFile='C:/Users/hubbardc/AppData/Local/temp/Err.txt'
				try:
					po = open(errorFile, 'a')
					try:
						po.write('====================================\n')	
						po.write('Error:\t'+oidCheck+' in\n')
						po.write('LegacyUID:\t'+oid+'\n')
						po.write('Path:\t'+vanityURL+'\n')
						po.write('=====================================\n')
						po.write('\n')
						# print oid
						# print len(oid)
					except Exception:
						print('Error: Writing data:' + filename + ' ' + traceback.format_exc())
						sys.exit(1)
					po.close()
				except Exception:
					print('Error: Opening file for append:' + filename + ' ' + traceback.format_exc())
					sys.exit(1)
	
print('Done')
sys.exit(0)






