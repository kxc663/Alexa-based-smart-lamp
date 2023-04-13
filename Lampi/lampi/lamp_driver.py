import colorsys
import pigpio

PWM_FREQUENCY = 1000
PWM_RANGE = 1000

RED_GPIO = 19
GREEN_GPIO = 26
BLUE_GPIO = 13

RGBs = [RED_GPIO, GREEN_GPIO, BLUE_GPIO]


class LampDriver(object):
    def __init__(self):
        self.pi = pigpio.pi()
        for g in RGBs:
            self.pi.set_PWM_frequency(g, PWM_FREQUENCY)
            self.pi.set_PWM_range(g, PWM_RANGE)
            self.pi.set_PWM_dutycycle(g, 0)

    def set_lamp_state(self, hue, saturation, brightness, is_on):
        rgb = [0.0, 0.0, 0.0]

        if is_on:
            rgb = list(colorsys.hsv_to_rgb(hue, saturation, 1.0))
            for c in range(len(rgb)):
                rgb[c] = rgb[c] * brightness

        for i in range(len(RGBs)):
            self.pi.set_PWM_dutycycle(RGBs[i], rgb[i] * PWM_RANGE)
