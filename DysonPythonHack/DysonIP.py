import BetterPrinting as bp
from Pytheas22 import Python_Port_Scanner
import sys


class DysonIP:
    def __init__(self):
        pass

    @staticmethod
    def auto_ip_addr_dyson():
        bp.color("Getting IP Address.....", "green")
        if sys.platform == "linux":
            get_lst = Python_Port_Scanner.PortScanner()
            get_lst.linux_lst()

        elif sys.platform == "win32" or sys.platform == "windows" or sys.platform == "win64":
            windows = Python_Port_Scanner.PortScanner()
            Python_Port_Scanner.PortScanner.every_ip_with_name = windows.internal_windows()

        for ip, name in Python_Port_Scanner.PortScanner.every_ip_with_name:
            if "Dyson" in name:
                return ip.strip()
        return False