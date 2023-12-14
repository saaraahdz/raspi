import time
from grove.grove_light_sensor_v1_2 import GroveLightSensor
import requests
import json
from seeed_dht import DHT
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
import RPi.GPIO as GPIO
from grove.grove_moisture_sensor import GroveMoistureSensor

def log_to_file(filename, data):
    with open(filename, 'a') as file:
        file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {data}\n")

def main():
	
	# connect to alalog pin 2(slot A2)
	PIN = 2
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(24,GPIO.OUT)
	sensor = GroveMoistureSensor(PIN)
	print('Detecting moisture...')
	
	# Grove - Light Sensor connected to port A0
	sensor1 = GroveLightSensor(0)
	
	# Grove - Temperature&Humidity Sensor connected to port D5
	sensor2 = DHT('11', 5)
	
	# Grove - Ultrasonic Ranger connected to port D16
	sensor3 = GroveUltrasonicRanger(16)
	
	while True:
		m = sensor.moisture
		
		if 0 <= m and m < 300:
			result = 'Dry'
			GPIO.output(24,False)
			
		else:
			result = 'Wet'
			GPIO.output(24, True)
			print('Moisture value: {0}, {1}'.format(m, result))
			
			light = sensor1.light
			print('light value {}'.format(light))
			humi, temp = sensor2.read()
			print('temperature {}C, humidity {}%'.format(temp, humi))
			distance = sensor3.get_distance()
			print('{} cm'.format(distance))
			time.sleep(1)
			headers={"Content-Type":"application/json"}
			data=json.dumps({"temperature":temp,"humidity":humi,"illuminance":light,"distance":distance})

			log_to_file("raspiData.json", data)
			
			url ="http://thingsboard.cloud/api/v1/9P7NpFIgXHpxfucsdFlv/telemetry"
			try:
				response=requests.post(url, headers=headers, data=data)
				response.raise_for_status()
			except requests.exceptions.RequestException as e:
				print(f"error:{e}")
if __name__ == '__main__':
	main()


