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
		port = 11312
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
		print "[*]---Parameter Names---"
		for i, param in enumerate(self.proxy.getParamNames("")[2]):
			print "%d: %s" %(i, param)

	def ReplayAttack(self):
		print "[*]replay attack"

	def TurnOffRos(self):
		#stage1 turn off nodes

		#stage2 turn off master
		print "[*]turn off ros"