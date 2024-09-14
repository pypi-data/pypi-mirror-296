from epidemmo import Standard, ModelIO
from matplotlib import pyplot as plt

sirs = Standard.get_SIRS_builder().build()
io = ModelIO()

io.save(sirs, 'test.json')
sirs2 = io.load('test.json')

r = sirs2.start(300)
r.plot()

plt.show()