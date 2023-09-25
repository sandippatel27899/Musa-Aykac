import traceback
from bs4 import BeautifulSoup as Soup


def get_info_from_table(table):
    records = {}
    tbody = table.find("tbody")
    t_rows = tbody.find_all("tr")
    
    for row in t_rows:
        title = row.find("td").text.strip()
        date = row.find("td", attrs={"class": "text-right"}).text.strip()
        records[title] = date
    
    return records

def extract_user_info(page_source):
    user_info = {}
    try:
        soup = Soup(page_source, "lxml")
        practitioner_tag = soup.find("div", attrs={"class": "practitioner"})
        tables = practitioner_tag.find_all("table")

        metadata_tag = practitioner_tag.find("div", attrs={"class": "practitioner-meta"})

        name, location, expiry_date, registration_status = "", "", "", ""
        for record in metadata_tag.find_all("dl"):
            try:
                if record.dt.text.strip() == "Name":
                    name = record.dd.text.strip()
            except:
                pass
            try:
                if record.dt.text.strip() == "Geographical locations":
                    location = record.dd.text.strip()
            except:
                pass
            try:
                if record.dt.text.strip() == "Expiry date":
                    expiry_date = record.dd.text.strip()
            except:
                pass

        try:
            registration_status = practitioner_tag.find("div", attrs={"class": "practitioner-status"}).find("p", attrs={"class": "lead"}).text.strip()
        except:
            pass
        user_info["name"] = name
        user_info["location"] = location
        user_info["expiry_date"] = expiry_date
        user_info["registration_status"] = registration_status
        
    
        for table in tables:
            try:
                header = table.find("th").text
            except:
                continue
            if header == "Register entry":
                records = get_info_from_table(table)
                user_info["register_entry"] = records
                
            
            if header == "Recorded qualifications":
                records = get_info_from_table(table)
                user_info["recorded_qualifications"] = records

        
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    
    return user_info
            