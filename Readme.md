# CP2112 interface

## Requirements
pip install hidapi

## CJMCU-2112
The CJMCU-2112 board is just a CP2112 with a micro USB and some pins. The following shows the pins on the board. GPIO.0 and GPIO.1 are used for activity LEDs.

|      |Left|Right|          |
|------|----|-----|----------|
|      |VCC |VCC  |          |
|      |GND |GND  |          |
|      |SDA |IO5  |GPIO.5    |
|      |SCL |IO6  |GPIO.6    |
|GPIO.2|WAK |IO7  |GPIO.7_CLK|
|GPIO.3|INT |SUS  |SUSPEND   |
|GPIO.4|RST |SUS- |/SUSPEND  |
