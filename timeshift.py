# coding: utf-8

"""
Update timestamps in time series data to keep the dataset current
"""
from dateutil.parser import parse
from datetime import timedelta
from datetime import datetime
from dateutil.parser import parse as dateparse
from datetime import timezone
from argparse import ArgumentParser
import json

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('file', help='ndjson file with time series data to shift')
    parser.add_argument('target', help='target file name for timeshifted data')
    parser.add_argument('-t', '--time-field', default='@timestamp',
            help='time field (default=@timestamp)')
    args = parser.parse_args()
    return args

def latest_time(filename):
    with open(filename) as f:
        latest = None
        for line in f:
            doc = json.loads(line)
            if latest is None or dateparse(doc[args.time_field]) > dateparse(latest):
                latest = doc[args.time_field]
        print(latest)
        return latest


def get_shift(latest):
    print(datetime.fromisoformat(latest))
    current_time = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-5), 'America/New_York'))
    print(current_time)
    shift = current_time - datetime.fromisoformat(latest)
    print(shift)
    return shift


def timeshift(doc, shift):
    shifted_time = dateparse(doc[args.time_field]) + shift
    doc[args.time_field] = shifted_time.isoformat()
    print(doc[args.time_field])
    return doc

args = parse_args()
shift = get_shift(latest_time(args.file))
with open(args.file) as f:
    with open(args.target, 'w') as f2:
        for line in f:
            doc = json.loads(line)
            shifted = timeshift(doc, shift)
            f2.write(json.dumps(shifted))
            f2.write('\n')
