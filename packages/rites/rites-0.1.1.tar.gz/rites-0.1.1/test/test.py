import time
from rites import chrono as ch

c = ch.Chrono()

c.stopwatch()

time.sleep(0.002)

c.stopwatch()

print(c.get_stopwatch_tabs())