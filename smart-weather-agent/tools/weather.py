
"""External geocoding and weather tools for the travel assistant."""

from datetime import date
from typing import Any

import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# Reuse connections and apply finite timeouts to external requests.
SESSION = requests.Session()
TIMEOUT = (3.05, 15)


class WeatherToolError(RuntimeError):
    """Raised when an external weather operation fails."""


def _get_json(url: str, params: dict[str, Any]) -> dict[str, Any]:
    """Fetch JSON and convert network/API failures to a safe error."""
    try:
        response = SESSION.get(
            url,
            params=params,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()

    except requests.RequestException as exc:
        raise WeatherToolError(
            "The weather service is temporarily unavailable."
        ) from exc
    except ValueError as exc:
        raise WeatherToolError(
            "The weather service returned invalid JSON."
        ) from exc

    if not isinstance(data, dict):
        raise WeatherToolError("Unexpected API response format.")

    return data


def geocode_location(city: str) -> dict[str, Any]:
    """Resolve a city name into coordinates and a display name."""
    city = city.strip()

    if not city or len(city) > 120:
        raise ValueError("City must contain 1–120 characters.")

    data = _get_json(
        GEOCODING_URL,
        {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        },
    )

    results = data.get("results") or []
    if not results:
        raise WeatherToolError(
            f"No matching location found for '{city}'."
        )

    place = results[0]

    return {
        "name": place.get("name", city),
        "admin1": place.get("admin1"),
        "country": place.get("country"),
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "timezone": place.get("timezone", "auto"),
    }


def get_weather(city: str, travel_date: str) -> dict[str, Any]:
    """
    Gemini-callable tool.

    Resolve a city, retrieve its forecast for the requested date,
    and return a compact, normalized observation.
    """
    try:
        requested_date = date.fromisoformat(travel_date)
    except ValueError as exc:
        raise ValueError(
            "travel_date must use YYYY-MM-DD format."
        ) from exc

    location = geocode_location(city)

    data = _get_json(
        FORECAST_URL,
        {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "daily": [
                "weather_code",
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_probability_max",
                "precipitation_sum",
                "wind_speed_10m_max",
            ],
            "timezone": location["timezone"],
            "start_date": travel_date,
            "end_date": travel_date,
        },
    )

    daily = data.get("daily") or {}
    dates = daily.get("time") or []

    if travel_date not in dates:
        raise WeatherToolError(
            "No forecast is available for that date. "
            "The date may be outside the provider's forecast range."
        )

    index = dates.index(travel_date)

    def value(key: str) -> Any:
        values = daily.get(key)
        if not isinstance(values, list) or index >= len(values):
            return None
        return values[index]

    return {
        "location": location,
        "travel_date": travel_date,
        "timezone": data.get("timezone"),
        "temperature_max_c": value("temperature_2m_max"),
        "temperature_min_c": value("temperature_2m_min"),
        "weather_code": value("weather_code"),
        "precipitation_probability_max_percent": value(
            "precipitation_probability_max"
        ),
        "precipitation_sum_mm": value("precipitation_sum"),
        "wind_speed_max_kmh": value("wind_speed_10m_max"),
        "source": "Open-Meteo",
    }