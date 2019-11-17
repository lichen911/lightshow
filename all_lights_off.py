#!/usr/bin/env python3

import gpiozero
import sys

def all_on(relay_list):
    for relay in relay_list:
        relay.on()


def all_off(relay_list):
    for relay in relay_list:
        relay.off()
def main():
    relay_pin_list = [24, 23, 25, 17, 27, 22, 8, 7]
    relay_list = []

    for relay_pin in relay_pin_list:
        relay_list.append(gpiozero.OutputDevice(relay_pin, active_high=False, initial_value=False))

    all_off(relay_list)


if __name__ == "__main__":
    main()
