# List Splunk Indexes
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
management = config.get('splunk','management')
proxy = config.get('splunk', 'proxy')
proxy_ip = config.get('splunk','proxy_ip')
proxy_port = config.get('splunk', 'proxy_port')

# Setting up Maltego entities and getting initial variables.

me = MaltegoTransform()

# Determine which REST call to make based on authentication setting.

if auth == "1":
	if proxy == "1":
		output = subprocess.check_output('curl -u ' + username + ':' + password + ' -s -k --socks5 ' + proxy_ip + ':' + proxy_port + ' --data-urlencode search="search index=* earliest=' + timeframe + ' | table index | dedup index" -d "output_mode=csv" https://' + searchhead + ':' + management + '/servicesNS/admin/search/search/jobs/export', shell=True)
	else:
		output = subprocess.check_output('curl -u ' + username + ':' + password + ' -s -k --data-urlencode search="search index=* earliest=' + timeframe + ' | table index | dedup index" -d "output_mode=csv" https://' + searchhead + ':' + management + '/servicesNS/admin/search/search/jobs/export', shell=True)

else:
	if proxy == "1":
		output = subprocess.check_output('curl -s -k --socks5 ' + proxy_ip + ':' + proxy_port + ' --data-urlencode search="search index=* earliest=' + timeframe + ' | table index | dedup index" -d "output_mode=csv" https://' + searchhead + ':' + management + '/servicesNS/admin/search/search/jobs/export', shell=True)
	else:
		output = subprocess.check_output('curl -s -k --data-urlencode search="search index=* earliest=' + timeframe + ' | table index | dedup index" -d "output_mode=csv" https://' + searchhead + ':' + management + '/servicesNS/admin/search/search/jobs/export', shell=True)
	
# Regex to find Indexes

index = re.findall(r'.+', output)
indexes = []
for i in index:
	if i[0] == '"':
		indexes.append(i[1:-1])
	else:
		indexes.append(i)

# Remove header value

indexes.remove('index')

# Adding new Index entities and properties.

for index in indexes:
	ent = me.addEntity("munk.Index",index)
	ent.addAdditionalFields('link#maltego.link.color','LinkColor','','0x86B34A')

# Return Maltego Output

me.returnOutput()
