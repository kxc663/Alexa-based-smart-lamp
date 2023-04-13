#!/usr/bin/env python3

import pigpio
import time

PIN_R = 19
PIN_G = 26
PIN_B = 13
PINS = [PIN_R, PIN_G, PIN_B]
PWM_RANGE = 1000
PWM_FREQUENCY = 1000


def ramp_up_and_down(pi, pins):
    for i in range(0, 1000, 2):
        for p in pins:
            pi.set_PWM_dutycycle(p, i)
        time.sleep(0.001)

    for i in range(1000, 0, -2):
        for p in pins:
            pi.set_PWM_dutycycle(p, i)
        time.sleep(0.001)


def setup_and_loop():

    pi = pigpio.pi()

    for pin in PINS:
        pi.set_mode(pin, pigpio.OUTPUT)
        pi.write(pin, 0)
        pi.set_PWM_frequency(pin, PWM_FREQUENCY)
        pi.set_PWM_range(pin, PWM_RANGE)
        pi.set_PWM_dutycycle(pin, 0)

    while (1):

        for pin in PINS:
            pi.write(pin, 0)

        time.sleep(1.0)

        ramp_up_and_down(pi, [PIN_R])
        ramp_up_and_down(pi, [PIN_G])
        ramp_up_and_down(pi, [PIN_B])
        ramp_up_and_down(pi, PINS)


if __name__ == "__main__":

    setup_and_loop()
