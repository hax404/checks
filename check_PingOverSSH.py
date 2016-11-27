#!/usr/bin/env python3

import argparse
import imp
import paramiko

def parseArgs():
	parser = argparse.ArgumentParser(description="let external machine check ping")
	parser.add_argument("--host", dest="host", required=True, help="Host that executes ping")
	parser.add_argument("--username", dest="username", help="SSH username")
	parser.add_argument("--password", dest="password", help="SSH password")
	parser.add_argument("--os", choices=["openwrt","mikrotik"], default="openwrt", required=True, help="OS of the machine that executes ping. Default=openwrt")
	parser.add_argument("--ping-command", dest="ping_command", help="Ping Command")
	parser.add_argument("--interface", dest="interface", help="the interface name from where the ping is sent")
	parser.add_argument("--ttl", dest="ttl", help="the time to live that is passed to the ping command")
	parser.add_argument("--count", dest="count", default="10", help="the number how many pings to sent for the statistic")
	parser.add_argument("--dest", dest="destination", required=True, help="destination of ping")
	return parser.parse_args()

def checkParamiko():
	try:
		imp.find_module("paramiko")
		print ("paramiko is installed")
	except:
		print ("paramiko is not installed. You need the package paramiko.")
		exit()

def pingOpenWRT(args):
	pingcommandlist = []
	pingcommandlist.append("ping")
	if(args.interface):
		pingcommandlist.append("-I")
		pingcommandlist.append(args.interface)
	if(args.ttl):
		pingcommandlist.append("-t")
		pingcommandlist.append(args.ttl)
	pingcommandlist.append("-c")
	pingcommandlist.append(args.count)
	pingcommandlist.append("-q")
	pingcommandlist.append(args.destination)
	pingcommand = " ".join(pingcommandlist)
	print(pingcommand)

	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.connect(args.host,username=args.username,password=args.password)
	stdin, stdout, stderr = client.exec_command(pingcommand)
	output = stdout.readlines()
	print(output)
	pkt_tx = output[3].split()[0]
	pkt_rx = output[3].split()[3]
	pkt_loss = output[3].split()[6]
	rt = output[4].split()[3]
	rt_min = output[4].split()[3].split('/')[0]
	rt_avg = output[4].split()[3].split('/')[1]
	rt_max = output[4].split()[3].split('/')[2]
	print ('pkt_tx:', pkt_tx)
	print ('pkt_rx:', pkt_rx)
	print ('pkt_loss:', pkt_loss)
	print ('rt_min:', rt_min)
	print ('rt_avg:', rt_avg)
	print ('rt_max:', rt_max)
	client.close

def main():
	print (parseArgs())
	checkParamiko()
	import paramiko
	args=parseArgs()
	print(args.os)
	if(args.os == "openwrt"):
		pingOpenWRT(args)




if __name__ == "__main__":
	main()

