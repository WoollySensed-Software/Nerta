from supabase import create_client

from Nerta.settings import DB_URL, DB_KEY


class DatabaseModule:

    def __init__(self):
        self.url = DB_URL
        self.key = DB_KEY
        self.db = create_client(self.url, self.key)
    
    def insert(self, table: str, request: dict | list):
        self.db.table(table).insert(request).execute()

    def get_auth_data(self, table: str, login: str):
        return (self.db.table(table)
                .select('login, password, access_status')
                .eq('login', login)
                .execute())
    
    def get_user_settings(self, table: str, login: str):
        return (self.db.table(table)
                .select('homep_links_long, homep_contracts_long, speakers_flag',)
                .eq('login', login)
                .execute())
    
    def upd_user_settings(self, table: str, login: str, request: dict):
        self.db.table(table).update(request).eq('login', login).execute()
