# List Splunk Indexers
# For use with Munk - Maltego for Splunk
# Author: Brian Warehime @nulltr0n
# 9/6/2014

# Importing various modules

from MaltegoTransform import *
import subprocess
import re
import sys
import ConfigParser
import os

# Configuration Parser to grab necessary options.

def getLocalConfPath():
   	pathname = os.path.dirname(sys.argv[0])
	pathname = os.path.abspath(pathname)
	pathname = os.path.join(pathname, '..','local', 'munk.conf')
	return os.path.normpath(pathname)

configFile = getLocalConfPath()
config = ConfigParser.SafeConfigParser()
config.read(configFile)

username = config.get('credentials', 'username')
password = config.get('credentials', 'password')
auth = config.get('splunk','auth')
searchhead = config.get('splunk','searchhead')
timeframe = config.get('splunk', 'timeframe')
status = config.get('splunk', 'status')
management = config.get('splunk','management')

# Setting up Maltego entities and getting initial variables.

me = MaltegoTransform()
host = sys.argv[1]

# Determine which REST call to make based on authentication setting.

if auth == "1":
	output = subprocess.check_output('curl -u ' + username + ':' + password + ' -s -k --data-urlencode search="search index=* earliest=' + timeframe + ' | table splunk_server | dedup splunk_server | rename splunk_server AS indexer" -d "output_mode=csv" https://' + searchhead + ':' + management + '/servicesNS/admin/search/search/jobs/export', shell=True)
if auth == "0":
	output = subprocess.check_output('curl -s -k --data-urlencode search="search index=* earliest=' + timeframe + ' | table splunk_server | dedup splunk_server | rename splunk_server AS indexer" -d "output_mode=csv" https://' + searchhead + ':' + management + '/servicesNS/admin/search/search/jobs/export', shell=True)

# Regex to find Indexers

index = re.findall(r'.+', output)
indexers = []
for i in index:
	if i[0] == '"':
		indexers.append(i[1:-1])
	else:
		indexers.append(i)

# Remove header value

indexers.remove('indexer')

# Adding new Indexer entities and properties.

for indexer in indexers:
	ent = me.addEntity("munk.Indexer",indexer)
	ent.addAdditionalFields('link#maltego.link.color','LinkColor','','0x86B34A')

	# If status is set, ping the server and set the bookmark color based on response.

	if status == "1":
		try:
			status = subprocess.check_output('ping -c 1 ' + indexer, shell=True)
			if "bytes from" in status:
				ent.addAdditionalFields('bookmark#','Bookmark','',"1")
			elif "cannot" in status:
				ent.addAdditionalFields('bookmark#','Bookmark','',"4")
		except subprocess.CalledProcessError, e:
			ent.addAdditionalFields('bookmark#','Bookmark','',"4")
	else:
		pass

# Return Maltego Output

me.returnOutput()
