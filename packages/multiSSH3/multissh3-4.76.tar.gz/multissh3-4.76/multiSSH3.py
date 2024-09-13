#!/usr/bin/env python3
import curses
import subprocess
import threading
import time,os
import argparse
from itertools import product
import re
import string
import ipaddress
import sys
import json
import socket
import io
import signal
import functools
import glob
try:
	# Check if functiools.cache is available
	cache_decorator = functools.cache
except AttributeError:
	try:
		# Check if functools.lru_cache is available
		cache_decorator = functools.lru_cache(maxsize=None)
	except AttributeError:
		# If neither is available, use a dummy decorator
		def cache_decorator(func):
			return func
		
version = '4.76'
VERSION = version

DEFAULT_ENV_FILE = '/etc/profile.d/hosts.sh'
DEFAULT_USERNAME = None
DEFAULT_EXTRA_ARGS = None
DEFAULT_PASSWORD = ''
DEFAULT_ONE_ON_ONE = False
DEFAULT_FILE_SYNC = False
DEFAULT_SCP = False
DEFAULT_TIMEOUT = 50
DEFAULT_REPEAT = 1
DEFAULT_INTERVAL = 0
DEFAULT_IPMI = False
DEFAULT_INTERFACE_IP_PREFIX = None
DEFAULT_IPMI_INTERFACE_IP_PREFIX = None
DEFAULT_QUIET = False
DEFAULT_ERROR_ONLY = False
DEFAULT_NO_OUTPUT = False
DEFAULT_NO_ENV = False
DEFAULT_MAX_CONNECTIONS = 4 * os.cpu_count()
DEFAULT_JSON_MODE = False
DEFAULT_PRINT_SUCCESS_HOSTS = False
DEFAULT_GREPPABLE_MODE = False
DEFAULT_NO_WATCH = False
DEFAULT_SKIP_UNREACHABLE = False
DEFAULT_SKIP_HOSTS = ''
DEFAULT_CURSES_MINIMUM_CHAR_LEN = 40
DEFAULT_CURSES_MINIMUM_LINE_LEN = 1
DEFAULT_SINGLE_WINDOW = False

DEFAULT_CALLED = True
DEFAULT_RETURN_UNFINISHED = False
DEFAULT_UPDATE_UNREACHABLE_HOSTS = True
DEFAULT_NO_START = False

global_suppress_printout = True

mainReturnCode = 0
failedHosts = set()
class Host:
	def __init__(self, name, command, files = None,ipmi = False,interface_ip_prefix = None,scp=False,extraargs=None):
		self.name = name # the name of the host (hostname or IP address)
		self.command = command # the command to run on the host
		self.returncode = None # the return code of the command
		self.output = [] # the output of the command for curses
		self.stdout = [] # the stdout of the command
		self.stderr = [] # the stderr of the command
		self.printedLines = -1 # the number of lines printed on the screen
		self.files = files # the files to be copied to the host
		self.ipmi = ipmi # whether to use ipmi to connect to the host
		self.interface_ip_prefix = interface_ip_prefix # the prefix of the ip address of the interface to be used to connect to the host
		self.scp = scp # whether to use scp to copy files to the host
		self.extraargs = extraargs # extra arguments to be passed to ssh
		self.resolvedName = None # the resolved IP address of the host
	def __iter__(self):
		return zip(['name', 'command', 'returncode', 'stdout', 'stderr'], [self.name, self.command, self.returncode, self.stdout, self.stderr])
	def __repr__(self):
		# return the complete data structure
		return f"Host(name={self.name}, command={self.command}, returncode={self.returncode}, stdout={self.stdout}, stderr={self.stderr}, output={self.output}, printedLines={self.printedLines}, files={self.files}, ipmi={self.ipmi}, interface_ip_prefix={self.interface_ip_prefix}, scp={self.scp}, extraargs={self.extraargs}, resolvedName={self.resolvedName})"
	def __str__(self):
		return f"Host(name={self.name}, command={self.command}, returncode={self.returncode}, stdout={self.stdout}, stderr={self.stderr})"

wildCharacters = ['*','?','x']

gloablUnavailableHosts = set()

ipmiiInterfaceIPPrefix = DEFAULT_IPMI_INTERFACE_IP_PREFIX

keyPressesIn = [[]]

emo = False

etc_hosts = {}

env_file = DEFAULT_ENV_FILE

