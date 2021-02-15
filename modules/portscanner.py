import logging
import argparse
import ipaddress
from datetime import datetime
from modules.module import Module
from scapy.all import *
from threading import Thread


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


def handle_targets(targets):
    targets_ = []

    try:
        targets_.append(format(ipaddress.ip_address(targets)))
    except ipaddress.AddressValueError or ValueError:
        try:
            for i in ipaddress.ip_network(targets):
                targets_.append(format(i))

            targets_.pop(0)
        except ValueError:
            logging.critical("ValueError: Use an valid IP Address!")

            return False

    return targets_


def ping_target(target):
    pkt = IP(dst=target) / ICMP()
    ans, _ = sr(pkt, retry=2, timeout=1, verbose=0)

    if not ans:
        return False

    return target


def check_target_is_online(targets: list):
    targets_ = []
    threads = []

    for target in targets:
        t = ThreadWithReturnValue(target=ping_target, args=(target,))
        t.start()
        threads.append(t)

    for thread in threads:
        res = thread.join()

        if res:
            targets_.append(res)

    return targets_


class PortScanner(Module):
    name = "PortScanner"
    optname = "portscan"
    desc = ""
    version = "1.0.0"
    scan_types = [
        "TCP-Connect",
        "TCP-SYN",
    ]
    required_options = [
        "target",
        "port",
    ]
    timeout = 2

    def initialize(self, options: dict):
        self.arguments = options

        if options[self.optname]:
            for opt in self.required_options:
                if not options[opt]:
                    return logging.critical(f"Required argument: \"{opt}\"")

            begin_time = datetime.now()
            logging.debug(f"Starting port scan!")

            # Handle arguments
            targets = handle_targets(options["target"])

            port = options["port"].split("-")
            port = [int(i) for i in port]

            scan_type = "TCP-SYN" if options["syn_scan"] else "TCP-Connect"
            dont_ping = options["dont_ping"]

            # Check arguments
            if not targets or not port:
                return False

            # Init portscan

            self.main(targets, port, scan_type, dont_ping)

            logging.debug(f"Port scan finished in {datetime.now() - begin_time}")

    def options(self, parser: argparse.ArgumentParser):
        parser.add_argument("-sS", "--syn-scan", help="Execute SYN Scan (Stealth)", action="store_true")
        parser.add_argument("-t", "--target", help="Target IP", type=str)
        parser.add_argument("-p", "--port", help="Port range to scan", type=str)
        parser.add_argument("-dP", "--dont-ping", help="Don't check if host is up", action="store_true")

    def main(self, targets: list, port_range: [int, int], scan_type: str, dont_ping: bool):
        if not dont_ping:
            logging.debug("Checking targets are up")
            targets = check_target_is_online(targets)

            if not targets:
                return logging.critical("Targets offline!")
            logging.info(f"{len(targets)} {'targets' if len(targets) > 1 else 'target'} up!")

        try:
            for target in targets:
                try:
                    for i in range(port_range[0], port_range[1]):
                        # logging.debug(f"{format(target)}:{i}")
                        result = self.port_scan(format(target), i, scan_type)

                        if result == "Open" or result == "Filtered":
                            logging.info(f"{format(target)}:{i} - {result}")
                except KeyboardInterrupt:
                    return
        except KeyboardInterrupt:
            return

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
