import pandas as pd

def load_data(path):
    try:
        df = pd.read_csv(path)
        if 'order_date' in df.columns:
            df['order_date'] = pd.to_datetime(df['order_date'])
        print(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
