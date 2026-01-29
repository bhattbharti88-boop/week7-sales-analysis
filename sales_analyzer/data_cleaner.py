import numpy as np

def clean_data(df):
    if df is None:
        return
    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Fill missing numeric values with median
    for col in df.select_dtypes(include=[np.number]).columns:
        df[col].fillna(df[col].median(), inplace=True)

    # Fill missing categorical values with mode
    for col in df.select_dtypes(include=['object']).columns:
        df[col].fillna(df[col].mode()[0], inplace=True)

    print("Data cleaned successfully")
