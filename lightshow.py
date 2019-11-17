#!/usr/bin/env python3

import gpiozero
import time
import random
import threading
import sys

DELAY = 0.100

def forward_and_reverse(relay_list):
    for relay in relay_list:
        relay.on()
        time.sleep(DELAY)

    for relay in relay_list[::-1]:
        relay.off()
        time.sleep(DELAY)


def forward(relay_list):
    for relay in relay_list:
        relay.on()
        time.sleep(DELAY)

    for relay in relay_list:
        relay.off()
        time.sleep(DELAY)


def all_on(relay_list):
    for relay in relay_list:
        relay.on()


def all_off(relay_list):
    for relay in relay_list:
        relay.off()


def rotate_one_lit(relay_list):
    for relay in relay_list:
        relay.on()
        time.sleep(DELAY)
        relay.off()


def rotate_one_dark(relay_list):
    all_on(relay_list)
    for relay in relay_list:
        relay.off()
        time.sleep(DELAY)
        relay.on()
    time.sleep(DELAY)
    all_off(relay_list)


def run_forever(function_name, args=()):
    while True:
        function_name(*args)


def random_effect(relay_list, effect_list):
    current_effect = random.choice(effect_list)
    current_effect(relay_list)


def main():
    relay_pin_list = [24, 23, 25, 17, 27, 22, 8, 7]
    relay_list = []

    for relay_pin in relay_pin_list:
        relay_list.append(gpiozero.OutputDevice(relay_pin, active_high=False, initial_value=False))

    effect_list = [forward_and_reverse, forward, all_on, all_off, rotate_one_dark, rotate_one_lit]

    # set1 = relay_list[:3]
    # set2 = relay_list[3:]

    # print(set1)
    # print(set2)

    # thread1 = threading.Thread(target=run_forever, args=(rotate_one_lit, (set1, )))
    # thread1.daemon = True
    # thread1.start()

    thread2 = threading.Thread(target=run_forever, args=(random_effect, (relay_list, effect_list)))
    thread2.daemon = True
    thread2.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Exiting')
        sys.exit(0)


if __name__ == "__main__":
    main()
