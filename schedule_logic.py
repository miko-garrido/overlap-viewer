import re
from datetime import datetime
import numpy as np
import pytz

DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
DAY_IDX = {'M':0, 'Tu':1, 'W':2, 'Th':3, 'F':4, 'Sa':5, 'Su':6}

def parse_time(tstr):
    tstr = tstr.strip().lower()
    fmt = '%I%p' if ':' not in tstr else '%I:%M%p'
    return datetime.strptime(tstr, fmt).time()

def convert_time_to_timezone(time_obj, source_tz, target_tz, base_date=None):
    if base_date is None:
        base_date = datetime.now().date()
    
    source_timezone = pytz.timezone(source_tz)
    target_timezone = pytz.timezone(target_tz)
    
    dt = datetime.combine(base_date, time_obj)
    source_dt = source_timezone.localize(dt)
    target_dt = source_dt.astimezone(target_timezone)
    
    return target_dt.time(), target_dt.date()

def parse_time_range(rng):
    rng = rng.strip()
    if '-' not in rng:
        raise ValueError(f"Invalid time range format: '{rng}' (expected format: 'start-end')")
    start_str, end_str = rng.split('-')
    start = parse_time(start_str)
    end = parse_time(end_str)
    return start, end

def expand_days(days_str):
    return [DAY_IDX[d] for d in re.findall(r'M|Tu|W|Th|F|Sa|Su', days_str)]

def add_block(grid, day, start, end):
    s, e = start.hour, end.hour
    if start < end:
        for h in range(s, e if end.minute == 0 else e+1):
            grid[day, h] = 1
    else:
        for h in range(s, 24):
            grid[day, h] = 1
        for h in range(0, e if end.minute == 0 else e+1):
            grid[(day+1)%7, h] = 1

def parse_pattern(pattern, days, source_timezone, display_timezone):
    # Handle empty or whitespace-only patterns, or 'nan' string
    if not pattern or not pattern.strip() or pattern.strip().lower() == 'nan':
        return np.zeros((7, 24))
    
    grid = np.zeros((7, 24))
    for rng in pattern.split(','):
        rng = rng.strip()  # Clean whitespace around ranges
        if not rng or rng.lower() == 'nan':  # Skip empty ranges or 'nan'
            continue
        start, end = parse_time_range(rng)
        
        # Convert times to display timezone
        start_converted, start_date = convert_time_to_timezone(start, source_timezone, display_timezone)
        end_converted, end_date = convert_time_to_timezone(end, source_timezone, display_timezone)
        
        for day in expand_days(days):
            # Handle potential day shifts due to timezone conversion
            start_day_offset = (start_date - datetime.now().date()).days
            end_day_offset = (end_date - datetime.now().date()).days
            
            add_block(grid, (day + start_day_offset) % 7, start_converted, end_converted)
    return grid

def build_schedule_grids(patterns, display_timezone='Asia/Manila'):
    return {entry['name']: parse_pattern(entry['pattern'], entry['days'], 
                                       entry['timezone'], display_timezone) 
            for entry in patterns} 