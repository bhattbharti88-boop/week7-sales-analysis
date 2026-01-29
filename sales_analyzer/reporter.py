import pandas as pd

def generate_report(df, output_path='sales_report.xlsx'):
    try:
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Data', index=False)
        print(f"Report generated: {output_path}")
    except Exception as e:
        print(f"Error generating report: {e}")
