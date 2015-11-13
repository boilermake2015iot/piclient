from sense_hat import SenseHat
import time

sense = SenseHat()

#sense.set_rotation(270)
#sense.show_message('Hello, world!')
X = [255, 0, 0] # red
O = [255, 255, 255] # white

question_mark = [
        O, O, O, X, X, O, O, O,
        O, O, X, O, O, X, O, O,
        O, O, O, O, O, X, O, O,
        O, O, O, O, X, O, O, O,
        O, O, O, X, O, O, O, O,
        O, O, O, X, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, X, O, O, O, O
        ]

sense.set_pixels(question_mark)
time.sleep(5)
sense.clear()
'''
sense.low_light = True
for i in xrange(9, 0, -1):
    sense.show_letter(str(i))
    time.sleep(1)

sense.clear()
sense.low_light = False
'''
