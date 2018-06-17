import pyprind
import time

n = 100
timesleep = 0.2

bar = pyprind.ProgBar(n, monitor=True)
for i in range(n):
    time.sleep(timesleep) # your computation here
    bar.update(10)
print(bar)