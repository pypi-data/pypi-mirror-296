import argparse
from . import iptools
from .cfapi import CloudflareAPI
import json
import os
import sys
import os.path
import re as regex
import time
import datetime

##################################
# Record management
##################################

def load_cf_option(args):
    options = {}
    if args.config_file:
        try:
            with open(args.config_file, 'r') as f:
                options = json.load(f)
        except:
            pass
    if args.domain:
        options['domain'] = args.domain
    if args.zone:
        options['zone'] = args.zone
    if args.token:
        options['token'] = args.token
    return options


def check_cf_option(opt, interactive=True):
    required = ['domain', 'zone', 'token']
    for r in required:
        if r not in opt:
            if interactive:
                opt[r] = input(f"{r}: ")
            else:
                return None
    return opt


def __cf_options(args):
    cf_opt = load_cf_option(args)
    cf_opt = check_cf_option(cf_opt, args.interactive)
    if cf_opt is None:
        raise ValueError("Missing Cloudflare options")
    if args.config_file:
        with open(args.config_file, 'w') as f:
            json.dump(cf_opt, f, indent=2, ensure_ascii=False)
    return cf_opt


def list_records(args):
    cf_opt = __cf_options(args)
    cf = CloudflareAPI(cf_opt['zone'], cf_opt['token'], ttl=args.ttl)
    records = cf.list_records(cf_opt['domain'])
    records += cf.list_records(cf_opt['domain'], type="AAAA")

    print(f'IP addresses of {cf_opt["domain"]}:')
    for r in records:
        print(f"{r['content']}")


def clear_records(args):
    cf_opt = __cf_options(args)
    cf = CloudflareAPI(cf_opt['zone'], cf_opt['token'], ttl=args.ttl)
    records = cf.list_records(cf_opt['domain'])
    records += cf.list_records(cf_opt['domain'], type="AAAA")

    print(f'Delete {len(records)} records of {cf_opt["domain"]}:')
    for r in records:
        print(f'  {r["content"]}')
        cf.delete_record(r['id'])


def update_records(args):
    cf_opt = __cf_options(args)
    cf = CloudflareAPI(cf_opt['zone'], cf_opt['token'], ttl=args.ttl)

    while True:
        print(f'Update {cf_opt["domain"]} records at {datetime.datetime.now()}')

        ip_list = iptools.select(parse_rules(args))
        clear_records(args)

        print(f'Create {len(ip_list)} records for {cf_opt["domain"]}:')
        for ip in ip_list:
            type = 'A' if '.' in ip else 'AAAA'
            name = cf_opt['domain']
            print(f'  {ip}')
            cf.create_record(type, name, ip)
        print()
        
        if not args.daemon:
            break
        time.sleep(args.interval)


###########################
# addr testing
###########################
def parse_rules(args):
    rule_desc = args.rules
    rule_desc = [rule_desc[i:i+2] for i in range(0, len(rule_desc), 2)]

    rules = []
    canonical_types = {
        '-s': 'source', '--select': 'source',
        '-f': 'filter', '--filter': 'filter',
        '-i': 'ifilter', '--inv-filter': 'ifilter'
    }

    for desc in rule_desc:
        if len(desc) != 2:
            raise ValueError(f"Invalid rule: {desc}")
        type, fn_args = desc
        canonical_type = canonical_types.get(type)
        if not canonical_type:
            raise ValueError(f"Invalid rule type '{type}' near {desc}")
        
        fn_args = fn_args.split(',')
        fn = fn_args[0]
        args = fn_args[1:]

        if canonical_type in ['filter', 'ifilter']:
            if fn not in iptools.FILTERS:
                raise ValueError(f"Unknown filter function '{fn}' near {desc}")

            rules.append({
                'type': canonical_type,
                'name': fn,
            })
        elif canonical_type == 'source':
            if fn not in iptools.SOURCES:
                raise ValueError(f"Unknown select function '{fn}' near {desc}")

            rules.append({
                'type': canonical_type,
                'name': fn,
                'args': args
            })

    return rules

def addr_testing(args):
    rules = parse_rules(args)
    ip_list = iptools.select(rules)
    for ip in ip_list:
        print(ip)

