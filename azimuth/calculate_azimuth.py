from astral.location import Location
from astral.sun import sun
from astral import LocationInfo
import csv
from datetime import datetime, timedelta
from dateutil.parser import parse

import pandas as pd
import matplotlib.pyplot as plt


def collect_location_info() -> LocationInfo:
    name = input("Enter the name of the location: ")
    region = input("Enter the region of the location: ")
    timezone = input("Enter the timezone of the location: ")
    latitude = float(input("Enter the latitude of the location: "))
    longitude = float(input("Enter the longitude of the location: "))

    return LocationInfo(
        name=name,
        region=region,
        timezone=timezone,
        latitude=latitude,
        longitude=longitude,
    )


def subtract(time):
    return str(datetime.strptime(str(time), "%H:%M:%S") - timedelta(hours=12)).split()


def get_date_range():
    start_date = datetime.strptime(
        input("Enter the start date (YYYY-MM-DD): "), "%Y-%m-%d"
    )
    end_date = datetime.strptime(input("Enter the end date (YYYY-MM-DD): "), "%Y-%m-%d")

    return start_date, end_date


def calculate_azimuth_data(location_info: LocationInfo):
    start_date, end_date = get_date_range()
    azimuth_data = []
    delta = timedelta(days=1)
    date = start_date

    while date <= end_date:
        sun_data = sun(location_info.observer, date=date, tzinfo=location_info.timezone)
        loc = Location(location_info)
        azimuth_rise = loc.solar_azimuth(sun_data["sunrise"])
        azimuth_set = loc.solar_azimuth(sun_data["sunset"])
        azimuth_data.append(
            {
                "date": datetime.strptime(str(date).split()[0], "%Y-%m-%d").strftime(
                    "%b. %d, %Y"
                ),
                "sunrise": str(sun_data["sunrise"].time()).split(".")[0] + " a.m.",
                "sunset": str(subtract(str(sun_data["sunset"].time()).split(".")[0])[1])
                + " p.m.",
                "azimuth_sunrise": str(round(azimuth_rise, 2)) + "\u00B0",
                "azimuth_sunset": str(round(azimuth_set, 2)) + "\u00B0",
            }
        )
        date += delta

    return azimuth_data


def write_to_csv(azimuth_data: list):
    with open("azimuth_data.csv", mode="w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=azimuth_data[0].keys())
        writer.writeheader()
        writer.writerows(azimuth_data)


# def plot_azimuth_data(azimuth_data):
#     # Read the data into a DataFrame
#     df = azimuth_data

#     # Convert the times to datetime format
#     df['sunrise'] = pd.to_datetime(df['sunrise'], format='%I:%M:%S %p').dt.time
#     df['sunset'] = pd.to_datetime(df['sunset'], format='%I:%M:%S %p').dt.time

#     # Plot sunrise and sunset times
#     plt.figure(figsize=(10, 5))
#     plt.plot(df['date'], df['sunrise'], label='Sunrise')
#     plt.plot(df['date'], df['sunset'], label='Sunset')
#     plt.xlabel('Date')
#     plt.ylabel('Time')
#     plt.title('Sunrise and Sunset Times')
#     plt.legend()
#     plt.show()

#     # Plot azimuth angles
#     plt.figure(figsize=(10, 5))
#     plt.plot(df['date'], df['azimuth_rise'], label='Azimuth Rise')
#     plt.plot(df['date'], df['azimuth_set'], label='Azimuth Set')
#     plt.xlabel('Date')
#     plt.ylabel('Azimuth Angle')
#     plt.title('Azimuth Angles at Sunrise and Sunset')
#     plt.legend()
#     plt.show()

def main():
    location_info = collect_location_info()
    azimuth_data = calculate_azimuth_data(location_info)
    write_to_csv(azimuth_data)

    # plot_azimuth_data(azimuth_data)
    
