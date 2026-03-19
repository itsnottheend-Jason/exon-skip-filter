#!/usr/bin/env python3
"""Filter exon skip events based on configurable criteria."""

import logging

# Get logger
logger = logging.getLogger("parser")

def filter_exon_skip(events):
    # keep only event_id starting with 'exon_skip'
    """Filter events where event_id starts with specified prefix.
    
    Args:
        events: List of event dictionaries
        prefix: Event ID prefix to match (default: 'exon_skip')
        
    Returns:
        Filtered events list
    """
    return [e for e in events if e['event_id'].startswith('exon_skip')]

def filter_conf_threshold(events, min_conf=10):
    # keep only event_id starting with 'exon_skip'
    """Filter events where ALL *_conf values are >= threshold.
    
    Args:
        events: List of event dictionaries
        min_conf: Minimum confidence threshold (default: 10.0)
        
    Returns:
        Events passing all confidence thresholds
    """
    def has_confs_below_threshold(event):
        conf_keys = [key for key in events[0].keys() if key.endswith('_conf')]
        # Keep only if all below threshold:
        return all(float(event[key]) >= min_conf for key in conf_keys if event[key])
    
    return [e for e in events if has_confs_below_threshold(e)]

def filter_psi(events):
    # find psi within [0.1 to 0.9]
    """Filter events where psi is within specified range.
    
    Args:
        events: List of event dictionaries
        min_psi: Minimum PSI value (default: 0.1)
        max_psi: Maximum PSI value (default: 0.9)
        
    Returns:
        Events within PSI bounds
    """
    return [e for e in events if 0.1 <= float(e['split_chr10:psi']) <= 0.9]

def apply_selected_filter(events, verbose=False, **filters):
    # selected filters
    """Apply selected filters dynamically by chaining them.
    
    Args:
        events: List of event dictionaries to filter
        verbose: Enable debug logging (default: False)
        **filters: Keyword arguments of filter functions
        
    Returns:
        Filtered events after applying all provided filters
        
    Raises:
        ValueError: If filter argument is not callable
        TypeError: If filter doesn't return a list
    """
    if not events:
        # print('warning: no events')
        logger.info("warning: no events")
        return []
    
    # validate all filters take (events) and return list
    for name, func in filters.items():
        if not callable(func):
            raise ValueError(f"(name) must be a function")
        
    result = events
    for filter_name, filter_func in filters.items():
        if verbose and len(events) > 1:    
            logger.info(f"Applying filter '{filter_name}' ... ")

        result = filter_func(result)

        if len(events) > 1:
            print(f"Applying {filter_name}... Kept {len(result)} events")
        if not isinstance(result, list):
            raise TypeError(f"{filter_name} must return list")
    return result


def apply_all_filters(events):
    # Chain filters.
    """Apply standard exon skip pipeline filters (convenience wrapper).
    
    Equivalent to: apply_selected_filter(events, exon_skip, conf_threshold, psi_range)
    """
    return filter_psi(filter_conf_threshold(filter_exon_skip(events)))


if __name__ == '__main__':
    """Demonstrate filter usage."""
    try:
        from parser import parse_events

        events = parse_events('data/events.txt')
        print(f"Original: {len(events)}")
    
        # Apply SELECTED filters only (e.g., skip conf check)
        filtered_some = apply_selected_filter(
            events,
            exon_skip = filter_exon_skip,
            # conf = filter_conf_threshold,
            psi = filter_psi,  # No conf filter
            
        )
        print(f"Selected filters: {len(filtered_some)} events")
        
    except FileNotFoundError as exc:
        print(f"Test data missing: {exc}")
    except Exception as exc:
        logger.error(f"Demo failed: {exc}")

    