# check if command sshpass is available
sshpassAvailable = False
try:
	subprocess.run(['which', 'sshpass'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
	sshpassAvailable = True
except:
	pass


@cache_decorator
def expandIPv4Address(hosts):
	'''
	Expand the IP address range in the hosts list

	Args:
		hosts (list): A list of IP addresses or IP address ranges

	Returns:
		list: A list of expanded IP addresses
	'''
	expandedHosts = []
	expandedHost = []
	for host in hosts:
		host = host.replace('[','').replace(']','')
		octets = host.split('.')
		expandedOctets = []
		for octet in octets:
			if '-' in octet:
				# Handle wildcards
				octetRange = octet.split('-')
				for i in range(len(octetRange)):
					if not octetRange[i] or octetRange[i] in wildCharacters:
						if i == 0:
							octetRange[i] = '0'
						elif i == 1:
							octetRange[i] = '255'
				
				expandedOctets.append([str(i) for i in range(int(octetRange[0]),int(octetRange[1])+1)])
			elif octet in wildCharacters:
				expandedOctets.append([str(i) for i in range(0,256)])
			else:
				expandedOctets.append([octet])
		# handle the first and last subnet addresses
		if '0' in expandedOctets[-1]:
			expandedOctets[-1].remove('0')
		if '255' in expandedOctets[-1]:
			expandedOctets[-1].remove('255')
		#print(expandedOctets)
		# Generate the expanded hosts
		for ip in list(product(expandedOctets[0],expandedOctets[1],expandedOctets[2],expandedOctets[3])):
			expandedHost.append('.'.join(ip))
	expandedHosts.extend(expandedHost)
	return expandedHosts

@cache_decorator
def readEnvFromFile(environemnt_file = ''):
	'''
	Read the environment variables from env_file
	Returns:
		dict: A dictionary of environment variables
	'''
	global env
	try:
		if env:
			return env
	except:
		env = {}
	global env_file
	if environemnt_file:
		envf = environemnt_file
	else:
		envf = env_file if env_file else DEFAULT_ENV_FILE
	if os.path.exists(envf):
		with open(envf,'r') as f:
			for line in f:
				if line.startswith('#') or not line.strip():
					continue
				key, value = line.replace('export ', '', 1).strip().split('=', 1)
				key = key.strip().strip('"').strip("'")
				value = value.strip().strip('"').strip("'")
				# avoid infinite recursion
				if key != value:
					env[key] = value.strip('"').strip("'")
	return env

@cache_decorator
def getIP(hostname,local=False):
	'''
	Get the IP address of the hostname

	Args:
		hostname (str): The hostname

	Returns:
		str: The IP address of the hostname
	'''
	global etc_hosts
	# First we check if the hostname is an IP address
	try:
		ipaddress.ip_address(hostname)
		return hostname
	except ValueError:
		pass
	# Then we check /etc/hosts
	if not etc_hosts and os.path.exists('/etc/hosts'):
		with open('/etc/hosts','r') as f:
			for line in f:
				if line.startswith('#') or not line.strip():
					continue
				#ip, host = line.split()[:2]
				chunks = line.split()
				if len(chunks) < 2:
					continue
				ip = chunks[0]
				for host in chunks[1:]:
					etc_hosts[host] = ip
	if hostname in etc_hosts:
		return etc_hosts[hostname]
	if local:
		return None
	# Then we check the DNS
	try:
		return socket.gethostbyname(hostname)
	except:
		return None

@cache_decorator 
def expand_hostname(text,validate=True,no_env=False):
	'''
	Expand the hostname range in the text.
	Will search the string for a range ( [] encloused and non enclosed number ranges).
	Will expand the range, validate them using validate_expand_hostname and return a list of expanded hostnames

	Args:
		text (str): The text to be expanded
		validate (bool, optional): Whether to validate the hostname. Defaults to True.

	Returns:
		set: A set of expanded hostnames
	'''
	expandinghosts = [text]
	expandedhosts = set()
	# all valid alphanumeric characters
	alphanumeric = string.digits + string.ascii_letters
	while len(expandinghosts) > 0:
		hostname = expandinghosts.pop()
		match = re.search(r'\[(.*?-.*?)\]', hostname)
		if not match:
			expandedhosts.update(validate_expand_hostname(hostname,no_env=no_env) if validate else [hostname])
			continue
		try:
			range_start, range_end = match.group(1).split('-')
		except ValueError:
			expandedhosts.update(validate_expand_hostname(hostname,no_env=no_env) if validate else [hostname])
			continue
		range_start = range_start.strip()
		range_end = range_end.strip()
		if not range_end:
			if range_start.isdigit():
				range_end = '9'
			elif range_start.isalpha() and range_start.islower():
				range_end = 'z'
			elif range_start.isalpha() and range_start.isupper():
				range_end = 'Z'
			else:
				expandedhosts.update(validate_expand_hostname(hostname,no_env=no_env) if validate else [hostname])
				continue
		if not range_start:
			if range_end.isdigit():
				range_start = '0'
			elif range_end.isalpha() and range_end.islower():
				range_start = 'a'
			elif range_end.isalpha() and range_end.isupper():
				range_start = 'A'
			else:
				expandedhosts.update(validate_expand_hostname(hostname,no_env=no_env) if validate else [hostname])
				continue
		if range_start.isdigit() and range_end.isdigit():
			padding_length = min(len(range_start), len(range_end))
			format_str = "{:0" + str(padding_length) + "d}"
			for i in range(int(range_start), int(range_end) + 1):
				formatted_i = format_str.format(i)
				if '[' in hostname:
					expandinghosts.append(hostname.replace(match.group(0), formatted_i, 1))
				else:
					expandedhosts.update(validate_expand_hostname(hostname.replace(match.group(0), formatted_i, 1),no_env=no_env) if validate else [hostname])
		else:
			if all(c in string.hexdigits for c in range_start + range_end):
				for i in range(int(range_start, 16), int(range_end, 16)+1):
					if '[' in hostname:
						expandinghosts.append(hostname.replace(match.group(0), format(i, 'x'), 1))
					else:
						expandedhosts.update(validate_expand_hostname(hostname.replace(match.group(0), format(i, 'x'), 1),no_env=no_env) if validate else [hostname])
			else:
				try:
					start_index = alphanumeric.index(range_start)
					end_index = alphanumeric.index(range_end)
					for i in range(start_index, end_index + 1):
						if '[' in hostname:
							expandinghosts.append(hostname.replace(match.group(0), alphanumeric[i], 1))
						else:
							expandedhosts.update(validate_expand_hostname(hostname.replace(match.group(0), alphanumeric[i], 1),no_env=no_env) if validate else [hostname])
				except ValueError:
					expandedhosts.update(validate_expand_hostname(hostname,no_env=no_env) if validate else [hostname])
	return expandedhosts

@cache_decorator
def expand_hostnames(hosts,no_env=False):
	'''
	Expand the hostnames in the hosts list

	Args:
		hosts (list): A list of hostnames

	Returns:
		list: A list of expanded hostnames
	'''
	expandedhosts = []
	if isinstance(hosts, str):
		hosts = [hosts]
	for host in hosts:
		host = host.strip()
		if not host:
			continue
		# we seperate the username from the hostname
		username = None
		if '@' in host:
			username, host = host.split('@',1)
		# first we check if the hostname is an range of IP addresses
		# This is done by checking if the hostname follows four fields of 
		# "(((\d{1,3}|x|\*|\?)(-(\d{1,3}|x|\*|\?))?)|(\[(\d{1,3}|x|\*|\?)(-(\d{1,3}|x|\*|\?))?\]))" 
		# seperated by .
		# If so, we expand the IP address range
		if re.match(r'^((((25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[1-9])|x|\*|\?)(-((25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[1-9])|x|\*|\?))?)|(\[((25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[1-9])|x|\*|\?)(-((25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[1-9])}|x|\*|\?))?\]))(\.((((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])|x|\*|\?)(-((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])|x|\*|\?))?)|(\[((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])|x|\*|\?)(-((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])|x|\*|\?))?\]))){2}(\.(((25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[1-9])|x|\*|\?)(-((25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[1-9])|x|\*|\?))?)|(\[((25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[1-9])|x|\*|\?)(-((25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[1-9])}|x|\*|\?))?\]))$', host):
			hostSetToAdd = sorted(expandIPv4Address(frozenset([host])),key=ipaddress.IPv4Address)
		else:
			hostSetToAdd = sorted(expand_hostname(host,no_env=no_env))
		if username:
			# we expand the username
			username = sorted(expand_hostname(username,validate=False,no_env=no_env))
			# we combine the username and hostname
			hostSetToAdd = [u+'@'+h for u,h in product(username,hostSetToAdd)]
		expandedhosts.extend(hostSetToAdd)
	return expandedhosts

@cache_decorator
def validate_expand_hostname(hostname,no_env=False):
	'''
	Validate the hostname and expand it if it is a range of IP addresses

	Args:
		hostname (str): The hostname to be validated and expanded

	Returns:
		list: A list of valid hostnames
	'''
	# maybe it is just defined in ./target_files/hosts.sh and exported to the environment
	# we will try to get the valid host name from the environment
	hostname = hostname.strip('$')
	if getIP(hostname,local=True):
		return [hostname]
	elif not no_env and hostname in os.environ:
		# we will expand these hostnames again
		return expand_hostnames(frozenset(os.environ[hostname].split(',')),no_env=no_env)
	elif hostname in readEnvFromFile():
		# we will expand these hostnames again
		return expand_hostnames(frozenset(readEnvFromFile()[hostname].split(',')),no_env=no_env)
	elif getIP(hostname,local=False):
		return [hostname]
	else:
		print(f"Error: {hostname} is not a valid hostname or IP address!")
		global mainReturnCode
		mainReturnCode += 1
		global failedHosts
		failedHosts.add(hostname)
		return []

def input_with_timeout_and_countdown(timeout, prompt='Please enter your selection'):
	"""
	Read an input from the user with a timeout and a countdown.

	Parameters:
	timeout (int): The timeout value in seconds.
	prompt (str): The prompt message to display to the user. Default is 'Please enter your selection'.

	Returns:
	str or None: The user input if received within the timeout, or None if no input is received.
	"""
	import select
	# Print the initial prompt with the countdown
	print(f"{prompt} [{timeout}s]: ", end='', flush=True)
	# Loop until the timeout
	for remaining in range(timeout, 0, -1):
		# If there is an input, return it
		if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
			return input().strip()
		# Print the remaining time
		print(f"\r{prompt} [{remaining}s]: ", end='', flush=True)
		# Wait a second
		time.sleep(1)
	# If there is no input, return None
	return None

def handle_reading_stream(stream,target, host):
	'''
	Read the stream and append the lines to the target list

	Args:
		stream (io.BytesIO): The stream to be read
		target (list): The list to append the lines to
		host (Host): The host object

	Returns:
		None
	'''
	def add_line(current_line,target, host, keepLastLine=True):
		if not keepLastLine:
			target.pop()
			host.output.pop()
			host.printedLines -= 1
		current_line_str = current_line.decode('utf-8',errors='backslashreplace')
		target.append(current_line_str)
		host.output.append(current_line_str)
	current_line = bytearray()
	lastLineCommited = True
	for char in iter(lambda:stream.read(1), b''):
		if char == b'\n':
			if (not lastLineCommited) and current_line:
				add_line(current_line,target, host, keepLastLine=False)
			elif lastLineCommited:
				add_line(current_line,target, host, keepLastLine=True)
			current_line = bytearray()
			lastLineCommited = True
		elif char == b'\r':
			add_line(current_line,target, host, keepLastLine=lastLineCommited)
			current_line = bytearray()
			lastLineCommited = False
		else:
			current_line.extend(char)
	if current_line:
		add_line(current_line,target, host, keepLastLine=lastLineCommited)

def handle_writing_stream(stream,stop_event,host):
	'''
	Write the key presses to the stream

	Args:
		stream (io.BytesIO): The stream to be written to
		stop_event (threading.Event): The event to stop the thread
		host (Host): The host object

	Returns:
		None
	'''
	global keyPressesIn
	# keyPressesIn is a list of lists. 
	# Each list is a list of characters to be sent to the stdin of the process at once. 
	# We do not send the last line as it may be incomplete.
	sentInput = 0
	while not stop_event.is_set():
		if sentInput < len(keyPressesIn) - 1 :
			stream.write(''.join(keyPressesIn[sentInput]).encode())
			stream.flush()
			host.output.append(' $ ' + ''.join(keyPressesIn[sentInput]).encode().decode().replace('\n', '↵'))
			host.stdout.append(' $ ' + ''.join(keyPressesIn[sentInput]).encode().decode().replace('\n', '↵'))
			sentInput += 1
		else:
			time.sleep(0.1)
	if sentInput < len(keyPressesIn) - 1 :
		print(f"Warning: {len(keyPressesIn)-sentInput} key presses are not sent before the process is terminated!")
	# # send the last line
	# if keyPressesIn and keyPressesIn[-1]:
	#     stream.write(''.join(keyPressesIn[-1]).encode())
	#     stream.flush()
	#     host.output.append(' $ ' + ''.join(keyPressesIn[-1]).encode().decode().replace('\n', '↵'))
	#     host.stdout.append(' $ ' + ''.join(keyPressesIn[-1]).encode().decode().replace('\n', '↵'))
	return sentInput

def ssh_command(host, sem, timeout=60,passwds=None):
	'''
	Run the command on the host. Will format the commands accordingly. Main execution function.

	Args:
		host (Host): The host object
		sem (threading.Semaphore): The semaphore to limit the number of concurrent SSH sessions
		timeout (int, optional): The timeout for the command. Defaults to 60.
		passwds (str, optional): The password for the host. Defaults to None.

	Returns:
		None
	'''
	global emo
	with sem:
		try:
			host.username = None
			host.address = host.name
			if '@' in host.name:
				host.username, host.address = host.name.rsplit('@',1)
			if "#HOST#" in host.command.upper() or "#HOSTNAME#" in host.command.upper():
				host.command = host.command.replace("#HOST#",host.address).replace("#HOSTNAME#",host.address).replace("#host#",host.address).replace("#hostname#",host.address)
			if "#USER#" in host.command.upper() or "#USERNAME#" in host.command.upper():
				if host.username:
					host.command = host.command.replace("#USER#",host.username).replace("#USERNAME#",host.username).replace("#user#",host.username).replace("#username#",host.username)
				else:
					host.command = host.command.replace("#USER#",'CURRENT_USER').replace("#USERNAME#",'CURRENT_USER').replace("#user#",'CURRENT_USER').replace("#username#",'CURRENT_USER')
			formatedCMD = []
			if host.extraargs:
				extraargs = host.extraargs.split()
			else:
				extraargs = []
			if ipmiiInterfaceIPPrefix:
				host.interface_ip_prefix = ipmiiInterfaceIPPrefix if host.ipmi and not host.interface_ip_prefix else host.interface_ip_prefix
			if host.interface_ip_prefix:
				try:
					hostOctets = getIP(host.address,local=False).split('.')
					prefixOctets = host.interface_ip_prefix.split('.')
					host.address = '.'.join(prefixOctets[:3]+hostOctets[min(3,len(prefixOctets)):])
					host.resolvedName = host.username + '@' if host.username else ''
					host.resolvedName += host.address
				except:
					host.resolvedName = host.name
			else:
				host.resolvedName = host.name
			if host.ipmi:
				if host.command.startswith('ipmitool '):
					host.command = host.command.replace('ipmitool ','')
				if not host.username:
					host.username = 'admin'
				if passwds:
					formatedCMD = ['bash','-c',f'ipmitool -H {host.address} -U {host.username} -P {passwds} {" ".join(extraargs)} {host.command}']
				else:
					formatedCMD = ['bash','-c',f'ipmitool -H {host.address} -U {host.username} {" ".join(extraargs)} {host.command}']
			else:
				if host.files:
						if host.scp:
							formatedCMD = ['scp','-rpB'] + extraargs +['--']+host.files+[f'{host.resolvedName}:{host.command}']
						else:
							formatedCMD = ['rsync','-ahlX','--partial','--inplace', '--info=name'] + extraargs +['--']+host.files+[f'{host.resolvedName}:{host.command}']	
				else:
					formatedCMD = ['ssh'] + extraargs +['--']+ [host.resolvedName, host.command]
				if passwds and sshpassAvailable:
					formatedCMD = ['sshpass', '-p', passwds] + formatedCMD
				elif passwds:
					host.output.append('Warning: sshpass is not available. Please install sshpass to use password authentication.')
					#host.stderr.append('Warning: sshpass is not available. Please install sshpass to use password authentication.')
					host.output.append('Please provide password via live input or use ssh key authentication.')
					# # try to send the password via keyPressesIn
					# keyPressesIn[-1] = list(passwds) + ['\n']
					# keyPressesIn.append([])
			host.output.append('Running command: '+' '.join(formatedCMD))
			#host.stdout = []
			proc = subprocess.Popen(formatedCMD,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
			# create a thread to handle stdout
			stdout_thread = threading.Thread(target=handle_reading_stream, args=(proc.stdout,host.stdout, host), daemon=True)
			stdout_thread.start()
			# create a thread to handle stderr
			#host.stderr = []
			stderr_thread = threading.Thread(target=handle_reading_stream, args=(proc.stderr,host.stderr, host), daemon=True)
			stderr_thread.start()
			# create a thread to handle stdin
			stdin_stop_event = threading.Event()
			stdin_thread = threading.Thread(target=handle_writing_stream, args=(proc.stdin,stdin_stop_event, host), daemon=True)
			stdin_thread.start()
			# Monitor the subprocess and terminate it after the timeout
			start_time = time.time()
			outLength = len(host.output)
			while proc.poll() is None:  # while the process is still running
				if len(host.output) > outLength:
					start_time = time.time()
					outLength = len(host.output)
				if timeout > 0:
					if time.time() - start_time > timeout:
						host.stderr.append('Timeout!')
						host.output.append('Timeout!')
						proc.send_signal(signal.SIGINT)
						time.sleep(0.1)

						proc.terminate()
						break
					elif time.time() - start_time >  min(10, timeout // 2):
						timeoutLine = f'Timeout in [{timeout - int(time.time() - start_time)}] seconds!'
						if host.output and not host.output[-1].strip().startswith(timeoutLine):
							# remove last line if it is a countdown
							if host.output and host.output[-1].strip().endswith('] seconds!') and host.output[-1].strip().startswith('Timeout in ['):
								host.output.pop()
								host.printedLines -= 1
							host.output.append(timeoutLine)
							outLength = len(host.output)
				if emo:
					host.stderr.append('Ctrl C detected, Emergency Stop!')
					host.output.append('Ctrl C detected, Emergency Stop!')
					proc.send_signal(signal.SIGINT)
					time.sleep(0.1)
					proc.terminate()
					break
				time.sleep(0.1)  # avoid busy-waiting
			stdin_stop_event.set()
			# Wait for output processing to complete
			stdout_thread.join(timeout=1)
			stderr_thread.join(timeout=1)
			stdin_thread.join(timeout=1)
			# here we handle the rest of the stdout after the subprocess returns
			host.output.append(f'Pipe Closed. Trying to read the rest of the stdout...')
			if not emo:
				stdout = None
				stderr = None
				try:
					stdout, stderr = proc.communicate(timeout=1)
				except subprocess.TimeoutExpired:
					pass
				if stdout:
					handle_reading_stream(io.BytesIO(stdout),host.stdout, host)
				if stderr:
					handle_reading_stream(io.BytesIO(stderr),host.stderr, host)
				# if the last line in host.stderr is Connection to * closed., we will remove it
			host.returncode = proc.poll()
			if not host.returncode:
				# process been killed via timeout or sigkill
				if host.stderr and host.stderr[-1].strip().startswith('Timeout!'):
					host.returncode = 124
				elif host.stderr and host.stderr[-1].strip().startswith('Ctrl C detected, Emergency Stop!'):
					host.returncode = 137
			host.output.append(f'Command finished with return code {host.returncode}')
			if host.stderr and host.stderr[-1].strip().startswith('Connection to ') and host.stderr[-1].strip().endswith(' closed.'):
				host.stderr.pop()
		except Exception as e:
			import traceback
			host.stderr.extend(str(e).split('\n'))
			host.output.extend(str(e).split('\n'))
			host.stderr.extend(traceback.format_exc().split('\n'))
			host.output.extend(traceback.format_exc().split('\n'))
			host.returncode = -1
	# If using ipmi, we will try again using ssh if ipmi connection is not successful
	if host.ipmi and host.returncode != 0 and any(['Unable to establish IPMI' in line for line in host.stderr]):
		host.stderr = []
		host.output.append('IPMI connection failed! Trying SSH connection...')
		host.ipmi = False
		host.interface_ip_prefix = None
		host.command = 'ipmitool '+host.command if not host.command.startswith('ipmitool ') else host.command
		ssh_command(host,sem,timeout,passwds)
	# If transfering files, we will try again using scp if rsync connection is not successful
	if host.files and not host.scp and host.returncode != 0 and host.stderr:
		host.stderr = []
		host.stdout = []
		host.output.append('Rsync connection failed! Trying SCP connection...')
		host.scp = True
		ssh_command(host,sem,timeout,passwds)

def start_run_on_hosts(hosts, timeout=60,password=None,max_connections=4 * os.cpu_count()):
	'''
	Start running the command on the hosts. Wrapper function for ssh_command

	Args:
		hosts (list): A list of Host objects
		timeout (int, optional): The timeout for the command. Defaults to 60.
		password (str, optional): The password for the hosts. Defaults to None.
		max_connections (int, optional): The maximum number of concurrent SSH sessions. Defaults to 4 * os.cpu_count().

	Returns:
		list: A list of threads that get started
	'''
	if len(hosts) == 0:
		return []
	sem = threading.Semaphore(max_connections)  # Limit concurrent SSH sessions
	threads = [threading.Thread(target=ssh_command, args=(host, sem,timeout,password), daemon=True) for host in hosts]
	for thread in threads:
		thread.start()
	return threads

def get_hosts_to_display (hosts, max_num_hosts, hosts_to_display = None):
	'''
	Generate a list for the hosts to be displayed on the screen. This is used to display as much relevant information as possible.

	Args:
		hosts (list): A list of Host objects
		max_num_hosts (int): The maximum number of hosts to be displayed
		hosts_to_display (list, optional): The hosts that are currently displayed. Defaults to None.

	Returns:
		list: A list of Host objects to be displayed
	'''
	# We will sort the hosts by running -> failed -> finished -> waiting
	# running: returncode is None and output is not empty (output will be appened immediately after the command is run)
	# failed: returncode is not None and returncode is not 0
	# finished: returncode is not None and returncode is 0
	# waiting: returncode is None and output is empty
	running_hosts = [host for host in hosts if host.returncode is None and host.output]
	failed_hosts = [host for host in hosts if host.returncode is not None and host.returncode != 0]
	finished_hosts = [host for host in hosts if host.returncode is not None and host.returncode == 0]
	waiting_hosts = [host for host in hosts if host.returncode is None and not host.output]
	new_hosts_to_display = (running_hosts + failed_hosts + finished_hosts + waiting_hosts)[:max_num_hosts]
	if not hosts_to_display:
		return new_hosts_to_display , {'running':len(running_hosts), 'failed':len(failed_hosts), 'finished':len(finished_hosts), 'waiting':len(waiting_hosts)}
	# we will compare the new_hosts_to_display with the old one, if some hosts are not in their original position, we will change its printedLines to 0
	for i, host in enumerate(new_hosts_to_display):
		if host not in hosts_to_display:
			host.printedLines = 0
		elif i != hosts_to_display.index(host):
			host.printedLines = 0
	return new_hosts_to_display , {'running':len(running_hosts), 'failed':len(failed_hosts), 'finished':len(finished_hosts), 'waiting':len(waiting_hosts)}

def generate_display(stdscr, hosts, threads,lineToDisplay = -1,curserPosition = 0, min_char_len = DEFAULT_CURSES_MINIMUM_CHAR_LEN, min_line_len = DEFAULT_CURSES_MINIMUM_LINE_LEN,single_window=DEFAULT_SINGLE_WINDOW):
	try:
		org_dim = stdscr.getmaxyx()
		new_configured = True
		# To do this, first we need to know the size of the terminal
		max_y, max_x = org_dim
		# we will use one line to print the aggregated stats for the hosts.
		max_y -= 1
		# bound the min_char_len and min_line_len to between 1 and the max_x -1 and max_y -1
		min_char_len_local = min(max(1,min_char_len),max_x-1)
		min_line_len_local = min(max(1,min_line_len),max_y-1)
		if single_window:
			min_char_len_local = max_x-1
			min_line_len_local = max_y-1
		# raise zero division error if the terminal is too small
		if max_x < 2 or max_y < 2:
			raise ZeroDivisionError
		if min_char_len_local < 1 or min_line_len_local < 1:
			raise ZeroDivisionError
		# We need to figure out how many hosts we can fit in the terminal
		# We will need at least 2 lines per host, one for its name, one for its output
		# Each line will be at least 61 characters long (60 for the output, 1 for the borders)
		max_num_hosts_x = max_x // (min_char_len_local + 1)
		max_num_hosts_y = max_y // (min_line_len_local + 1)
		max_num_hosts = max_num_hosts_x * max_num_hosts_y
		if max_num_hosts < 1:
			raise ZeroDivisionError
		hosts_to_display , host_stats = get_hosts_to_display(hosts, max_num_hosts)
		if len(hosts_to_display) == 0:
			raise ZeroDivisionError
		# Now we calculate the actual number of hosts we will display for x and y
		optimal_len_x = max(min_char_len_local, 80)
		num_hosts_x = max(min(max_num_hosts_x, max_x // optimal_len_x),1)
		num_hosts_y = len(hosts_to_display) // num_hosts_x
		while num_hosts_y > max_num_hosts_y:
			num_hosts_x += 1
			# round up for num_hosts_y
			num_hosts_y = len(hosts_to_display) // num_hosts_x + (len(hosts_to_display) % num_hosts_x > 0)
			if num_hosts_x > max_num_hosts_x:
				num_hosts_x = 1
				num_hosts_y = len(hosts_to_display)
				while num_hosts_y > max_num_hosts_y:
					num_hosts_x += 1
					num_hosts_y = len(hosts_to_display) // num_hosts_x + (len(hosts_to_display) % num_hosts_x > 0)
				break

		# We calculate the size of each window
		host_window_height = max_y // num_hosts_y
		host_window_width = max_x // num_hosts_x
		if host_window_height < 1 or host_window_width < 1:
			raise ZeroDivisionError

		old_stat = ''
		old_bottom_stat = ''
		old_cursor_position = -1
		# we refresh the screen every 0.1 seconds
		last_refresh_time = time.perf_counter()
		stdscr.clear()
		#host_window.refresh()
		global keyPressesIn
		stdscr.nodelay(True)
		# we generate a stats window at the top of the screen
		stat_window = curses.newwin(1, max_x, 0, 0)
		# We create a window for each host
		host_windows = []
		for i, host in enumerate(hosts_to_display):
			# We calculate the coordinates of the window
			# We need to add 1 to y for the stats line
			y = (i // num_hosts_x) * host_window_height +1
			x = (i % num_hosts_x) * host_window_width
			#print(f"Creating a window at {y},{x}")
			# We create the window
			host_window = curses.newwin(host_window_height, host_window_width, y, x)
			host_windows.append(host_window)
		# If there is space left, we will draw the bottom border
		bottom_border = None
		if y + host_window_height  < org_dim[0]:
			bottom_border = curses.newwin(1, max_x, y + host_window_height, 0)
			bottom_border.clear()
			bottom_border.addstr(0, 0, '-' * (max_x - 1))
			bottom_border.refresh()
		while host_stats['running'] > 0 or host_stats['waiting'] > 0:
			# Check for keypress
			key = stdscr.getch()
			if key != -1:  # -1 means no keypress
				# we store the keypresses in a list of lists.
				# Each list is a list of characters to be sent to the stdin of the process at once.
				# When we encounter a newline, we add a new list to the list of lists. ( a new line of input )
				# with open('keylog.txt','a') as f:
				#     f.write(str(key)+'\n')
				if key == 410: # 410 is the key code for resize
					raise Exception('Terminal size changed. Please reconfigure window.')                
				# We handle positional keys
				# uparrow: 259; downarrow: 258; leftarrow: 260; rightarrow: 261
				# pageup: 339; pagedown: 338; home: 262; end: 360
				elif key in [259, 258, 260, 261, 339, 338, 262, 360]: 
					# if the key is up arrow, we will move the line to display up
					if key == 259: # 259 is the key code for up arrow
						lineToDisplay = max(lineToDisplay - 1, -len(keyPressesIn))
					# if the key is down arrow, we will move the line to display down
					elif key == 258: # 258 is the key code for down arrow
						lineToDisplay = min(lineToDisplay + 1, -1)
					# if the key is left arrow, we will move the cursor left
					elif key == 260: # 260 is the key code for left arrow
						curserPosition = min(max(curserPosition - 1, 0), len(keyPressesIn[lineToDisplay]) -1)
					# if the key is right arrow, we will move the cursor right
					elif key == 261: # 261 is the key code for right arrow
						curserPosition = max(min(curserPosition + 1, len(keyPressesIn[lineToDisplay])), 0)
					# if the key is page up, we will move the line to display up by 5 lines
					elif key == 339: # 339 is the key code for page up
						lineToDisplay = max(lineToDisplay - 5, -len(keyPressesIn))
					# if the key is page down, we will move the line to display down by 5 lines
					elif key == 338: # 338 is the key code for page down
						lineToDisplay = min(lineToDisplay + 5, -1)
					# if the key is home, we will move the cursor to the beginning of the line
					elif key == 262: # 262 is the key code for home
						curserPosition = 0
					# if the key is end, we will move the cursor to the end of the line
					elif key == 360: # 360 is the key code for end
						curserPosition = len(keyPressesIn[lineToDisplay])
				# We are left with these are keys that mofidy the current line.
				else:
					# This means the user have done scrolling and is committing to modify the current line.
					if lineToDisplay  < -1:
						# We overwrite the last line (current working line) with the line to display, removing the newline at the end
						keyPressesIn[-1] = keyPressesIn[lineToDisplay][:-1]
						lineToDisplay = -1
					curserPosition = max(0, min(curserPosition, len(keyPressesIn[lineToDisplay])))
					if key == 10: # 10 is the key code for newline
						keyPressesIn[-1].append(chr(key))
						keyPressesIn.append([])
						lineToDisplay = -1
						curserPosition = 0
					# if the key is backspace, we will remove the last character from the last list
					elif key in [8,263]: # 8 is the key code for backspace
						if curserPosition > 0:
							keyPressesIn[lineToDisplay].pop(curserPosition - 1)
							curserPosition -= 1
					# if the key is ESC, we will clear the last list
					elif key == 27: # 27 is the key code for ESC
						keyPressesIn[-1] = []
						curserPosition = 0
					# ignore delete key
					elif key in [127, 330]: # 330 is the key code for delete key
						# delete the character at the cursor position
						if curserPosition < len(keyPressesIn[lineToDisplay]):
							keyPressesIn[lineToDisplay].pop(curserPosition)
					else:
						# if the key is not a special key, we will add it
						keyPressesIn[lineToDisplay].insert(curserPosition, chr(key))
						curserPosition += 1
			# reconfigure when the terminal size changes
			# raise Exception when max_y or max_x is changed, let parent handle reconfigure
			if org_dim != stdscr.getmaxyx():
				raise Exception('Terminal size changed. Please reconfigure window.')
			# We generate the aggregated stats if user did not input anything
			if not keyPressesIn[lineToDisplay]:
				stats = '┍'+ f"Total: {len(hosts)}  Running: {host_stats['running']}  Failed: {host_stats['failed']}  Finished: {host_stats['finished']}  Waiting: {host_stats['waiting']}"[:max_x - 2].center(max_x - 2, "━")
			else:
				# we use the stat bar to display the key presses
				encodedLine = ''.join(keyPressesIn[lineToDisplay]).encode().decode().strip('\n') + ' '
				# # add the flashing indicator at the curse position
				# if time.perf_counter() % 1 > 0.5:
				#     encodedLine = encodedLine[:curserPosition] + '█' + encodedLine[curserPosition:]
				# else:
				#     encodedLine = encodedLine[:curserPosition] + ' ' + encodedLine[curserPosition:]
				stats = '┍'+ f"Send CMD: {encodedLine}"[:max_x - 2].center(max_x - 2, "━")
			if bottom_border:
				bottom_stats = '└'+ f"Total: {len(hosts)}  Running: {host_stats['running']}  Failed: {host_stats['failed']}  Finished: {host_stats['finished']}  Waiting: {host_stats['waiting']}"[:max_x - 2].center(max_x - 2, "─")
				if bottom_stats != old_bottom_stat:
					old_bottom_stat = bottom_stats
					bottom_border.clear()
					bottom_border.addstr(0, 0, bottom_stats)
					bottom_border.refresh()
			if stats != old_stat or curserPosition != old_cursor_position:
				old_stat = stats
				old_cursor_position = curserPosition
				# calculate the real curser position in stats as we centered the stats
				if 'Send CMD: ' in stats:
					curserPositionStats = min(min(curserPosition,len(encodedLine) -1) + stats.find('Send CMD: ')+len('Send CMD: '), max_x -2)
				else:
					curserPositionStats = max_x -2
				stat_window.clear()
				#stat_window.addstr(0, 0, stats)
				# add the line with curser that inverses the color at the curser position
				stat_window.addstr(0, 0, stats[:curserPositionStats], curses.color_pair(1))
				stat_window.addstr(0, curserPositionStats, stats[curserPositionStats], curses.color_pair(2))
				stat_window.addstr(0, curserPositionStats + 1, stats[curserPositionStats + 1:], curses.color_pair(1))
				stat_window.refresh()
			# set the maximum refresh rate to 100 Hz
			if time.perf_counter() - last_refresh_time < 0.01:
				time.sleep(max(0,0.01 - time.perf_counter() + last_refresh_time))
			#stdscr.clear()
			hosts_to_display, host_stats = get_hosts_to_display(hosts, max_num_hosts,hosts_to_display)
			for host_window, host in zip(host_windows, hosts_to_display):
				# we will only update the window if there is new output or the window is not fully printed
				if new_configured or host.printedLines < len(host.output):
					try:
						host_window.clear()
						# we will try to center the name of the host with ┼ at the beginning and end and ─ in between
						linePrintOut = f'┼{(host.name+":["+host.command+"]")[:host_window_width - 2].center(host_window_width - 1, "─")}'.replace('\n', ' ').replace('\r', ' ').strip()
						host_window.addstr(0, 0, linePrintOut)
						# we will display the latest outputs of the host as much as we can
						for i, line in enumerate(host.output[-(host_window_height - 1):]):
							# print(f"Printng a line at {i + 1} with length of {len('│'+line[:host_window_width - 1])}")
							# time.sleep(10)
							linePrintOut = ('│'+line[:host_window_width - 2].replace('\n', ' ').replace('\r', ' ')).strip()
							host_window.addstr(i + 1, 0, linePrintOut)
						# we draw the rest of the available lines
						for i in range(len(host.output), host_window_height - 1):
							# print(f"Printng a line at {i + 1} with length of {len('│')}")
							host_window.addstr(i + 1, 0, '│')
						host.printedLines = len(host.output)
						host_window.refresh()
					except Exception as e:
						# import traceback
						# print(str(e).strip())
						# print(traceback.format_exc().strip())
						if org_dim != stdscr.getmaxyx():
							raise Exception('Terminal size changed. Please reconfigure window.')
			new_configured = False
			last_refresh_time = time.perf_counter()

	except ZeroDivisionError:
		# terminial is too small, we skip the display
		pass
	except Exception as e:
		stdscr.clear()
		stdscr.refresh()
		generate_display(stdscr, hosts, threads, lineToDisplay, curserPosition, min_char_len, min_line_len, single_window)

def curses_print(stdscr, hosts, threads, min_char_len = DEFAULT_CURSES_MINIMUM_CHAR_LEN, min_line_len = DEFAULT_CURSES_MINIMUM_LINE_LEN,single_window = DEFAULT_SINGLE_WINDOW):
	'''
	Print the output of the hosts on the screen

	Args:
		stdscr (curses.window): The curses window to print the output
		hosts (list): A list of Host objects
		threads (list): A list of threads that are running the commands

	Returns:
		None
	'''
	# We create all the windows we need
	# We initialize the color pair
	curses.start_color()
	curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)
	curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
	curses.init_pair(8, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_RED)
	curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_GREEN)
	curses.init_pair(11, curses.COLOR_WHITE, curses.COLOR_YELLOW)
	curses.init_pair(12, curses.COLOR_WHITE, curses.COLOR_BLUE)
	curses.init_pair(13, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
	curses.init_pair(14, curses.COLOR_WHITE, curses.COLOR_CYAN)
	curses.init_pair(15, curses.COLOR_BLACK, curses.COLOR_RED)
	curses.init_pair(16, curses.COLOR_BLACK, curses.COLOR_GREEN)
	curses.init_pair(17, curses.COLOR_BLACK, curses.COLOR_YELLOW)
	curses.init_pair(18, curses.COLOR_BLACK, curses.COLOR_BLUE)
	curses.init_pair(19, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
	curses.init_pair(20, curses.COLOR_BLACK, curses.COLOR_CYAN)
	generate_display(stdscr, hosts, threads,min_char_len = min_char_len, min_line_len = min_line_len, single_window = single_window)

def print_output(hosts,usejson = False,quiet = False,greppable = False):
	'''
	Print / generate the output of the hosts to the terminal

	Args:
		hosts (list): A list of Host objects
		usejson (bool, optional): Whether to print the output in JSON format. Defaults to False.
		quiet (bool, optional): Whether to print the output. Defaults to False.

	Returns:
		str: The pretty output generated 
	'''
	global keyPressesIn
	global global_suppress_printout
	hosts = [dict(host) for host in hosts]
	if usejson:
		# [print(dict(host)) for host in hosts]
		#print(json.dumps([dict(host) for host in hosts],indent=4))
		rtnStr = json.dumps(hosts,indent=4)
	elif greppable:
		outputs = {}
		# transform hosts to dictionaries
		for host in hosts:
			hostPrintOut = f" | cmd: {host['command']} | stdout: "+'↵ '.join(host['stdout'])
			if host['stderr']:
				if host['stderr'][0].strip().startswith('ssh: connect to host '):
					host['stderr'][0] = 'SSH not reachable!'
				hostPrintOut += " | stderr: "+'↵ '.join(host['stderr'])
			hostPrintOut += f" | return_code: {host['returncode']}"
			if hostPrintOut not in outputs:
				outputs[hostPrintOut] = [host['name']]
			else:
				outputs[hostPrintOut].append(host['name'])
		rtnStr = ''
		for output, hosts in outputs.items():
			rtnStr += f"{','.join(hosts)}{output}\n"
		if keyPressesIn[-1]:
			CMDsOut = [''.join(cmd).encode('unicode_escape').decode().replace('\\n', '↵') for cmd in keyPressesIn if cmd]
			rtnStr += 'User Inputs: '+ '\nUser Inputs: '.join(CMDsOut)
			#rtnStr += '\n'
	else:
		outputs = {}
		for host in hosts:
			if global_suppress_printout:
				if host['returncode'] == 0:
					continue
			hostPrintOut = f"  Command:\n    {host['command']}\n"
			hostPrintOut += "  stdout:\n    "+'\n    '.join(host['stdout'])
			if host['stderr']:
				if host['stderr'][0].strip().startswith('ssh: connect to host '):
					host['stderr'][0] = 'SSH not reachable!'
				hostPrintOut += "\n  stderr:\n  "+'\n    '.join(host['stderr'])
			hostPrintOut += f"\n  return_code: {host['returncode']}"
			if hostPrintOut not in outputs:
				outputs[hostPrintOut] = [host['name']]
			else:
				outputs[hostPrintOut].append(host['name'])
		rtnStr = ''
		for output, hosts in outputs.items():
			if global_suppress_printout:
				rtnStr += f'Error returncode produced by {hosts}:\n'
				rtnStr += output+'\n'
			else:
				rtnStr += '*'*80+'\n'
				rtnStr += f"These hosts: {hosts} have a response of:\n"
				rtnStr += output+'\n'
		if not global_suppress_printout or outputs:
			rtnStr += '*'*80+'\n'
		if keyPressesIn[-1]:
			CMDsOut = [''.join(cmd).encode('unicode_escape').decode().replace('\\n', '↵') for cmd in keyPressesIn if cmd]
			#rtnStr += f"Key presses: {''.join(keyPressesIn).encode('unicode_escape').decode()}\n"
			#rtnStr += f"Key presses: {keyPressesIn}\n"
			rtnStr += "User Inputs: \n  "
			rtnStr += '\n  '.join(CMDsOut)
			rtnStr += '\n'
			keyPressesIn = [[]]
		if global_suppress_printout and not outputs:
			rtnStr += 'Success'
	if not quiet:
		print(rtnStr)
	return rtnStr

sshConfigged = False
def verify_ssh_config():
	'''
	Verify that ~/.ssh/config exists and contains the line "StrictHostKeyChecking no"

	Args:
		None

	Returns:
		None
	'''
	global sshConfigged
	if not sshConfigged:
		# first we make sure ~/.ssh/config exists
		config = ''
		if not os.path.exists(os.path.expanduser('~/.ssh')):
			os.makedirs(os.path.expanduser('~/.ssh'))
		if os.path.exists(os.path.expanduser('~/.ssh/config')):
			with open(os.path.expanduser('~/.ssh/config'),'r') as f:
				config = f.read()
		if config:
			if 'StrictHostKeyChecking no' not in config:
				with open(os.path.expanduser('~/.ssh/config'),'a') as f:
					f.write('\nHost *\n\tStrictHostKeyChecking no\n')
		else:
			with open(os.path.expanduser('~/.ssh/config'),'w') as f:
				f.write('Host *\n\tStrictHostKeyChecking no\n')
		sshConfigged = True

def signal_handler(sig, frame):
	'''
	Handle the Ctrl C signal

	Args:
		sig (int): The signal
		frame (frame): The frame

	Returns:
		None
	'''
	global emo
	if not emo:
		print('Ctrl C caught, exiting...')
		emo = True
	else:
		print('Ctrl C caught again, exiting immediately!')
		# wait for 0.1 seconds to allow the threads to exit
		time.sleep(0.1)
		os.system(f'pkill -ef {os.path.basename(__file__)}')
		sys.exit(0)


def processRunOnHosts(timeout, password, max_connections, hosts, returnUnfinished, quiet, json, called, greppable,unavailableHosts,willUpdateUnreachableHosts,curses_min_char_len = DEFAULT_CURSES_MINIMUM_CHAR_LEN, curses_min_line_len = DEFAULT_CURSES_MINIMUM_LINE_LEN,single_window = DEFAULT_SINGLE_WINDOW):
	global gloablUnavailableHosts
	threads = start_run_on_hosts(hosts, timeout=timeout,password=password,max_connections=max_connections)
	if not quiet and threads and not returnUnfinished and any([thread.is_alive() for thread in threads]) and sys.stdout.isatty() and os.get_terminal_size() and os.get_terminal_size().columns > 10:
		curses.wrapper(curses_print, hosts, threads, min_char_len = curses_min_char_len, min_line_len = curses_min_line_len, single_window = single_window)
	if not returnUnfinished:
		# wait until all hosts have a return code
		while any([host.returncode is None for host in hosts]):
			time.sleep(0.1)
		for thread in threads:
			thread.join(timeout=3)
	# update the unavailable hosts and global unavailable hosts
	if willUpdateUnreachableHosts:
		unavailableHosts.update([host.name for host in hosts if host.stderr and ('No route to host' in host.stderr[0].strip() or host.stderr[0].strip().startswith('Timeout!'))])
		gloablUnavailableHosts.update(unavailableHosts)
	# print the output, if the output of multiple hosts are the same, we aggragate them
	if not called:
		print_output(hosts,json,greppable=greppable)

@cache_decorator
def formHostStr(host) -> str:
	"""
	Forms a comma-separated string of hosts.

	Args:
		host: A string or a set of hosts.

	Returns:
		A string representing the hosts, separated by commas.
	"""
	if not host or len(host) == 0:
		return 'EMPTY_HOSTS'
	if type(host) is str:
		host = set(host.replace(',',' ').replace('\n',' ').replace('\r',' ').replace('\t',' ').replace(';', ' ').replace('|', ' ').replace('/', ' ').replace('&',' ').split())
	else:
		host = set(host)
	if 'local_shell' in host:
		host.remove('local_shell')
		host.add('localhost')
	host = ','.join(host)
	return host


@cache_decorator
def __formCommandArgStr(oneonone = DEFAULT_ONE_ON_ONE, timeout = DEFAULT_TIMEOUT,password = DEFAULT_PASSWORD,
						 quiet = DEFAULT_QUIET,json = DEFAULT_JSON_MODE,max_connections=DEFAULT_MAX_CONNECTIONS,
						 files = None,ipmi = DEFAULT_IPMI,interface_ip_prefix = DEFAULT_INTERFACE_IP_PREFIX,
						 scp=DEFAULT_SCP,username=DEFAULT_USERNAME,extraargs=DEFAULT_EXTRA_ARGS,skipUnreachable=DEFAULT_SKIP_UNREACHABLE,
						 no_env=DEFAULT_NO_ENV,greppable=DEFAULT_GREPPABLE_MODE,skip_hosts = DEFAULT_SKIP_HOSTS,
						 file_sync = False, error_only = DEFAULT_ERROR_ONLY,
						 shortend = False) -> str:
	argsList = []
	if oneonone: argsList.append('--oneonone' if not shortend else '-11')
	if timeout and timeout != DEFAULT_TIMEOUT: argsList.append(f'--timeout={timeout}' if not shortend else f'-t={timeout}')
	if password and password != DEFAULT_PASSWORD: argsList.append(f'--password="{password}"' if not shortend else f'-p="{password}"')
	if quiet: argsList.append('--quiet' if not shortend else '-q')
	if json: argsList.append('--json' if not shortend else '-j')
	if max_connections and max_connections != DEFAULT_MAX_CONNECTIONS: argsList.append(f'--maxconnections={max_connections}' if not shortend else f'-m={max_connections}')
	if files: argsList.extend([f'--file="{file}"' for file in files] if not shortend else [f'-f="{file}"' for file in files])
	if ipmi: argsList.append('--ipmi')
	if interface_ip_prefix and interface_ip_prefix != DEFAULT_INTERFACE_IP_PREFIX: argsList.append(f'--interface_ip_prefix="{interface_ip_prefix}"' if not shortend else f'-pre="{interface_ip_prefix}"')
	if scp: argsList.append('--scp')
	if username and username != DEFAULT_USERNAME: argsList.append(f'--username="{username}"' if not shortend else f'-u="{username}"')
	if extraargs and extraargs != DEFAULT_EXTRA_ARGS: argsList.append(f'--extraargs="{extraargs}"' if not shortend else f'-ea="{extraargs}"')
	if skipUnreachable: argsList.append('--skipUnreachable' if not shortend else '-su')
	if no_env: argsList.append('--no_env')
	if greppable: argsList.append('--greppable' if not shortend else '-g')
	if error_only: argsList.append('--error_only' if not shortend else '-eo')
	if skip_hosts and skip_hosts != DEFAULT_SKIP_HOSTS: argsList.append(f'--skip_hosts="{skip_hosts}"' if not shortend else f'-sh="{skip_hosts}"')
	if file_sync: argsList.append('--file_sync' if not shortend else '-fs')
	return ' '.join(argsList)

def getStrCommand(hosts,commands,oneonone = DEFAULT_ONE_ON_ONE, timeout = DEFAULT_TIMEOUT,password = DEFAULT_PASSWORD,
						 quiet = DEFAULT_QUIET,json = DEFAULT_JSON_MODE,called = DEFAULT_CALLED,max_connections=DEFAULT_MAX_CONNECTIONS,
						 files = None,ipmi = DEFAULT_IPMI,interface_ip_prefix = DEFAULT_INTERFACE_IP_PREFIX,returnUnfinished = DEFAULT_RETURN_UNFINISHED,
						 scp=DEFAULT_SCP,username=DEFAULT_USERNAME,extraargs=DEFAULT_EXTRA_ARGS,skipUnreachable=DEFAULT_SKIP_UNREACHABLE,
						 no_env=DEFAULT_NO_ENV,greppable=DEFAULT_GREPPABLE_MODE,willUpdateUnreachableHosts=DEFAULT_UPDATE_UNREACHABLE_HOSTS,no_start=DEFAULT_NO_START,
						 skip_hosts = DEFAULT_SKIP_HOSTS, curses_min_char_len = DEFAULT_CURSES_MINIMUM_CHAR_LEN, curses_min_line_len = DEFAULT_CURSES_MINIMUM_LINE_LEN,
						 single_window = DEFAULT_SINGLE_WINDOW,file_sync = False,error_only = DEFAULT_ERROR_ONLY, shortend = False):
	hosts = hosts if type(hosts) == str else frozenset(hosts)
	hostStr = formHostStr(hosts)
	files = frozenset(files) if files else None
	argsStr = __formCommandArgStr(oneonone = oneonone, timeout = timeout,password = password,
						 quiet = quiet,json = json,max_connections=max_connections,
						 files = files,ipmi = ipmi,interface_ip_prefix = interface_ip_prefix,scp=scp,
						 username=username,extraargs=extraargs,skipUnreachable=skipUnreachable,no_env=no_env,
						 greppable=greppable,skip_hosts = skip_hosts, file_sync = file_sync,error_only = error_only, shortend = shortend)
	commandStr = '"' + '" "'.join(commands) + '"' if commands else ''
	return f'multissh {argsStr} {hostStr} {commandStr}'

def run_command_on_hosts(hosts,commands,oneonone = DEFAULT_ONE_ON_ONE, timeout = DEFAULT_TIMEOUT,password = DEFAULT_PASSWORD,
						 quiet = DEFAULT_QUIET,json = DEFAULT_JSON_MODE,called = DEFAULT_CALLED,max_connections=DEFAULT_MAX_CONNECTIONS,
						 files = None,ipmi = DEFAULT_IPMI,interface_ip_prefix = DEFAULT_INTERFACE_IP_PREFIX,returnUnfinished = DEFAULT_RETURN_UNFINISHED,
						 scp=DEFAULT_SCP,username=DEFAULT_USERNAME,extraargs=DEFAULT_EXTRA_ARGS,skipUnreachable=DEFAULT_SKIP_UNREACHABLE,
						 no_env=DEFAULT_NO_ENV,greppable=DEFAULT_GREPPABLE_MODE,willUpdateUnreachableHosts=DEFAULT_UPDATE_UNREACHABLE_HOSTS,no_start=DEFAULT_NO_START,
						 skip_hosts = DEFAULT_SKIP_HOSTS, curses_min_char_len = DEFAULT_CURSES_MINIMUM_CHAR_LEN, curses_min_line_len = DEFAULT_CURSES_MINIMUM_LINE_LEN,
						 single_window = DEFAULT_SINGLE_WINDOW,file_sync = False,error_only = DEFAULT_ERROR_ONLY):
	f'''
	Run the command on the hosts, aka multissh. main function

	Args:
		hosts (str/iterable): A string of hosts seperated by space or comma / iterable of hosts.
		commands (list): A list of commands to run on the hosts. When using files, defines the destination of the files.
		oneonone (bool, optional): Whether to run the commands one on one. Defaults to {DEFAULT_ONE_ON_ONE}.
		timeout (int, optional): The timeout for the command. Defaults to {DEFAULT_TIMEOUT}.
		password (str, optional): The password for the hosts. Defaults to {DEFAULT_PASSWORD}.
		quiet (bool, optional): Whether to print the output. Defaults to {DEFAULT_QUIET}.
		json (bool, optional): Whether to print the output in JSON format. Defaults to {DEFAULT_JSON_MODE}.
		called (bool, optional): Whether the function is called by another function. Defaults to {DEFAULT_CALLED}.
		max_connections (int, optional): The maximum number of concurrent SSH sessions. Defaults to 4 * os.cpu_count().
		files (list, optional): A list of files to be copied to the hosts. Defaults to None.
		ipmi (bool, optional): Whether to use IPMI to connect to the hosts. Defaults to {DEFAULT_IPMI}.
		interface_ip_prefix (str, optional): The prefix of the IPMI interface. Defaults to {DEFAULT_INTERFACE_IP_PREFIX}.
		returnUnfinished (bool, optional): Whether to return the unfinished hosts. Defaults to {DEFAULT_RETURN_UNFINISHED}.
		scp (bool, optional): Whether to use scp instead of rsync. Defaults to {DEFAULT_SCP}.
		username (str, optional): The username to use to connect to the hosts. Defaults to {DEFAULT_USERNAME}.
		extraargs (str, optional): Extra arguments to pass to the ssh / rsync / scp command. Defaults to {DEFAULT_EXTRA_ARGS}.
		skipUnreachable (bool, optional): Whether to skip unreachable hosts. Defaults to {DEFAULT_SKIP_UNREACHABLE}.
		no_env (bool, optional): Whether to not read the current sat system environment variables. (Will still read from files) Defaults to {DEFAULT_NO_ENV}.
		greppable (bool, optional): Whether to print the output in greppable format. Defaults to {DEFAULT_GREPPABLE_MODE}.
		willUpdateUnreachableHosts (bool, optional): Whether to update the global unavailable hosts. Defaults to {DEFAULT_UPDATE_UNREACHABLE_HOSTS}.
		no_start (bool, optional): Whether to return the hosts without starting the command. Defaults to {DEFAULT_NO_START}.
		skip_hosts (str, optional): The hosts to skip. Defaults to {DEFAULT_SKIP_HOSTS}.
		min_char_len (int, optional): The minimum character per line of the curses output. Defaults to {DEFAULT_CURSES_MINIMUM_CHAR_LEN}.
		min_line_len (int, optional): The minimum line number for each window of the curses output. Defaults to {DEFAULT_CURSES_MINIMUM_LINE_LEN}.
		single_window (bool, optional): Whether to use a single window for the curses output. Defaults to {DEFAULT_SINGLE_WINDOW}.
		file_sync (bool, optional): Whether to use file sync mode to sync directories. Defaults to {DEFAULT_FILE_SYNC}.

	Returns:
		list: A list of Host objects
	'''
	global gloablUnavailableHosts
	global global_suppress_printout
	if not max_connections:
		max_connections = 4 * os.cpu_count()
	elif max_connections == 0:
		max_connections = 1048576
	elif max_connections < 0:
		max_connections = (-max_connections) * os.cpu_count()
	if not commands:
		commands = []
	verify_ssh_config()
	# load global unavailable hosts only if the function is called (so using --repeat will not load the unavailable hosts again)
	if called:
		# if called,
		# if skipUnreachable is not set, we default to skip unreachable hosts within one command call
		global_suppress_printout = True
		if skipUnreachable is None:
			skipUnreachable = True
		if skipUnreachable:
			unavailableHosts = gloablUnavailableHosts
		else:
			unavailableHosts = set()
	else:
		# if run in command line ( or emulating running in command line, we default to skip unreachable hosts within one command call )
		if skipUnreachable:
			unavailableHosts = gloablUnavailableHosts
		else:
			unavailableHosts = set()
			skipUnreachable = True
	global emo
	emo = False
	# We create the hosts
	hostStr = formHostStr(hosts)
	skipHostStr = formHostStr(skip_hosts) if skip_hosts else ''

	if username:
		userStr = f'{username.strip()}@'
		# we also append this userStr to all hostStr which does not have username already defined
		hostStr = hostStr.split(',')
		for i, host in enumerate(hostStr):
			if '@' not in host:
				hostStr[i] = userStr + host
		hostStr = ','.join(hostStr)
		if skipHostStr:
			skipHostStr = skipHostStr.split(',')
			for i, host in enumerate(skipHostStr):
				if '@' not in host:
					skipHostStr[i] = userStr + host
			skipHostStr = ','.join(skipHostStr)
	targetHostsList = expand_hostnames(frozenset(hostStr.split(',')),no_env=no_env)
	skipHostsList = expand_hostnames(frozenset(skipHostStr.split(',')),no_env=no_env)
	if skipHostsList:
		if not global_suppress_printout: print(f"Skipping hosts: {skipHostsList}")
	if files and not commands:
		# if files are specified but not target dir, we default to file sync mode
		file_sync = True
	if file_sync:
		# set the files to the union of files and commands
		files = set(files+commands) if files else set(commands)
	if files:
		# try to resolve files first (like * etc)
		pathSet = set()
		for file in files:
			try:
				pathSet.update(glob.glob(file,include_hidden=True,recursive=True))
			except:
				pathSet.update(glob.glob(file,recursive=True))
		if not pathSet:
			print(f'Warning: No source files at {files} are found after resolving globs!')
			sys.exit(66)
		if file_sync:
			# use abosolute path for file sync
			commands = [os.path.abspath(file) for file in pathSet]
			files = []
		else:
			files = list(pathSet)
	if oneonone:
		hosts = []
		if len(commands) != len(targetHostsList) - len(skipHostsList):
			print("Error: the number of commands must be the same as the number of hosts")
			print(f"Number of commands: {len(commands)}")
			print(f"Number of hosts: {len(targetHostsList - skipHostsList)}")
			sys.exit(255)
		if not global_suppress_printout:
			print('-'*80)
			print("Running in one on one mode")
		for host, command in zip(targetHostsList, commands):
			if not ipmi and skipUnreachable and host.strip() in unavailableHosts:
				if not global_suppress_printout: print(f"Skipping unavailable host: {host}")
				continue
			if host.strip() in skipHostsList: continue
			if file_sync:
				hosts.append(Host(host.strip(), os.path.dirname(command)+os.path.sep, files = [command],ipmi=ipmi,interface_ip_prefix=interface_ip_prefix,scp=scp,extraargs=extraargs))
			else:
				hosts.append(Host(host.strip(), command, files = files,ipmi=ipmi,interface_ip_prefix=interface_ip_prefix,scp=scp,extraargs=extraargs))
			if not global_suppress_printout: 
				print(f"Running command: {command} on host: {host}")
		if not global_suppress_printout: print('-'*80)
		if not no_start: processRunOnHosts(timeout, password, max_connections, hosts, returnUnfinished, quiet, json, called, greppable,unavailableHosts,willUpdateUnreachableHosts,curses_min_char_len = curses_min_char_len, curses_min_line_len = curses_min_line_len,single_window=single_window)
		return hosts
	else:
		allHosts = []
		if not commands:
			# run in interactive mode ssh mode
			hosts = []
			for host in targetHostsList:
				if not ipmi and skipUnreachable and host.strip() in unavailableHosts:
					if not global_suppress_printout: print(f"Skipping unavailable host: {host}")
					continue
				if host.strip() in skipHostsList: continue
				if file_sync:
					print(f"Error: file sync mode need to be specified with at least one path to sync.")
					return []
				elif files:
					print(f"Error: files need to be specified with at least one path to sync")
				elif ipmi:
					print(f"Error: ipmi mode is not supported in interactive mode")
				else:
					hosts.append(Host(host.strip(), '', files = files,ipmi=ipmi,interface_ip_prefix=interface_ip_prefix,scp=scp,extraargs=extraargs))
			if not global_suppress_printout:
				print('-'*80)
				print(f"Running in interactive mode on hosts: {hostStr}" + (f"; skipping: {skipHostStr}" if skipHostStr else ''))
				print('-'*80)
			if no_start:
				print(f"Warning: no_start is set, the command will not be started. As we are in interactive mode, no action will be done.")
			else:
				processRunOnHosts(timeout, password, max_connections, hosts, returnUnfinished, quiet, json, called, greppable,unavailableHosts,willUpdateUnreachableHosts,curses_min_char_len = curses_min_char_len, curses_min_line_len = curses_min_line_len,single_window=single_window)
			return hosts
		for command in commands:
			hosts = []
			for host in targetHostsList:
				if not ipmi and skipUnreachable and host.strip() in unavailableHosts:
					if not global_suppress_printout: print(f"Skipping unavailable host: {host}")
					continue
				if host.strip() in skipHostsList: continue
				if file_sync:
					hosts.append(Host(host.strip(), os.path.dirname(command)+os.path.sep, files = [command],ipmi=ipmi,interface_ip_prefix=interface_ip_prefix,scp=scp,extraargs=extraargs))
				else:
					hosts.append(Host(host.strip(), command, files = files,ipmi=ipmi,interface_ip_prefix=interface_ip_prefix,scp=scp,extraargs=extraargs))
			if not global_suppress_printout and len(commands) > 1:
				print('-'*80)
				print(f"Running command: {command} on hosts: {hostStr}" + (f"; skipping: {skipHostStr}" if skipHostStr else ''))
				print('-'*80)
			if not no_start: processRunOnHosts(timeout, password, max_connections, hosts, returnUnfinished, quiet, json, called, greppable,unavailableHosts,willUpdateUnreachableHosts,curses_min_char_len = curses_min_char_len, curses_min_line_len = curses_min_line_len,single_window=single_window)
			allHosts += hosts
		return allHosts

def main():
	global emo
	global global_suppress_printout
	global gloablUnavailableHosts
	global mainReturnCode
	global failedHosts
	global keyPressesIn
	global ipmiiInterfaceIPPrefix
	global sshpassAvailable
	global env_file
	emo = False


	# We handle the signal
	signal.signal(signal.SIGINT, signal_handler)
	# We parse the arguments
	parser = argparse.ArgumentParser(description='Run a command on multiple hosts, Use #HOST# or #HOSTNAME# to replace the host name in the command')
	parser.add_argument('hosts', metavar='hosts', type=str, help='Hosts to run the command on, use "," to seperate hosts')
	parser.add_argument('commands', metavar='commands', type=str, nargs='+',help='the command to run on the hosts / the destination of the files #HOST# or #HOSTNAME# will be replaced with the host name.')
	parser.add_argument('-u','--username', type=str,help=f'The general username to use to connect to the hosts. Will get overwrote by individual username@host if specified. (default: {DEFAULT_USERNAME})',default=DEFAULT_USERNAME)
	parser.add_argument('-ea','--extraargs',type=str,help=f'Extra arguments to pass to the ssh / rsync / scp command. Put in one string for multiple arguments.Use "=" ! Ex. -ea="--delete" (default: {DEFAULT_EXTRA_ARGS})',default=DEFAULT_EXTRA_ARGS)
	parser.add_argument('-p', '--password', type=str,help=f'The password to use to connect to the hosts, (default: {DEFAULT_PASSWORD})',default=DEFAULT_PASSWORD)
	parser.add_argument("-11",'--oneonone', action='store_true', help=f"Run one corresponding command on each host. (default: {DEFAULT_ONE_ON_ONE})", default=DEFAULT_ONE_ON_ONE)
	parser.add_argument("-f","--file", action='append', help="The file to be copied to the hosts. Use -f multiple times to copy multiple files")
	parser.add_argument('--file_sync', action='store_true', help=f'Operate in file sync mode, sync path in <COMMANDS> from this machine to <HOSTS>. Treat --file <FILE> and <COMMANDS> both as source as source and destination will be the same in this mode. (default: {DEFAULT_FILE_SYNC})', default=DEFAULT_FILE_SYNC)
	parser.add_argument('--scp', action='store_true', help=f'Use scp for copying files instead of rsync. Need to use this on windows. (default: {DEFAULT_SCP})', default=DEFAULT_SCP)
	#parser.add_argument("-d",'-c',"--destination", type=str, help="The destination of the files. Same as specify with commands. Added for compatibility. Use #HOST# or #HOSTNAME# to replace the host name in the destination")
	parser.add_argument("-t","--timeout", type=int, help=f"Timeout for each command in seconds (default: 0 (disabled))", default=0)
	parser.add_argument("-r","--repeat", type=int, help=f"Repeat the command for a number of times (default: {DEFAULT_REPEAT})", default=DEFAULT_REPEAT)
	parser.add_argument("-i","--interval", type=int, help=f"Interval between repeats in seconds (default: {DEFAULT_INTERVAL})", default=DEFAULT_INTERVAL)
	parser.add_argument("--ipmi", action='store_true', help=f"Use ipmitool to run the command. (default: {DEFAULT_IPMI})", default=DEFAULT_IPMI)
	parser.add_argument("-mpre","--ipmi_interface_ip_prefix", type=str, help=f"The prefix of the IPMI interfaces (default: {DEFAULT_IPMI_INTERFACE_IP_PREFIX})", default=DEFAULT_IPMI_INTERFACE_IP_PREFIX)
	parser.add_argument("-pre","--interface_ip_prefix", type=str, help=f"The prefix of the for the interfaces (default: {DEFAULT_INTERFACE_IP_PREFIX})", default=DEFAULT_INTERFACE_IP_PREFIX)
	parser.add_argument("-q","--quiet", action='store_true', help=f"Quiet mode, no curses, only print the output. (default: {DEFAULT_QUIET})", default=DEFAULT_QUIET)
	parser.add_argument("-ww",'--window_width', type=int, help=f"The minimum character length of the curses window. (default: {DEFAULT_CURSES_MINIMUM_CHAR_LEN})", default=DEFAULT_CURSES_MINIMUM_CHAR_LEN)
	parser.add_argument("-wh",'--window_height', type=int, help=f"The minimum line height of the curses window. (default: {DEFAULT_CURSES_MINIMUM_LINE_LEN})", default=DEFAULT_CURSES_MINIMUM_LINE_LEN)
	parser.add_argument('-sw','--single_window', action='store_true', help=f'Use a single window for all hosts. (default: {DEFAULT_SINGLE_WINDOW})', default=DEFAULT_SINGLE_WINDOW)
	parser.add_argument('-eo','--error_only', action='store_true', help=f'Only print the error output. (default: {DEFAULT_ERROR_ONLY})', default=DEFAULT_ERROR_ONLY)
	parser.add_argument("-no","--nooutput", action='store_true', help=f"Do not print the output. (default: {DEFAULT_NO_OUTPUT})", default=DEFAULT_NO_OUTPUT)
	parser.add_argument('--no_env', action='store_true', help=f'Do not load the environment variables. (default: {DEFAULT_NO_ENV})', default=DEFAULT_NO_ENV)
	parser.add_argument("--env_file", type=str, help=f"The file to load the environment variables from. (default: {DEFAULT_ENV_FILE})", default=DEFAULT_ENV_FILE)
	parser.add_argument("-m","--maxconnections", type=int, help=f"Max number of connections to use (default: 4 * cpu_count)", default=DEFAULT_MAX_CONNECTIONS)
	parser.add_argument("-j","--json", action='store_true', help=F"Output in json format. (default: {DEFAULT_JSON_MODE})", default=DEFAULT_JSON_MODE)
	parser.add_argument("--success_hosts", action='store_true', help=f"Output the hosts that succeeded in summary as wells. (default: {DEFAULT_PRINT_SUCCESS_HOSTS})", default=DEFAULT_PRINT_SUCCESS_HOSTS)
	parser.add_argument("-g","--greppable", action='store_true', help=f"Output in greppable format. (default: {DEFAULT_GREPPABLE_MODE})", default=DEFAULT_GREPPABLE_MODE)
	parser.add_argument("-nw","--nowatch", action='store_true', help=f"Do not watch the output in curses modem, Use \\r. Not implemented yet. (default: {DEFAULT_NO_WATCH})", default=DEFAULT_NO_WATCH)
	parser.add_argument("-su","--skipunreachable", action='store_true', help=f"Skip unreachable hosts while using --repeat. Note: Timedout Hosts are considered unreachable. Note: multiple command sequence will still auto skip unreachable hosts. (default: {DEFAULT_SKIP_UNREACHABLE})", default=DEFAULT_SKIP_UNREACHABLE)
	parser.add_argument("-sh","--skiphosts", type=str, help=f"Skip the hosts in the list. (default: {DEFAULT_SKIP_HOSTS})", default=DEFAULT_SKIP_HOSTS)
	parser.add_argument("-V","--version", action='version', version=f'%(prog)s {version} {("with sshpass " if sshpassAvailable else "")}by pan@zopyr.us')
	
	# parser.add_argument('-u', '--user', metavar='user', type=str, nargs=1,
	#                     help='the user to use to connect to the hosts')
	args = parser.parse_args()

	env_file = args.env_file
	# if there are more than 1 commands, and every command only consists of one word,
	# we will ask the user to confirm if they want to run multiple commands or just one command.
	if not args.file and len(args.commands) > 1 and all([len(command.split()) == 1 for command in args.commands]):
		print(f"Multiple one word command detected, what to do? (s/f/n)")
		print(f"1:  Run 1 command [{' '.join(args.commands)}] on all hosts ( default )")
		print(f"m:  Run multiple commands [{', '.join(args.commands)}] on all hosts")
		print(f"n:  Exit")
		inStr = input_with_timeout_and_countdown(3)
		if (not inStr) or inStr.lower().strip().startswith('1'):
			args.commands = [" ".join(args.commands)]
			print(f"\nRunning 1 command: {args.commands[0]} on all hosts")
		elif inStr.lower().strip().startswith('m'):
			print(f"\nRunning multiple commands: {', '.join(args.commands)} on all hosts")
		else:
			sys.exit(0)
	
	ipmiiInterfaceIPPrefix = args.ipmi_interface_ip_prefix

	if not args.greppable and not args.json and not args.nooutput:
		global_suppress_printout = False

	if not global_suppress_printout:
		print('> ' + getStrCommand(args.hosts,args.commands,oneonone=args.oneonone,timeout=args.timeout,password=args.password,
						 quiet=args.quiet,json=args.json,called=args.nooutput,max_connections=args.maxconnections,
						 files=args.file,file_sync=args.file_sync,ipmi=args.ipmi,interface_ip_prefix=args.interface_ip_prefix,scp=args.scp,username=args.username,
						 extraargs=args.extraargs,skipUnreachable=args.skipunreachable,no_env=args.no_env,greppable=args.greppable,skip_hosts = args.skiphosts,
						 curses_min_char_len = args.window_width, curses_min_line_len = args.window_height,single_window=args.single_window,error_only=args.error_only))
	if args.error_only:
		global_suppress_printout = True

	for i in range(args.repeat):
		if args.interval > 0 and i < args.repeat - 1:
			print(f"Sleeping for {args.interval} seconds")
			time.sleep(args.interval)

		if not global_suppress_printout: print(f"Running the {i+1}/{args.repeat} time") if args.repeat > 1 else None
		hosts = run_command_on_hosts(args.hosts,args.commands,
							 oneonone=args.oneonone,timeout=args.timeout,password=args.password,
							 quiet=args.quiet,json=args.json,called=args.nooutput,max_connections=args.maxconnections,
							 files=args.file,file_sync=args.file_sync,ipmi=args.ipmi,interface_ip_prefix=args.interface_ip_prefix,scp=args.scp,username=args.username,
							 extraargs=args.extraargs,skipUnreachable=args.skipunreachable,no_env=args.no_env,greppable=args.greppable,skip_hosts = args.skiphosts,
							 curses_min_char_len = args.window_width, curses_min_line_len = args.window_height,single_window=args.single_window,error_only=args.error_only)
		#print('*'*80)

		if not global_suppress_printout: print('-'*80)
	
	succeededHosts = set()
	for host in hosts:
		if host.returncode and host.returncode != 0:
			mainReturnCode += 1
			failedHosts.add(host.name)
		else:
			succeededHosts.add(host.name)
	succeededHosts -= failedHosts
	# sort the failed hosts and succeeded hosts
	failedHosts = sorted(failedHosts)
	succeededHosts = sorted(succeededHosts)
	if mainReturnCode > 0:
		if not global_suppress_printout: print(f'Complete. Failed hosts (Return Code not 0) count: {mainReturnCode}')
		# with open('/tmp/bashcmd.stdin','w') as f:
		#     f.write(f"export failed_hosts={failedHosts}\n")
		if not global_suppress_printout: print(f'failed_hosts: {",".join(failedHosts)}')
	else:
		if not global_suppress_printout: print('Complete. All hosts returned 0.')
	
	if args.success_hosts and not global_suppress_printout:
		print(f'succeeded_hosts: {",".join(succeededHosts)}')

	if threading.active_count() > 1:
		if not global_suppress_printout: print(f'Remaining active thread: {threading.active_count()}')
		# os.system(f'pkill -ef  {os.path.basename(__file__)}')
		# os._exit(mainReturnCode)
	
	sys.exit(mainReturnCode)



if __name__ == "__main__":
	main()
