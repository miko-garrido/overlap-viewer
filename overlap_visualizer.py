import re
from datetime import datetime
import numpy as np

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

def grid_to_html(name, grid):
    html = f'<h2>{name}</h2>'
    html += '<table class="sched"><tr><th></th>'
    for h in range(24):
        html += f'<th>{h}</th>'
    html += '</tr>'
    for d, day in enumerate(DAYS):
        html += f'<tr><td>{day}</td>'
        for h in range(24):
            cell = 'busy' if grid[d, h] else ''
            html += f'<td class="{cell}"></td>'
        html += '</tr>'
    html += '</table>'
    return html

def write_html(schedules):
    style = '''<style>
table.sched { border-collapse: collapse; margin-bottom: 30px; }
table.sched th, table.sched td { border: 1px solid #ccc; width: 20px; height: 20px; text-align: center; }
table.sched td.busy { background: #7fc97f; }
table.sched th { background: #eee; }
table.sched td:first-child, table.sched th:first-child { background: #fff; }
</style>'''
    html = f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>Schedule Overlap</title>{style}</head><body>'
    for name, grid in schedules.items():
        html += grid_to_html(name, grid)
    html += '</body></html>'
    with open('overlap_visualizer.html', 'w') as f:
        f.write(html)

# Example usage
if __name__ == '__main__':
    patterns = {
        'RJ': {"timezone": "Asia/Manila", "pattern": "2pm-5pm, 9pm-1am", "days": "M,Tu,W,Th,F"},
        'Kai': {"timezone": "Asia/Manila", "pattern": "12am-5am", "days": "M,Tu,W,Th,F"},
        'Lucca': {"timezone": "Asia/Manila", "pattern": "12am-5am, 7pm-12am", "days": "M,Tu,W,Th,F"},
        'Miko': {"timezone": "Asia/Manila", "pattern": "5am-8am, 6pm-9pm", "days": "M,Tu,W,Th,F"},
    }
    sched_grids = {name: parse_pattern(info['pattern'], info['days']) for name, info in patterns.items()}
    write_html(sched_grids) 