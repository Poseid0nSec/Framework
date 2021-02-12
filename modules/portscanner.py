import logging
import argparse
from datetime import datetime
from modules.module import Module
from scapy.all import *


class PortScanner(Module):
    name = "PortScanner"
    optname = "portscan"
    desc = ""
    version = "1.0.0"
    scan_types = [
        "TCP-Connect",
        "TCP-SYN",
    ]
    timeout = 2

    def send_tcp(self, target: str, dport: int, flags: str):
        pkt = IP(dst=target) / TCP(dport=dport, flags=flags)
        res = sr1(pkt, timeout=self.timeout, verbose=0)

        return res

    def port_scan(self, target: str, port: int, scan_type: str = "TCP-Connect"):
        if scan_type not in self.scan_types:
            return False

        if scan_type == "TCP-SYN":
            res = self.send_tcp(target, port, "S")

            if res is None:
                return "Filtered"
            elif res.haslayer(TCP):
                if res.getlayer(TCP).flags == 0x12:  # 0x12 SYN+ACk
                    self.send_tcp(target, port, "R")

                    return "Open"
                elif res.getlayer(TCP).flags == 0x14:
                    return "Closed"
            elif res.haslayer(ICMP):
                if int(res.getlayer(ICMP).type) == 3 and int(res.getlayer(ICMP).code in [1, 2, 3, 9, 10, 13]):
                    return "Filtered"
            else:
                return "Filtered"
        elif scan_type == "TCP-Connect":
            res = self.send_tcp(target, port, "S")

            if res is None:
                return "Filtered"
            elif res.haslayer(TCP):
                if res.getlayer(TCP).flags == 0x12:  # 0x12 SYN+ACk
                    self.send_tcp(target, port, "AR")
                    return "Open"
                elif res.getlayer(TCP).flags == 0x14:
                    return "Closed"

    def main(self, target: str, port_range: [int, int], scan_type: str):
        try:
            for i in range(port_range[0], port_range[1]):
                result = self.port_scan(target, i, scan_type)

                if result == "Open" or result == "Filtered":
                    logging.info(f"{target}:{i} - {result}")
        except KeyboardInterrupt:
            return

    def initialize(self, options: dict):
        self.arguments = options

        if options[self.optname]:
            begin_time = datetime.now()
            logging.debug(f"Starting port scan!")

            port = options["port"].split("-")
            port = [int(i) for i in port]

            scan_type = "TCP-SYN" if options["syn_scan"] else "TCP-Connect"

            self.main(options["target"], port, scan_type)

            logging.debug(f"Port scan finished in {datetime.now() - begin_time}")

    def options(self, parser: argparse.ArgumentParser):
        parser.add_argument("-sS", "--syn-scan", help="Execute SYN Scan (Stealth)", action="store_true")
        parser.add_argument("-t", "--target", help="Target IP", type=str)
        parser.add_argument("-p", "--port", help="Port range to scan", type=str)
