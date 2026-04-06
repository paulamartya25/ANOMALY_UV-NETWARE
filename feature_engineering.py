import pandas as pd

def process(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    visitor_stats = df.groupby("visitor_id").agg({
        "session_id": "count",
        "session_duration": "mean",
        "clicks": "mean",
        "converted": "mean"
    }).rename(columns={
        "session_id": "user_total_sessions",
        "session_duration": "user_avg_duration",
        "clicks": "user_avg_clicks",
        "converted": "user_conversion_rate"
    })

    df = df.merge(visitor_stats, on="visitor_id", how="left")

    df['sessions_per_user'] = df.groupby("visitor_id")['session_id'].transform('count')
    df['hour'] = df['timestamp'].dt.hour
    df['click_rate'] = df['clicks'] / (df['session_duration'] + 1)
    df['events_per_click'] = df['events_count'] / (df['clicks'] + 1)

    return df