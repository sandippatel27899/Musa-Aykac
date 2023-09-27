import psycopg2
import sshtunnel
import os
import traceback
import json
from tqdm import tqdm
import time

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

postgres_hostname = (
    "pythonite-3360.postgres.pythonanywhere-services.com"  # You will have your own here
)
postgres_host_port = 13360  #  You will have your own port here


def get_insert_query_values(batch_record):
    values = []
    for record in batch_record:
        name = record.get("Name", "") or ""
        registration_number = record.get("Registration number","") or ""
        status = record.get("Status","") or ""
        period = record.get("Period","") or ""
        modalities = record.get("Modalities","") or ""
        location = record.get("Location","") or ""

        values.append((name, registration_number, status, period, modalities, location))

    return values

def insert_records(batch_records):
    with sshtunnel.SSHTunnelForwarder(
        ("ssh.pythonanywhere.com"),
        ssh_username="pythonite",
        ssh_password="&L3en@M-9jE9,A7",
        remote_bind_address=(postgres_hostname, postgres_host_port),
    ) as tunnel:
        connection = psycopg2.connect(
            user="super",
            password="W2s4ZgxQEM2yQ7qx",
            host="127.0.0.1",
            port=tunnel.local_bind_port,
            database="production",
        )
        cursor = connection.cursor()

        print("connection successful, db insert starts...")
        try:
            values = get_insert_query_values(batch_records)
            cursor.executemany(
                """
                    INSERT INTO hcpc (name, registration_number, status, period, modalities, location)
                    VALUES(%s,%s,%s,%s,%s, %s)
                    ON CONFLICT (registration_number)
                    DO UPDATE SET
                    name = EXCLUDED.name,
                    status = EXCLUDED.status,
                    period = EXCLUDED.period,
                    modalities = EXCLUDED.modalities,
                    location = EXCLUDED.location;
                """,
                  values)
        except Exception as e:
            print(f"failed to insert,  Exception {e}" )
            print(traceback.format_exc())

        try:
            connection.commit()
            connection.close()
        except:
            pass
        print("connection closed ..")
        print("db inserted successfully ..")
