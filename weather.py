import urllib2
import json
import time
import RPi.GPIO as GPIO

#set up GPIO
GPIO.setmode(GPIO.BOARD)

#Assign GPIOs to LEDs
lp_led = 15
hp_led = 13
storm_led = 11
pc_led = 7
c_led = 5
sunny_led = 3

#Tell GPIOs to be Output for LEDs
GPIO.setup(lp_led, GPIO.OUT)
GPIO.setup(hp_led, GPIO.OUT)
GPIO.setup(storm_led, GPIO.OUT)
GPIO.setup(pc_led, GPIO.OUT)
GPIO.setup(c_led, GPIO.OUT)
GPIO.setup(sunny_led, GPIO.OUT)

#dictionary of weather codes
dict = {}
dict['Light Drizzle'] = 1
dict['Light Rain'] = 2
dict['Light Snow'] = 3
dict['Light Snow Grains'] = 4
dict['Light Ice Crystals'] = 5
dict['Light Ice Pellets'] = 6
dict['Light Hail'] = 7
dict['Light Mist'] = 8
dict['Light Low Drifting Snow'] = 9
dict['Light Blowing Snow'] = 10
dict['Light Rain Mist'] = 11
dict['Light Rain Showers'] = 12
dict['Light Snow Showers'] = 13
dict['Light Snow Blowing Snow Mist'] = 14
dict['Light Ice Pellet Showers'] = 15
dict['Light Hail Showers'] = 16
dict['Light Small Hail Showers'] = 17
dict['Light Freezing Drizzle'] = 18
dict['Light Freezing Rain'] = 19
dict['Light Freezing Fog'] = 20
dict['Heavy Drizzle'] = 21
dict['Heavy Rain'] = 22
dict['Heavy Snow'] = 23
dict['Heavy Snow Grains'] = 24
dict['Heavy Ice Crystals'] = 25
dict['Heavy Ice Pellets'] = 26
dict['Heavy Hail'] = 27
dict['Heavy Mist'] = 28
dict['Heavy Low Drifting Snow'] = 29
dict['Heavy Blowing Snow'] = 30
dict['Heavy Rain Mist'] = 31
dict['Heavy Rain Showers'] = 32
dict['Heavy Snow Showers'] = 33
dict['Heavy Snow Blowing Snow Mist'] = 34
dict['Heavy Ice Pellet Showers'] = 35
dict['Heavy Hail Showers'] = 36
dict['Heavy Small Hail Showers'] = 37
dict['Heavy Freezing Drizzle'] = 38
dict['Heavy Freezing Rain'] = 39 
dict['Heavy Freezing Fog'] = 40
dict['Drizzle'] = 41
dict['Rain'] = 42
dict['Snow'] = 43
dict['Snow Grains'] = 44   
dict['Ice Crystals'] = 45
dict['Ice Pellets'] = 46
dict['Mist'] = 47
dict['Low Drifting Snow'] = 48
dict['Blowing Snow'] = 49
dict['Rain Mist'] = 50
dict['Rain Showers'] = 51
dict['Snow Showers'] = 52
dict['Snow Blowing Snow Mist'] = 53
dict['Freezing Drizzle'] = 54
dict['Freezing Rain'] = 55
dict['Squalls'] = 56  
dict['Light Volcanic Ash'] = 57
dict['Light Thunderstorm'] = 58
dict['Light Thunderstorms and Rain'] = 59
dict['Light Thunderstorms and Snow'] = 60
dict['Light Thunderstorms and Ice Pellets'] = 61
dict['Light Thunderstorms with Hail'] = 62
dict['Light Thunderstorms with Small Hail'] = 63
dict['Heavy Volcanic Ash'] = 64
dict['Heavy Dust Whirls'] = 65
dict['Heavy Sandstorm'] = 66
dict['Heavy Thunderstorm'] = 67 
dict['Heavy Thunderstorms and Rain'] = 68
dict['Heavy Thunderstorms and Snow'] = 69
dict['Heavy Thunderstorms and Ice Pellets'] = 70
dict['Heavy Thunderstorms with Hail'] = 71
dict['Heavy Thunderstorms with Small Hail'] = 72
dict['Hail'] = 73
dict['Smoke'] = 74
dict['Volcanic Ash'] = 75
dict['Widespread Dust'] = 76
dict['Dust Whirls'] = 77
dict['Sandstorm'] = 78
dict['Ice Pellet Showers'] = 79
dict['Hail Showers'] = 80
dict['Small Hail Showers'] = 81
dict['Thunderstorm'] = 82
dict['Thunderstorms and Rain'] = 83  
dict['Thunderstorms and Snow'] = 84
dict['Thunderstorms and Ice Pellets'] = 85
dict['Thunderstorms with Hail'] = 86
dict['Thunderstorms with Small Hail'] = 87
dict['Small Hail'] = 88
dict['Funnel Cloud'] = 89
dict['Light Dust Whirls'] = 90
dict['Light Sandstorm'] = 91
dict['Light Haze'] = 92    
dict['Light Spray'] = 93 
dict['Light Low Drifting Widespread Dust'] = 94
dict['Light Low Drifting Sand'] = 95
dict['Light Blowing Widespread Dust'] = 96
dict['Light Blowing Sand'] = 97
dict['Patches of Fog'] = 98
dict['Shallow Fog'] = 99 
dict['Partial Fog'] = 100
dict['Overcast'] = 101
dict['Partly Cloudy'] = 102  
dict['Mostly Cloudy'] = 103
dict['Scattered Clouds'] = 104
dict['Light Fog'] = 105
dict['Light Fog Patches'] = 106
dict['Light Smoke'] = 107
dict['Light Widespread Dust'] = 108
dict['Light Sand'] = 109
dict['Heavy Fog'] = 110
dict['Heavy Fog Patches'] = 111
dict['Heavy Smoke'] = 112
dict['Heavy Widespread Dust'] = 113
dict['Heavy Sand'] = 114
dict['Heavy Haze'] = 115
dict['Heavy Spray'] = 116
dict['Heavy Low Drifting Widespread Dust'] = 117
dict['Heavy Low Drifting Sand'] = 118
dict['Heavy Blowing Widespread Dust'] = 119
dict['Heavy Blowing Sand'] = 120
dict['Fog'] = 121
dict['Fog Patches'] = 122
dict['Sand'] = 123
dict['Haze'] = 124
dict['Spray'] = 125
dict['Low Drifting Widespread Dust'] = 126
dict['Low Drifting Sand'] = 127
dict['Blowing Widespread Dust'] = 128
dict['Blowing Sand'] = 129
dict['Freezing Fog'] = 130
dict['Clear'] = 131
dict['Unknown Precipitation'] = 132
dict['Unknown'] = 133

