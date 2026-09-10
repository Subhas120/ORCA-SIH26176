WEATHER = {
    "wind_speed": 22,
    "wind_direction": 250,
    "rain_probability": 30,
    "visibility": 8,
    "temperature": 28.0,
    "wave_height": 1.2,
    "wave_period": 7,
    "storm": False,
    "cyclone": False,
    "lightning": False,
    "warning": False,
    "warning_type": None,
    "warning_severity": None,
}

# Small demo polygon near Kochi. Replace with authoritative marine-zone GeoJSON.
RESTRICTED_ZONES = [
    {
        "id": "demo-restricted-1",
        "name": "Demo Restricted Marine Zone",
        "type": "restricted",
        "penalty": 1000,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [76.28, 9.93],
                [76.285, 9.93],
                [76.285, 9.935],
                [76.28, 9.935],
                [76.28, 9.93],
            ]]
        }
    }
]

PFZS = [
    {"id": "PFZ-1", "name": "PFZ Alpha", "latitude": 9.95, "longitude": 76.30},
    {"id": "PFZ-2", "name": "PFZ Bravo", "latitude": 9.94, "longitude": 76.28},
    {"id": "PFZ-3", "name": "PFZ Charlie", "latitude": 9.99, "longitude": 76.33},
]
