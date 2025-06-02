import streamlit as st
import pandas as pd
import json
from schedule_logic import DAYS, build_schedule_grids

with open('patterns.json') as f:
    patterns = json.load(f)

timezones = ['Asia/Manila', 'America/New_York', 'America/Los_Angeles', 'Australia/Sydney', 'Europe/London']
display_timezone = st.sidebar.selectbox('Display timezone', timezones, index=1)

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

# Create display dataframe with empty strings
display_df = pd.DataFrame('', index=df.index, columns=df.columns)

def style_cells(df):
    def apply_style(val, row_idx, col_idx):
        hour = row_idx  # row_idx corresponds to hour (0-23)
        # Base colors for different time periods
        if 8 <= hour <= 16:  # 8am to 5pm
            base_color = '#f8f9fa' if val == 0 else '#c8e6c9'
        elif 17 <= hour <= 19:  # 5pm to 8pm
            base_color = '#e9ecef' if val == 0 else '#a5d6a7'
        else:  # 8pm to 8am
            base_color = '#d6d8db' if val == 0 else '#94c497'
        return f'background-color: {base_color}'
    
    styled = pd.DataFrame('', index=df.index, columns=df.columns)
    for i, row_idx in enumerate(df.index):
        for j, col in enumerate(df.columns):
            styled.iloc[i, j] = apply_style(df.iloc[i, j], i, j)
    return styled

styled_df = display_df.style.apply(lambda _: style_cells(df), axis=None)
st.dataframe(styled_df, height=700) 