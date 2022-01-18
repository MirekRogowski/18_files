import sys
import requests
import json
from datetime import datetime
from datetime import timedelta
import csv
import os

# 592182cf7fmshdb1d75181a2e92dp199a88jsnd11a7a24d87c
FORECAST_DAYS = "16"


class WeatherForecast:
    def __init__(self, api_key=""):
        self.api_key = api_key
        self.cache = {}
        self.weather_date = []
        self.date = ""
        self.init_forecast()

    def __getitem__(self, item):
        if item == self.date:
            return self.check_day()


    def __iter__(self):
        # print(self.weather_date)
        for i in self.weather_date:
            yield i[0]

    def items(self):
        for i in self.weather_date:
            # yield i[0], i[1]
            if i[1] in ['Snow', 'Rain']:
                yield i[0], "będzie padać"
            else:
                yield i[0], "nie będzie padać"

    def init_forecast(self):
        if os.path.exists("data.csv"):
            # print("test warunek 1")
            self.read_from_csv_file()
        if os.path.exists("out.json"):
            # print("test warunek 2")
            self.read_from_json_file()
            self.write_data()
            # self.print_data()
        if not self.weather_date:
            # print("test warunek 3")
            self.read_api()

    def read_from_json_file(self):
        # print("funkcja read_from_json_file ")
        with open("out.json") as f:
            self.cache = json.load(f)
        # self.print_data()

    def read_from_csv_file(self):
        with open("data.csv", newline='') as f:
            reader = csv.reader(f)
            for i in reader:
                self.weather_date.append([i[0], i[1]])

    def read_api(self):
        url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"
        querystring = {"q": "Konin", "lat": "35", "lon": "139", "cnt": FORECAST_DAYS, "units": "metric or imperial"}
        headers = {
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
            'x-rapidapi-key': self.api_key
        }
        print("______ api update ______")
        response = requests.request("GET", url, headers=headers, params=querystring)
        out_url = response.json()
        with open("out.json", 'w') as json_file:
            json.dump(out_url, json_file)
        self.read_from_json_file()
        self.write_data()

    def read_from_weather_date(self):
        for i in self.weather_date:
            if i[0] == self.date:
                return self.date

    def check_forecast(self):
        for i in self.weather_date:
            if i[0] == self.date:
                if i[1] in ['Snow', 'Rain']:
                    return f"W dniu {self.date} - Będzie padać"
                return f"W dniu {self.date} - Nie będzie padać"

    def check_day(self):
        if not self.check_forecast():
            self.read_api()
            return f"Dla daty {self.date} {self.check_forecast()}"
        return self.check_forecast()

    def write_to_wetaher_date(self):
        for i in range(len(self.cache['list'])):
            day = str(datetime.fromtimestamp(self.cache['list'][i]['dt']).date())
            self.date = day
            forecast = self.cache['list'][i]['weather'][0]['main']
            if day != self.read_from_weather_date():
                self.weather_date.append([day, forecast])

    def write_data(self):
        self.write_to_wetaher_date()
        self.write_csv_file()

    def write_csv_file(self):
        with open("data.csv", "w", newline="") as f:
            csv_writer = csv.writer(f)
            for line in self.weather_date:
                csv_writer.writerow(line)

    def days_between(self, date):
        d1 = datetime.now().date()
        d2 = datetime.strptime(date, "%Y-%m-%d").date()
        return (d2 - d1).days

    def print_data(self):
        print("testowanie: "+"*" * 50)
        print(self.api_key)
        # print(self.cache)
        print(self.weather_date)
        print(self.date)


def main():
    if len(sys.argv) < 2:
        print("Brak api")
        exit()
    wf = WeatherForecast(sys.argv[1])
    if len(sys.argv) == 2:
        wf.date = str(datetime.now().date() + timedelta(days=1))
        wf[sys.argv[2]]
    elif len(sys.argv) == 3:
        wf.date = sys.argv[2]
        print(f"Dla daty {wf.date} brak danych ") if wf.days_between(sys.argv[2]) >= int(FORECAST_DAYS) \
            else print(wf.check_day())
    else:
        wf.date = str(datetime.now().date())
        for row in wf.items():
            print(row)
        print("*"*50)
        for i in wf:
            print(i)


main()
