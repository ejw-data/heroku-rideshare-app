# Rideshare-Flask-App
#### This project only contains the web interface for an app and does not contain the files used to develop the machine learning algorithm.  The ML algorithm was developed as a separate project and the parameters of the model were stored in a pickle file and called in model.py.

#### This app does not use a database.  The inputs to the machine learning algorithm are pulled from the server time and API calls to mapquest, openweather, and google locations.  These inputs provide estimators for the time, date, start longitude, end longitude, estimated directions with distance and time estimates, and a variety of weather data.  

##### The inputs were also manipulated to determine the community that the ride began and ended in (reverse geocoding) and to determine the taxes applied based on the Chicago tax regions (longitude/latitude calculation).
