import numpy as np
x=np.array([i for i in np.arange(0,6,1)])
y=np.array([i for i in np.arange(0,6)])
print x,y
X,Y= np.meshgrid(x,y)
print X
