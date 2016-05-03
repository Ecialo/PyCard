# coding: utf-8
"""
Хелпер для просмотра логов клиента.
"""

import io, sys
import argparse
from twisted.logger import eventsFromJSONLogFile, textFileLogObserver


def print_log(fp, user=None, n=1, dest=sys.stdout):
    output = textFileLogObserver(dest)
    events, startups = [], []

    for event in eventsFromJSONLogFile(io.open(fp)):
        events.append(event)
        if event.get('log_format') == 'Start client':
            startups.append(event.get('log_time'))

    last_start_time = 0
    if len(startups) >= n:
        last_start_time = startups[-n]
    elif startups:
        last_start_time = startups[0]

    for event in events:
        fitting_timestamp = (last_start_time <= event.get('log_time'))
        fitting_name = (not user or user == event.get('player_name'))

        if fitting_timestamp and fitting_name:
            output(event)

def main():
    parser = argparse.ArgumentParser(description='Prettify logs produced by twisted.logger.jsonFileLogObserver')
    parser.add_argument('-f', '--file', dest='path', help='Path to log file', required=True)
    parser.add_argument('-n', '--launches', dest='n', type=int, default=1, help='Print last N client runs. By default, only the most recent run is printed')
    parser.add_argument('-u', '--user', dest='user', help='Name of the user whose logs you want to read')

    args = parser.parse_args()
    print_log(fp=args.path, user=args.user, n=args.n)


if __name__ == '__main__':
    main()
