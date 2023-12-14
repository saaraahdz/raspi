import time
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime


def main():

    url = "https://www.capitan-marea.com/mareas/R%C3%ADa%20de%20Bilbao"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all tables with class 'table-bordered'
    tables = soup.find_all('table', class_='table-bordered')

    all_cols = []

    for i, table in enumerate(tables, 1):

        if (i ==1):
            # Rest of your code to extract and print the table data
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['th'])
                cols = [col.text.strip() for col in cols]
                all_cols.append(cols)
                print(cols)

    all_cols = all_cols[2:]

    print(all_cols)

    hora_actual = datetime.now().strftime("%H:%M")
    horaActual = datetime.strptime(hora_actual, "%H:%M").time()

    altura = 0

    for fila in all_cols:

        hora_obj = datetime.strptime(fila[1], "%H:%M").time()
        if horaActual > hora_obj:
            continue

        else:

            print(fila[2])

            altura = fila[2]
            headers={"Content-Type":"application/json"}
            data=json.dumps({"height":altura})
            url ="http://thingsboard.cloud/api/v1/9P7NpFIgXHpxfucsdFlv/telemetry"

            try:
                response=requests.post(url, headers=headers, data=data)
                response.raise_for_status()
                print("Dato enviado con exito!!! :)")
            except requests.exceptions.RequestException as e:
                print(f"error:{e}")

            break



    
if __name__ == '__main__':

    main()
