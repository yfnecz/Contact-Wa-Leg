import geopandas as gpd, os
from shapely.geometry import Point

class LegislativeDistrictLocator:
    def __init__(self, shapefile_path="Washington_State_Legislative_Districts_2024.shp"):
        # Load the shapefile once during initialization
        dir = os.path.dirname(__file__)
        shapefile_path = os.path.join(dir, "Legislative", shapefile_path)
        self.districts = gpd.read_file(shapefile_path)
        
        # Convert to WGS84 if not already in lat/lon
        if self.districts.crs != "EPSG:4326":
            self.districts = self.districts.to_crs(epsg=4326)

    def get_district(self, lat, lon):
        """
        Returns the district info for a given (lat, lon) pair.
        """
        point = Point(lon, lat)  # Note: (lon, lat) order for shapely
        match = self.districts[self.districts.contains(point)]

        if not match.empty:
            return match.iloc[0].to_dict()
        else:
            return None
