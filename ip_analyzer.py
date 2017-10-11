#!/usr/bin/env python

import json
import os
import re
import socket
import sys

def main():
    pat = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    pat = re.compile(pat)
    by_ip = {}
    by_account = {}
    by_password = {}
    for arg in sys.argv[1:]:
        with open(arg, 'r') as f:
            for line in f.readlines():
                for ip in pat.findall(line):
                    by_ip[ip] = by_ip.get(ip, 0) + 1
                if 'login attempt' in line:
                    # 2013-09-06 01:50:17-0400 [SSHService ssh-userauth on HoneyPotTransport,24437,124.232.147.105] login attempt [root/1qaz3edc] failed
                    login = line.split()[-2].strip('[').strip(']')
                    try: account, password = login.split('/', 1)
                    except ValueError: continue
                    try: account = account.encode('ascii', 'ignore')
                    except UnicodeDecodeError: continue
                    try: password = password.encode('ascii', 'ignore')
                    except UnicodeDecodeError: continue
                    by_account[account] = by_account.get(account, 0) + 1
                    by_password[password] = by_password.get(password, 0) + 1
    with open('by_account.json', 'w') as f:
        f.write(json.dumps(by_account))
    with open('by_ip.json', 'w') as f:
        f.write(json.dumps(by_ip))
    with open('by_password.json', 'w') as f:
        f.write(json.dumps(by_password))

    data = ['begin', 'countrycode']
    data.extend(by_ip.keys())
    data.append('end')
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('whois.cymru.com', 43))
    sock.sendall('\n'.join(data))
    res = ''
    print 'doing whois ...'
    while True:
        try:
            r = sock.recv(32)
        except KeyboardIterrupt: break
        res += r
        if len(r) < 32:
            r = ''
            break
    print 'done'
    res += r
    sock.close()
    """
    with open('ips.tmp', 'w') as f:
        f.write('\n'.join(data))
    p = os.popen('cat ips.tmp | nc whois.cymru.com 43')
    res = p.read()
    p.close()
    with open('whois.txt', 'w') as f:
        f.write(res)

if __name__ == '__main__':
    main()
