import os
import csv
from bs4 import BeautifulSoup

input_dir = 'formatted_html'
output_file = 'assessment_summary.csv'
results = []

for filename in os.listdir(input_dir):
    if not filename.endswith('.html'):
        continue

    filepath = os.path.join(input_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

        # Extract course status (e.g. "Development Approval")
        status_label = soup.find('td', class_='fieldlabel', string=lambda t: t and 'Status' in t)
        if status_label:
            status_cell = status_label.find_next_sibling('td')
            if status_cell:
                status_text = status_cell.get_text(strip=True)
            else:
                status_text = 'Unknown'
        else:
            status_text = 'Unknown'

        # Look for the "Assessment" section heading
        assessment_heading = soup.find(lambda tag: tag.name == "h1" and "Assessment" in tag.get_text())
        if not assessment_heading:
            continue

        # Find the gridtable immediately after the heading
        table = assessment_heading.find_next('table', {'class': 'gridtable'})
        if not table:
            continue

        # Extract Assessment Strategy
        strategy_label = soup.find('td', class_='fieldlabel', string=lambda t: t and 'Assessment Strategy' in t)
        if strategy_label:
            strategy_cell = strategy_label.find_next_sibling('td')
            if strategy_cell:
                assessment_strategy = strategy_cell.get_text(separator=' ', strip=True)
            else:
                assessment_strategy = ''
        else:
            assessment_strategy = ''


        for tbody in table.find_all('tbody'):
            for row in tbody.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) >= 3:
                    type_cell = cells[1].get_text(strip=True)
                    weight_cell = cells[2].get_text(strip=True)

                    # Skip header rows
                    if "Title" in type_cell or "Weighting" in weight_cell:
                        continue

                    if type_cell and '%' in weight_cell:
                        results.append({
                            'Course': filename.replace('.html', ''),
                            'Assessment Type': type_cell,
                            'Weighting': weight_cell,
                            'Status': status_text,
                            'Assessment Strategy': assessment_strategy
                        })


# Write to CSV
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Course', 'Assessment Type', 'Weighting', 'Status', 'Assessment Strategy'])
    writer.writeheader()
    writer.writerows(results)

print(f"✅ Extracted {len(results)} rows to {output_file}")
