import csv
import logging

# Get logger
logger = logging.getLogger("parser")

def parse_events(file_path):
    events = []
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            events.append(row)
    return events

def iter_events(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        # return list(reader)
        for row in reader:
            yield row                               # Pauses, yields ONE row, remembers position, for large files

# Manual test
if __name__ == "__main__":
    events = iter_events('data/events.txt')
    print(type(events))
  