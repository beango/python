import matplotlib
matplotlib.use('Tkagg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt

fig1 = plt.figure()
plt.plot(range(10))
fig1.savefig('f1.png')
#plt.show()

fig2 = plt.figure()
plt.plot(range(3))
fig2.savefig("f2.png")
plt.show()
