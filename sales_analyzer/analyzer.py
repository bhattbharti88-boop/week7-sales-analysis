# analyzer.py - Sales Data Analysis
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import os

class SalesAnalyzer:
    """Analyzes sales data and generates insights"""
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load sales data from CSV file"""
        try:
            self.df = pd.read_csv(self.data_path)
            # Convert date column to datetime
            if 'order_date' in self.df.columns:
                self.df['order_date'] = pd.to_datetime(self.df['order_date'])
            print(f"Data loaded successfully. Shape: {self.df.shape}")
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def clean_data(self):
        """Clean the sales data"""
        if self.df is None:
            print("No data loaded")
            return
        
        # Remove duplicates
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates()
        removed = initial_rows - len(self.df)
        print(f"Removed {removed} duplicate rows")
        
        # Handle missing values
        missing_values = self.df.isnull().sum()
        if missing_values.sum() > 0:
            print("Missing values found:")
            print(missing_values[missing_values > 0])
            # Fill numerical columns with median
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if self.df[col].isnull().sum() > 0:
                    self.df[col].fillna(self.df[col].median(), inplace=True)
            # Fill categorical columns with mode
            categorical_cols = self.df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                if self.df[col].isnull().sum() > 0:
                    self.df[col].fillna(self.df[col].mode()[0], inplace=True)
    
    def calculate_basic_stats(self):
        """Calculate basic sales statistics"""
        if self.df is None:
            return {}
        
        stats = {
            'total_sales': self.df['total_amount'].sum(),
            'average_order': self.df['total_amount'].mean(),
            'total_orders': len(self.df),
            'unique_customers': self.df['customer_id'].nunique(),
            'unique_products': self.df['product_id'].nunique()
        }
        
        # Add date range if available
        if 'order_date' in self.df.columns:
            stats['date_range'] = {
                'start': self.df['order_date'].min().strftime('%Y-%m-%d'),
                'end': self.df['order_date'].max().strftime('%Y-%m-%d')
            }
        
        return stats
    
    def analyze_sales_by_category(self):
        """Analyze sales by product category"""
        if 'category' not in self.df.columns:
            return pd.DataFrame()
        
        category_sales = self.df.groupby('category').agg({
            'total_amount': 'sum',
            'quantity': 'sum',
            'order_id': 'count'
        }).rename(columns={'order_id': 'order_count'})
        
        category_sales = category_sales.sort_values('total_amount', ascending=False)
        return category_sales
    
    def analyze_monthly_trends(self):
        """Analyze monthly sales trends"""
        if 'order_date' not in self.df.columns:
            return pd.DataFrame()
        
        # Extract month-year
        self.df['month_year'] = self.df['order_date'].dt.to_period('M')
        
        monthly_sales = self.df.groupby('month_year').agg({
            'total_amount': 'sum',
            'quantity': 'sum',
            'customer_id': 'nunique',
            'order_id': 'count'
        }).rename(columns={
            'customer_id': 'unique_customers',
            'order_id': 'order_count'
        })
        
        # Calculate month-over-month growth
        monthly_sales['growth_rate'] = monthly_sales['total_amount'].pct_change() * 100
        
        return monthly_sales
    
    def create_visualizations(self, output_dir='output'):
        """Create visualizations of sales data"""
        os.makedirs(output_dir, exist_ok=True)

        # 1. Monthly sales trend
        monthly_data = self.analyze_monthly_trends()
        if not monthly_data.empty:
            plt.figure(figsize=(12, 6))
            x_labels = monthly_data.index.astype(str)
            plt.plot(x_labels, monthly_data['total_amount'], marker='o')
            plt.title('Monthly Sales Trend')
            plt.xlabel('Month')
            plt.ylabel('Total Sales ($)')
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f'{output_dir}/monthly_trend.png')
            plt.close()

        # 2. Sales by category
        category_data = self.analyze_sales_by_category()
        if not category_data.empty:
            plt.figure(figsize=(10, 6))
            category_data.head(10)['total_amount'].plot(kind='bar')
            plt.title('Top 10 Product Categories by Sales')
            plt.xlabel('Category')
            plt.ylabel('Total Sales ($)')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig(f'{output_dir}/category_sales.png')
            plt.close()

        # 3. Order value distribution
        plt.figure(figsize=(10, 6))
        plt.hist(self.df['total_amount'], bins=30, edgecolor='black', alpha=0.7)
        plt.title('Order Value Distribution')
        plt.xlabel('Order Value ($)')
        plt.ylabel('Frequency')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/order_distribution.png')
        plt.close()

        print(f"Visualizations saved to {output_dir}/")
    
    def generate_report(self, output_path='sales_report.xlsx'):
        """Generate comprehensive sales report"""
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Basic stats sheet
                stats = self.calculate_basic_stats()
                stats_df = pd.DataFrame([stats])
                stats_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Monthly trends sheet
                monthly_data = self.analyze_monthly_trends()
                if not monthly_data.empty:
                    monthly_data.to_excel(writer, sheet_name='Monthly Trends')
                
                # Category analysis sheet
                category_data = self.analyze_sales_by_category()
                if not category_data.empty:
                    category_data.to_excel(writer, sheet_name='Category Analysis')
                
                # Raw data sample sheet
                self.df.head(1000).to_excel(writer, sheet_name='Sample Data', index=False)
                
            print(f"Report generated: {output_path}")
            return True
        except Exception as e:
            print(f"Error generating report: {e}")
            return False

# ===========================
# MAIN EXECUTION BLOCK
# ===========================
if __name__ == "__main__":
    data_path = "data/sales_data.csv"  # adjust path if needed

    analyzer = SalesAnalyzer(data_path)
    analyzer.clean_data()

    # Basic stats
    stats = analyzer.calculate_basic_stats()
    print("\n=== Basic Sales Statistics ===")
    for k, v in stats.items():
        print(f"{k}: {v}")

    # Top 5 categories
    category_data = analyzer.analyze_sales_by_category()
    if not category_data.empty:
        print("\n=== Top 5 Product Categories by Sales ===")
        print(category_data.head(5))

    # Monthly trends
    monthly_data = analyzer.analyze_monthly_trends()
    if not monthly_data.empty:
        print("\n=== Monthly Sales Trends ===")
        print(monthly_data.head(5))  # show first 5 rows

    # Visualizations
    print("\nCreating visualizations...")
    analyzer.create_visualizations()
    print("Visualizations saved to 'output/' folder.")

    # Excel report
    print("\nGenerating Excel report...")
    analyzer.generate_report()
    print("Excel report saved as 'sales_report.xlsx'.")
