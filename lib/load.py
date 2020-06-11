import csv

def load(file_name):
  rows = []
  with open('data/S1_Dataset/'+file_name, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
      rows.append(row)