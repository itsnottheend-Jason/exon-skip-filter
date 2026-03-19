import csv

# def parse_events(file_path):
#     events = []
#     with open(file_path, 'r') as f:
#         reader = csv.DictReader(f, delimiter='\t')
#         for row in reader:
#             events.append(row)
#     return events

def parse_events(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        return list(reader)

if __name__ == "__main__":
    events = parse_events('data/events.txt')
    print(events[10])
    # print(events[0].keys())
    # print("Event 0 type:", type(events[0]))  # <class 'dict'>
    # print("Has keys?", hasattr(events[0], 'keys'))  # True
    # print("Keys:", list(events[0].keys())[:3])  # ['chrm', 'strand', 'event_id']
  