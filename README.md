# CM Scraper

This project is used to extract module information from the University of Liverpool's Curriculum Manager web application.

## Usage

Clone this repository

```{bash}
git clone https://github.com/rtreharne/cm_scraper
```

Create a virtual environment and install requirements
```{bash}
python -m virtualenv .venv 
.\.venv\Scripts\activate
pip install -r requirements.txt
```

If ChromeDriver is out of date checkout the latest stable versions at: https://googlechromelabs.github.io/chrome-for-testing/#stable

Download and extract the correct chromedriver.exe to your working directory.

Need to know what version of Chrome you're currently using?

```{bash}
reg query "HKLM\Software\Wow6432Node\Google\Update\Clients\{8A69D345-D564-463c-AFF1-A69D9E530F96}" /v pv
``````

Run the `main.py` script and follow prompts.

```{bash}
python main.py
```

There is another file, `extract_outcomes.py`. Running this will get all the Learning Outcomes from each course and save them to `module_outcomes.csv`.

```{bash}
python extract_outcomes.py
```

If you encounter an erro it's probably because one of your .html files contains no tables. Look for a weird filename and delete the file from the fomratted_html directory.










