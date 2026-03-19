#!/usr/bin/env python3
"""Parse tab-separated bioinformatics event files into dicts or iterables."""

import csv
import logging
from pathlib import Path
from typing import Iterator, List, Dict, Any, Union

# Configure module logger
logger = logging.getLogger(__name__)


def parse_events(file_path: Union[str, Path]) -> List[Dict[str, str]]:
    """Parse TSV file into list of event dictionaries (for small files/testing).
    
    Args:
        file_path: Path to tab-separated events file
        
    Returns:
        List of dictionaries, where keys are column headers
        
    Raises:
        FileNotFoundError: If file_path doesn't exist
        csv.Error: If file has malformed CSV/TSV structure
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Events file not found: {file_path}")
    
    events: List[Dict[str, str]] = []
    try:
        with file_path.open('r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            events.extend(reader)
        logger.debug(f"Parsed {len(events)} events from {file_path}")
    except csv.Error as exc:
        logger.error(f"TSV parsing error in {file_path}: {exc}")
        raise
    
    return events


def iter_events(file_path: Union[str, Path]) -> Iterator[Dict[str, str]]:
    """Stream events one-by-one from TSV (memory efficient for large files).
    
    Args:
        file_path: Path to tab-separated events file
        
    Yields:
        Dictionary per row (column headers → values)
        
    Raises:
        FileNotFoundError: If file_path doesn't exist
        csv.Error: If file has malformed CSV/TSV structure
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Events file not found: {file_path}")
    
    try:
        with file_path.open('r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            yield from reader
    except csv.Error as exc:
        logger.error(f"TSV parsing error in {file_path}: {exc}")
        raise


if __name__ == "__main__":
    """Manual test both parsers."""
    try:
        # Test list parser (small files)
        events_list = parse_events('data/events.txt')
        print(f"List parser: {len(events_list)} events, type: {type(events_list[0])}")
        
        # Test streaming parser (large files)
        events_iter = iter_events('data/events.txt')
        print(f"Iter parser type: {type(events_iter)}")
        first_event = next(events_iter)
        print(f"First event keys: {list(first_event.keys())[:5]}...")
        
    except FileNotFoundError as exc:
        print(f"Test failed - {exc}. Create data/events.txt first.")
