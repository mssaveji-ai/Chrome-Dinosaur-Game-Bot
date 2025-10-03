import pyautogui as gui
import time

print("5 ثانیه وقت داری موس رو ببری روی نقطه موردنظر...")
time.sleep(5)
x, y = gui.position()
print("مختصات نقطه:", x, y)

