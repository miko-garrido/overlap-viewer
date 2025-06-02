# Overlap Viewer - Dorxata Team Schedule Management

A Streamlit application designed to help the Dorxata management team handle multi-timezone overlap across different teams and manage coverage for clients across multiple timezones.

**Live Application:** https://dorxata-sched.streamlit.app/

## Features

- **Multi-timezone Schedule Visualization**: View team member schedules across different timezones
- **Team-based Filtering**: Filter schedules by teams (core, ops, projects, design)
- **Google Sheets Integration**: Automatically loads schedule data from Google Sheets
- **Interactive Schedule Grid**: Color-coded 24-hour schedule view
- **Timezone Conversion**: Supports major timezones (Asia/Manila, America/New_York, America/Los_Angeles, Australia/Sydney, Europe/London)

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd overlap-viewer
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run viewer.py
```

The application will open in your browser at `http://localhost:8501`

## Project Structure

```
overlap-viewer/
├── viewer.py           # Main Streamlit application
├── schedule_logic.py   # Core scheduling logic and timezone conversion
├── test.py            # Google Sheets connection testing
├── patterns.json      # Fallback schedule data
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## Usage

1. **Select Display Timezone**: Choose the timezone to display all schedules in
2. **Choose Day**: Select which day of the week to view
3. **Filter by Teams**: Select specific teams to view their members' schedules
4. **Select Individual Names**: Optionally select specific team members
5. **View Schedule Grid**: Color-coded availability with green intensity indicating work hours

## Schedule Color Coding

- **Light Green**: Core work hours (8 AM - 4 PM)
- **Medium Green**: Extended hours (5 PM - 7 PM)
- **Dark Green**: Off-hours availability

## Data Source

The application loads schedule data from a Google Sheets document. If the connection fails, it falls back to the local `patterns.json` file.

## Configuration

Schedule patterns are defined with:
- `name`: Team member name
- `timezone`: Their local timezone
- `pattern`: Work hours (e.g., "9am-5pm" or "9pm-5am")
- `days`: Working days (M,Tu,W,Th,F,Sa,Su)
- `teams`: Team affiliations (core, ops, projects, design)

## Testing

Run the Google Sheets connection test:

```bash
python3 test.py
```

## Dependencies

- streamlit
- pandas
- numpy
- matplotlib
- requests
- pytz (for timezone handling)