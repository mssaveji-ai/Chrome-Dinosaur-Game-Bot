import pygetwindow as gw
from PIL import ImageGrab
import time
from pynput.keyboard import Controller, Key
import math

''' 
فایل دیگری که قرار دادم برای پیدا کردن مختصات نقطه مورد نظر در صفحه می باشد 
قبل از ران کردن پروژه به این صفحه بروید
chrome://dino/
 بعد از ران کردن پروژه در صورتیکه پیام شروع ربات آمد به صفحه گفته شده دوباره بروید و اسپیس را بزنید
'''
keyboard_ctrl = Controller()  # برای فشردن کلیدها در صفحه کلید

# Chrome گرفتن اسکرین‌شات از پنجره
def get_chrome_screenshot():
    try:
        win = gw.getWindowsWithTitle("Google Chrome")[0]
        x, y, w, h = win.left, win.top, win.width, win.height
        img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        return img, w
    except IndexError:
        print("❌ Google Chrome window not found! Please open Chrome first.")
        return None, 0

# گرفتن رنگ یک پیکسل
def get_px(img, x, y):
    w, h = img.size
    if 0 <= x < w and 0 <= y < h:
        return img.getpixel((x, y))
    else:
        return (255, 255, 255)

# حلقه اصلی ربات
def start():
    print("🚀Dino robot is started")
    jump_time, last_jump, curr_jump, last_int = 0, 0, 0, 0
    time.sleep(3)  # فرصت برای رفتن به بازی

    jump_time, last_jump, curr_jump = 0, 0, 0
    x_s, x_e = 740, 760
    y1, y2 = 290, 315
    y_bird = 289

    while True:
        img, w = get_chrome_screenshot()
        if img is None:
            break
        
        # رنگ پس‌زمینه فعلی
        bg_color = get_px(img, 638, 175)
        # بررسی موانع جلو
        for i in reversed(range(x_s, x_e)):
            # کاکتوس بلند
            if get_px(img, i, y1) != bg_color:
                keyboard_ctrl.press(Key.up)
                if x_e >900:
                    time.sleep(0.1)
                else:
                    time.sleep(0.13)
                keyboard_ctrl.release(Key.up)
                jump_time = time.time()
                curr_jump = jump_time
                break
             # کاکتوس کوتاه
            if get_px(img, i, y2) != bg_color:
                keyboard_ctrl.press(Key.up)
                time.sleep(0.08)
                keyboard_ctrl.release(Key.up)
                jump_time = time.time()
                curr_jump = jump_time
                break
            # پرنده
            if get_px(img, i, y_bird) != bg_color:
                keyboard_ctrl.press(Key.down)
                time.sleep(0.4)
                keyboard_ctrl.release(Key.down)
                break
    
        # Adjust for speed (محدوده بررسی جلوتر می‌رود)
        int_time = curr_jump - last_jump
        if last_int != 0 and math.floor(int_time) != math.floor(last_int):
            x_e += 4
            print(f" x_e:{x_e}")
            if x_e >= w:
                x_e = w
        last_jump = jump_time
        last_int = int_time

if __name__ == "__main__":
    start()
