import numpy as np

def acceleration(af, av, al):
  v = np.array([af, av, al])
  return np.linalg.norm(v)

def acceleration_coef(af, av, al, alpha, beta, gamma):
  a = 1 if alpha == None else pow(alpha, 2)
  b = 1 if beta == None else pow(beta, 2)
  c = 1 if gamma == None else pow(gamma, 2)

  v = np.array([af * a, av * b, al * c])
  return np.linalg.norm(v)