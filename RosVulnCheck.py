import Attack
import Sheild
import re

RED     = lambda x: "\033[31m "+x+" \033[0m"
BLUE    = lambda x: "\033[34m "+x+" \033[0m"
YELLOW  = lambda x: "\033[33m "+x+" \033[0m"
BGREEN  = lambda x: "\033[36m "+x+" \033[0m"

ADDED   = BLUE("[+]")
ERROR   = RED("[-]")
NOTIFY  = BGREEN("[*]")

def intro():
    print BLUE('''
        ____                               __            _    __ 
       / __ \   ____     _____   ____     / /  ____     (_)  / /_
      / /_/ /  / __ \   / ___/  / __ \   / /  / __ \   / /  / __/
     / _, _/  / /_/ /  (__  )  / /_/ /  / /  / /_/ /  / /  / /_  
    /_/ |_|   \____/  /____/  / .___/  /_/   \____/  /_/   \__/  
                             /_/                    
    '''),
    print RED('\t\t\t\t\t\t\td[ o_O ]b')

    print YELLOW('''
        ;        /              ,--. 		    !
       ["]      ["]  ,<        |__**|		  \["]/
      /[_]\     [~]\/        ~ |//  |		   [_]
       ] [      OOO        ~ ~ /o|__|		   / |
	''')


def is_ipv4(ip):
	match = re.match("^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
	if not match:
		return False
	quad = []
	for number in match.groups():
		quad.append(int(number))
	if quad[0] < 1:
		return False
	for number in quad:
		if number > 255 or number < 0:
			return False
	return True

def main():
	intro()

	print ""
	print ADDED + "Enter target ros ip address"
	
	while True:
	    inputIP = raw_input('ros > ')

	    if(is_ipv4(inputIP)):
	        break
	    else:
	        print ERROR + "Invalid ip address.."
	        print ERROR + "Try again..."


	attack = Attack.Attack()
	attack.PortScanning(inputIP)
	attack.FingerPrinting()
	attack.findPack()

if __name__ == '__main__':
	main()