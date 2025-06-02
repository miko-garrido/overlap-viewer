import re
from datetime import datetime
import numpy as np

DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
DAY_IDX = {'M':0, 'Tu':1, 'W':2, 'Th':3, 'F':4, 'Sa':5, 'Su':6}

def parse_time(tstr):
    tstr = tstr.strip().lower()
    fmt = '%I%p' if ':' not in tstr else '%I:%M%p'
    return datetime.strptime(tstr, fmt).time()

def parse_time_range(rng):
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

def parse_pattern(pattern, days):
    grid = np.zeros((7, 24))
    for rng in pattern.split(','):
        start, end = parse_time_range(rng)
        for day in expand_days(days):
            add_block(grid, day, start, end)
    return grid

def build_schedule_grids(patterns):
    return {entry['name']: parse_pattern(entry['pattern'], entry['days']) for entry in patterns} 