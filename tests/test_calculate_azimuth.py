from unittest.mock import patch, MagicMock
import pytest
from azimuth.calculate_azimuth import main, get_location_info, calculate_azimuth_data, write_to_csv


# def test_collect_location_info():
#     pass


def test_main(mock_get_location_info, mock_calculate_azimuth_data, mock_write_to_csv):
    main()
    mock_get_location_info.assert_called_once()
    mock_calculate_azimuth_data.assert_called_once()
    mock_write_to_csv.assert_called_once()


def test_get_location_info(monkeypatch):
    inputs = iter(['Test Name', 'Test Region', 'America/Denver', '50.555', '-39.543'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    location_info = get_location_info()
    # breakpoint()
    assert 1 == location_info


@pytest.fixture
def mock_get_location_info():
    with patch('azimuth.calculate_azimuth.get_location_info') as mock:
        yield mock

@pytest.fixture
def mock_calculate_azimuth_data():
    with patch('azimuth.calculate_azimuth.calculate_azimuth_data') as mock:
        yield mock

@pytest.fixture
def mock_write_to_csv():
    with patch('azimuth.calculate_azimuth.write_to_csv') as mock:
        yield mock