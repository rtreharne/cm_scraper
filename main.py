from utils import CMSession
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import validators
import time

css = """
<style>
table{
border-collapse:collapse;
border:1px solid black;
}

table td{
border:1px solid black;
}

.fieldlabel {
width: 100px;
}
</style>
"""

def get_courses(session, url):
    session.browser.get(url)
    time.sleep(5)
    elems = session.browser.find_elements(By.TAG_NAME, 'a')
    courses = list(set([x.get_attribute("href") for x in elems if "record.jx?recordid="  in str(x.get_attribute("href"))]))
    return courses

def scrape_course(session, course):
    headers = ["Details", "Outcomes", "Assessment", "Hours", "In Programmes"]

    #try:
    session.browser.get(course)
    links = session.browser.find_elements(By.TAG_NAME, 'a')
    html = ""
    for item in headers:
        tab = get_webelem_from_text(links, item)
        try:
            tab.click()
            html += session.browser.page_source
        except:
            continue
    
    return format_html(html)
    #except:
        #pass
     
def get_webelem_from_text(links, keyword):
    for link in links:
        if keyword in link.get_attribute("text"):
            return link
      
def format_html(html):
    soup = BeautifulSoup(html, "html.parser")
    myDivs = soup.find_all("div", {"class": "wt-record-wrapper"})
    html_string = ""

    for div in myDivs:
        sub_div = div.find_all("div", {"class": "tabpanel"})
        for i, sub in enumerate(sub_div):
            if len(str(sub.text)) != 0:
                html_string += str(sub)


    try:
        values = myDivs[0].find_all("td", {"class": "fieldvalue"})
        
        code = values[2].text
    
        fname = "{0}_{1}".format(str(code), str(values[0].text.upper())).replace(":", "-")

        html_string = html_string.replace("â€‹", "-")


        if not os.path.exists("formatted_html"):
            os.makedirs("formatted_html")

        with open("formatted_html/{0}".format(fname)+".html", 'w', encoding='utf-8') as f:
                    f.write(css+str(html_string))
                    success_string = "File saved as {0}".format(fname)+".html"
        
        return success_string
    except:
        return "Sweeping error under the carpet. Nothing to see here."

def main():
    print("""
 ::::::::  ::::    ::::      ::::::::   ::::::::  :::::::::      :::     :::::::::  :::::::::: :::::::::  
:+:    :+: +:+:+: :+:+:+    :+:    :+: :+:    :+: :+:    :+:   :+: :+:   :+:    :+: :+:        :+:    :+: 
+:+        +:+ +:+:+ +:+    +:+        +:+        +:+    +:+  +:+   +:+  +:+    +:+ +:+        +:+    +:+ 
+#+        +#+  +:+  +#+    +#++:++#++ +#+        +#++:++#:  +#++:++#++: +#++:++#+  +#++:++#   +#++:++#:  
+#+        +#+       +#+           +#+ +#+        +#+    +#+ +#+     +#+ +#+        +#+        +#+    +#+ 
#+#    #+# #+#       #+#    #+#    #+# #+#    #+# #+#    #+# #+#     #+# #+#        #+#        #+#    #+# 
 ########  ###       ###     ########   ########  ###    ### ###     ### ###        ########## ###    ### 
"""
          )
    print("By R. Treharne. 2024")
    # print blanklines
    print("")
    print("")
    print("Logging in to Worktribe (You must be on campus to do this!) ...")
    print("")
    session = CMSession()
    print("")
    while True:
        url = input("Input the URL of the Worktribe page you want to scrape: ")
        if validators.url(url):
            break
        else:
            print("Invalid URL. Please try again.")

    courses = get_courses(session, url)
    print("")
    print("Wait ...")
    print("")
    for i, course in enumerate(courses):
        response = scrape_course(session, course)
        print(f"{i+1}/{len(courses)}: {response}")

    print("")

    print("Finished scraping courses. Exiting ...")

    
if __name__ == "__main__":
    main()