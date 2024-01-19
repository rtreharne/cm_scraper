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

Run the `main.py` script and follow prompts. Good luck to you.

```{bash}
python main.py
```










