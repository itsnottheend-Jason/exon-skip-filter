import json
from parser import parse_events
from filters import apply_all_filters
from enrichment import enrich_events

def run_pipeline(input_path, output_path):
    # Pipeline: parse, filter, enrich - json.
    events = parse_events(input_path)
    filtered = apply_all_filters(events)
    enriched = enrich_events(filtered)

    with open(output_path,'w') as f:
        json.dump(enriched, f, indent = 2)

    print(f"File written to {output_path} with {len(enriched)} events, named as xxx")

# Manual test
if __name__ == "__main__":
    run_pipeline('data/events.txt', 'output/output.json')