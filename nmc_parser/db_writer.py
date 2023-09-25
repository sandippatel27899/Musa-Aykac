import psycopg2
import sshtunnel
import traceback
import json

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

postgres_hostname = (
    "pythonite-3360.postgres.pythonanywhere-services.com"  # You will have your own here
)
postgres_host_port = 13360  #  You will have your own port here


def get_insert_query_values(batch_record):
    values = []
    for record in batch_record:
        name = record.get("name", "") or ""
        location = record.get("location", "") or ""
        expiry_date = record.get("expiry_date", "") or ""
        registration_status = record.get("registration_status","") or ""
        recorded_qualifications = json.dumps(record.get("recorded_qualifications", {}) or {})
        register_entry = json.dumps(record.get("register_entry", {}) or {})
        profile_link = record.get("profile_link","") or ""

        values.append((name, location, expiry_date, registration_status, recorded_qualifications, register_entry, profile_link))

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
            cursor.executemany("""
                    INSERT INTO nmc (name, location, expiry_date, registration_status, recorded_qualifications, register_entry, profile_link)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (profile_link) DO UPDATE
                    SET
                        location = EXCLUDED.location,
                        expiry_date = EXCLUDED.expiry_date,
                        registration_status = EXCLUDED.registration_status,
                        recorded_qualifications = EXCLUDED.recorded_qualifications,
                        register_entry = EXCLUDED.register_entry,
                        profile_link = EXCLUDED.profile_link
                """, values)
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