def print_funcs(funcs):
    indent = 2
    gap = 2
    max_width = 80

    name_len = max([len(k) for k in funcs.keys()])
    doc_width = max_width - name_len - gap
    doc_indent = ' ' * (name_len + gap + indent)

    for k, fn in funcs.items():
        doc = fn.__doc__.strip()
        doc = doc.replace('\n', ' ')
        doc = regex.sub(r'\s+', ' ', doc)

        print(' ' * indent, end='')
        print(k, end='')
        print(' ' * (name_len - len(k)), end='')
        print(' ' * gap, end='')
        print(doc[:doc_width])

        doc = doc[doc_width:]
        while doc:
            print(' ' * len(doc_indent), end='')
            print(doc[:doc_width])
            doc = doc[doc_width:]


def show_rule_funcs(args):
    print('FUNC for SELECT rules: ')
    print_funcs(iptools.SOURCES)

    print()
    print('FUNC for FILTER rules: ')
    print_funcs(iptools.FILTERS)


##################################
# Service management
##################################

def __check_systemd():
    # is Linux
    if sys.platform != 'linux':
        raise NotImplementedError("systemd is only available on Linux")

    if not os.path.exists("/bin/systemctl"):
        raise NotImplementedError("systemd is not available on this system")

def __check_privilege():
    if os.geteuid() != 0:
        raise PermissionError("You need root privilege to install/uninstall systemd service")

def list_services(args):
    __check_systemd()

    location = "/etc/systemd/system"
    services = os.listdir(location)
    services = [s for s in services if s.startswith('cfddns-') and s.endswith(".service")]
    print(f'Find {len(services)} services:')
    for s in services:
        print(f'  {s}')


def compose_svc_name(input):
    name = input
    if not name.startswith('cfddns-'):
        name = 'cfddns-' + name
    if not name.endswith('.service'):
        name += '.service'
    return name


def uninstall(args):
    __check_systemd()
    __check_privilege()

    location = "/etc/systemd/system"
    name = compose_svc_name(args.name)
    path = os.path.join(location, name)

    if not os.path.exists(path):
        print(f"Service {name} not found")
        return
    
    print(f"Service {name} at {path} will be removed, sure?")
    if not args.yes:
        confirm = input("[N/y]: ")
        if confirm != 'y':
            print('Abort')
            return
    
    os.system(f"systemctl stop {name}")
    os.system(f"systemctl disable {name}")
    os.remove(path)


SERVICE_TEMPLATE = """
[Unit]
Description=Cloudflare Dynamic DNS
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=5
User=root
StandardOutput=journal
StandardError=journal
Environment="PYTHONUNBUFFERED=1"
ExecStart={python} -m cfddns record update -d {domain} -z {zone} -t {token} --ttl {ttl} --daemon --interval {interval} -r {rules}

[Install]
WantedBy=multi-user.target
"""


def install(args):
    __check_systemd()
    __check_privilege()

    cf_opt = __cf_options(args)
    rules = parse_rules(args)   # parse to check the syntax
    
    location = "/etc/systemd/system"
    name = compose_svc_name(args.name)
    path = os.path.join(location, name)

    if os.path.exists(path):
        raise FileExistsError(f"Service {name} already exists")
    
    service_str = SERVICE_TEMPLATE.format(
        python=args.python,
        domain=cf_opt['domain'], zone=cf_opt['zone'], token=cf_opt['token'],
        ttl=args.ttl, interval=args.interval, 
        rules=' '.join([f'"{e}"' for e in args.rules])
    )
    
    print(f"Install to {path}")
    if input("[N/y]: ") != 'y':
        print('Abort')
        return
    
    with open(path, 'w') as f:
        f.write(service_str)

    import stat
    os.chmod(path, stat.S_IWUSR | stat.S_IRUSR)

    print("Run the following commands to enable and start the service:")
    print(f"  systemctl enable {name}")
    print(f"  systemctl start {name}")
    print()
    print(f"Run the following commands to check the service log:")
    print(f"  journalctl -r -u {name}")


