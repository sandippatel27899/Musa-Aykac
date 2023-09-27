
# from details_page_links import hyperlinks
from input_reader import hyperlinks
from fetcher import fetch_url
from details_page_parser import extract_user_info
from tqdm import tqdm
from db_writer import insert_records

def main():
    user_info_batch = []

    for link in tqdm(hyperlinks):
        response_text = fetch_url(link)
        if not response_text:
            continue

        user_info = extract_user_info(response_text)
        if not user_info:
            continue
        user_info["profile_link"] = link

        user_info_batch.append(user_info)
        
        if len(user_info_batch) > 100:
            try:
                insert_records(user_info_batch)
                user_info_batch = []
            except Exception as e:
                print(e)
                pass
    
    if user_info_batch:
        try:
            insert_records(user_info_batch)
        except Exception as e:
            print(e)
            pass

        
if __name__ == "__main__":
    main()
    