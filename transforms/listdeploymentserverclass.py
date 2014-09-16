# List Splunk Deployment Server Classes
# For use with Munk - Maltego for Splunk
# Author: Brian Warehime @nulltr0n
# 9/6/2014

# Importing various modules

from MaltegoTransform import *
import subprocess
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
application = sys.argv[1]
ds = me.getVar("ds")
dsport = me.getVar("dsport")

# Determine which REST call to make based on authentication setting.

if auth == "1":
	output = subprocess.check_output('curl -u ' + username + ':' + password + ' -s -k https://' + ds + ':' + dsport + '/services/deployment/server/clients', shell=True)
if auth == "0":
	output = subprocess.check_output('curl -s -k https://' + ds + ':' + dsport + '/services/deployment/server/clients', shell=True)

# XML Parsing with ElementTree

root = ET.fromstring(output)
entry = root.find('{http://www.w3.org/2005/Atom}entry')
content = entry.find('{http://www.w3.org/2005/Atom}content')
dic = content.find('{http://dev.splunk.com/ns/rest}dict')
app = ".//{http://dev.splunk.com/ns/rest}key[@name='" + application + "']"
app2 = content.find(app)
app_d = app2[0]
sc =  app_d.find(".//{http://dev.splunk.com/ns/rest}key[@name='serverclasses']")
serverclass = sc[0][0].text

# Adding new Server Class entities and properties based on XML results.

ent = me.addEntity("munk.ServerClass",serverclass)
ent.addAdditionalFields('link#maltego.link.color','LinkColor','','0x86B34A')
ent.addAdditionalFields('ds','DS IP','',ds)
ent.addAdditionalFields('dsport', 'DS Port','',dsport)

# Return Maltego Output

me.returnOutput()
