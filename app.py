#!/usr/bin/env python

import json
import os
import sys

from flask import Flask, render_template, request, send_from_directory

sys.stdout = sys.stderr

app = Flask(__name__)
app.debug = True

def ksort(D):
    D = [ (v,k) for k,v in D.iteritems() ]
    D.sort()
    D.reverse()
    return [ (k,v) for v,k in D ]

def top(T, n):
    res = T[:n]
    other = sum([ x[1] for x in T[n:] ])
    res.append(('other', other))
    return res

@app.route('/transitions.json')
def get_transitions():
    return open('transitions.json', 'r').read()

@app.route('/')
def root():
    by_cc = json.load(open('by_cc.json', 'r'))
    durations = json.load(open('durations.json', 'r'))
    durations = [ (int(k),v) for k,v in durations.iteritems() ]
    durations.sort()

    by_asn = json.load(open('by_asn.json', 'r'))
    top_asns = top(ksort(by_asn), 10)

    by_account = json.load(open('by_account.json', 'r'))
    top_accounts = top(ksort(by_account), 10)

    by_password = json.load(open('by_password.json', 'r'))
    top_passwords = top(ksort(by_password), 10)

    daily_activity = json.load(open('daily_activity.json', 'r'))
    daily_activity = [ (k,v) for k,v in daily_activity.iteritems() ]
    daily_activity.sort()

    html = render_template('index.html',
                           top_asns=top_asns, daily_activity=daily_activity,
                           top_accounts=top_accounts, top_passwords=top_passwords,
                           by_cc=by_cc, durations=durations)
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
