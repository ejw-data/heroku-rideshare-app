def tax_model(lon, lat):

    import datetime as dt

    surcharge = 0

    # O'Hare Tax
    if lat > 41.959286 and lat < 41.998335:
        if lon > (-87.933253) and lon < (-87.885189):
            surcharge = 3.75

    # Downtown Tax
    ride_time = dt.datetime.today().hour
    if ride_time >= 6 and ride_time < 22:

        if lat > 41.890892 and lat < 41.91076:
            if lon > -0.72394*(lat-41.910757)-87.655472:
                surcharge = 1.75

        if lat < 41.890892 and lat > 41.876307:
            if lon > -87.666702:
                surcharge = 1.75
        
        if lat < 41.876307 and lat > 41.867186:
            if lon > -87.643986:
                surcharge = 1.75
    
    # Navy Pier taxes - can overwrite downtown tax
    if lat > 41.88886 and lat < 41.896847:
        if lon > (-87.613413) and lon < (-87.597715):
            surcharge = 3.75

    # McCormick Taxes
    if lat < 41.855952 and lat > 41.853069:
        if lon > -87.6182:
            surcharge = 3.75

    if lat < 41.853069 and lat >41.848305:
        if lon > -87.622153:
            surcharge = 3.75

    # Midway Taxes
    if lat > 41.777956 and lat < 41.792612:
        if lon > (-87.76158) and lon < (-87.738585):
            surcharge = 3.75

    return surcharge