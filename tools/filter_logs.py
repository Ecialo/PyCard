# coding: utf-8
"""
Хелпер для просмотра логов клиента.
"""

import io, sys
import argparse
from twisted.logger import eventsFromJSONLogFile, textFileLogObserver


def print_log(fp, name=None, last_only=True, dest=sys.stdout):
    output = textFileLogObserver(dest)
    events = []

    last_start_time = 0 if not last_only else 1e64 # should get us covered till the end of time (literally)
    for event in eventsFromJSONLogFile(io.open(fp)):
        events.append(event)
        if event.get('log_format') == 'Start client':
            last_start_time = event.get('log_time')

    for event in events:
        fitting_timestamp = (not last_only or last_start_time <= event.get('log_time'))
        fitting_name = (not name or name == event.get('player_name'))

        if fitting_timestamp and fitting_name:
            output(event)

def main():
    parser = argparse.ArgumentParser(description='Prettify logs produced by twisted.logger.jsonFileLogObserver')
    parser.add_argument('-f', '--file', dest='path', help='Path to log file', required=True)
    parser.add_argument('-a', '--all', dest='last_only', action='store_false', help='Print the whole log. By default, only last run is printed')
    parser.add_argument('-n', '--name', dest='name', help='Name of the user whose logs you want to read')

    args = parser.parse_args()
    print_log(fp=args.path, name=args.name, last_only=args.last_only)


if __name__ == '__main__':
    main()
