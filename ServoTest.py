from devices import *
import time
setup()
servo = OutputDevice(12,50)
set_out("servo",servo)
servo.start(7.5)
time.sleep(2)
servo.change_duty_cycle(12.5)
time.sleep(2)
servo.change_duty_cycle(2.5)
time.sleep(2)
cleanup()
