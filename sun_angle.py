import math


"""
This subroutine calculates the local azimuth and elevation of the sun at a specific location
 and time using an approximation to equations used to generate tables in The Astronomical Almanac. 
 Refraction correction is added so sun position is the apparent one.
 
The Astronomical Almanac, U.S. Gov't Printing Office, Washington, DC (1985)

input parameters
    year = year (e.g., 1986)
    day = day of year (e.g., Feb. 1 = 32)
    hour = hours plus fraction in UT (e.g., 8:30 A.M. eastern daylight time is equal to 8.5 
        + 5 (5 hours west of Greenwich) - 1 (for daylight savings time correction)
    lat = latitude in degrees (north is positive) c
    long = longitude in degrees (east is positive)
    
output parameters
    a = sum azimuth angle (measured east from north, 0 to 360°)
    e = sun elevation angle (degs) plus others, but note the units indicated before return
"""
def sunae(year, day, hour, lat, long):
    # work with real variables and define some constants, including one to change between degs and radians
    twopi, pi, rad = 6.2831853, 3.1415927, 0.017453293

    # get the current julian date (actually add 2,400,000 for input parameters jd)
    delta = year - 1949.0
    leap = int(delta / 4.0)
    jd = 32916.5 + delta * 365. + leap - day + hour / 24

    # 1st no. is mid. 0 jan 1949 minus 2.4e6: leap = leap days since 1949
    # calculate ecliptic coordinates
    time = jd - 51545.0
    # 51545.0 + 2.4e6 = noon I jan 2000

    # force mean longitude between 0 and 360 degs
    mnlong = 280.460 + 0.9856474 * time
    mnlong = mnlong % 360.0
    if mnlong < 0.0:
        mnlong += 360.0

    # mean anomaly in radians between 0 and 2*pi
    mnanom = 357.528 + 0.9856003 * time
    mnanom = mnanom % 360.0
    if mnanom < 0.0:
        mnanom += 360.0
    mnanom = mnanom * rad

    # compute ecliptic longitude and obliquity of ecliptic in radians
    eclong = mnlong + 1.915 * mnanom + 0.20 * math.sin(2.0 * mnanom)
    eclong = eclong % 360.0
    if eclong < 0.0:
        eclong += 360.0
    oblqec = 23.429 - 0.000004 * time
    eclong = eclong * rad
    oblqec = oblqec * rad

    # calculate right ascension and declination
    num = math.cos(oblqec) * math.sin(eclong)
    den = math.cos(eclong)
    ra = math.atan2(num, den)

    # force ra between 0 and 2*pi
    if den < 0:
        ra += pi
    elif num < 0:
        ra += twopi

    # dec in radians
    dec = math.asin(math.sin(oblqec) * math.sin(eclong))

    # calculate Greenwich mean sidereal time in hours
    gmst = 6.697375 + 0.0657098242 * time + hour
    # hour not changed to sidereal since 'time' includes the fractional day
    gmst = gmst % 24.0
    if gmst < 0.0:
        gmst += 24.0
    # calculate local mean sidereal time in radians
    lmst = gmst + long / 15.0
    lmst = lmst % 24.0
    if lmst < 0.0:
        lmst += 24.0
    lmst = lmst * 15.0 * rad
    ha = lmst - ra
    if ha < -pi:
        ha += twopi
    elif ha > pi:
        ha -= twopi
    lat = lat * rad
    el = math.asin(math.sin(dec) * math.sin(lat) + math.cos(dec) * math.cos(lat) * math.cos(ha))
    az = math.asin(-math.cos(dec) * math.sin(ha) / math.cos(el))
    elc = math.asin(math.sin(dec) / math.sin(lat))
    if el >= elc:
        az = pi - az
    elif el <= elc and ha > 0.0:
        az += twopi
    el = el / rad
    if el > -0.56:
        refrac = 3.51561 * (0.1594 + 0.0196 * el + 0.00002 * el ** 2) / (1.0 + 0.505 * el + 0.0845 * el ** 2)
    else:
        refrac = 0.56
    el += refrac
    az = az / rad
    lat = lat / rad
    return az, el


if __name__ == "__main__":
    # Example usage:
    year = 2023
    day = 353 # 19 dec
    hour = 23.75
    lat = 45.627031343394115  # Latitude in degrees
    long = 25.489147381233582  # Longitude in degrees

    azimuth, elevation = sunae(year, day, hour, lat, long)
    print("Azimuth:", azimuth)
    print("Elevation:", elevation)
