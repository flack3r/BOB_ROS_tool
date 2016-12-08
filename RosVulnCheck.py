import Attack
import Sheild

def main():
	attack = Attack.Attack()
	sheild = Sheild.Sheild()
	
	attack.PortScanning()
	attack.FingerPrinting()
	attack.shutdown()

if __name__ == '__main__':
	main()