import time
import requests
import json

def log_to_file(filename, data):
    with open(filename, 'a') as file:
        file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {data}\n")
	    
def main():
	while True:
			
		try:
			with open("/sys/class/thermal/thermal_zone0/temp","r") as file:
				temperature_str = file.readline()
				temp_raspi=float(temperature_str)/1000.0
				print("CPU temperature: {: .2f} ºC".format(temp_raspi))
		except IOError as e:
			print("Error reading temperature:", str(e))
		
		time.sleep(1)
		headers={"Content-Type":"application/json"}
		data=json.dumps({"temp_raspi":temp_raspi})

		log_to_file("tempRaspi.txt", data)
		
		url ="http://thingsboard.cloud/api/v1/9P7NpFIgXHpxfucsdFlv/telemetry"
		try:
			response=requests.post(url, headers=headers, data=data)
			response.raise_for_status()
		except requests.exceptions.RequestException as e:
			print(f"error:{e}")	
		
	
	
	
if __name__ == '__main__':

    main()
