# ship-tracker
Track cruise ship GPS locations as reported.

This project was initiated to track a friend's cruise itinerary relative to a nearby hurricane.

![image](https://github.com/drintoul/ship-tracker/assets/40215603/75d50726-2f56-41ec-9ac4-cb4f031a4ab9)

Ship is in blue, hurricane in orange.

# Solution Approach
* This Python program uses the request library to retrieve a ship's location at one hour intervals from a public website
* BeautifulSoup and Regex are used to extract desired GPS coordinates and other information
* Actual reporting time using relative references such as "... reported 43 minutes ago"
* For my personal use, I write this information to my MySQL database but this functionality is disabled for GitHub
