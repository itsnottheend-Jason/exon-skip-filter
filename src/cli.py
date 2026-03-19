#!/usr/bin/env python3
"""Command-line interface for exon skip filtering pipeline."""

import sys
import argparse
from pipeline import run_pipeline
import logging
from __init__ import __version__

logger = logging.getLogger('cli')

def main():
    parser = argparse.ArgumentParser(description="Filter exon skip events")
    parser.add_argument('--input', '-i', required=True, help="Path to events.txt")
    parser.add_argument('--output', '-o', default= 'output/output.json', help="Output JSON")
    parser.add_argument('-c', '--config', help="Config YAML")
    parser.add_argument('--version', action='version', version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    # Orchestrator Exit Codes
    # 0 = Success
    # 1 = File not found  
    # 2 = Pipeline error
    try:
        run_pipeline(args.input, args.output)
    except FileNotFoundError as e:
        logger.error(f"Input file not found: (e)")
        sys.exit(1)
    except Exception as e:
        logger.exception("Pipeline failed")
        sys.exit(2)

if __name__ == "__main__":
    main()