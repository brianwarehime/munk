# Run a Splunk Search on the Selected Index
# For use with Munk - Maltego for Splunk
# Author: Brian Warehime @nulltr0n
# 9/6/2014

# Importing various modules

from MaltegoTransform import *
import sys
import webbrowser
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
splunkweb_port = config.get('splunk','splunkweb_port')

# Setting up Maltego entities and getting initial variables.

me = MaltegoTransform()
me.parseArguments(sys.argv);
sourcetype = me.getVar("properties.sourcetype")

# Opens default webbrowser with a Splunk Search set to the hostname of the host entity selected.

webbrowser.open('http://' +  searchhead + ':' + splunkweb_port + '/en-US/app/search/search?q=search%20index%3D*%20sourcetype%3D' + str(sourcetype) + '&earliest=' + timeframe)

# Return Maltego Output

me.returnOutput()
