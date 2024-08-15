from app.postgres_create import Postgres_Create


class PostgresVideo:
    def __init__(self):
        self.db = Postgres_Create()

    def save_video(self, video_url, video_id):
        conn = self.db.conn
        insert_query = """
        INSERT INTO public.post_data(url,platform,unique_id)
        VALUES(%s, 'facebook', %s)
        ON CONFLICT (url) DO NOTHING;
        """
        curr = conn.cursor()
        try:
            curr.execute(insert_query, (video_url, video_id))
            conn.commit()
            print(f"{video_url} added")
        except Exception as e:
            print(f"Error occurred while adding {video_url}: {e}")
            conn.rollback()
        finally:
            curr.close()

    def save_user_url(self, user_url, fullname, follower_count, following_count, video_url):
        if user_url == 'N/A' or "watch" in user_url:
            return
        conn = self.db.conn
        insert_query = """
        INSERT INTO public.user_data(profile_url, fullname, follower_count, following_count, platform)
        VALUES(%s, %s, %s, %s, 'facebook')
        ON CONFLICT (profile_url) DO NOTHING;
        """
        curr = conn.cursor()
        try:
            curr.execute(insert_query, (user_url, fullname, follower_count, following_count))
            conn.commit()
            print(f"{user_url} added")
            self.find_user_id(user_url, video_url)
        except Exception as e:
            print(f"Error occurred while adding {user_url}: {e}")
        finally:
            curr.close()

    def save_video_info(self, like_count, comment_count, description, video_url):
        conn = self.db.conn
        update_query = """
        UPDATE public.post_data
        SET
            description = %s,
            like_count = %s,
            comment_count = %s
        WHERE url = %s
        """
        curr = conn.cursor()
        try:
            curr.execute(update_query, (description, like_count, comment_count, video_url))
            conn.commit()
            print(f"{video_url} info updated")
        except Exception as e:
            print(f"Error occurred while updating {video_url} info: {e}")
            conn.rollback()
        finally:
            curr.close()

    def find_urls(self):
        conn = self.db.conn
        select_query = """
        SELECT url
        FROM public.post_data
        WHERE like_count IS NULL and platform = 'facebook'
        """
        curr = conn.cursor()
        try:
            curr.execute(select_query)
            urls = curr.fetchall()
            return urls
        except Exception as e:
            print(f"Error occurred while fetching URLs: {e}")
        finally:
            curr.close()

    def update_video_user_data_id(self, video_url, user_id):
        conn = self.db.conn
        update_query = """
        UPDATE public.post_data
        SET user_data_id = %s
        WHERE url = %s
        """
        curr = conn.cursor()
        try:
            curr.execute(update_query, (user_id, video_url))
            conn.commit()
            print(f"{video_url} user id updated")
        except Exception as e:
            print(f"Error occurred while updating {video_url} user id: {e}")
            conn.rollback()
        finally:
            curr.close()

    def find_user_id(self, user_url, video_url):
        conn = self.db.conn
        select_query = """
        SELECT id
        FROM public.user_data
        WHERE profile_url = %s
        """
        curr = conn.cursor()
        try:
            curr.execute(select_query, (user_url,))
            user_id = curr.fetchone()
            self.update_video_user_data_id(video_url, user_id)
        except Exception as e:
            print(f"Error occurred while fetching user ID: {e}")
        finally:
            curr.close()

    def delete_video(self, video_url):
        conn = self.db.conn
        delete_query = """
        DELETE FROM public.post_data
        WHERE url = %s
        """
        curr = conn.cursor()
        try:
            curr.execute(delete_query, (video_url,))
            conn.commit()
            print(f"{video_url} deleted")
        except Exception as e:
            print(f"Error occurred while deleting {video_url}: {e}")
            conn.rollback()
        finally:
            curr.close()
