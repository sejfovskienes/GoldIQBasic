import os 
from dotenv import load_dotenv
from supabase import create_client

load_dotenv(override=True)

supabase = create_client(
    os.getenv("SUPABASE_PROJECT_URL"), 
    os.getenv("SUPABASE_SERVICE_ROLE_KEY"),
)