import requests, sys
from geopy import distance
from geopy.geocoders import Nominatim
import plotly.express as px


def main():
    # Prompt user for city and convert to coordinates
    city = get_coordinates(input("Enter your city: "))

    # Prompt user for maximum distance they will travel
    max_distance = int(input("What is the greatest distance in km you are willing to travel? "))

    # Prompt user for items to donate and store in list
    donations = get_donations("Enter item(s) to be donated. Enter 'c' to exit. ")

    # Call API and store foodbank need data
    r1 = call_api('https://www.givefood.org.uk/api/2/needs/')
    needs = get_need_data(r1)

    # Call API and store foodbank location data
    r2 = call_api('https://www.givefood.org.uk/api/2/locations/')
    locations = get_location_data(r2)

    # Return list of food banks with need matching donation
    matches = get_matches(donations, needs)

    # Get coordinates and distance from origin for each match
    new_matches, matches_lat, matches_lon = [], [], []
    for match in matches:
        if match in locations.keys():
            if distance.distance(city, locations[match]).km < max_distance:
                new_matches.append(match)
                lat, lon = locations[match].split(',')
                matches_lat.append(lat)
                matches_lon.append(lon)

    # Plot food bank matches within max distance
    fig = px.scatter_geo(lat=matches_lat, lon=matches_lon,
        title='Foodbanks in Need of Your Donation(s)',
        scope = 'europe',
        hover_name=new_matches,
    )
    fig.show()


def get_coordinates(city):
    """Convert city to coordinates."""
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(city)
    return location.latitude, location.longitude


def get_donations(prompt):
    """Return list of items to donate."""
    donations = []
    while True:
        donation = input(prompt)
        if donation == 'c':
            return donations
        else:
            donations.append(donation)


def call_api(url):
    """Call API and quit program if API call unsuccessful."""
    r = requests.get(url)
    if r.status_code != 200:
        sys.exit("API request unsuccessful")
    else:
        # Convert data to readable format
        return r.json()


def get_need_data(response_data):
    """Store foodbank name and needs from API call in dictionary."""
    response_dict = {}
    for dict in response_data:
        foodbank = dict["foodbank"]["name"]
        needs = dict["needs"]
        response_dict[foodbank] = needs
    return response_dict


def get_location_data(response_data):
    """Store foodbank name and location from API call in dictionary."""
    response_dict = {}
    for dict in response_data:
        foodbank = dict["foodbank"]["name"]
        lat_long = dict["lat_lng"]
        response_dict[foodbank] = lat_long
    return response_dict


def get_matches(donations, needs):
    """Return list of foodbanks with needs matching donations."""
    matches = []
    for donation in donations:
        for foodbank in needs:
            if donation in needs[foodbank]:
                matches.append(foodbank)
    return matches


if __name__ == "__main__":
    main()