#!/usr/bin/env python

# analyze kippo session durations

import json
import sys
import time

def main():
    res = {}
    ips = {}
    for arg in sys.argv[1:]:
        with open(arg, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if 'login attempt' in line and 'succeeded' in line:
                    line = line.split()
                    timestamp = '%s %s' % (line[0], line[1])
                    try: start = time.strptime(timestamp, '%Y-%m-%d %H:%M:%S-0400')
                    except ValueError: start = time.strptime(timestamp, '%Y-%m-%d %H:%M:%S-0500')
                    key = line[5].strip('[').strip(']')
                    res[key] = {'start': start}
                    ip = key.split(',')[-1]
                    if ips.has_key(ip):
                        print 'Repeat visitor! %s' % ips[ip]
                    I = ips.get(ip, [])
                    I.append(key)
                    ips[ip] = I
                if 'connection lost' in line:
                    # 2013-09-07 13:55:50-0400 [HoneyPotTransport,21667,94.228.44.10] connection lost
                    line = line.split()
                    try: key = line[2].strip('[').strip(']')
                    except IndexError: continue
                    timestamp = '%s %s' % (line[0], line[1])
                    try: end = time.strptime(timestamp, '%Y-%m-%d %H:%M:%S-0400')
                    except ValueError: end = time.strptime(timestamp, '%Y-%m-%d %H:%M:%S-0500')
                    try: res[key]['end'] = end
                    except KeyError: pass   # never logged in
    durations = {5:0,          # 5 seconds
                 60: 0,        # 1 minute
                 300: 0,       # 5 minutes
                 900: 0,       # 15 minutes
                 1800: 0,      # 30 minutes
                 3600: 0,      # 1 hour
                 86400: 0,     # 1 day
                 99999999: 0}  # longer
    D = durations.keys()
    D.sort()
    for key, times in res.iteritems():
        old = min(D)
        try: dur = long(time.strftime('%s', times['end'])) - long(time.strftime('%s', times['start']))
        except KeyError: continue
        for d in D:
            if dur > d: old = d
            else: break
        durations[old] = durations[old] + 1
    with open('durations.json', 'w') as f:
        f.write(json.dumps(durations))

    print 'Repeat visitor stats:'
    C = filter(lambda x: x[0] > 1, [ (len(v), k) for k,v in ips.iteritems() ])
    C.sort()
    C.reverse()
    print 'Most frequent repeat visitor:', C[0]
    for ip, visits in ips.iteritems():
        print ip, len(visits)

if __name__ == '__main__':
    main()
