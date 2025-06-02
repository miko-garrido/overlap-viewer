import streamlit as st
import pandas as pd
import json
from schedule_logic import DAYS, build_schedule_grids

with open('patterns.json') as f:
    patterns = json.load(f)

sched_grids = build_schedule_grids(patterns)
day = st.selectbox('Select day', DAYS)
day_idx = DAYS.index(day)
hours = [f'{h:02}:00' for h in range(24)]
table = []
for h in range(24):
    row = [int(sched_grids[name][day_idx, h]) for name in sched_grids]
    table.append(row)
df = pd.DataFrame(table, columns=list(sched_grids.keys()), index=hours)
def highlight(val):
    color = '#7fc97f' if val else ''
    return f'background-color: {color}'
st.title('Schedule Overlap Viewer')
st.dataframe(df.style.applymap(highlight), height=700) 