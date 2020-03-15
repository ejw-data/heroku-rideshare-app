def ride_share_calcs(start, stop):
    import openweathermapy.core as owm
    import requests
    import geopip
    #import os
    import datetime as dt
    from model import prediction_model
    from taxes import tax_model

    # Weather API
    from config import ow_api_key

    # MapQuest API
    from config import mq_api_key

    # Set geopip to look at geojson file
    #os.environ['REVERSE_GEOCODE_DATA'] = 'Resources/Data/community_areas.geojson'

    # Form Inputs
    start_address = start     #'405 N Wabash Avenue, Chicago, IL'
    end_address = stop        #'938 W Webster Ave, Chicago, IL 60614'

    # make default app time the current time
    noncoded_time = dt.datetime.today()

    def coded_week(date_input):
        weekdays = 7     

        coded_week = []
        for i in range(weekdays):
            if i == date_input-1:
                coded_week.append(1)
            else:
                coded_week.append(0)
            
        return coded_week

    # List of Coded Weekday Values
    start_date = dt.datetime.today().weekday()
    coded_week = coded_week(start_date)

    def coded_date(list, type):
        if type == 'months':
            time_frame = 12
            list_var = 0
            
        elif type == 'days':
            if list[0] in [1,3,5,7,8,10,12]:
                time_frame = 31
                list_var= 1
            
            if list[0] in [4,6,9,11]:
                time_frame = 30
                list_var= 1
            
            if list[0] in [2]:
                time_frame = 28
                list_var= 1
            
            
        elif type == 'hr-mins':
            time_frame = 96
            hours = 24
            hour = list[2]
            minute = list[3]
            quarter_hour = []
            

            for j in range(hours):
                if j == hour:
                    if minute >=45:
                        quarter_hour += [0,0,0,1]
                    elif minute >=30:
                        quarter_hour += [0,0,1,0]
                    elif minute >=15:
                        quarter_hour += [0,1,0,0]
                    else:
                        quarter_hour += [1,0,0,0]
                else:
                    quarter_hour += [0,0,0,0]

        
        if type in ['months', 'days']:
            coded_time = []
            for i in range(time_frame):
                if i == list[list_var]-1:
                    coded_time.append(1)
                else:
                    coded_time.append(0)
            return coded_time
        else:
            return quarter_hour

    # List of Coded Months and Days (96 Quarter Hour Periods)
    noncoded_month = noncoded_time.month
    noncoded_day = noncoded_time.day
    noncoded_hour = noncoded_time.hour
    noncoded_minute = noncoded_time.minute
    date_list = [noncoded_month, noncoded_day, noncoded_hour, noncoded_minute]
    coded_dates = coded_date(date_list, 'months')+coded_date(date_list, 'days')+coded_date(date_list, 'hr-mins')

    # Extract Map Information - variables added to model
    url = f'https://www.mapquestapi.com/directions/v2/optimizedRoute?json={{"locations":["{start_address}","{end_address}"]}}&outFormat=json&key={mq_api_key}'
    format = "json"

    street_directions = requests.get(f"{url}").json()
    distance = street_directions["route"]['distance']
    duration = street_directions["route"]["time"]
    start_longitude = street_directions["route"]["boundingBox"]["lr"]['lng']
    start_latitude = street_directions["route"]["boundingBox"]["lr"]['lat']
    end_longitude = street_directions["route"]["boundingBox"]["ul"]['lng']
    end_latitude = street_directions["route"]["boundingBox"]["ul"]['lat']

    def coded_community(community):
        number_communities = 77     

        coded_location = []
        for i in range(number_communities):
            if i == community-1:
                coded_location.append(1)
            else:
                coded_location.append(0)
            
        return coded_location

    # List of Coded Start Community
    #start_geo = int(geopip.search(start_longitude, start_latitude)['area_num_1'])
    #coded_start_community = coded_community(start_geo)

    # List of Coded End Community
    #end_geo = int(geopip.search(end_longitude, end_latitude)['area_num_1'])
    #coded_end_community = coded_community(end_geo)

    # Retrieve Weather Data
    settings = {"units": "imperial", "appid": ow_api_key}
    location = (start_latitude, start_longitude)
    current_weather_chicago = owm.get_current(location, **settings)
    actual_temp = current_weather_chicago('main.temp')
    feels_temp = current_weather_chicago('main.feels_like')
    pressure = current_weather_chicago('main.pressure')
    humidity = current_weather_chicago('main.humidity')

    # Precipitation calc
    # https://openweathermap.org/weather-conditions
    # https://openweathermap.org/weather-data

    # weather code converted into average precipitation value
    rain_light_precipitation = [200, 230, 231, 300, 301, 310, 311, 500, 520]
    rain_moderate_precipitation = [201, 232, 302, 312, 313, 321, 501, 521]
    rain_intense_precipitation = [202, 314, 502, 503, 504, 531]

    weather_code = current_weather_chicago('cod')

    if weather_code in rain_light_precipitation:
        rain = 0.1
    elif weather_code in rain_moderate_precipitation:
        rain = 1.0
    elif weather_code in rain_intense_precipitation:
        rain = 2.0
    else:
        rain = 0.0

    snow_light_precipitation = [600, 620]
    snow_moderate_precipitation = [601, 612, 613, 615, 616, 621]
    snow_intense_precipitation = [602, 611, 622]

    if weather_code in snow_light_precipitation:
        snow = 0.1
    elif weather_code in snow_moderate_precipitation:
        snow = 1.0
    elif weather_code in snow_intense_precipitation:
        snow = 2.0
    else:
        snow = 0.0

    weather = [actual_temp, feels_temp, pressure, humidity, rain, snow]

    # Need Variables:  duration, distance, rain_1h, PCA_76, DCA_76, temp, November, PCA_56, DCA_56, snow_1h
    # Variables Translated:  duration, distance, rain, start_geo[75], end_geo[75], actual_temp, coded_date[10], start_geo[55], end_geo[55], snow
    #ML_input_original = [duration, distance, start_geo, end_geo, start_longitude, start_latitude, end_longitude, end_latitude] + coded_week + coded_date + coded_start_community + coded_end_community + weather

    #ML_input_values = [duration, distance, rain, coded_start_community[75], coded_end_community[75], actual_temp, coded_dates[10], coded_start_community[55], coded_end_community[55], snow]
    ML_input_values = [duration, distance, rain, 0, 0, actual_temp, coded_dates[10], 0, 0, snow]
 
    # Base fare
    base_fare = prediction_model(ML_input_values)

    # City-wide Tax Surcharge
    base_surcharge = 1.25

    # Additional Tax Surcharges
    start_fare = tax_model(start_longitude, start_latitude)
    end_fare = tax_model(end_longitude, end_latitude)

    if start_fare >= end_fare:
        special_surcharge = start_fare
    else:
        special_surcharge = end_fare

    total_fare = [base_fare, base_surcharge, special_surcharge]
    
    return total_fare