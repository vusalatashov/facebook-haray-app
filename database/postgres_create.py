import os
import logging
from psycopg2 import connect, OperationalError

class Postgres_Create:
    def __init__(self):
        try:
            connection_params = Postgres_Create.get_connection_params()
            self.conn = connect(**connection_params)
            logging.info("connected to the database")
        except OperationalError as e:
            logging.error(f"Database connection error: {e}")

    @staticmethod
    def get_connection_params() -> dict:
        connection_params = {
            'dbname': 'postgres',
            'user': 'postgres',
            'password': 'postgres',
            'host': 'localhost',
            'port': '5430'
        }
        return connection_params

    def create_user_table(self) -> None:
        conn = self.conn
        create_query = """
        CREATE TABLE IF NOT EXISTS public.user_data
        (id               SERIAL PRIMARY KEY,
        fullname          varchar(255),
        username          varchar(30) UNIQUE,
        is_verified       BOOLEAN DEFAULT FALSE,
        video_count       INTEGER,
        follower_count    INTEGER,
        following_count   INTEGER,
        like_count        INTEGER,
        email             varchar(320),
        phone_number      varchar(15));
        CREATE INDEX IF NOT EXISTS idx_username ON public.user_data (username);
        """
        curr = conn.cursor()
        try:
            curr.execute(create_query)
            self.conn.commit()
            logging.info("create user_data table")
        except Exception as e:
            logging.error(f"Error creating user_data table: {e}")
        finally:
            curr.close()

    def create_video_table(self) -> None:
        conn = self.conn
        create_query = """
        CREATE TABLE IF NOT EXISTS public.video_data
        (id              BIGSERIAL PRIMARY KEY,
        url              varchar(255) NOT NULL UNIQUE,
        play_count       BIGINT,
        description      varchar(2200),
        share_date       DATE,
        share_count      INTEGER,
        like_count       INTEGER,
        comment_count    INTEGER,
        user_id          INT REFERENCES public.user_data (id),
        is_downloaded    BOOLEAN DEFAULT FALSE);
        CREATE INDEX IF NOT EXISTS idx_url ON public.video_data (url);
        """
        curr = conn.cursor()
        try:
            curr.execute(create_query)
            self.conn.commit()
            print("create video_data table")
        except Exception as e:
            print(f"Error creating video_data table: {e}")
        finally:
            curr.close()

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
