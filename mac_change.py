import subprocess
import optparse
import re
import os
import sys
import random
import string
from datetime import datetime
class Style:
    CYAN = '\033[36m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    BOLD = '\033[1m'
    REVERSE = '\033[7m'
    RESET = '\033[0m'


def show_banner():
    
    banner = f"""{Style.CYAN}{Style.BOLD}
    ███╗   ███╗ █████╗  ██████╗     ██████╗██╗  ██╗ ██████╗ ██████╗ 
    ████╗ ████║██╔══██╗██╔════╝    ██╔════╝██║  ██║██╔════╝ ██╔══██╗
    ██╔████╔██║███████║██║         ██║     ███████║██║  ███╗██████╔╝
    ██║╚██╔╝██║██╔══██║██║         ██║     ██╔══██║██║   ██║██╔══██╗
    ██║ ╚═╝ ██║██║  ██║╚██████╗    ╚██████╗██║  ██║╚██████╔╝██║  ██║
    ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝     ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
    {Style.REVERSE}           MAC ADDRESS CHANGER | v2.0         {Style.RESET}{Style.CYAN}{Style.BOLD}
    {Style.REVERSE} GitHub: https://github.com/UZinfosec404      {Style.RESET}
    """
    print(banner)
def get_time():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

##Network interface 
# def get_interfaces():
#     output = subprocess.check_output(["ip", "link"], text=True)
#     interfaces = re.findall(r"\d+:\s+([^:]+):", output)
#     return interfaces
# interfaces_list=get_interfaces()


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to change its mac adress")
    parser.add_option("-m", "--mac_address", dest="mac_address", help="new mac adress")
    parser.add_option("-r", "--random",action="store_true",dest="random_address",help="set random mac address")

    (options, arguments)=parser.parse_args()
    if not options.interface:
        parser.error(f"{Style.RED}[!] plase specify an interface,use --help for more info {Style.RESET}")
    return options
def change_mac(interface,mac_address):
    print("[+] mac interfeyce " + interface + " new mac_address " + mac_address.lower())
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    try:
        ifconfig_result = subprocess.check_output(["ifconfig", interface])
        mac_adress_search = re.search(rb"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
        if mac_adress_search:
            return mac_adress_search.group(0).decode("utf-8")
        else:
            print("could not read mac adress")
    except subprocess.CalledProcessError:
        return None


def get_random_mac_address():
    """Generate and return a MAC address in the format of Linux"""
    # get the hexdigits uppercased
    uppercased_hexdigits = ''.join(set(string.hexdigits.upper()))
    # 2nd character must be 0, 2, 4, 6, 8, A, C, or E
    mac = ""
    for i in range(6):
        for j in range(2):
            if i == 0:
                mac += random.choice("02468ACE")
            else:
                mac += random.choice(uppercased_hexdigits)
        mac += ":"
    return mac.strip(":")


if os.geteuid() != 0:
    print(f"{Style.RED}[-] ROOT permission (sudo python3 ...){Style.RESET}")
    sys.exit()
show_banner()
options = get_arguments()
while True:
        
    if options.random_address:
        new_mac = get_random_mac_address()
    elif options.mac_address :
        new_mac = options.mac_address
    else:
        print("[-] Please specify a MAC address with -m or use --random (-r)")
        sys.exit()

    current_mac = get_current_mac(options.interface)
    print("Current MAC:", current_mac)
    old_address=current_mac
    change_mac(options.interface, new_mac)

    current_mac = get_current_mac(options.interface)

    print("\n" + "═"*80)
    if current_mac == new_mac.lower():
        print(f"{Style.GREEN}{Style.BOLD}[+] MAC address successfully changed to {Style.RESET}", current_mac )
        with open("mac_address_change.log",'a') as f:
            f.write(f"[{get_time()}] Interface: {options.interface} | Old: {old_address} | New: {new_mac}\n")
            
        print("═"*80 + "\n")
        break
        
    else:
        print(f"{Style.RED}{Style.BOLD}[-] MAC address did not change!{Style.RESET}")
        print("═"*80 + "\n")
        break

