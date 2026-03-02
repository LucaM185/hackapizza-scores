#!/usr/bin/env python3
"""
Generate a JavaScript matrix from competition.csv that can be pasted directly into page.html
This makes the dashboard work on GitHub Pages without needing to load an external CSV file.
"""

import csv
import json

def generate_js_matrix():
    # Read the CSV file
    data = []
    teams = []
    time_labels = []
    
    with open('competition.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # Get header row
        
        # Extract team names (all columns except 'time')
        teams = [col for col in header if col != 'time']
        
        # Read data rows
        for row in reader:
            time_label = row[0]
            scores = [int(val) for val in row[1:]]
            
            time_labels.append(time_label)
            data.append(scores)
    
    # Generate JavaScript code
    js_code = f"""// ════════════════════════════════════════════════════════
//  EMBEDDED DATA MATRIX (generated from competition.csv)
// ════════════════════════════════════════════════════════

const EMBEDDED_TIME_LABELS = {json.dumps(time_labels)};

const EMBEDDED_TEAMS = {json.dumps(teams)};

const EMBEDDED_MATRIX = {json.dumps(data)};

// Initialize dashboard with embedded data
function initDashboardEmbedded() {{
  const raw = EMBEDDED_TIME_LABELS.map((time, idx) => {{
    const row = {{ time }};
    EMBEDDED_TEAMS.forEach((team, teamIdx) => {{
      row[team] = EMBEDDED_MATRIX[idx][teamIdx];
    }});
    return row;
  }});
  
  initDashboard(raw, EMBEDDED_TEAMS);
}}

// Replace the Papa.parse call with this function
// Comment out the Papa.parse section and call initDashboardEmbedded() instead
"""
    
    return js_code

if __name__ == '__main__':
    js_output = generate_js_matrix()
    
    # Print to console so user can copy
    print(js_output)
    
    # Also save to a file for reference
    with open('embedded_data.js', 'w') as f:
        f.write(js_output)
    
    print("\n" + "="*60)
    print("✅ JavaScript matrix generated!")
    print("="*60)
    print("\nSaved to: embedded_data.js")
    print("\nTo use in page.html:")
    print("1. Copy the code above")
    print("2. Paste it into page.html before the closing </script> tag")
    print("3. Comment out or replace the Papa.parse() call with: initDashboardEmbedded()")
