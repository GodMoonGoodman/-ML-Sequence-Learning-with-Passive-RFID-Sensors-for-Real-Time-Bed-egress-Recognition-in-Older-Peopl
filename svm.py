from lib.plot import color_shape
from data.load import origin_data_load as load_data, DATA_PATH
from lib.const import *
from lib.median import median
from lib.hypothesis import acceleration_coef

from os import listdir
import sys
import matplotlib.pyplot as plt

from sklearn.svm import SVC
import numpy as np

activity_labels = [LABEL_LYING, LABEL_SIT_ON_BED, LABEL_SIT_ON_CHAIR, LABEL_AMBULATING]

def draw_chart(file_name, save = False):
  # x - axis data
  x = []
  # y - axis data
  y = []

  acceleration_of_lying =  {
    'a_f': [],
    'a_v': [],
    'a_l': []
  }

  median_acceleration_of_lying = {
    'a_f': 1,
    'a_v': 1,
    'a_l': 1
  }

  rows = load_data(file_name)
  
  # only lying
  for row in list(filter(lambda row: row['label'] == LABEL_LYING, rows)):
    acceleration_of_lying['a_f'].append(row['a_f'])
    acceleration_of_lying['a_v'].append(row['a_v'])
    acceleration_of_lying['a_l'].append(row['a_l'])

  median_acceleration_of_lying['a_f'] = median(acceleration_of_lying['a_f'])
  median_acceleration_of_lying['a_v'] = median(acceleration_of_lying['a_v'])
  median_acceleration_of_lying['a_l'] = median(acceleration_of_lying['a_l'])

  before_row = None

  train_points = []
  labels = []
  
  classifier = SVC(kernel = 'linear')

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

    row['acc'] = acc

    if before_row != None:
      time_gap = row['time'] - before_row['time']
      acc_gap = abs(row['acc'] - before_row['acc'])

      if time_gap > MIN_TIME_GAP:
        x.append(acc_gap)
        y.append(acc)

        train_points.append([acc_gap, acc])
        labels.append('r' if row['label'] == LABEL_LYING else 'y')

    before_row = row
  try:
    classifier.fit(train_points, labels)
  except ValueError:
    return

  predicts = classifier.predict(train_points)
  success_count = 0
  for i, v in enumerate(predicts):
    if v == labels[i]:
      success_count += 1

  accuracy = round(success_count / len(predicts), 2)

  plt.scatter(x, y, c=labels, s=30, cmap=plt.cm.Paired, marker="x")
  ax = plt.gca()
  xlim = ax.get_xlim()
  ylim = ax.get_ylim()
  xx = np.linspace(xlim[0], xlim[1], 30)
  yy = np.linspace(ylim[0], ylim[1], 30)
  YY, XX = np.meshgrid(yy, xx)
  xy = np.vstack([XX.ravel(), YY.ravel()]).T
  Z = classifier.decision_function(xy).reshape(XX.shape)
  ax.contour(XX, YY, Z, colors='k', levels=[-1,0,1], alpha=0.5, linestyles=['--', '-', '--'])

  plt.xlabel('time')
  plt.ylabel('acc')
  plt.title('data: {}, accuracy: {}'.format(file_name, str(accuracy * 100) + '%'))

  if save:
    SAVE_PATH = 'figures/result/'
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
