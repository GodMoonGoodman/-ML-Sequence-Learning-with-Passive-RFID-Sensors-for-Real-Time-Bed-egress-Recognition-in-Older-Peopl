from lib.plot import color_shape
from data.load import origin_data_load as load_data, DATA_PATH
from lib.const import *
from lib.median import median
from lib.hypothesis import acceleration_coef

from os import listdir
import sys
import matplotlib.pyplot as plt

activity_labels = [LABEL_LYING, LABEL_SIT_ON_BED, LABEL_SIT_ON_CHAIR, LABEL_AMBULATING]

def draw_chart(file_name, save = False):
  # x - axis data
  # key is label
  # value is array of time(n)
  x = {
    '1': [],
    '2': [],
    '3': [],
    '4': [],
  }
  # y - axis data
  # key is label
  # value is array of acc(n)
  y = {
    '1': [],
    '2': [],
    '3': [],
    '4': []
  }

  # used for calculating alpha, beta, gamma coefficient
  acceleration_of_lying =  {
    'a_f': [],
    'a_v': [],
    'a_l': []
  }

  # alpha, beta, gamma coefficient
  median_acceleration_of_lying = {
    'a_f': 1,
    'a_v': 1,
    'a_l': 1
  }

  # import dataset
  rows = load_data(file_name)
  
  # collect acceleraton datas of only lying activity
  for row in list(filter(lambda row: row['label'] == LABEL_LYING, rows)):
    acceleration_of_lying['a_f'].append(row['a_f'])
    acceleration_of_lying['a_v'].append(row['a_v'])
    acceleration_of_lying['a_l'].append(row['a_l'])

  # calculate coefficient, median of each axis acceleration
  median_acceleration_of_lying['a_f'] = median(acceleration_of_lying['a_f'])
  median_acceleration_of_lying['a_v'] = median(acceleration_of_lying['a_v'])
  median_acceleration_of_lying['a_l'] = median(acceleration_of_lying['a_l'])

  for row in rows:
    label = str(row['label'])
    time = row['time']
    af = row['a_f']
    av = row['a_v']
    al = row['a_l']
    acc = acceleration_coef(
      af = af,
      av = av,
      al = al,
      alpha = median_acceleration_of_lying['a_f'],
      beta = median_acceleration_of_lying['a_v'],
      gamma = median_acceleration_of_lying['a_l']
    )

    # x-axis : time sequence
    x[label].append(time)
    # y-axis : improved acceleration
    y[label].append(acc)

  plt.xlabel('time')
  plt.ylabel('acc')
  plt.title('data: {}'.format(file_name))

  for label in [str(label) for label in activity_labels]:
    plt.plot(x[label], y[label], color_shape[label])

  if save:
    SAVE_PATH = 'figures/hypothesis2/'
    file_path = '{}{}.png'.format(SAVE_PATH, file_name)
    plt.savefig(file_path, dpi=300)
    plt.clf()

    print('{} was saved'.format(file_path))
  else:
    plt.show()


if __name__ == "__main__":
  cmd = sys.argv[1]
  if cmd == '-d':
    file_name = sys.argv[2]
    draw_chart(file_name, save = '-s' in sys.argv)
  elif cmd == '-a':
    file_names = [f for f in listdir(DATA_PATH)]
    for file_name in file_names:
      draw_chart(file_name, save = '-s' in sys.argv)
