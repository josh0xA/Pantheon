# IPGeolocation.py
from ip2geotools.databases.noncommercial import DbIpCity

class IPGeolocation:
    @staticmethod
    def get_location(ip_address):
        try:
            response = DbIpCity.get(ip_address, api_key='free')
            return {
                'ip': response.ip_address,
                'city': response.city,
                'region': response.region,
                'country': response.country,
                'latitude': response.latitude,
                'longitude': response.longitude
            }
        except Exception as e:
            print(f"Error getting location for IP {ip_address}: {str(e)}")
            return None
