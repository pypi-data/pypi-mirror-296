# simple cfddns

A simple that conviently set up a DDNS service based on Cloudflare.

## install 

```
pip3 install simple-cfddns
```



## usage

**check help messages**

`cfddns --help` keeps the latest help document.

``` bash
cfddns -h
```

``` text
usage: cfddns [-h] {record,addr,service} ...

positional arguments:
  {record,addr,service}
    record              DNS record management
    addr                IP address tools
    service             Systemd service management
```

All subcommands provide `-h` help messages, so remember to check them.  For example:

``` bash
cfddns record update -h
```

gives

```
usage: cfddns record update [-h] [-d DOMAIN] [-z ZONE] [-t TOKEN] [-c CONFIG_FILE] [-i] [--ttl TTL] [--daemon] [--interval INTERVAL] -r ...

options:
  -h, --help            show this help message and exit
  -r ..., --rules ...   IP selection rules. See `cfddns addr list -h` for the rule syntax

Cloudflare options:
  -d DOMAIN, --domain DOMAIN
                        Domain name
  -z ZONE, --zone ZONE  Zone ID
  -t TOKEN, --token TOKEN
                        API Token
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        Config file path. If provided, the options are loaded from this file, overrided by command line options, and saved back to this file.
  -i, --interactive     Interactive mode
  --ttl TTL             DNS record TTL

Daemon options:
  --daemon              Daemon mode
  --interval INTERVAL   Update interval, in seconds
```





**Daily Operations**

Select some IP addresses and filter them:

``` bash
cfddns addr list -r -s all_ip -f is_global
```

* If the command prints nothing, it indicates that your machine does not have a global IP addresses. Contact your ISP for more information. But for the this tutorial, you can delete `-f is_global` part and move forward
* Arguments after `-r` forms the rules to select and filter IP addresses. You can get different sets of IP addresses with different combinations of rules. For more example, check `cfddns addr list -h` and `cfddns addr show_func`



Update(Create) DNS records:

``` bash
cfddns record update \
	-d mypc.example.com -t TOKEN -z ZONE \
	-c cfddns.json \
	-r -s all_ip -f is_global
```

* `-d`/`-t`/`-z` are required options to call Cloudflare APIs

* If `-c FILE` is provided, `-d`/`-t`/`-z` are first loaded from this file, overridden by command line options, and saved back to this file

* `cfddns.json` has the following content:

    ``` json
    {
      "domain": "mypc.example.com",
      "zone": "ZONE",
      "token": "TOKEN"
    }
    ```

    As it contains sensitive data, keep it safe.



List current records:

``` bash
cfddns record list -c cfddns.json
```



Clear records to this domain:

``` bash
cfddns record clear -c cfddns.json
```



**Supported rule functions**

``` bash
cfddns addr show_func
```

``` text
FUNC for SELECT rules:
  all_ipv4           Get all IPv4 addresses of the host.
  all_ipv6           Get all IPv6 addresses of the host.
  all_ip             Get all IP addresses of the host, including both IPv4 and IPv
                     6.
  ip_of_nic          Get all IP addresses of a network interface card.
  default_ipv4       Get the default IPv4 address that the OS uses to connect to t
                     he internet.
  default_ipv6       Get IPv6 address that has the connection to the internet.
  ipv4_seen_by_inet  Get the IPv4 address that the internet sees. The ip address r
                     eturned may not be the ip address of the host if the host is
                     behind a NAT.
  ipv6_seen_by_inet  Get the IPv6 address that the internet sees. The ip address r
                     eturned may not be the ip address of the host if the host is
                     behind a NAT.

FUNC for FILTER rules:
  is_private     Check if an ip address is a private ip address.
  is_link_local  Check if an ip address is a link local ip address.
  is_loopback    Check if an ip address is a loopback ip address.
  is_global      Check if an ip address is a global ip address.
  conn_to_inet   Check if an ip address has the connection to the internet by send
                 ing a DNS query to a famous DNS server. This is a slow operation,
                  so filter the IPs by other filters first.
```





## run as a systemd service

Run the `cfddns` as daemon process that updates DNS records periodically and use `systemd` to manage the daemon. Note that this feature is only supported on Linux systems with `systemd`.

**Install** a new cfddns service:

``` bash
prog=$(which cfddns)
sudo $prog service install \
	-n test \
	-c cfddns.json \
	--interval 60 \
	-r -s ip_of_nic,enp6s0 -f is_global
```

* `-n test` give the service the name of `cfddns-test`
* `-c cfddns.json` could be replaced by `-z`, `-t` and `-d`
* `--interval 60` update DNS records every 60 seconds

Then, enable and start the service:

``` bash 
sudo systemctl start cfddns-test
sudo systemctl enable cfddns-test
```

Check its log:

``` bash
sudo journalctl -r -u cfddns-test
```

