# parse columns of each row
# this is for raw data, new features were not included
def origin_row_parser(row):
  return {
    # Time in seconds
    'time': float(row[0]),
    # Acceleration reading in G for frontal axis
    'a_f': float(row[1]),
    # Acceleration reading in G for vertical axis
    'a_v': float(row[2]),
    # Acceleration reading in G for lateral axis
    'a_l': float(row[3]),
    # ID of antena reading sensor
    # not used in this project
    'id': int(row[4]),
    # Received signal strength indicator (RSSI)
    # not used in this project
    'rssi': float(row[5]),
    # Phase
    # not used in this project
    'phase': float(row[6]),
    # Frequancy
    # not used in this project
    'frequancy': float(row[7]),
    # Label of activity
    # 1: sit on bed
    # 2: sit on chair
    # 3: lying
    # 4: ambulating
    'label': int(row[8])
  }

def new_feature_row_parser(row):
  return {
    # Time in seconds
    'time': float(row[0]),
    # X of new feature
    'xn': float(row[1]),
    # Y of new feature
    'xn': float(row[2]),
    # Label of activity
    # 1: sit on bed
    # 2: sit on chair
    # 3: lying
    # 4: ambulating
    'label': int(row[3])
  }