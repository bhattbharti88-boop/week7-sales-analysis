import matplotlib.pyplot as plt
import os

def create_visualizations(df, output_dir='output'):
    os.makedirs(output_dir, exist_ok=True)

    # Monthly trend
    if 'order_date' in df.columns:
        df['month_year'] = df['order_date'].dt.to_period('M')
        monthly = df.groupby('month_year')['total_amount'].sum()
        plt.figure(figsize=(10, 5))
        plt.plot(monthly.index.astype(str), monthly.values, marker='o')
        plt.title("Monthly Sales Trend")
        plt.xlabel("Month")
        plt.ylabel("Total Sales")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/monthly_trend.png")
        plt.close()

    print(f"Visualizations saved to {output_dir}/")
