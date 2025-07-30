from supabase import create_client

SUPABASE_URL = "https://qpgtqtgysrctqisorwxv.supabase.co"
SUPABASE_KEY = "sb_secret_cX_9D-4tszosM3y0t6WSxA_w8oNWg6e"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
