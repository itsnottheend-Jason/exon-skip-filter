import subprocess
import json

def obtain_gene_name(gene_id):
    #  fetch name via ensembl REST API.
    try:
        cmd = ['curl', '-s', f"https://rest.ensembl.org/lookup/id/{gene_id}?content-type=application/json"]
        result = subprocess.run(cmd, capture_output=True, text=True, timemout = 5)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get('display_name', 'Unknown')
    except Exception:
        pass
    return 'Unknown'

def enrich_events(events):
    #  Add GENE-NAME to each event.
    for event in events:
        event['GENE-NAME'] = obtain_gene_name(event['gene_name']) # in the events.txt shall be gene_id
    return events

# Manual Test
if __name__ == "__main__":
    from filters import apply_all_filters
    from parser import parse_events
    events = parse_events('data/events.txt')
    filtered = apply_all_filters(events)
    enriched = enrich_events(filtered)
    print(enriched[0])  # Should show GENE-NAME: TASOR2 for ENSG00000108021