#!/usr/bin/python

#       Route your traffic through Tor
#       Do this by first "chmod +x install.sh"
#       Then install by "./install.sh" and you're good to go
#       Enjoy remining anonymous 




import os
import sys
from commands import getoutput
import time
import signal
from json import load
from urllib2 import urlopen

class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[31m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BGRED = '\033[41m'
    WHITE = '\033[37m'


def t():
    current_time = time.localtime()
    ctime = time.strftime('%H:%M:%S', current_time)
    return "["+ ctime + "]"
def shutdown():
	print ""
	print bcolors.BGRED + bcolors.WHITE + t() + "[info] shutting down the onion" + bcolors.ENDC +"\n\n"
	sys.exit()


def sigint_handler(signum, frame):
    print '\n user interrupt ! shutting down'
    shutdown()

def logo():
	os.system("clear")
	print bcolors.RED + bcolors.BOLD
	print """
  _______ _             ____        _
 |__   __| |           / __ \      (_)
    | |  | |__   ___  | |  | |_ __  _  ___  _ __
    | |  | '_ \ / _ \ | |  | | '_ \| |/ _ \| '_ \
    | |  | | | |  __/ | |__| | | | | | (_) | | | |
    |_|  |_| |_|\___|  \____/|_| |_|_|\___/|_| |_|
	BetaVersion - The Rainbow Hacker
    """
	print bcolors.ENDC
def usage():
	logo()
	print """
	USAGE:
        onion start -----(start onion)
        onion stop  -----(stop onion)
    """
	sys.exit()

def ip():
	while True:
		try:
			ipadd = load(urlopen('https://api.ipify.org?format=json'))['ip']
		except :
			continue
		break
	return ipadd

signal.signal(signal.SIGINT, sigint_handler)

TorrcCfgString = """
VirtualAddrNetwork 10.0.0.0/10
AutomapHostsOnResolve 1
TransPort 9040
DNSPort 53
"""

resolvString = "nameserver 127.0.0.1"

Torrc = "/etc/tor/torrc"
resolv = "/etc/resolv.conf"


def start_onion():



	if TorrcCfgString in open(Torrc).read():
	    print t()+" Torrc file already configured"
	else:
		with open(Torrc, "a") as myfile:
			print t()+" Configuring torrc file.. ",
			myfile.write(TorrcCfgString)
			print bcolors.GREEN+"[done]"+bcolors.ENDC
	if resolvString in open(resolv).read():
	    print t()+" DNS resolv.conf file already configured"
	else:
		with open(resolv, "w") as myfile:
			print t()+" Configuring DNS resolv.conf file.. ",
			myfile.write(resolvString)
			print bcolors.GREEN+"[done]"+bcolors.ENDC

	print t()+" Starting tor service.. ",
	os.system("service tor start")
	print bcolors.GREEN+"[done]"+bcolors.ENDC
	print t()+" setting up iptables rules",

	iptables_rules = """
	NON_TOR="192.168.1.0/24 192.168.0.0/24"
	TOR_UID=%s
	TRANS_PORT="9040"
	iptables -F
	iptables -t nat -F
	iptables -t nat -A OUTPUT -m owner --uid-owner $TOR_UID -j RETURN
	iptables -t nat -A OUTPUT -p udp --dport 53 -j REDIRECT --to-ports 53
	for NET in $NON_TOR 127.0.0.0/9 127.128.0.0/10; do
	 iptables -t nat -A OUTPUT -d $NET -j RETURN
	done
	iptables -t nat -A OUTPUT -p tcp --syn -j REDIRECT --to-ports $TRANS_PORT
	iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
	for NET in $NON_TOR 127.0.0.0/8; do
	 iptables -A OUTPUT -d $NET -j ACCEPT
	done
	iptables -A OUTPUT -m owner --uid-owner $TOR_UID -j ACCEPT
	iptables -A OUTPUT -j REJECT
	"""%(getoutput("id -ur debian-tor"))

	os.system(iptables_rules)
	print bcolors.GREEN+"[done]"+bcolors.ENDC
	print t()+" Fetching current IP..."
	print t()+" CURRENT IP : "+bcolors.GREEN+ip()+bcolors.ENDC

def stop_onion():
	print bcolors.RED+t()+"STOPPING onion"+bcolors.ENDC
	print t()+" Flushing iptables, resetting to default",
	IpFlush = """
	iptables -P INPUT ACCEPT
	iptables -P FORWARD ACCEPT
	iptables -P OUTPUT ACCEPT
	iptables -t nat -F
	iptables -t mangle -F
	iptables -F
	iptables -X
	"""
	os.system(IpFlush)
	print bcolors.GREEN+"[done]"+bcolors.ENDC
	print t()+" Restarting Network manager",
	os.system("service network-manager restart")
	print bcolors.GREEN+"[done]"+bcolors.ENDC
	print t()+" Fetching current IP..."
	print t()+" CURRENT IP : "+bcolors.GREEN+ip()+bcolors.ENDC

arg = sys.argv[1:]


if len(arg)!=1:
	usage()
elif sys.argv[1] == "start":
	logo()
	start_onion()
elif sys.argv[1] == "stop":
	logo()
	stop_onion()
else:
	usage()
