from datetime import datetime
from unittest.mock import MagicMock, mock_open, patch

import astral
import pytest

from azimuth.calculate_azimuth import (
    calculate_azimuth_data,
    get_azimuth_data,
    get_date_range,
    get_input,
    get_location_info,
    main,
    write_to_csv,
)


def test_get_input():
    prompt = return_value = "test"
    with patch("builtins.input", return_value=return_value):
        assert get_input(prompt) == return_value


def test_get_location_info(mock_get_input):
    inputs = {
        "name": "New York",
        "region": "New York",
        "timezone": "America/New_York",
        "latitude": "40.7128",
        "longitude": "74.0060",
    }
    mock_get_input.side_effect = inputs.values()

    assert get_location_info() == astral.LocationInfo(**inputs)


def test_get_date_range(mock_get_input):
    inputs = {
        "2024-01-01": datetime.strptime("2024-01-01", "%Y-%m-%d"),
        "2024-01-31": datetime.strptime("2024-01-31", "%Y-%m-%d"),
    }
    mock_get_input.side_effect = inputs.keys()

    x = get_date_range()
    assert x == tuple(inputs.values())


def test_get_azimuth_data(mock_location, mock_sun):
    mock_date = MagicMock(strftime=MagicMock(return_value="Jan. 01, 2024"))
    mock_sun.return_value = {
        "sunrise": datetime.strptime("07:20:00", "%H:%M:%S"),
        "sunset": datetime.strptime("17:20:00", "%H:%M:%S"),
    }
    mock_location.return_value.solar_azimuth.side_effect = [119.78, 240.22]

    assert get_azimuth_data(MagicMock(), mock_date) == {
        "date": "Jan. 01, 2024",
        "sunrise": "07:20:00 a.m.",
        "sunset": "05:20:00 p.m.",
        "azimuth_sunrise": "119.78°",
        "azimuth_sunset": "240.22°",
    }


def test_calculate_azimuth_data(mock_get_date_range, mock_get_azimuth_data):
    location_info = astral.LocationInfo(
        name="New York",
        region="New York",
        timezone="America/New_York",
        latitude=40.7128,
        longitude=74.0060,
    )
    mock_get_date_range.return_value = (
        datetime.strptime("2024-01-01", "%Y-%m-%d"),
        datetime.strptime("2024-01-31", "%Y-%m-%d"),
    )
    data = {
        "date": "Jan. 01, 2024",
        "sunrise": "07:20:00 a.m.",
        "sunset": "05:20:00 p.m.",
        "azimuth_sunrise": "119.78°",
        "azimuth_sunset": "240.22°",
    }
    mock_get_azimuth_data.return_value = data

    azimuth_data = calculate_azimuth_data(location_info)
    assert len(azimuth_data) == 31
    assert azimuth_data[0] == data


def test_write_to_csv():
    azimuth_data = [
        {
            "date": "Jan. 01, 2022",
            "sunrise": "07:20:00 a.m.",
            "sunset": "05:20:00 p.m.",
            "azimuth_sunrise": "119.78°",
            "azimuth_sunset": "240.22°",
        },
    ]
    location_info = astral.LocationInfo(
        name="New York",
        region="New York",
        timezone="America/New_York",
        latitude=40.7128,
        longitude=74.0060,
    )

    file = mock_open()
    with patch("builtins.open", file), patch("csv.DictWriter") as mock_dict_writer:
        write_to_csv(azimuth_data, location_info)
        file().write.assert_called_once_with(
            "Latitude: "
            + str(location_info.latitude)
            + ",Longitude: "
            + str(location_info.longitude)
            + "\n"
        )
        mock_dict_writer.assert_called_once_with(
            file(), fieldnames=azimuth_data[0].keys()
        )
        mock_dict_writer().writeheader.assert_called_once()
        mock_dict_writer().writerows.assert_called_once_with(azimuth_data)


def test_main(mock_get_location_info, mock_calculate_azimuth_data, mock_write_to_csv):
    main()
    mock_get_location_info.assert_called_once()
    mock_calculate_azimuth_data.assert_called_once()
    mock_write_to_csv.assert_called_once()


@pytest.fixture
def mock_get_location_info():
    with patch("azimuth.calculate_azimuth.get_location_info") as mock:
        yield mock


@pytest.fixture
def mock_calculate_azimuth_data():
    with patch("azimuth.calculate_azimuth.calculate_azimuth_data") as mock:
        yield mock


@pytest.fixture
def mock_write_to_csv():
    with patch("azimuth.calculate_azimuth.write_to_csv") as mock:
        yield mock


@pytest.fixture
def mock_get_date_range():
    with patch("azimuth.calculate_azimuth.get_date_range") as mock:
        yield mock


@pytest.fixture
def mock_get_azimuth_data():
    with patch("azimuth.calculate_azimuth.get_azimuth_data") as mock:
        yield mock


@pytest.fixture
def mock_location():
    with patch("azimuth.calculate_azimuth.Location") as mock:
        yield mock


@pytest.fixture
def mock_sun():
    with patch("azimuth.calculate_azimuth.sun") as mock:
        yield mock


@pytest.fixture
def mock_get_input():
    with patch("azimuth.calculate_azimuth.input") as mock:
        yield mock
