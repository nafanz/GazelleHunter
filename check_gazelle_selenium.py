import time
import misc


driver = misc.web_surfing()

for tracker in misc.trackers.items():
    driver.get(tracker[1])
    time.sleep(5)
    driver.save_screenshot(f'{tracker[0]}.png')