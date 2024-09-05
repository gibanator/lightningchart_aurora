import requests


url1 = "https://services.swpc.noaa.gov/products/solar-wind/mag-1-day.json"
url2 = "https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json"

data1 = requests.get(url1).json()
data2 = requests.get(url2).json()

merged_list = [sublist1 + sublist2 for sublist1, sublist2 in zip(data1, data2)]
file_path = 'data/output.csv'

# Write the merged list to the file
with open(file_path, 'w') as file:
    for sublist in merged_list:
        l = [str(item) if item is not None else '' for item in sublist]
        string_to_write = ','.join(l)
        file.write(string_to_write + "\n")