# List Splunk Deployment Server ServerClass Hosts
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
import xml.etree.cElementTree as ET

# Configuration Parser to grab necessary options.

def getLocalConfPath():
   	pathname = os.path.dirname(sys.argv[0])
	pathname = os.path.abspath(pathname)
	pathname = os.path.join(pathname,'..', 'local', 'munk.conf')
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

# Setting up Maltego entities and getting initial variables.

me = MaltegoTransform()
me.parseArguments(sys.argv)
serverclass = sys.argv[1]
dsport = me.getVar("dsport")
ds = me.getVar("ds")

# Determine which REST call to make based on authentication setting.

if auth == "1":
	output = subprocess.check_output('curl -u ' + username + ':' + password + ' -s -k https://' + ds + ':' + dsport + '/services/deployment/server/serverclasses/' + serverclass + '/clients', shell=True)
if auth == "0":
	output = subprocess.check_output('curl -s -k https://' + ds + ':' + dsport + '/services/deployment/server/serverclasses/' + serverclass + '/clients', shell=True)

# Regex to find hostnames

hostrex = re.findall(r'hostname">(.+)<',output)
hosts = []
for i in hostrex:
	hosts.append(i)

# Adding new ServerClass Host entities and properties.

for host in hosts:
        ent = me.addEntity("munk.Host",host)
        ent.addAdditionalFields('ds','DS IP','',ds)
        ent.addAdditionalFields('dsport', 'DS Port','',dsport)
        ent.addAdditionalFields('link#maltego.link.color','LinkColor','','0x86B34A')

# Return Maltego Output

me.returnOutput()
