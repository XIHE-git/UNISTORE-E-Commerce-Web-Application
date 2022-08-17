import requests
from pandas import json_normalize
from cs50 import SQL

"""
read_process_university --- A function to read information (address and name) about U.S. colleges and universities and generate a pandas dataframe.

@return:
    df_university --- A pandas dataframe containing address and name columns
"""
def read_process_university():
    # API URL for U.S. universities and colleges
    URL_API = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-colleges-and-universities&q=&lang=EN&rows=7000"
    data = requests.get(URL_API)
    # load into JSON
    json_data = data.json()
    # Read JSON into Pandas Dataframe
    df_university = json_normalize(json_data['records'])
    # Drop rows with the same address
    df_university.drop_duplicates(subset ="fields.address", keep = False, inplace = True)
    # Keep longitude, latitude, name, and address columns
    df_university = df_university[['fields.name','fields.address']]
    # Rename columns
    df_university.rename(columns = {"fields.name": "name","fields.address" : "address"}, inplace = True)
    # Drop columns
    df_university = df_university[['name', 'address']]
    return df_university

if __name__ == "__main__":
    db = SQL("sqlite:///SecondHandTransaction.db")
    # Create university SQL table
    db.execute("""Create table if not exists university
    (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    address TEXT NOT NULL
    )""")

    # Update information into table
    university_df = read_process_university()
    for index, row in university_df.iterrows():
        db.execute("INSERT INTO university(name, address) VALUES (?, ?)",
                    row['name'], row['address'])