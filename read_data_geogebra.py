

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

###This fnc is used to read csv file and filter the data based on the feature list in the csv file.
###Format of csv file:
###Name,Definition,Value
###Point B, ,"B = (1.84, 3.57)"
###Segment f,"Segment(A, B)",f = 4.48
###Arc c,"CircularArc(G, H, I)",c = 6.28
###List l1,"{c, d, f, g, h, i, j, k, J}",..
def filter_csv(file_path,result):
    # read csv file
    df = pd.read_csv(file_path)

    # search for List in Name column
    list_data = df[df['Name'].str.contains('List ', case=True, na=False)]

    feature_list = list_data['Definition'].values[0]

    #search for feature_list in Name column
    filtered_df = df[df['Name'].str.startswith(('Segment', 'Arc', 'Point')) & df['Name'].str.contains('| '.join(feature_list), case=True, na=False)]

    print("start")
    print(filtered_df)
    print("end")

    # Save feature to csv
    filtered_df.to_csv(result, index=False)


# Example usage
html_file = 'map1.html'  
output_csv_file = 'output.csv'
result_file = 'filtered_feature.csv'

html_table_to_csv(html_file, output_csv_file)

filter_csv(output_csv_file,result_file)