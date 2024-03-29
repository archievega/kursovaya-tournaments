from supabase import create_client, Client
from src.config import settings


async def get_supabase_client() -> Client:
    supabase_client: Client = create_client(settings.SUPABASE_URL,
                                            settings.SUPABASE_KEY)
    return supabase_client
