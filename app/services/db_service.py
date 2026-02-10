from app.core.supabase import supabase

#--- preidiction service
def save_prediction(prediction_data: dict) -> None:
    supabase.table("predictions").insert(prediction_data).execute()

def get_latest_prediction() -> dict:
    latest_prediction_response = supabase.table("predictions").select("*") \
    .order("date_created", desc=True).limit(1).execute()
    return latest_prediction_response.data[0]

#--- metrics service
def get_model_metrics() -> list[dict]:
    metrics = supabase.table("model_metrics").select("*") \
    .order("trained_at", desc=True).limit(10).execute()
    return metrics.data