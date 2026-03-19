import argparse
from pipeline import run_pipeline

def exon_skip_filter_pipeline():
    parser = argparse.ArgumentParser(description="Filter exon skip events")
    parser.add_argument('--input', '-i', required=True, help="Path to events.txt")
    parser.add_argument('--output', '-o', default= 'output.json', help="Output JSON")
    args = parser.parse_args()
    run_pipeline(args.input, args.output)

if __name__ == "__main__":
    exon_skip_filter_pipeline()