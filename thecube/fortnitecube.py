from gpiozero import Button
from time import sleep, time
import blinkt
import random
import requests
import sys
from constants import *

FNT_URL = "https://api.fortnitetracker.com/v1/profile/{}/{}"
FNT_REFRESH_TIME_SECS = 30
# debug shorter refresh
# FNT_REFRESH_TIME_SECS = 10

class FortniteAPIError(Exception):
    pass

class FortniteResponseError(Exception):
    pass

def get_lifetime_wins():

    header = {"TRN-Api-Key": FNT_API_KEY}

    url = FNT_URL.format("all", FN_PLAYER)

    response = requests.get(url, headers=header)

    # debug
    # print(response)
    # print(response.headers)
    # with open("response.txt", "w") as f:
    #     f.write(response.text)
    
    if response.status_code != 200:
        raise FortniteResponseError("HTTP Status {}".format(response.status_code))

    # check its a valid json response
    try:
        response.json()
    except ValueError:
        raise FortniteAPIError("Invalid JSON response")

    # check for errors
    if "error" in response.json().keys():
        raise FortniteAPIError(response.json()["error"])

    # get the stats
    life_time_stats = response.json()["lifeTimeStats"]

    # debug
    # print(life_time_stats)

    response.close()

    # convert key value pair to a dictionary
    data = {}
    for stat in life_time_stats:
        if stat["value"].isnumeric():
            stat["value"] = int(stat["value"])

        data[stat["key"]] = stat["value"]

    return data

def on(r=255, g=255, b=255):
    blinkt.set_all(r, g, b)
    blinkt.show()

def off():
    blinkt.clear()
    blinkt.show()

def flash(r, g, b, times, delay):
    for i in range(times):
        blinkt.set_all(r, g, b)
        blinkt.show()
        sleep(delay)
        off()
        sleep(delay)

def crazy_lights(min_leds, max_leds, r1, r2, g1, g2, b1, b2, length, delay):

    start_time = time()

    while time() - start_time < length:
        # how many pixels
        pixels = random.sample(range(blinkt.NUM_PIXELS), random.randint(min_leds, max_leds))
        for pixel in range(blinkt.NUM_PIXELS):

            r, g, b = random.randint(r1,r2), random.randint(g1,g2), random.randint(b1,b2)

            if pixel in pixels:
                # blinkt.set_pixel(pixel, random.randint(r1,r2), random.randint(g1,g2), random.randint(b1,b2))
                blinkt.set_pixel(pixel, r, g, b)
            else:
                blinkt.set_pixel(pixel, 0, 0, 0)

        blinkt.show()
        sleep(delay)

def run_cube():    
    # check connection
    on(0, 255, 0)
    prev_life_time_wins = get_lifetime_wins()
    flash(0, 255, 0, 3, 0.25)
    
    # start
    on()

    next_check = time() + FNT_REFRESH_TIME_SECS

    while switch.is_pressed:
    # debug with button
    # while not switch.is_pressed:

        sleep(0.1)
        if time() > next_check:
            
            life_time_wins = get_lifetime_wins()

            # debug
            # print(life_time_wins)

            # check a win                
            if life_time_wins["Wins"] > prev_life_time_wins["Wins"]:
                crazy_lights(5, 8, 0, 255, 0, 255, 0, 255, 10, 0.1)
                print("Wins")
                on()

            # check a high position
            elif life_time_wins["Top 3s"] > prev_life_time_wins["Top 3s"]:
                crazy_lights(1, 5, 0, 255, 0, 255, 0, 255, 10, 0.4)
                print("Top 3s")
                on()
                
            elif life_time_wins["Top 10"] > prev_life_time_wins["Top 10"]:
                crazy_lights(1, 5, 0, 255, 0, 255, 0, 255, 10, 0.4)
                print("Top 10")
                on()
                
            elif life_time_wins["Top 5s"] > prev_life_time_wins["Top 5s"]:
                crazy_lights(1, 5, 0, 255, 0, 255, 0, 255, 10, 0.4)
                print("Top 5s")
                on()

            prev_life_time_wins = life_time_wins

            next_check = time() + FNT_REFRESH_TIME_SECS
            
    off()
    print("Fortnite stopped")

    # debug with button
    # switch.wait_for_release()

switch = Button(17)
blinkt.set_clear_on_exit()

running = True

print("Service running")
while running:

    try:
        switch.wait_for_press()
        # debug with button
        # switch.wait_for_release()

        print("Fortnite started")
        run_cube()

    except FortniteResponseError as err:
        print("Fortnite Response Error: {}".format(err))
        flash(255, 0, 255, 3, 0.25)
        run_cube()
        
    except FortniteAPIError as err:
        print("Stopping - Fortnite API Error: {}".format(err))
        flash(255, 0, 255, 3, 0.25)
        on(255, 0, 255)
        switch.wait_for_release()
        off()

    except KeyboardInterrupt:
        print("Service cancelled")
        off()
        running = False

    except:
        print("Stopping - Unexpected error:", sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
        flash(255, 0, 0, 3, 0.25)
        on(255,0,0)
        switch.wait_for_release()
        off()
