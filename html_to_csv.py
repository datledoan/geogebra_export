import pandas as pd

# Function to convert HTML table to CSV
def html_table_to_csv(html_filename, csv_filename):
    # Read HTML file into a list of DataFrames
    tables = pd.read_html(html_filename)

    if not tables:
        print("No tables found in the HTML file.")
        return

    # Assuming the first table is the target table
    target_table = tables[0]

    # Save the table to a CSV file
    target_table.to_csv(csv_filename, index=False, encoding='utf-8')

# Example usage
html_file = 'nic_1.html'  # Replace with the path to your HTML file
output_csv_file = 'output.csv'

html_table_to_csv(html_file, output_csv_file)