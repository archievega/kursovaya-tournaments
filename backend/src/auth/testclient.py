from supabase import create_client, Client


async def get_supabase_client() -> Client:
    supabase_client: Client = create_client(settings.SUPABASE_URL,
                                            settings.SUPABASE_KEY)
    return supabase_client

SB_URL = "http://localhost:8000"
SB_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyAgCiAgICAicm9sZSI6ICJhbm9uIiwKICAgICJpc3MiOiAic3VwYWJhc2UtZGVtbyIsCiAgICAiaWF0IjogMTY0MTc2OTIwMCwKICAgICJleHAiOiAxNzk5NTM1NjAwCn0.dc_X5iR_VP_qT0zsiyj_I_OZ2T9FtRU2BBNWN8Bu4GE"
sb = create_client(SB_URL,SB_KEY)
res = sb.auth.sign_up({
  'email': 'arslan.semenoff@gmail.com',
  'password': 'example-password'}
)