import socket as S
import ipaddress as ipaddr
import os
import sys
import psutil
from . import dns

#####################################
# IP Selector
#####################################

FILTERS = {}
SOURCES = {}

def reg_filter(f):
    FILTERS[f.__name__] = f
    return f

def reg_source(f):
    SOURCES[f.__name__] = f
    return f

def select(rules):
    """
    Rule: {
        'type': 'filter' | 'ifilter' | 'source', 
        'name': <func_name>, 
        'args': []
    }
    Rule List: list of rules and rule lists
    """

    def _not(func):
        def inner(x):
            return not func(x)
        return inner
    IFILTERS = {k: _not(v) for k, v in FILTERS.items()}

    ip = []
    for e in rules:
        if isinstance(e, dict):
            fnmap = { 
                'filter': FILTERS,
                'ifilter': IFILTERS,
                'source': SOURCES,
            }.get(e.get('type'))
            if not fnmap: raise ValueError(f"Invalid rule type: {e.get('type')}")

            func = fnmap.get(e.get('name'))
            if not func: raise ValueError(f"Invalid function name: {e.get('name')}")

            if fnmap in [FILTERS, IFILTERS]:
                ip = list(filter(func, ip))
            elif fnmap == SOURCES:
                rst = func(*e.get('args', []))
                if isinstance(rst, str): ip.append(rst)
                elif isinstance(rst, list): ip.extend(rst)
            else:
                raise ValueError("Invalid rule")

        elif isinstance(e, list):
            ip.extend(select(e))
    
    return ip


#####################################
# IP Filters
#####################################

@reg_filter
def is_private(ip):
    """
    Check if an ip address is a private ip address.
    """
    return ipaddr.ip_address(ip).is_private

@reg_filter
def is_link_local(ip):
    """
    Check if an ip address is a link local ip address.
    """
    return ipaddr.ip_address(ip).is_link_local

@reg_filter
def is_loopback(ip):
    """
    Check if an ip address is a loopback ip address.
    """
    return ipaddr.ip_address(ip).is_loopback

@reg_filter
def is_global(ip):
    """
    Check if an ip address is a global ip address.
    """
    return ipaddr.ip_address(ip).is_global

@reg_filter
def conn_to_inet(ip):
    """
    Check if an ip address has the connection to the internet by sending a DNS
    query to a famous DNS server. This is a slow operation, so filter the IPs
    by other filters first.
    """
    # Check by sending a DNS query to famous DNS servers.
    family = S.AF_INET if '.' in ip else S.AF_INET6
    dns_server = {
        S.AF_INET: '8.8.8.8',
        S.AF_INET6: '2001:4860:4860::8888'
    }[family]
    with S.socket(family, S.SOCK_DGRAM) as s:
        try:
            s.bind((ip, 0))
            s.connect((dns_server, 53))
            s.settimeout(1)

            dns_qry = dns.build_dns_qry('google.com')
            s.send(dns_qry)
            rsp = s.recv(512)
            
            return True
        except Exception as e:
            # print(f"E: {ip}, {e}")
            return False


####################################
# IP Sources
# - Functions here return a single ip address, or a list of ip addresses.
####################################

def __addr_of_types(families):
    l = []
    for i in psutil.net_if_addrs().values():
        for j in i:
            if j.family in families:
                l.append(j.address)
    return l

@reg_source
def all_ipv4():
    """
    Get all IPv4 addresses of the host.
    """
    return __addr_of_types([S.AF_INET])

@reg_source
def all_ipv6():
    """
    Get all IPv6 addresses of the host.
    """
    return __addr_of_types([S.AF_INET6])

@reg_source
def all_ip():
    """
    Get all IP addresses of the host, including both IPv4 and IPv6.
    """
    return __addr_of_types([S.AF_INET, S.AF_INET6])

@reg_source
def ip_of_nic(name):
    """
    Get all IP addresses of a network interface card.
    """
    l = []
    for i in psutil.net_if_addrs().get(name, []):
        if i.family in [S.AF_INET, S.AF_INET6]:
            l.append(i.address)
    return l

@reg_source
def default_ipv4():
    """
    Get the default IPv4 address that the OS uses to connect to the internet.
    """
    with S.socket(S.AF_INET, S.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

@reg_source
def default_ipv6():
    """
    Get IPv6 address that has the connection to the internet.
    """
    with S.socket(S.AF_INET6, S.SOCK_DGRAM) as s:
        s.connect(("2001:4860:4860::8888", 80))
        return s.getsockname()[0]

@reg_source
def ipv4_seen_by_inet():
    """
    Get the IPv4 address that the internet sees. 
    
    The ip address returned may not be the ip address of the host if the host is
    behind a NAT.
    """
    return __ident_me(use_ipv6 = False)

@reg_source
def ipv6_seen_by_inet():
    """
    Get the IPv6 address that the internet sees. 
    
    The ip address returned may not be the ip address of the host if the host is
    behind a NAT.
    """
    return __ident_me(use_ipv6 = True)


def __ident_me(use_ipv6 = False):
    """
    Use inet.me to get the ip address that has the connection to the internet. The ip address 
    returned may not be the ip address of the host if the host is behind a NAT.
    """
    host = "ident.me"
    
    with S.socket(S.AF_INET6 if use_ipv6 else S.AF_INET, S.SOCK_STREAM) as s:
        s.connect((host, 80))
        s.send(b"GET / HTTP/1.1\r\n")
        s.send(b"Host: ident.me\r\n")
        s.send(b"User-Agent: Python Raw Socket\r\n")
        s.send(b"Connection: close\r\n")
        s.send(b"\r\n")
        
        res = (s.recv(2048) or b'').decode("utf-8")
        lines = res.split("\r\n")
        if lines[0] and lines[0].split(" ")[-1] == 'OK':
            return lines[-1]
    return None