import matplotlib as mpl
import pandas as pd
from matplotlib import pyplot as plt

world_data = pd.DataFrame()
us_data = pd.DataFrame()
mpl.rcParams.update(mpl.rcParamsDefault)


def download_data():
    global world_data, us_data

    world_data = pd.read_csv(
        "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISan"
        "dData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_glo"
        "bal.csv&filename=time_series_covid19_confirmed_global.csv")

    us_data = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')


def confirmed_cases():
    fig, ax = plt.subplots()
    ax.patch.set_edgecolor('black')
    ax.patch.set_linewidth('1')
    ax.margins(x=0.001)
    fig.dpi = 100

    # to update the style so I dont have to reset the cell each time I want a style change
    plt.style.use('seaborn-darkgrid')

    # .plot method is the same as plt.plot(), wrapper
    world_data.iloc[:, 4:].sum().plot(label="Worldwide Total Cases", figsize=(10, 6), fontsize=13)
    world_data.iloc[225, 4:].plot(label="U.S. Total Cases")

    for line, name in zip(ax.lines, world_data.columns):
        y = line.get_ydata()[-1]
        ax.annotate(str(y) + "\n " + world_data.columns[-1], xy=(1, y), xytext=(6, 0), color=line.get_color(),
                    xycoords=ax.get_yaxis_transform(), textcoords="offset points",
                    size=14, va="center")

    plt.title("Confirmed Cases of COVID-19", fontsize=22)
    plt.xlabel("Date", fontsize=15)
    plt.ylabel("Number of cases", fontsize=15)

    plt.legend()
    plt.savefig("corona/world_cases.png")
    return "corona/world_cases.png"


def top10():
    largest = world_data.iloc[:, -1]
    largest = largest.nlargest(10).keys()

    fig, ax = plt.subplots()
    fig.figsize = (10, 6)
    ax.patch.set_edgecolor('black')
    ax.patch.set_linewidth('1')
    ax.margins(x=0.001)
    fig.dpi = 100

    for country in largest:
        world_data.iloc[country, 4:].plot(label=world_data.loc[country, "Country/Region"] + ": " + str(world_data.iloc[country, -1]),
                                     figsize=(10, 6), fontsize=13)

    plt.style.use('seaborn-darkgrid')
    plt.title("Top 10 Countries by number of cases", fontsize=22)
    plt.xlabel("Date", fontsize=15)
    plt.ylabel("Number of cases", fontsize=15)

    plt.legend()
    plt.savefig("corona/top_10.png")
    return "corona/top_10.png"


def world_growth_rate():
    sums = world_data.iloc[:, 4:].sum()
    rates = []
    for day in range(len(sums) - 1):
        rates.append(sums[day + 1] / sums[day])

    test2 = pd.Series(rates, index=world_data.columns[5:])

    fig, ax = plt.subplots()
    fig.figsize = (10, 6)
    ax.patch.set_edgecolor('black')
    ax.patch.set_linewidth('1')
    fig.dpi = 100

    plt.style.use('seaborn-darkgrid')
    plt.title("Daily Growth Rate (World)", fontsize=22)
    plt.xlabel("Date", fontsize=18, color='blue')
    plt.ylabel("Growth rate", fontsize=15, color='blue')

    test2.plot(fontsize=13, color='green', figsize=(10, 6))

    newest_date = f"{world_data.columns[-2]} to\n {world_data.columns[-1]}"
    for line, name in zip(ax.lines, world_data.columns):
        y = line.get_ydata()[-1]
        ax.annotate(str(round(y, 4)) + "\n " + newest_date, xy=(1, y), xytext=(6, 0), color=line.get_color(),
                    xycoords=ax.get_yaxis_transform(), textcoords="offset points",
                    size=14, va="center")

    plt.savefig('corona/growth_rate.png')
    return "corona/growth_rate.png"


def usa_growth_rate():
    sums = world_data.iloc[225, 4:]
    rates = []
    for day in range(len(sums) - 1):
        rates.append(sums[day + 1] / sums[day])

    test2 = pd.Series(rates, index=world_data.columns[5:])

    fig, ax = plt.subplots()
    fig.figsize = (10, 6)
    ax.patch.set_edgecolor('black')
    ax.patch.set_linewidth('1')
    fig.dpi = 100

    plt.style.use('seaborn-darkgrid')
    plt.title("Daily Growth Rate (USA)", fontsize=22)
    plt.xlabel("Date", fontsize=18, color='blue')
    plt.ylabel("Growth rate", fontsize=15, color='blue')

    test2.plot(fontsize=13, color='green', figsize=(10, 6))

    newest_date = f"{world_data.columns[-2]} to\n {world_data.columns[-1]}"
    for line, name in zip(ax.lines, world_data.columns):
        y = line.get_ydata()[-1]
        ax.annotate(str(round(y, 4)) + "\n " + newest_date, xy=(1, y), xytext=(6, 0), color=line.get_color(),
                    xycoords=ax.get_yaxis_transform(), textcoords="offset points",
                    size=14, va="center")

    plt.savefig('corona/growth_rate_usa.png')
    return "corona/growth_rate_usa.png"


def daily_cases_w():
    sums2 = world_data.iloc[:, 4:].sum()
    daily_cases = []
    for day in range(len(sums2) - 1):
        daily_cases.append(sums2[day + 1] - sums2[day])

    labels = []

    for i in range(len(daily_cases)):
        if i % 4 == 0:
            labels.append(world_data.columns[5 + i])
        else:
            labels.append('')

    labels[-1] = world_data.columns[-1]

    fig, ax = plt.subplots()
    ax.patch.set_edgecolor('black')
    ax.patch.set_linewidth('1')
    fig.dpi = 100
    plt.style.use('seaborn-darkgrid')

    daily_cases = pd.Series(daily_cases, labels)
    daily_cases.plot(kind='bar', width=0.85, label=f"{world_data.columns[-1]}: {daily_cases[-1]} cases reported",
                     figsize=(10, 7))

    plt.title("Worldwide Daily Cases", fontsize=22)
    plt.xlabel("Date", fontsize=18, color='blue')
    plt.ylabel("Number of Cases", fontsize=15, color='blue')

    plt.legend()
    plt.savefig('corona/daily_cases.png')
    return "corona/daily_cases.png"


def daily_cases_us():
    usa_cases = world_data.iloc[225, 4:]
    daily_cases = []
    for day in range(len(usa_cases) - 1):
        daily_cases.append(usa_cases[day + 1] - usa_cases[day])

    labels = []

    for i in range(len(daily_cases)):
        if i % 4 == 0:
            labels.append(world_data.columns[5 + i])
        else:
            labels.append('')

    labels[-1] = world_data.columns[-1]

    fig, ax = plt.subplots()
    ax.patch.set_edgecolor('black')
    ax.patch.set_linewidth('1')
    fig.dpi = 100
    mpl.rcParams.update(mpl.rcParamsDefault)
    plt.style.use('seaborn-darkgrid')

    daily_cases = pd.Series(daily_cases, labels)
    daily_cases.plot(kind='bar', width=0.85, label=f"{world_data.columns[-1]}: {daily_cases[-1]} cases reported",
                     figsize=(10, 7))

    plt.title("US Daily Cases", fontsize=22)
    plt.xlabel("Date", fontsize=18, color='blue')
    plt.ylabel("Number of Cases", fontsize=15, color='blue')

    plt.legend()
    plt.savefig('corona/daily_cases_usa.png')
    return "corona/daily_cases_usa.png"


download_data()
confirmed_cases()
top10()
world_growth_rate()
usa_growth_rate()
daily_cases_w()
daily_cases_us()
