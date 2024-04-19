from astral.location import Location
from astral.sun import sun
from astral import LocationInfo
import csv
from datetime import datetime, timedelta


def get_date_range():
    # start_date = input("Enter the start date (YYYY-MM-DD): ")
    # end_date = input("Enter the end date (YYYY-MM-DD): ")

    start = datetime.strptime("2024-01-01", "%Y-%m-%d")
    end = datetime.strptime("2024-12-31", "%Y-%m-%d")

    return start, end


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
                "date": date,
                "sunrise": sun_data["sunrise"],
                "sunset": sun_data["sunset"],
                "azimuth_rise": str(round(azimuth_rise, 2)) + "\u00B0",
                "azimuth_set": str(round(azimuth_set, 2)) + "\u00B0",
            }
        )
        date += delta

    return azimuth_data


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


def main():
    location_info = collect_location_info()
    azimuth_data = calculate_azimuth_data(location_info)

    with open("azimuth_data.csv", mode="w") as file:
        writer = csv.DictWriter(file, fieldnames=azimuth_data[0].keys())
        writer.writeheader()
        writer.writerows(azimuth_data)


if __name__ == "__main__":
    main()
