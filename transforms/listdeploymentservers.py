# List Splunk Deployment Servers
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
	output = subprocess.check_output('curl -u ' + username + ':' + password + ' -s -k https://' + searchhead + ':' + management + '/services/deployment/client', shell=True)

if auth == "0":
	output = subprocess.check_output('curl -s -k https://' + searchhead + ':' + management + '/services/deployment/client', shell=True)

# Regex to find Deployment Servers

dservers = re.findall(r'key name="targetUri">(.*):\d{1,5}', output)
deployserver = []
for ds in dservers:
	deployserver.append(ds)

# Regex to find Deployment Server management port

dsport = re.findall(r'targetUri">[^\s]+:(\d+)</s:key>', output)
dsportfix = dsport[0]

# Adding new Deployment Server entities and properties.

for server in deployserver:
	ent = me.addEntity("munk.DeploymentServer",server)
	ent.addAdditionalFields('link#maltego.link.color','LinkColor','','0x86B34A')
	ent.addAdditionalFields('dsport','DS Port','',dsportfix)

    # If status is set, ping the server and set the bookmark color based on response.

	if status == "1":
		try:
			status = subprocess.check_output('ping -c 1 ' + server, shell=True)
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