#Access URL of wunderground API
f = urllib2.urlopen('http://api.wunderground.com/api/[insert your API key here]/conditions/q/MN/Minneapolis.json')

#read and parse the JSON file from wunderground
json_string = f.read()
parsed_json = json.loads(json_string)

#variables from JOSN
location = parsed_json['current_observation']['display_location']['city']
temp_f = parsed_json['current_observation']['temp_f']
current_condition = parsed_json['current_observation']['weather']

print "Current temperature in %s is: %s F" % (location, temp_f)

print "Current weather is %s in %s" % (current_condition, location)

#Reference Current Condition in dictionary and return paired value
value_code = dict[current_condition]

#Flashing lights
GPIO.output(lp_led, True)
time.sleep(.2)
GPIO.output(lp_led,False)
GPIO.output(hp_led,True)
time.sleep(.2)
GPIO.output(hp_led, False)
GPIO.output(storm_led, True)
time.sleep(.2)
GPIO.output(storm_led, False)
GPIO.output(pc_led, True)
time.sleep(.2)
GPIO.output(pc_led, False)
GPIO.output(c_led, True)
time.sleep(.2)
GPIO.output(c_led, False)
GPIO.output(sunny_led, True)
time.sleep(.2)
GPIO.output(sunny_led,False)
time.sleep(1)

#Signal correct light based on value
if value_code <=20:
        GPIO.output(lp_led, True)
        GPIO.output(hp_led, False)
        GPIO.output(storm_led, False)
        GPIO.output(pc_led, False) 
        GPIO.output(c_led, False)
        GPIO.output(sunny_led, False)

elif value_code >20 and value_code <=56:
        GPIO.output(lp_led, False)
        GPIO.output(hp_led, True)
        GPIO.output(storm_led, False)
        GPIO.output(pc_led, False)
        GPIO.output(c_led, False)
        GPIO.output(sunny_led, False)


elif value_code >56 and value_code <=91:
        GPIO.output(lp_led, False)
        GPIO.output(hp_led, False)
        GPIO.output(storm_led, True)
        GPIO.output(pc_led, False)
        GPIO.output(c_led, False)
        GPIO.output(sunny_led, False)

elif value_code >91 and value_code <=104:
        GPIO.output(lp_led, False)
        GPIO.output(hp_led, False)
        GPIO.output(storm_led, False)
        GPIO.output(pc_led, True)
        GPIO.output(c_led, False)
        GPIO.output(sunny_led, False)

elif value_code >104 and value_code <=130:
        GPIO.output(lp_led, False)
        GPIO.output(hp_led, False)
        GPIO.output(storm_led, False)
        GPIO.output(pc_led, False)
        GPIO.output(c_led, True)
        GPIO.output(sunny_led, False)
elif value_code == 131:  
        GPIO.output(lp_led, False)
        GPIO.output(hp_led, False)
        GPIO.output(storm_led, False)
        GPIO.output(pc_led, False)
        GPIO.output(c_led, False)
        GPIO.output(sunny_led, True)

elif value_code >131 and value_code <=133:
        GPIO.output(lp_led, False)
        GPIO.output(hp_led, False)
        GPIO.output(storm_led, False)
        GPIO.output(pc_led, False)
        GPIO.output(c_led, False)
        GPIO.output(sunny_led, True)

time.sleep(10)
GPIO.cleanup()
        
f.close()
        

                                   
