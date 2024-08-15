import os
from psycopg2 import connect, OperationalError
from dotenv import load_dotenv

class Postgres_Create:
    def __init__(self):
        try:
            connection_params = Postgres_Create.get_connection_params()
            self.conn = connect(**connection_params)
            print("Verilənlər bazasına uğurla qoşuldu")
        except OperationalError as e:
            print(f"Bağlantı zamanı səhv baş verdi: {e}")

    @staticmethod
    def get_connection_params() -> dict:
        load_dotenv()  # .env faylının məzmununu yükləyir
        connection_params = {
            'dbname': os.getenv("DB_NAME"),
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASSWORD"),
            'host': os.getenv("DB_HOST"),
            'port': os.getenv("DB_PORT")
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
            print("user_data cədvəli yaradıldı")
        except Exception as e:
            print(f"user_data cədvəli yaradılarkən səhv baş verdi: {e}")
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
            print("video_data cədvəli yaradıldı")
        except Exception as e:
            print(f"video_data cədvəli yaradılarkən səhv baş verdi: {e}")
        finally:
            curr.close()

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Verilənlər bazası bağlantısı bağlandı")
