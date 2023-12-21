import math

from sun_angle import sunae
import matplotlib.pyplot as plt
import numpy as np

year = 2023
day = 355  # 21 dec
hour = 23.75
lat = 45.627031343394115  # Latitude in degrees
long = 25.489147381233582  # Longitude in degrees

max_roof_angle = 30
slope_angle = 0


def roof_angle(azimuth, max_roof_angle):
    azimuth = np.array(azimuth)
    return np.arctan(np.tan(max_roof_angle*np.pi/180) * np.cos(azimuth*np.pi/180))*180/np.pi


if __name__ == "__main__":
    x = np.linspace(0, 24, 24 * 6 + 1)
    for i in range(4):
        e_list = []
        a_list = []
        for hour in x:
            azimuth, elevation = sunae(year, day - math.floor(365/4*i), hour, lat, long)
            e_list.append(elevation)
            a_list.append(azimuth)

        plt.scatter(a_list, e_list, s=1)

    plt.scatter(a_list, roof_angle(a_list, max_roof_angle), s=1)
    plt.plot([0, 360], [0, 0], color="black")
    plt.plot([0, 360], [90, 90], color="black")
    plt.plot([0, 360], [-90, -90], color="black")

    plt.show()

