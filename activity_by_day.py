#!/usr/bin/env python

# analyze kippo session durations

import json
import sys
import time

def main():
    res = {}
    for arg in sys.argv[1:]:
        with open(arg, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if 'login attempt' in line:
                    date = line.split()[0]
                    if 'succeeded' in line:
                        r = res.get(date, {'failed': 0, 'succeeded': 0})
                        r['succeeded'] = r['succeeded'] + 1
                        res[date] = r
                    if 'failed' in line:
                        r = res.get(date, {'failed': 0, 'succeeded': 0})
                        r['failed'] = r['failed'] + 1
                        res[date] = r
                        line = line.split()

    with open('daily_activity.json', 'w') as f:
        f.write(json.dumps(res))

if __name__ == '__main__':
    main()
