import Attack
import Sheild

def main():
	attack = Attack.Attack()
	sheild = Sheild.Sheild()
	
	attack.PortScanning()
	attack.FingerPrinting()


if __name__ == '__main__':
	main()