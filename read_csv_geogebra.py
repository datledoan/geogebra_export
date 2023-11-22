###This script is used to read csv file and filter the data based on the feature list in the csv file.
###Format of csv file:
###Name,Definition,Value
###Point B, ,"B = (1.84, 3.57)"
###Segment f,"Segment(A, B)",f = 4.48
###Arc c,"CircularArc(G, H, I)",c = 6.28
###List l1,"{c, d, f, g, h, i, j, k, J}",..

import pandas as pd

# path to csv file
file_path = 'Untitled.csv'

# read csv file
df = pd.read_csv(file_path)

# search for List in Name column
list_data = df[df['Name'].str.contains('List ', case=True, na=False)]

feature_list = list_data['Definition'].values[0]

#search for feature_list in Name column
filtered_df = df[df['Name'].str.contains('| '.join(feature_list), case=True, na=False)]

print("start")
print(filtered_df)
print("end")

# Save feature to csv
filtered_df.to_csv('filtered_feature.csv', index=False)
