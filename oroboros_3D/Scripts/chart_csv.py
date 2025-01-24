import bpy
import os
import csv

HOME = os.path.expanduser("~").replace('\\', '/') if os.name == 'nt' else os.path.expanduser("~")
MINTING = 'minting_tokenomics'
EPHEMERAL = 'ephemeral_tokenomics'
CSV = MINTING+'.csv'
CSV_PATH = os.path.join(HOME, 'Documents', 'oroboros_3D', CSV)

def read_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
        return data
    
def csv_column(data, col):
    array = []
    for y, row in enumerate(data):
        if y == 0:
            continue
        array.append(row[col])
        
    return array

def csv_column_header(data, col):
    array = []
    for y, row in enumerate(data):
        if y == 0:
            return row[col]


data = read_csv(CSV_PATH)

Adjusted_XRO_To_ICP_Header = csv_column_header(data, 9)
Adjusted_XRO_To_ICP_ExchangeRate = csv_column(data, 9)

Adjusted_XRO_To_ETH_Header = csv_column_header(data, 16)
Adjusted_XRO_To_ETH_ExchangeRate = csv_column(data, 16)

Adjusted_XRO_To_BTC_Header = csv_column_header(data, 21)
Adjusted_XRO_To_BTC_Exchange_Rate = csv_column(data, 21)

One_XRO_In_ICP = csv_column(data, 29)

print(CSV_PATH)
print(os.path.isfile(CSV_PATH))

print(Adjusted_XRO_To_ETH_Header)