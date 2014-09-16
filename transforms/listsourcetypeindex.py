# List Splunk Sourcetypes for each Index
# For use with Munk - Maltego for Splunk
# Author: Brian Warehime @nulltr0n
# 9/6/2014

# Importing various modules

from MaltegoTransform import *
import subprocess
import sys
import re
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
management = config.get('splunk', 'management')

# Setting up Maltego entities and getting initial variables.

me = MaltegoTransform()
sourcetype = sys.argv[1]

# Determine which REST call to make based on authentication setting.

if auth == "1":
	output = subprocess.check_output('curl -u ' + username + ':' + password + ' -s -k --data-urlencode search="search index=' + sourcetype + ' earliest=' + timeframe + ' | table sourcetype | dedup sourcetype" -d "output_mode=csv" https://' + searchhead + ':' + management + '/servicesNS/admin/search/search/jobs/export', shell=True)
else:
	output = subprocess.check_output('curl -s -k --data-urlencode search="search index=' + sourcetype + ' earliest=' + timeframe + ' | table sourcetype | dedup sourcetype" -d "output_mode=csv" https://' + searchhead + ':' + management + '/servicesNS/admin/search/search/jobs/export', shell=True)

# Regex to find Sourcetype

sourcetype = re.findall(r'.+', output)
sourcetypes = []
for i in sourcetype:
	if i[0] == '"':
		sourcetypes.append(i[1:-1])
	else:
		sourcetypes.append(i)

# Remove header value

sourcetypes.remove('sourcetype')

# Adding new Sourcetype entities and properties.

for source in sourcetypes:
	ent = me.addEntity("munk.Sourcetype",source)
	ent.addAdditionalFields('link#maltego.link.color','LinkColor','','0x86B34A')

# Return Maltego Output

me.returnOutput()
