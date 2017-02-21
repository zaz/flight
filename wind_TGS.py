import numpy as np
import plotly
import plotly.plotly as py
from plotly.graph_objs import *

# FIXME: Graph generated shows that as wind speed increases, the angle at which
# it increases ground speed increases past 90deg.  This is clearly incorrect.

def cart2pol(x, y):
    theta = np.rad2deg(np.arctan2(y, x))
    r = np.hypot(x, y)
    return r, theta

def pol2cart(r, theta):
    x = r * np.sin(np.deg2rad(theta))
    y = r * np.cos(np.deg2rad(theta))
    return x, y

def vec(r, theta):
    return np.array(pol2cart(r, theta))


class Plane:
    def __init__(self, U_wind, D_wind):
        '''Speed and direction of wind.  All angles are relative to course.
        This is analagous to a plane always travelling north.'''
        self.wind = vec(U_wind, D_wind)

    def get_heading(self):
        crab_component = -self.wind[1]  # XXX x?
        course_component = np.sqrt(1 - self.wind[1]**2)
        return np.array([crab_component, course_component])

    def get_groundspeed(self):
        return self.get_heading() + self.wind


def wind_correction(wind, angle):
    '''Takes wind speed and wind - course angle'''
    return -np.rad2deg(np.arcsin(wind*np.sin(np.deg2rad(angle))))

def groundspeed(wind, angle):
    '''Takes wind speed and heading - wind angle.
    Returns groundspeed / heading'''
    return np.sqrt(1 + wind**2 - 2 * wind * np.cos(np.deg2rad(angle)))

def groundspeed_for_course(wind, angle):
    '''Takes wind speed and course - wind angle.
    Returns groundspeed / heading'''
    wind *= 0.01
    return groundspeed(wind, angle + wind_correction(wind, angle))


data = Data([
    Contour(
        z = np.fromfunction(groundspeed_for_course, (46, 361)),
        contours=dict(
            #start=0.5,
            #end=1.5,
            #size=.05,
        )
    )
])


layout = Layout(
    title='Ground Speed',
    orientation=-90,
    xaxis=dict(
        autotick=False,
        ticks='outside',
        tick0=0,
        dtick=10
    )
)
fig = Figure(data=data, layout=layout)

if __name__ == "__main__":
    plotly.offline.plot(fig)
