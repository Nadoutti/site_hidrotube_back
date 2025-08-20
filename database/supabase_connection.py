import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Defina SUPABASE_URL e SUPABASE_SERVICE_ROLE/ANON_KEY.")

def supabase() -> Client:
    # 👇 ATENÇÃO: é para **retornar** o client; não chame como função depois.
    return create_client(SUPABASE_URL, SUPABASE_KEY)
