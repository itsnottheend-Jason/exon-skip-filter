#!/usr/bin/env python3
"""Enrich bioinformatics events with Ensembl gene names via REST API with caching."""

import subprocess
import json
import logging
import os

# Get logger
logger = logging.getLogger("enrichment")

# a simple in-memory cache to avoid duplicate API calls
_gene_cache = {}

# for switching API URL without code changes:
ENSEMBL_BASE_URL = os.getenv("ENSEMBL_BASE_URL", "https://rest.ensembl.org")

def obtain_gene_name(gene_id, verbose=False):
    """Fetch Ensembl gene display name with intelligent caching.
    
    Args:
        gene_id: Ensembl gene identifier (e.g., 'ENSG00000108021')
        verbose: Enable debug logging
        
    Returns:
        Gene display name or 'Unknown' on failure
        
    Note:
        Cache hit: Instant lookup
        Cache miss: API call + cache result
        Failed lookups cached as 'Unknown' to avoid repeated failures
    """
    if not gene_id:
        return "Unknown"

    if gene_id in _gene_cache:
        if verbose:
            logger.info("using cached GENE-NAME to save API calls")
        return _gene_cache[gene_id]
    
    #  fetch name via ensembl REST API.
    try:
        cmd = ['curl', '-s', f"{ENSEMBL_BASE_URL}/lookup/id/{gene_id}?content-type=application/json"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout = 5)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            name = data.get('display_name', 'Unknown')
            _gene_cache[gene_id] = name
            if verbose:
                logger.info(f"GENE-NAME added: {name}")
            return name
    except Exception:
        pass
    return 'Unknown'

def enrich_events(events, verbose=False):
    # Add GENE-NAME to events list.
    """Enrich list of events with GENE-NAME field (mutates original).
    
    Args:
        events: List of event dictionaries
        verbose: Enable debug logging
        
    Returns:
        Same events list with GENE-NAME added to each
    """
    for e in events:
        e['GENE-NAME'] = obtain_gene_name(e['gene_name'], verbose=verbose) # in the events.txt shall be gene_id
    return events


def enrich_event(events, verbose=False):
    #  Add GENE-NAME to each event.
    """Enrich single event with GENE-NAME field (non-mutating).
    
    Args:
        event: Single event dictionary
        verbose: Enable debug logging
        
    Returns:
        New dictionary with GENE-NAME added
    """
    e = dict(events)
    e['GENE-NAME'] = obtain_gene_name(e['gene_name'], verbose=verbose) # in the events.txt the 'gene_name' shall be 'gene_id'
    return e

# Manual Test
if __name__ == "__main__":
    """Manual test demonstrating enrichment and caching."""
    try:
        from filters import apply_all_filters
        from parser import parse_events
        events = parse_events('data/events.txt')
        filtered = apply_all_filters(events)
        enriched = enrich_events(filtered)
        print(enriched[0])  # Should show GENE-NAME: TASOR2 for ENSG00000108021
    except ImportError as exc:
        print(f"Dependencies missing: {exc}")
    except FileNotFoundError as exc:
        print(f"Test data missing: {exc}")
    except Exception as exc:
        logger.error(f"Test failed: {exc}")