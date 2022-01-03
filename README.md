# The cube

The cube is a physical device which connects to the internet and lights up when you win (or don't) playing [FortNite](https://www.epicgames.com/fortnite/en-US/home).

![the fortnite cube, a 70mm white acrylic cube lit up](docs/images/fn_cube.jpg)

Created by [Martin O'Hanlon](https://github.com/martinohanlon) [@martinohanlon](https://twitter.com/martinohanlon), [stuffaboutco.de](https://stuffaboutco.de).

## Design

The fortnite cube uses a [Raspberry Pi Zero](https://www.raspberrypi.com/products/raspberry-pi-zero-w/) with a [Pimoroni blinkt](https://shop.pimoroni.com/products/blinkt) and a single toggle switch to activate it.

The cube is laser cut from white opal acrylic - the svg is [here](docs/resources/cube.svg).

The Raspberry Pi Zero sits inside a 3d printed frame - the stl is [here](docs/resources/cube_base.stl)

## Code

A python program, [fortnitecube.py](thecube/fortnitecube.py) controls the cube, connecting to [fortnitetracker.com](https://fortnitetracker.com) once every 30 seconds when turned on (via a switch at the back of the cube) and controls the LEDs inside based on changing player stats (e.g. flashing colours when the number of wins increases).

## Install

+ Clone this repository

```bash
git clone https://github.com/martinohanlon/thecube
```

+ Install the pre-requisite Python packages

```bash
pip3 install requests
sudo pip3 install blinkt
```
+ Sign up for a [fortnitetracker.com API Key](https://fortnitetracker.com/site-api)

+ Create a `constants.py` file in the `thecube/thecube` folder and add the fortnitetracker.com API Key and players name and in the format.

```python
FNT_API_KEY = "api key"
FN_PLAYER = "players name"
```

## Run

+ Run the `fortnitecube.py` program:

```bash
python3 fortnitecube.py
```

+ Flick the switch to on will start the fortnight cube

## Cube status lights

The cube will turn green when connecting and flash 3 times once it has connected before turning white.

If an incorrect repsonse is returned from the fortnitetracker.com API the cube will flash purple 3 times, return to white and continue running.

If an error is captured while communicating with fortnitetracker.com the cube will flash purple 3 times and stop. If any other errors are captured, the cube will flash RED 3 times and stop. The switch should be turned on / off to restart the cube.

## Status 

In active development.
