import numpy as np 
import matplotlib.pyplot as plt

train = np.loadtxt(r"./ML_Math/click.csv", delimiter=",",skiprows=1)
train_x = train[:,0]
train_y = train[:,1]

# plt.plot(train_x,train_y,"o")
# plt.show()