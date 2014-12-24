import sys
import time
import datetime
import urllib2
import json

import Adafruit_DHT
import gspread

# Type of sensor
DHT_TYPE = Adafruit_DHT.DHT22

# Sensor Connected to pin 4
DHT_PIN  = 4


# Google Docs account email, password, and spreadsheet name.
GDOCS_EMAIL            = 'nick.throckmorton@gmail.com'
GDOCS_PASSWORD         = 'bkplrybaxryajvwx'
GDOCS_SPREADSHEET_NAME = 'Inside Outside'

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS      = 30




def login_open_sheet(email, password, spreadsheet):
	"""Connect to Google Docs spreadsheet and return the first worksheet."""
	try:
		gc = gspread.login(email, password)
		worksheet = gc.open(spreadsheet).sheet1
		return worksheet
	except:
		print ('Unable to login and get spreadsheet.  Check email, password, spreadsheet name.')
		sys.exit(1)


print ('Logging sensor measurements to {0} every {1} seconds.').format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS)
print ('Press Ctrl-C to quit.')
worksheet = None
while True:
	# Login if necessary.
	if worksheet is None:
		worksheet = login_open_sheet(GDOCS_EMAIL, GDOCS_PASSWORD, GDOCS_SPREADSHEET_NAME)

	# Attempt to get sensor reading.
	humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)
	
	
	# Skip to the next reading if a valid measurement couldn't be taken.
	if humidity is None or temp is None:
		time.sleep(2)
		continue
	
	#Access URL of wunderground API
  	f = urllib2.urlopen('http://api.wunderground.com/api/ffd38634c3e2642d/conditions/q/MN/Minneapolis.json')

  	#read and parse the JSON file from wunderground
  	json_string = f.read()
	parsed_json = json.loads(json_string)

  	#variables from JSON
  	location = parsed_json['current_observation']['display_location']['full']
  	temp_f = parsed_json['current_observation']['temp_f']
  	current_condition = parsed_json['current_observation']['weather']
  	rel_humidity = parsed_json['current_observation']['relative_humidity']
	
	int_temp_f = temp*1.8 +32
	print ('Temperature: {0:0.1f} F').format(int_temp_f)
	print ('Humidity:    {0:0.1f} %').format(humidity)
        print "Current temperature in %s is: %s F" % (location, temp_f)
        print "Current weather is %s in %s" % (current_condition, location)
        print "Current relative humidity is %s in %s" % (rel_humidity, location)

	# Append the data in the spreadsheet, including a timestamp
	try:
		worksheet.append_row((datetime.datetime.now(), int_temp_f, temp_f, humidity, rel_humidity, current_condition, location))
	except:
		# Error appending data, most likely because credentials are stale.
		# Null out the worksheet so a login is performed at the top of the loop.
		print ('Append error, logging in again')
		worksheet = None
		time.sleep(FREQUENCY_SECONDS)
		continue

	# Wait 30 seconds before continuing
	print ('Wrote a row to {0}').format(GDOCS_SPREADSHEET_NAME)
	
	time.sleep(FREQUENCY_SECONDS)
