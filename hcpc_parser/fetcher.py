import requests
from bs4 import BeautifulSoup as Soup



def parse_hcpc_record(response_text):
    data_dict = {}
    if "No results returned" in response_text:
        return data_dict

    soup = Soup(response_text, "lxml")
    table = soup.find("table")
    all_rows = table.find_all("tr")
    for row in all_rows:
        data_lines = row.find_all("td")
        tag = data_lines[0].text.strip()
        value = data_lines[1].text.strip()
        data_dict[tag] = value

    return data_dict



def fetch_hcpc_record(query_id, profession):
    headers = {
        'authority': 'www.hcpc-uk.org',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'referer': 'https://www.hcpc-uk.org/check-the-register/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }

    cookies = {
        'cf_clearance': 'vz_2wmjBM0Hd8AZuiM.7k03TWqMasdYazxwG6dAaetw-1694776778-0-1-1157a58.1590852f.561425b8-250.0.0',
    }

    params = {
        'query': query_id,
        'profession': profession.strip("0"),
    }

    response = requests.get(
        'https://www.hcpc-uk.org/check-the-register/professional-registration-detail/',
        params=params,
        headers=headers,
        cookies=cookies
    )

    return parse_hcpc_record(response.text)
