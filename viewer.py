import streamlit as st
import pandas as pd
import json
import requests
import ssl
import urllib3
from schedule_logic import DAYS, build_schedule_grids

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Google Sheets URL - replace with your sheet ID
SHEET_URL = "https://docs.google.com/spreadsheets/d/1u2wKp756BwFvE3ZeLgurpRX-yVt1wSrSTbV65b7o-_o/export?format=csv&gid=0"

def load_data():
    """Load and process schedule patterns from Google Sheets."""
    try:
        # Use requests with SSL verification disabled as fallback
        response = requests.get(SHEET_URL, verify=False)
        response.raise_for_status()
        
        # Read CSV from response content
        from io import StringIO
        df = pd.read_csv(StringIO(response.text))
        
        # Convert DataFrame to the expected JSON structure
        patterns = []
        for _, row in df.iterrows():
            # Handle potential column name variations and strip whitespace
            name = str(row.get("name", row.get("Name", ""))).strip()
            timezone = str(row.get("timezone", row.get("Timezone", "Asia/Manila"))).strip()
            pattern = str(row.get("pattern", row.get("Pattern", ""))).strip()
            days = str(row.get("days", row.get("Days", "M,Tu,W,Th,F"))).strip()
            teams_str = str(row.get("teams", row.get("Teams", ""))).strip()
            
            # Skip rows with empty names
            if not name or name == "nan":
                continue
                
            teams = [t.strip() for t in teams_str.split(",") if t.strip() and t.strip() != "nan"]
            
            pattern_dict = {
                "name": name,
                "timezone": timezone, 
                "pattern": pattern,
                "days": days,
                "teams": teams
            }
            patterns.append(pattern_dict)
        
        return patterns
    except Exception as e:
        st.error(f"Error loading data from Google Sheets: {e}")
        # Fallback to local JSON if available
        try:
            with open('patterns.json') as f:
                return json.load(f)
        except:
            return []

def create_sidebar_controls(patterns):
    """Create all sidebar controls and return their values."""
    timezones = ['Asia/Manila', 'America/New_York', 'America/Los_Angeles', 'Australia/Sydney', 'Europe/London']
    display_timezone = st.sidebar.selectbox('Display timezone', timezones, index=1)
    
    day = st.sidebar.selectbox('Select day', DAYS)
    
    # Get all unique teams
    all_teams = set()
    for entry in patterns:
        all_teams.update(entry.get('teams', []))
    all_teams = sorted(list(all_teams))
    
    selected_teams = st.sidebar.multiselect('Select teams', all_teams, default=[])
    
    return display_timezone, day, selected_teams

def filter_schedules(patterns, selected_teams, sched_grids):
    """Filter schedules based on team selection and return filtered names."""
    names = list(sched_grids.keys())
    selected_names = st.sidebar.multiselect('Select names', names, default=[])
    
    # Filter patterns by selected teams
    filtered_by_teams = [p['name'] for p in patterns if any(team in selected_teams for team in p.get('teams', []))]
    
    # Combine filters: show union of team members and selected names
    if not selected_teams and not selected_names:
        final_names = names
    else:
        final_names = list(set(filtered_by_teams + selected_names))
        final_names = [name for name in final_names if name in names]
    
    return final_names

def create_schedule_dataframe(sched_grids, final_names, day_idx):
    """Create the schedule dataframe for display."""
    hours = [f'{h:02}:00' for h in range(24)]
    
    table = []
    for h in range(24):
        row = [int(sched_grids[name][day_idx, h]) for name in final_names]
        table.append(row)
    
    df = pd.DataFrame(table, columns=final_names, index=hours)
    return df

def style_schedule_cells(df):
    """Apply styling to the schedule dataframe."""
    display_df = pd.DataFrame('', index=df.index, columns=df.columns)
    
    def style_cells(df):
        def apply_style(val, row_idx, col_idx):
            if val == 0:
                return ''
            
            hour = row_idx
            if 8 <= hour <= 16:
                return 'background-color: #81c784'
            elif 17 <= hour <= 19:
                return 'background-color: #66bb6a'
            else:
                return 'background-color: #4caf50'
        
        styled = pd.DataFrame('', index=df.index, columns=df.columns)
        for i, row_idx in enumerate(df.index):
            for j, col in enumerate(df.columns):
                styled.iloc[i, j] = apply_style(df.iloc[i, j], i, j)
        return styled
    
    return display_df.style.apply(lambda _: style_cells(df), axis=None)

def setup_page():
    """Configure Streamlit page settings and CSS."""
    st.set_page_config(layout="wide")
    
    st.markdown("""
    <style>
    .block-container {
        padding-bottom: 0rem;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Main application function."""
    setup_page()
    
    patterns = load_data()
    display_timezone, day, selected_teams = create_sidebar_controls(patterns)
    
    sched_grids = build_schedule_grids(patterns, display_timezone)
    day_idx = DAYS.index(day)
    
    final_names = filter_schedules(patterns, selected_teams, sched_grids)
    df = create_schedule_dataframe(sched_grids, final_names, day_idx)
    styled_df = style_schedule_cells(df)
    
    st.dataframe(styled_df, height=750, use_container_width=True)

if __name__ == "__main__":
    main() 