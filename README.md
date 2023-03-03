# Food Bank Match
#### Video Demo: <https://youtu.be/lrLEV7UXUmI>
#### Description:
This project seeks to address the topic of food rescue. Many potential donors lack the necessary information to make donations.
The program first solicits input from the user to include their location, the maximum distance they are willing to travel, and a list of items they are willing to donate.
The ```get_coordinates``` function converts the name of the city to a pair of coordinates, which will be used later in the program to compute distances between food bank matches and the user location.
A list of donations is generated from the ```get_donations``` function, which implements a ```while``` loop to solicit input from the user, item by item, until they enter 'c' to escape the loop and the program stores the items entered in the list of donations.
Two calls to the UK foodbank API are made with the ```call_api``` function, returning a dictionary of foodbanks and their needs, and a dictionary of foodbanks and their locations.
```get_matches``` takes as arguments the list of donations and the dictionary of foodbank needs, loops through both data structures, looking for matches between items in the donation list and items in the needs dictionary, and returns a new list of foodbanks where items in the list of donations match the needs of the foodbank.
The program will then loop through the list of matches, compute the distance between those matches and the user location, and return a new list of matches where the distance between the user location and the match is less than the maximum distance input by the user.
During this loop, the program will also split the coordinates in the location dictionary and create two new lists, one consisting of latitudes and the other of longitudes, with which the program will use as parameters for plot these locations on a map output to the user.
Plotly will generate a map of Europe and plot the matches using the lists of longitudes and latitudes and will also provide the capability to hover over each plot to view the names of the foodbanks.
