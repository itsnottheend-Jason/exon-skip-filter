#!/usr/bin/env python3
"""Main exon skip filtering pipeline orchestrating parsing, filtering, and enrichment."""

import sys
import yaml
import json
from parser import iter_events
from enrichment import enrich_event
import logging
from __init__ import __version__
from logging_config import setup_logging

from filters import (
    apply_selected_filter,
    filter_exon_skip,      # add all defined filters
    filter_conf_threshold, 
    filter_psi             
)

# Setup logging ONCE (entrypoint only)
setup_logging()
logger = logging.getLogger('pipeline')

# Load configuration yaml file to select different filters.
def run_pipeline(input_path, output_path, config_path=None):
    logger.info(f"=== Starting exon skip pipeline {__version__} ===")
    logger.info(f"Input: {input_path}")

    # Count total events (fast first pass)
    total_events = 0
    for _ in iter_events(input_path):
        total_events += 1
    logger.info(f"Total events to process: {total_events:,}")

    all_filters = {
        'exon_skip': filter_exon_skip,
        'conf_threshold': filter_conf_threshold,
        'psi': filter_psi
    }

    """Execute complete exon skip filtering pipeline.
    
    Args:
        input_path: Path to input TSV file
        output_path: Path to output JSON file
        config_path: Optional YAML config for custom filters
    """
    
    if config_path:
        with open(config_path) as f:
            config = yaml.safe_load(f)
        filters_to_apply = {k: all_filters[k] for k in config['filters']}
    else:
        filters_to_apply = all_filters

    def passes_all_filters(event):
        events  = [event]
        filtered = apply_selected_filter(
            events,
            verbose=False,
            **filters_to_apply
            )
        return len(filtered) == 1
    
    output_events = []
        
    with open(output_path, 'w') as out:
        out.write("[\n")
        isfirst = True
        for event in iter_events(input_path):
            if not passes_all_filters(event):
                continue
            enriched = enrich_event(event, verbose=True)
            if not isfirst:
                out.write(",\n")
            json.dump(enriched, out)
            isfirst = False
            output_events.append(enriched)
        out.write("\n]")

    """Generate comprehensive summary statistics from enriched events.
    
    Args:
        final_data: List of enriched event dictionaries
        
    Returns:
        Summary statistics dictionary
    """
    # Read final JSON for stats (super simple!)
    with open(output_path, 'r') as f:
        final_data = json.load(f)
        unique_genes = len({e.get('GENE-NAME') for e in final_data if e.get('GENE-NAME') != 'Unknown'})

    logger.info(f"Pipeline complete!")
    logger.info(f"Processed: {total_events:,} → Output: {len(output_events):,} events")
    logger.info(f"Cache stats: {(unique_genes)} unique genes found")
    logger.info(f"Results saved to: {output_path}")

# Manual test
if __name__ == "__main__":
    """Entry point for manual testing."""
    try:
        logger.info("=== Pipeline started ===")
        run_pipeline('data/events.txt', 'output/output.json', config_path="config/config.yaml")
        logger.info("Log file created!")
        logger.info("Pipeline test successful!")
    except FileNotFoundError as exc:
        logger.error(f"Input/output files missing: {exc}")
        sys.exit(1)
    except yaml.YAMLError as exc:
        logger.error(f"Config parsing failed: {exc}")
        sys.exit(2)
    except Exception as exc:
        logger.exception("Pipeline execution failed")
        sys.exit(3)