def main():
    parser = argparse.ArgumentParser(prog="cfddns")
    sub_parsers = parser.add_subparsers(dest="scope", required=True)
    
    ## Record parser
    record_parser = sub_parsers.add_parser("record", help="DNS record management")
    record_parser.set_defaults(handler=lambda x: record_parser.print_help())

    actions = record_parser.add_subparsers(dest="action", required=True)
    list = actions.add_parser("list", help="List all DNS records")
    update = actions.add_parser("update", help="Update a DNS record")
    clear = actions.add_parser("clear", help="Clear DNS records to this domain")

    list.set_defaults(handler=list_records)
    update.set_defaults(handler=update_records)
    clear.set_defaults(handler=clear_records)

    def add_cf_opt_group(parser):
        # Note that 'cfddns service install' share this group
        cfopt = parser.add_argument_group("Cloudflare options")
        cfopt.add_argument('-d', '--domain', help="Domain name")
        cfopt.add_argument('-z', '--zone', help="Zone ID")
        cfopt.add_argument('-t', '--token', help="API Token")
        cfopt.add_argument(
            '-c', '--config-file', 
            help="Config file path. If provided, the options are loaded from this file, " 
               + "overridden by command line options, and saved back to this file.")
        cfopt.add_argument(
            '-i', '--interactive', action="store_true",
            help="Interactive mode. If provided, the program will ask for missing options.")
        cfopt.add_argument('--ttl', help="DNS record TTL", type=int, default=60)
    add_cf_opt_group(list)
    add_cf_opt_group(update)
    add_cf_opt_group(clear)

    daemon_opt = update.add_argument_group("Daemon options")
    daemon_opt.add_argument('--daemon', help="Daemon mode", default=False, action="store_true")
    daemon_opt.add_argument('--interval', help="Update interval, in seconds", type=int, default=60)
    update.add_argument(
        '-r', '--rules', 
        help="IP selection rules. See `cfddns addr list -h` for the rule syntax", 
        nargs=argparse.REMAINDER, required=True
    )

    ## Addr parser
    addr_parser = sub_parsers.add_parser("addr", help="IP address tools")
    addr_acts = addr_parser.add_subparsers(dest="action", required=True)

    show_funcs = addr_acts.add_parser("show_func", help="Show available FUNCs for rules")
    show_funcs.set_defaults(handler=show_rule_funcs)

    list_addr = addr_acts.add_parser(
        "list", help="List IP addresses based on rules",
        epilog=
"""
rule syntax:
  these options can be applied multiple times, and evaluated in order.

  -s, --select FUNC[,args]     select IP address by FUNC
  -f, --filter FUNC            filter IP address by FUNC
  -i, --inv-filter FUNC        filter IP address by FUNC, but keep the inverse result

  examples:
    select all global IP addresses:
      cfddns addr list -r -s all_ip -f is_global

    select IPv6 address that has connection to the internet:
      cfddns addr list -r -s all_ipv6 -f conn_to_inet
""",
        formatter_class=argparse.RawTextHelpFormatter
    )

    list_addr.add_argument(
        '-r', '--rules', 
        help="IP selection rules", nargs=argparse.REMAINDER,
        required=True
    )
    list_addr.set_defaults(handler=addr_testing)


    ## Service parser
    service_parser = sub_parsers.add_parser("service", help="Systemd service management")
    service_parser.set_defaults(handler=lambda x: service_parser.print_help())

    svc_acts = service_parser.add_subparsers(dest="action", required=True)
    list_svc = svc_acts.add_parser("list", help="List all services")
    install_svc = svc_acts.add_parser("install", help="Install a service")
    uninstall_svc = svc_acts.add_parser("uninstall", help="Uninstall a service")

    list_svc.set_defaults(handler=list_services)

    install_svc.add_argument('-n', '--name', help="Service name", required=True)
    install_svc.add_argument(
        '--interval', help="Update interval, in seconds, default 60s", 
        type=int, default=60
    )
    install_svc.add_argument('-p', '--python', help="Python executable path", default=sys.executable)
    add_cf_opt_group(install_svc)
    install_svc.add_argument(
        '-r', '--rules',
        required=True, nargs=argparse.REMAINDER,
        help="IP selection rules. See `cfddns addr list -h` for the rule syntax",
    )
    install_svc.set_defaults(handler=install)

    uninstall_svc.add_argument('-n', '--name', help="Service name", required=True)
    uninstall_svc.add_argument('-y', '--yes', help="Skip confirmation", action="store_true")
    uninstall_svc.set_defaults(handler=uninstall)
    
    ## Execute
    args = parser.parse_args()

    try:
        args.handler(args)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)