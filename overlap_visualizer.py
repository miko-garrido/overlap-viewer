import re
from datetime import datetime
import numpy as np
import streamlit as st
import pandas as pd

DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
DAY_IDX = {'M':0, 'Tu':1, 'W':2, 'Th':3, 'F':4, 'Sa':5, 'Su':6}

# Parse time like '2pm', '1am', '12:30pm'
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
    # grid: 7x24, day: 0-6, start/end: time
    s, e = start.hour, end.hour
    if start < end:
        for h in range(s, e if end.minute == 0 else e+1):
            grid[day, h] = 1
    else:  # crosses midnight
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

def main():
    st.title('Schedule Overlap Viewer')
    patterns = {
        'RJ': {"timezone": "Asia/Manila", "pattern": "2pm-5pm, 9pm-1am", "days": "M,Tu,W,Th,F"},
        'Kai': {"timezone": "Asia/Manila", "pattern": "12am-5am", "days": "M,Tu,W,Th,F"},
        'Lucca': {"timezone": "Asia/Manila", "pattern": "12am-5am, 7pm-12am", "days": "M,Tu,W,Th,F"},
        'Miko': {"timezone": "Asia/Manila", "pattern": "5am-8am, 6pm-9pm", "days": "M,Tu,W,Th,F"},
    }
    sched_grids = {name: parse_pattern(info['pattern'], info['days']) for name, info in patterns.items()}
    day = st.selectbox('Select day', DAYS)
    day_idx = DAYS.index(day)
    hours = [f'{h:02}:00' for h in range(24)]
    # Build table: rows=hours, cols=people
    table = []
    for h in range(24):
        row = [int(sched_grids[name][day_idx, h]) for name in sched_grids]
        table.append(row)
    # Render table with color
    st.write(f'### {day}')
    st.write('**Green = Busy**')
    st.write('')
    df = pd.DataFrame(table, columns=list(sched_grids.keys()), index=hours)
    def highlight(val):
        color = '#7fc97f' if val else ''
        return f'background-color: {color}'
    st.dataframe(df.style.applymap(highlight), height=700)

if __name__ == '__main__':
    main() 