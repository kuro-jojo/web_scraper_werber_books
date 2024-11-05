from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

url = "https://en.wikipedia.org/wiki/Bernard_Werber"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

headers = soup.find_all("div", class_="mw-heading mw-heading3")

titles = [h.h3.text for h in headers]

book_list_elements = soup.css.select("div.mw-heading.mw-heading3 + ul")

df = pd.DataFrame(columns=["Category", "Title", "Year"])
for i, elt in enumerate(book_list_elements):
    for li in elt.find_all("li"):
        cnts = li.text.split(",")
        if cnts and len(cnts) > 2 and cnts[2].strip().isnumeric():
            cnts.pop(1)
        cnts = cnts[:2]
        cnts[0] = cnts[0].removesuffix("[fr]").removesuffix("(short").strip()
        cnts[1] = re.split("^(\s?\d{4}).?\(.+\)$", cnts[1].strip())[0]
        cnts[1] = cnts[1] if cnts[1].isnumeric() else ""

        df.loc[len(df)] = [titles[i], *cnts]

print(df)
df.to_csv("werber_books.csv", index=False)
