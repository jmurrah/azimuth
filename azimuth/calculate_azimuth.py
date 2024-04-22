from astral.location import Location
from astral.sun import sun
import astral
import csv
from datetime import datetime, timedelta


def get_location_info() -> astral.LocationInfo:
    name = input("Enter the name of the location: ")
    region = input("Enter the region of the location: ")
    timezone = input("Enter the timezone of the location: ")
    latitude = float(input("Enter the latitude of the location: "))
    longitude = float(input("Enter the longitude of the location: "))

    return astral.LocationInfo(
        name=name,
        region=region,
        timezone=timezone,
        latitude=latitude,
        longitude=longitude,
    )


def get_date_range() -> tuple[datetime, datetime]:
    start_date = datetime.strptime(
        input("Enter the start date (YYYY-MM-DD): "), "%Y-%m-%d"
    )
    end_date = datetime.strptime(input("Enter the end date (YYYY-MM-DD): "), "%Y-%m-%d")

    return start_date, end_date


def get_azimuth_data(
    location_info: astral.LocationInfo, date: datetime
) -> dict[str, str]:
    sun_data = sun(location_info.observer, date=date, tzinfo=location_info.timezone)
    loc = Location(location_info)
    azimuth_rise = loc.solar_azimuth(sun_data["sunrise"])
    azimuth_set = loc.solar_azimuth(sun_data["sunset"])

    return {
        "date": date.strftime("%b. %d, %Y"),
        "sunrise": f"{sun_data['sunrise'].time().strftime('%I:%M:%S')} a.m.",
        "sunset": f"{(sun_data['sunset'] - timedelta(hours=12)).time().strftime('%I:%M:%S')} p.m.",
        "azimuth_sunrise": f"{round(azimuth_rise, 2)}\u00B0",
        "azimuth_sunset": f"{round(azimuth_set, 2)}\u00B0",
    }


def calculate_azimuth_data(location_info: astral.LocationInfo) -> list[dict[str, str]]:
    start_date, end_date = get_date_range()
    delta = timedelta(days=1)
    date = start_date
    azimuth_data = []

    while date <= end_date:
        azimuth_data.append(get_azimuth_data(location_info, date))
        date += delta

    return azimuth_data


def write_to_csv(
    azimuth_data: list[dict[str, str]], location_info: astral.LocationInfo
):
    with open("azimuth_data.csv", mode="w", newline="") as file:
        file.write(
            "Latitude: "
            + str(location_info.latitude)
            + ",Longitude: "
            + str(location_info.longitude)
            + "\n"
        )
        writer = csv.DictWriter(file, fieldnames=azimuth_data[0].keys())
        writer.writeheader()
        writer.writerows(azimuth_data)


def main():
    location_info = get_location_info()
    azimuth_data = calculate_azimuth_data(location_info)
    write_to_csv(azimuth_data, location_info)
