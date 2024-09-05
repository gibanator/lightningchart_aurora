from datetime import datetime
import math

import pandas as pd
import lightningchart as lc
import numpy as np

with open("license_key.txt", "r") as file:  # License key is stored in 'license_key.txt'
    key = file.read()
lc.set_license(key)

df = pd.read_csv('data/output.csv')  # read csv

# normalize phi - first calculated using np.arctan2() and then mapped to range(0, 2pi) using np.mod
df['phi_gsm'] = np.degrees(np.mod(np.arctan2(df["by_gsm"], df["bx_gsm"]), 2 * np.pi))

df.fillna(0, inplace=True)  # fill na values as 0s to avoid errors
print(df.head(), df.tail())  # print head tail of dataframe (optional)

# create lists
y_bz = df['bz_gsm'].to_list()
y_density = df['density'].to_list()
y_phi = df['phi_gsm'].to_list()
y_speed = df['speed'].to_list()
y_temp = df['temperature'].to_list()
x = df['time_tag'].to_list()


# Method to convert datetime in given format to timestamp in milliseconds (needed for lightningchart to work properly)
def convert_to_timestamp(dt_str):
    dt_format = "%Y-%m-%d %H:%M:%S.%f"

    # parse the datetime string into a datetime object
    dt = datetime.strptime(dt_str, dt_format)

    # convert datetime object to Unix timestamp
    timestamp = dt.timestamp() * 1000

    return timestamp


x_time = [convert_to_timestamp(dt) for dt in x]

dashboard = lc.Dashboard(columns=1, rows=5, theme=lc.Themes.Black)  # initialize Dashboard

chart_bz = dashboard.ChartXY(column_index=0, row_index=0, title='Bz')  # create first chart
chart_bz.get_default_x_axis().dispose()
chart_bz.add_x_axis(axis_type="linear-highPrecision").set_tick_strategy("DateTime")  # change axis to datetime format
series_bz = chart_bz.add_point_series().append_samples(  # insert data
    x_values=x_time,
    y_values=y_bz
).set_point_size(3)  # size of points (for visual purposes)

chart_phi = dashboard.ChartXY(column_index=0, row_index=1, title='Phi')
chart_phi.get_default_x_axis().dispose()
chart_phi.add_x_axis(axis_type="linear-highPrecision").set_tick_strategy("DateTime")
series_phi = chart_phi.add_point_series().append_samples(
    x_values=x_time,
    y_values=y_phi
).set_point_size(3).set_point_color_lookup_table(  # color points
    steps=[
        {'value': math.nextafter(225, 226), 'color': lc.Color('blue')},  # blue color if phi > 225
        {'value': 225, 'color': lc.Color('red')}  # red color if phi <= 225
    ],
    look_up_property='y',  # based on y value
    interpolate=True,
    percentage_values=False
)

chart_density = dashboard.ChartXY(column_index=0, row_index=2, title='Density')
chart_density.get_default_x_axis().dispose()
chart_density.add_x_axis(axis_type="linear-highPrecision").set_tick_strategy("DateTime")
series_density = chart_density.add_point_series().append_samples(
    x_values=x_time,
    y_values=y_density
).set_point_size(3).set_point_color(lc.Color('orange'))

chart_speed = dashboard.ChartXY(column_index=0, row_index=3, title='Speed')
chart_speed.get_default_y_axis().set_interval_restrictions(start_min=250)  # restriction to avoid showing na data
chart_speed.get_default_x_axis().dispose()
chart_speed.add_x_axis(axis_type="linear-highPrecision").set_tick_strategy("DateTime")
series_speed = chart_speed.add_point_series().append_samples(
    x_values=x_time,
    y_values=y_speed
).set_point_size(3).set_point_color(lc.Color('yellow'))

chart_temperature = dashboard.ChartXY(column_index=0, row_index=4, title='Temperature')
chart_temperature.get_default_y_axis().set_interval_restrictions(start_min=10000)
chart_temperature.get_default_x_axis().dispose()
chart_temperature.add_x_axis(axis_type="linear-highPrecision").set_tick_strategy("DateTime")
series_temperature = chart_temperature.add_point_series().append_samples(
    x_values=x_time,
    y_values=y_temp
).set_point_size(3).set_point_color(lc.Color('green'))

dashboard.open()
