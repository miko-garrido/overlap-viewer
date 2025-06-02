import streamlit as st
import pandas as pd
import json
from schedule_logic import DAYS, build_schedule_grids

with open('patterns.json') as f:
    patterns = json.load(f)

timezones = ['Asia/Manila', 'America/New_York', 'America/Los_Angeles', 'Australia/Sydney', 'Europe/London']
display_timezone = st.sidebar.selectbox('Display timezone', timezones, index=1)

sched_grids = build_schedule_grids(patterns, display_timezone)

# Get all unique teams
all_teams = set()
for entry in patterns:
    all_teams.update(entry.get('teams', []))
all_teams = sorted(list(all_teams))

selected_teams = st.sidebar.multiselect('Select teams', all_teams, default=[])

# Filter patterns by selected teams
filtered_by_teams = [p['name'] for p in patterns if any(team in selected_teams for team in p.get('teams', []))]

day = st.sidebar.selectbox('Select day', DAYS)
day_idx = DAYS.index(day)
hours = [f'{h:02}:00' for h in range(24)]
names = list(sched_grids.keys())
selected_names = st.sidebar.multiselect('Select names', names, default=[])

# Combine filters: show union of team members and selected names
if not selected_teams and not selected_names:
    # No filters selected, show everyone
    final_names = names
else:
    # Show union of team filters and name filters
    final_names = list(set(filtered_by_teams + selected_names))
    # Keep only names that exist in the schedule
    final_names = [name for name in final_names if name in names]

table = []
for h in range(24):
    row = [int(sched_grids[name][day_idx, h]) for name in final_names]
    table.append(row)
df = pd.DataFrame(table, columns=final_names, index=hours)

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