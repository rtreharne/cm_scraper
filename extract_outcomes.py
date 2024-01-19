import pandas as pd

# get all file paths in formatted_html folder
import os
from os import listdir
from os.path import isfile, join
import re

def get_learning_outcomes_table(tables):# find first table with "Learning Outcomes" at loc[0, 0]
    for i, table in enumerate(tables):
        try:
            if table.loc[0, 0] == "Learning Outcomes":
                return table
        except:
            continue

def get_files(dir="formatted_html"):
    mypath = os.getcwd() + f'/{dir}'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def get_objectives(file, dir="formatted_html"):
    print(file)
    print(os.getcwd() + f'/{dir}/' + file)
    
    tables = pd.read_html(f'{dir}/' + file)

    module_short_name = tables[5].loc[0, 1]
    module_code = tables[6].loc[0, 1]

    table = get_learning_outcomes_table(tables)

    if table is None:
        return None

    outcomes = table.loc[:, 1:2]
    outcomes = outcomes.dropna(subset=[1])

    lo_pattern = re.compile(r'LO\d{1,2}')
    skill_pattern = re.compile(r'S\d{1,2}')
    lo_rows = outcomes[outcomes[1].str.match(lo_pattern)]
    skill_rows = outcomes[outcomes[1].str.match(skill_pattern)]

    rows = []


    for index, row in lo_rows.iterrows():
        rows.append({
            'module_short_name': module_short_name,
            'module_code': module_code,
            'type': "LO",
            'label': row[1],
            'description': row[2],
        })


        for index, row in skill_rows.iterrows():
            rows.append({
                'label': row[1],
                'description': row[2],
                'module_short_name': module_short_name,
                'module_code': module_code,
                'type': "SKILL",
            })

    new_table = pd.DataFrame(rows)

    return new_table
    
def main():
    files = get_files()
    all_tables = []
    for file in files:
        table = get_objectives(file)
        print(table)
        if table is not None:
            all_tables.append(table)
    all_tables = pd.concat(all_tables)
    all_tables.to_csv("module_outcomes.csv", encoding='utf-8', index=False)

if __name__ == "__main__":
    main()