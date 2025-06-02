import streamlit as st
import pandas as pd
import json
from schedule_logic import DAYS, build_schedule_grids

with open('patterns.json') as f:
    patterns = json.load(f)

timezones = ['Asia/Manila', 'America/New_York', 'America/Los_Angeles', 'Australia/Sydney', 'Europe/London']
display_timezone = st.sidebar.selectbox('Display timezone', timezones, index=0)

sched_grids = build_schedule_grids(patterns, display_timezone)
day = st.sidebar.selectbox('Select day', DAYS)
day_idx = DAYS.index(day)
hours = [f'{h:02}:00' for h in range(24)]
names = list(sched_grids.keys())
selected_names = st.sidebar.multiselect('Select names', names, default=names)
table = []
for h in range(24):
    row = [int(sched_grids[name][day_idx, h]) for name in selected_names]
    table.append(row)
df = pd.DataFrame(table, columns=selected_names, index=hours)
def highlight(val):
    color = '#7fc97f' if val else ''
    return f'background-color: {color}'
st.title('Schedule Overlap Viewer')
st.dataframe(df.style.applymap(highlight), height=700) 