from lib.plot import color_shape
from data.load import origin_data_load as load_data, DATA_PATH
from lib.const import *
from lib.hypothesis import acceleration

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

  rows = load_data(file_name)
  
  for row in rows:
    label = str(row['label'])
    time = row['time']
    af = row['a_f']
    av = row['a_v']
    al = row['a_l']
    acc = acceleration(af, av, al)

    x[label].append(time)
    y[label].append(acc)

  plt.xlabel('time')
  plt.ylabel('acc')
  plt.title('data: {}'.format(file_name))

  for label in [str(label) for label in activity_labels]:
    plt.plot(x[label], y[label], color_shape[label])

  if save:
    SAVE_PATH = 'figures/hypothesis1/'
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
