FIRST_NAMES = [
                "a", "b", "c", "d", "e", "f",
                "g", "h", "i", "j", "k", "l",
                "m", "n", "o", "p", "q", "r",
                "s", "t", "u", "v", "w", "x",
                "y", "z"
            ]


from tqdm import tqdm
import sys
import requests
from bs4 import BeautifulSoup as Soup
from db_insert import insert_records

for first_name in FIRST_NAMES:
    try:
        for page_no in range(1, 300):
            try:

                headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
                }

                response = requests.get(
                    f'https://www.pharmacyregulation.org/registers/pharmacytechnician/firstnames/{first_name}/page/{page_no}',
                    headers=headers,
                )

                soup = Soup(response.text, "lxml")
                table_div = soup.find("div", attrs={"class": "table-responsive"})
                tbody = table_div.find("tbody")
                values = []
                for tr_tag in tbody.find_all("tr"):
                    values.append(tuple([td.text.strip() for td in tr_tag.find_all("td")]))

                if values:
                    insert_records(values)


            except:
                pass 
    except:
        pass
