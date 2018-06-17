# import pyprind
import time
from tqdm import tqdm

n = 100
timesleep = 5

# bar = pyprind.ProgBar(n, monitor=True)
# bar.update(0)

# for i in range(n):
#     time.sleep(timesleep) # your computation here
#     bar.update(10)
# print(bar)



pbar = tqdm(total=n)
for i in range(n):
    time.sleep(timesleep) # your computation here
    pbar.update(1)