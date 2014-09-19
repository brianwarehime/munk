# List Splunk Hosts by Sourcetype
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
status = config.get('splunk', 'status')
management = config.get('splunk', 'management')
proxy = config.get('splunk', 'proxy')
proxy_ip = config.get('splunk','proxy_ip')
proxy_port = config.get('splunk', 'proxy_port')

# Setting up Maltego entities and getting initial variables.

me = MaltegoTransform()
me.parseArguments(sys.argv)
sourcetype = sys.argv[1]
hostip = me.getVar("host")

# Determine which REST call to make based on authentication setting.

if auth == "1":
	if proxy == "1":
		output = subprocess.check_output('curl -u ' + username + ':' + password + ' -s -k --socks5 ' + proxy_ip + ':' + proxy_port + ' --data-urlencode search="search index=* earliest=' + timeframe + ' sourcetype=' +  sourcetype + ' | table host | dedup host" -d "output_mode=csv" https://' + searchhead + ':' + management + '/servicesNS/admin/search/search/jobs/export', shell=True)
	else:
		output = subprocess.check_output('curl -u ' + username + ':' + password + ' -s -k --data-urlencode search="search index=* earliest=' + timeframe + ' sourcetype=' +  sourcetype + ' | table host | dedup host" -d "output_mode=csv" https://' + searchhead + ':' + management + '/servicesNS/admin/search/search/jobs/export', shell=True)

else:
	if proxy == "1":
		output = subprocess.check_output('curl -s -k --socks5 ' + proxy_ip + ':' + proxy_port + ' --data-urlencode search="search index=* earliest=' + timeframe + ' sourcetype=' +  sourcetype + ' | table host | dedup host" -d "output_mode=csv" https://' + searchhead + ':' + management + '/servicesNS/admin/search/search/jobs/export', shell=True)
	else:
		output = subprocess.check_output('curl -s -k --data-urlencode search="search index=* earliest=' + timeframe + ' sourcetype=' +  sourcetype + ' | table host | dedup host" -d "output_mode=csv" https://' + searchhead + ':' + management + '/servicesNS/admin/search/search/jobs/export', shell=True)

# Regex to find hosts

hosts = re.findall(r'.+', output)
host = []
for i in hosts:
	if i[0] == '"':
		host.append(i[1:-1])
	else:
		host.append(i)

# Remove header value

host.remove('host')

# Adding new Host entities and properties.

for a in host:
	ent = me.addEntity("munk.Host",a)
	ent.addAdditionalFields('link#maltego.link.color','LinkColor','','0x86B34A')

	# If status is set, ping the server and set the bookmark color based on response.

	if status == "1":
		try:
			status = subprocess.check_output('ping -c 1 ' + a, shell=True)
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



