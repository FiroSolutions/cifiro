#!/usr/bin/python3.6    
# -*- coding: utf-8 -*- 

import re, sys, os, glob
import json, requests, pkg_resources
from pathlib import Path

apinyckeln = ''

def canihazapikey():
	global apinyckeln #cache apikey
	if len(sys.argv) == 2 and "apikey=" in str(sys.argv):
		print("Checking api key")
		right = sys.argv[1].split('apikey=')[1]
		if not 'Invalid' in requests.post("https://api.firosolutions.com/latest", json={'apikey': str(right)}).text:
			print("Api Key accepted")
			apinyckeln = right
			with open(str(Path.home())+'/.cifiro', 'w+b') as minfil:
				minfil.write(right.encode())
			return True


	if not os.path.isfile(str(Path.home())+"/.cifiro"):
		print('no api key found :-(')
		print('Login and go to profile in order to view your APi key')
		legitnyckel = False
		while not legitnyckel:
			nycklen = input('Give me a API key: ').replace(' ', '')
			print('validating key')
			if not 'Invalid' in requests.post("https://api.firosolutions.com/latest", json={'apikey': str(nycklen)}).text:
				legitnyckel = True
				print('Thanks :)')
				apinyckeln = str(nycklen)
				with open(str(Path.home())+'/.cifiro', 'w+b') as minfil:
#reported as a bug https://bugs.python.org/issue37307
#				with open('~/.cifiro', 'w+b') as minfil:
					minfil.write(nycklen.encode())
				print('api key saved!')
			else:
				print('invalid apikey')
	else:
		with open(str(Path.home())+'/.cifiro', 'rb') as tempp:
			cnyckel = tempp.read()
		if not 'Invalid' in requests.post("https://api.firosolutions.com/latest", json={'apikey': str(cnyckel)}).text:
			os.system("rm ~/.cifiro")
		else:
			apinyckeln = cnyckel


def askfiro(language, libs):
	cipher = {}
	url = {'rust':'https://api.firosolutions.com/rustlibs', 'nodejs': 'https://api.firosolutions.com/nodejslibs'}
	if not url.keys().__contains__(language.lower()):
		return "Invalid language"
#pass on language version
#syntax example,  "libraries":{"protobuf":"version", "ammonia":"0", "tay":"man"}
	if not isinstance(libs, list):
		return 'i only eat lists'
	joe = {}
	for x in libs:
		if not isinstance(x, tuple):
			return 'i only want tuple in the list'
		if not len(x) == 2:
			return '%s is invalid' % x
		joe[x[0]] = x[1]
		result = requests.post(url.get(language.lower()), json={"apikey": apinyckeln, "libraries":joe}).text
		cipher[x[0]] = {}
		cipher[x[0]]['result'] = json.loads(result).get(x[0])
		cipher[x[0]]['version'] = x[1]
	return cipher



def dorust():
	sant = False
	for x in glob.glob('*'):#cuz ppl..
		if x.lower() == 'cargo.toml':
			print('i found the Cargo.toml!')
			with open(str(os.getcwd()+'/'+x), 'rb') as minfil:
				myfile = minfil.read()
			for z, linje in enumerate(myfile.decode().split('\n')):
				if linje[:1] == '#':
					pass
				if '[dependencies]' in linje:
					sant = z
				if sant:
					if linje[:1] == '[' and sant != z:
						sant = False
					if len(linje) > 3:
						mog = re.findall(r'^([a-z-A-Z-0-9-_]{1,})\s\=\s\"(\*|[0-9-.]{1,})\"', linje)
						if len(mog) >=1:
							print('Checking library',mog[0][0], 'version',mog[0][1])
							print('Result:')
							lifes = askfiro("rust", mog)
							if lifes.get(mog[0][0]).get('result') == 'not found':
								print('\x1b[1;32;40m','nothing found', '\x1b[0m')
							else:
								print(json.dumps(lifes.get(mog[0][0]).get('result'), indent=4))

def donodejs():
	print('doing nodejs')
	for x in glob.glob('*'):
		if x.lower() == 'package.json':
			print('i found the Packages.json!')
			with open(str(os.getcwd()+'/'+x), 'rb') as minfil:
				myfile = json.loads(minfil.read())

			for x in myfile.get('dependencies'):
				lifes = askfiro("nodejs", [(x, myfile.get('dependencies').get(x).replace('^', ''))])
				if lifes.get(x).get('result') == 'not found':
					print('Library:',x,'\x1b[1;32;40m','nothing found', '\x1b[0m')
				else:
					print(json.dumps(lifes.get(x).get('result'), indent=4))
	return True




#guardian of da API key
if __name__ == '__main__':
	print('checking key')
	canihazapikey()
	print('checked key!')
	if glob.glob('*').__contains__('Cargo.toml'):
		print('detected Rust')
		dorust()

	elif sum(1 for en in Path(os.getcwd()).rglob('requirements*txt').__iter__()) >= 1:
		print('python is not yet supported')
		pass

	elif sum(1 for en in Path(os.getcwd()).rglob('package.json').__iter__()) >=1 :
		print("NodeJS detected!")
		donodejs()
