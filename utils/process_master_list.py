# Collected a list of coordinates from http://bulk.openweathermap.org/sample/ after little cleaning.
# Assumption : Scope is US only.

import json
import sys


def create_master_coordinates():
    """Create a list of dict with coordinates - lon,lat"""
    try:
        lookup_file = "./lookup_data/usa_coordinates.json"
        with open(lookup_file, "r", encoding="utf-8") as file:
            master_recs = []
            for rec in json.load(file):
                rec.pop("city")
                rec.pop("country")
                master_recs.append(rec)
        return master_recs
    except FileNotFoundError:
        sys.exit(1)
