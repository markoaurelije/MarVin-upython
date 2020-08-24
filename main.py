from my.ledmatrix import LedMatrix

color = (0x20,0x20,0x40)

led = LedMatrix(8,7,3)
led.clear(color)

import ntptime
import machine
import utime
rtc = machine.RTC()
t = ntptime.time()
t += 7200
tm = utime.localtime(t)
rtc.datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))

def showTime(timer):
    _, _, _, _, h, m, _, _ = rtc.datetime()
    time = '{:2d}:{:02d}'.format(h,m)
    led.text(time, color)
    print(time)
    print()

showTime(None)

t=machine.Timer(0)
t.init(period=60000, mode=machine.Timer.PERIODIC, callback=showTime)