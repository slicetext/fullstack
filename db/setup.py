import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

password: str = os.getenv("PASSWORD")

conn_str: str = f"postgresql://project_user:{password}@localhost:5432/project_db"

with psycopg.connect(conn_str) as conn:
    with conn.cursor() as cur:
        # # Make IP Addresses
        # # Wired Addresses
        # # 10.0 to 10.255
        # for i in range(0, 256):
        #     for j in range(0, 256):
        #         for k in range(0, 256):
        #             address: str = f"10.{i}.{j}.{k}"
        #             cur.execute(
        #                     f"INSERT INTO ip (ip_address, owner_id, description) VALUES ('{address}', NULL, NULL);"
        #             )
        # # 192.168.111.0 to 192.168.111.255
        # for i in range(0, 256):
        #     address: str = f"192.168.111.{i}"
        #     cur.execute(
        #             f"INSERT INTO ip (ip_address, owner_id, description) VALUES ('{address}', NULL, NULL);"
        #     )
        #
        # Reserve blacklisted addresses
        blacklisted: dict[str, str] = {
                "10.0.0.1" : "Firewall",
                "192.168.111.254" : "Cryan Framework",
                "192.168.111.253" : "Gormes Framework",
                "192.168.111.255" : "Broadcast",
                "10.0.0.2" : "Alpha Cluster",
                # 10.0.30.0 - 10.0.30.255 Gormes reserved
                "10.0.255.0" : "Delphi (AI)",
                "10.0.255.1" : "Cassandra (AI)",
                "10.0.255.2" : "Sybil (AI)"
        }
        # Gormes reserved
        for i in range(0, 256):
            blacklisted[f"10.0.30.{i}"] = "Gormes reserved"

        # Reserved user
        cur.execute(
                f"INSERT INTO owner (name, password) VALUES ('EPIC Reserved', NULL);"
        )

        # Get EPIC Reserved id
        cur.execute("SELECT owner_id FROM owner WHERE name='EPIC Reserved';")
        reserved_id = cur.fetchone()[0]
        print(reserved_id)

        # Enter reserved addresses
        for address, description in blacklisted.items():
            cur.execute(
                    f"INSERT INTO ip (ip_address, owner_id, description) VALUES ('{address}', {reserved_id},\'{description}\');"
            )
