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


def bounce(relay_list):
    for relay in relay_list:
        relay.on()
        time.sleep(DELAY)
        relay.off()

    for relay in relay_list[len(relay_list)-2:0:-1]:
        relay.on()
        time.sleep(DELAY)
        relay.off()


def alternate_lit(relay_list):
    list_one = []
    list_two = []

    for index, relay in enumerate(relay_list):
        if index % 2 == 0:
            list_one.append(relay)
        else:
            list_two.append(relay)

    for _ in range(2):
        all_on(list_one)
        all_off(list_two)
        time.sleep(DELAY)
        all_off(list_one)
        all_on(list_two)
        time.sleep(DELAY)


def outside_in(relay_list):
    relay_count = len(relay_list)

    for _ in range(2):
        middle_case = False
        for index in range(relay_count):
            other_side = relay_count - index - 1
            if abs(other_side - index) == 1:
                if middle_case:
                    continue
                else:
                    middle_case = True
            # skip lighting the last at the end of the run so it
            # looks better when looping
            elif index == relay_count - 1 or other_side == 0:
                    continue
            relay_list[index].on()
            relay_list[other_side].on()
            time.sleep(DELAY)
            relay_list[index].off()
            relay_list[other_side].off()


def inside_out(relay_list):
    relay_count = len(relay_list)
    if relay_count % 2 == 0:
        middle_high = int(relay_count / 2)
        middle_low = middle_high - 1

    for _ in range(2):
        for index in range(int(relay_count / 2)):
            current_low = middle_low - index
            current_high = middle_high + index
            relay_list[current_low].on()
            relay_list[current_high].on()
            time.sleep(DELAY)
            relay_list[current_low].off()
            relay_list[current_high].off()


def stacker(relay_list):
    relay_count = len(relay_list)
    for index in range(relay_count):
        for inner_idx, relay in enumerate(relay_list[0:relay_count-index]):
            relay.on()
            time.sleep(DELAY)
            if inner_idx != relay_count - index - 1:
                relay.off()
    all_off(relay_list)


def run_forever(function_name, args=()):
    while True:
        function_name(*args)


def random_effect(relay_list, effect_list):
    global DELAY
    delay_times = [0.100, 0.200, 0.300, 0.400]
    DELAY = random.choice(delay_times)
    current_effect = random.choice(effect_list)
    list_reversed = random.choice([True, False])
    toggle = False


    all_on(relay_list)
    time.sleep(10)
    all_off(relay_list)

    for _ in range(10):
        if current_effect == stacker:
            # make the stacker effect reverse the list every time
            # because it makes for a better effect
            if toggle:
                current_effect(relay_list[::-1])
                toggle = False
            else:
                current_effect(relay_list)
                toggle = True
        elif list_reversed:
            current_effect(relay_list[::-1])
        else:
            current_effect(relay_list)


def show_1(relay_list):
    all_on(relay_list)
    time.sleep(10)
    all_off(relay_list)
    time.sleep(0.200)
    all_on(relay_list)
    time.sleep(0.200)
    all_off(relay_list)
    for _ in range(10):
        bounce(relay_list)


def main():
    relay_pin_list = [24, 23, 25, 17, 27, 22, 8, 7]
    relay_list = []

    for relay_pin in relay_pin_list:
        relay_list.append(gpiozero.OutputDevice(relay_pin, active_high=False, initial_value=False))

    effect_list = [forward_and_reverse, forward, rotate_one_dark, rotate_one_lit, bounce, alternate_lit, outside_in, inside_out]
    #effect_list = [stacker]

    # set1 = relay_list[:3]
    # set2 = relay_list[3:]

    # print(set1)
    # print(set2)

    # rotate first 3 forever
    # thread1 = threading.Thread(target=run_forever, args=(rotate_one_lit, (set1, )))
    # thread1.daemon = True
    # thread1.start()

    # run all effects randomly
    thread2 = threading.Thread(target=run_forever, args=(random_effect, (relay_list, effect_list)))
    thread2.daemon = True
    thread2.start()

    # thread3 = threading.Thread(target=run_forever, args=(show_1, (relay_list, )))
    # thread3.daemon = True
    # thread3.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Exiting')
        sys.exit(0)


if __name__ == "__main__":
    main()
