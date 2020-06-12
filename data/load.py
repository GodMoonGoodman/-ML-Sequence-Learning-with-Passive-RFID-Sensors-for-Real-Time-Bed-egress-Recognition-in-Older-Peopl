import csv
from .row_parser import origin_row_parser

DATA_PATH = 'data/S1_Dataset/'

def origin_data_load(file_name):
  rows = []
  with open(DATA_PATH + file_name, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
      rows.append(origin_row_parser(row))
  return rows