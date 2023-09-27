from tqdm import tqdm
import sys
import traceback
from constant import RANGE_START, RANGE_END, PROFESSION_PREFIXES
from fetcher import fetch_hcpc_record
from db_insert import insert_records

import concurrent.futures


for prefix in PROFESSION_PREFIXES:
    print(f"=============== parsing started for profession - {prefix} =============", flush=True)
    batch = []
    total_iterations = RANGE_END - RANGE_START
    progress_bar = tqdm(total=total_iterations)

    for i in range(RANGE_START, RANGE_END):
        try:
            query_id = prefix + str(i)
            batch.append(query_id)
            if len(batch) < 100:
                continue

            response_batch = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
                future_to_url = {executor.submit(fetch_hcpc_record, query_id, prefix): query_id for query_id in batch}
                for future in concurrent.futures.as_completed(future_to_url):
                    query_id = future_to_url[future]
                    try:
                        response_data = future.result()
                        if response_data:
                            response_batch.append(response_data)
                    except Exception as exc:
                        print(f'{query_id} generated an exception: {exc}')
            if response_batch:
                insert_records(response_batch)

            progress_bar.update(len(batch))
            sys.stdout.flush()
            batch = []
        except Exception as e:
            print("[ERROR] failed for ", prefix, "---", i, flush=True)
            print(traceback.format_exc(), flush=True)
    
    try:
        response_batch = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
            future_to_url = {executor.submit(fetch_hcpc_record, query_id, prefix): query_id for query_id in batch}
            for future in concurrent.futures.as_completed(future_to_url):
                query_id = future_to_url[future]
                try:
                    response_data = future.result()
                    if response_data:
                        response_batch.append(response_data)
                except Exception as exc:
                    print(f'{query_id} generated an exception: {exc}', flush=True)
        if response_batch:
            insert_records(response_batch)
    except:
        pass

    progress_bar.update(len(batch))
    sys.stdout.flush()
    progress_bar.close()


