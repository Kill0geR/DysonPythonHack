import os
import BetterPrinting as bp
from Pytheas22 import Python_Port_Scanner
import sys
import subprocess
import re


class DysonIP:
    def __init__(self):
        pass

    @staticmethod
    def get_dyson_ip(host_ip):
        Python_Port_Scanner.PortScanner.my_ip_address = host_ip[1][0][0]
        all_data = subprocess.run(["netdiscover", "-r", f"{host_ip[0]}/{host_ip[1][0][1]}", "-P"],
                                  capture_output=True).stdout.decode()

        order_ips = sorted([int(each.split()[0].split(".")[-1]) for each in all_data.split("\n") if
                            re.findall(r"\d+.\d+.\d+.\d+", each)] + [
                               int(str(Python_Port_Scanner.PortScanner.my_ip_address).split(".")[-1])])

        get_all_hostnames = {each.split()[0]: " ".join(each.split()[4:]) for each in all_data.split("\n") if
                             re.findall(r"\d+.\d+.\d+.\d+", each)}

        get_all_hostnames[Python_Port_Scanner.PortScanner.my_ip_address] = "MY IP-ADDRESS"
        sorted_ips = [(ip, host) for each_number in order_ips for ip, host in get_all_hostnames.items() if
                      str(each_number) == ip.split(".")[-1]]
        return sorted_ips

    def auto_ip_addr_dyson(self):
        bp.color("Getting IP Address.....", "green")
        if sys.platform == "linux":
            if os.getuid() != 0:
                bp.color("\nThis program must be run in root!!!!\n".upper(), "red")
                quit()
            host_ip = Python_Port_Scanner.PortScanner.get_ip()
            all_ips = self.get_dyson_ip(host_ip)
            Python_Port_Scanner.PortScanner.every_ip_with_name = all_ips

        elif sys.platform == "win32" or sys.platform == "windows" or sys.platform == "win64":
            windows = Python_Port_Scanner.PortScanner()
            Python_Port_Scanner.PortScanner.every_ip_with_name = windows.internal_windows()

        for ip, name in Python_Port_Scanner.PortScanner.every_ip_with_name:
            if "Dyson" in name:
                return ip.strip()
        return False
