import time
from seeed_dht import DHT
import requests
import json

def main():
	# Grove - Temperature&Humidity Sensor connected to port D5
	sensor = DHT('11', 5)
	while True:
		humi, temp = sensor.read()
		print('temperature {}C, humidity {}%'.format(temp, humi))
		time.sleep(1)
		headers={"Content-Type":"application/json"}
		data=json.dumps({"temperature":temp})
		url ="http://thingsboard.cloud/api/v1/9P7NpFIgXHpxfucsdFlv/telemetry"

		try:
			response=requests.post(url, headers=headers, data=data)
			response.raise_for_status()
			print("biennn")
		except requests.exceptions.RequestException as e:
			print(f"error:{e}")
if __name__ == '__main__':
	main()
