import csv
from datetime import datetime

import matplotlib.pyplot as plt
from numpy import finfo

filename = "data\\sitka_weather_2021_simple.csv"

with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    for index, column_header in enumerate(header_row):
        print(index, column_header)

    # Get dates and high temperatures from this file. (index 2 & 5)
    dates, highs, lows = [], [], []
    for row in reader:
        current_date = datetime.strptime(row[2], "%Y-%m-%d")
        high = int(row[4])
        low = int(row[5])
        dates.append(current_date)
        highs.append(high)
        lows.append(low)

# Plot the high temperatures.
plt.style.use("bmh")
fig, ax = plt.subplots()
ax.plot(dates, highs, c="red")
ax.plot(dates, lows, c="blue")
plt.fill_between(dates, highs, lows, facecolor="blue", alpha=0.1)

# Formal plot.
plt.title("Daily high and low temperatures - 2021", fontsize=24)
plt.xlabel("", fontsize=16)
fig.autofmt_xdate()
plt.ylabel("Temperature (F)", fontsize=16)
plt.tick_params(axis="both", which="major", labelsize=16)

plt.show()

# print(highs)
