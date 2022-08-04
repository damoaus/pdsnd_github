import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ['all', "january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
          "november", "december"]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = ""
    filter_time = ""
    month = ""
    day = ""

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while city not in CITY_DATA:
        city = input("To analyze data please select one of the following cities: Chicago ,New York City or Washington \n").lower()

    time_options = ["month", "day", "both", "none"]
    while filter_time not in time_options:
        filter_time = input("Please enter month, day, both or none to analyze \n").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    if filter_time == 'month' or filter_time == 'both':
        while month not in months:
            month = input("which month would you like to filter month? \n").lower()
        if filter_time == 'month':
            day = 'all'

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ["all", "mon", "tues", "wed", "thurs", "fri", "sat", "sun"]
    if filter_time == "day" or filter_time == 'both':
        while day not in days:
            day = input("which day would you like to filter day? Enter Mon, Tues, Weds, Thurs, Fri, Sat or Sun. \n")
        if filter_time == 'day':
            month = 'all'

    if filter_time == 'none':
        month = 'all'
        day = 'all'

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    "Updating the dataframe to include a month column if filtered by month"
    if month != 'all':
        month = months.index(month)
        df = df[df['month'] == month]

    "Creating dictionary to change shorthand into long form"
    weekday_dic = {'mon': 'Monday',
                   'tues': 'Tuesday',
                   'wed': 'Wednesday',
                   'thurs': 'Thursday',
                   'fri': 'Friday',
                   'sat': 'Saturday',
                   'sun': 'Sunday'}

    if day != 'all':
        df = df[df['day_of_week'] == weekday_dic[day]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    popular_month = months[df['month'].mode()[0]].capitalize()

    # TO DO: display the most common day of week

    popular_day = df['day_of_week'].mode()[0]
    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    print('Most popular month was: {} \nMost popular day was {} \nMost popular hour was {} \n'.format(popular_month,
                                                                                                      popular_day,
                                                                                                      popular_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_s_station = df['Start Station'].mode()[0]

    # TO DO: display most commonly used end station
    popular_e_station = df['End Station'].mode()[0]

    # TO DO: display most frequent combination of start station and end station trip
    combination_station = df.groupby('Start Station')['End Station'].value_counts().idxmax()
    combination_station_s = combination_station[0]
    combination_station_e = combination_station[1]
    print(
        'The most popular start station was: {}\nThe most popular end station was: {}\nThe most frequent combination of start station and end station trip was: {} and {} \n'.format(
            popular_s_station, popular_e_station, combination_station_s, combination_station_e))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel time'] = df['End Time'] - df['Start Time']
    total_travel_time = df['Travel time'].sum()

    # TO DO: display mean travel time
    mean_travel_time = df['Travel time'].mean()

    print('Total travel time was: {}\nMean travel time was:{}'.format(total_travel_time, mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    df2 = df.dropna(axis=0)
    user_types = df2['User Type'].value_counts()

    print(user_types)
    # TO DO: Display counts of gender
    try:
        gender = df2['Gender'].value_counts()
        print(gender)
    except KeyError:
        print("Gender data not available")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_birth = int(df2['Birth Year'].min())
        most_recent_birth = int(df2['Birth Year'].max())
        most_common_birth = int(df2['Birth Year'].mode()[0])

        print(
            'The earliest year of birth was: {} \nThe most recent birth was: {}\nThe most common year of birth was: {}'.format(
                earliest_birth, most_recent_birth, most_common_birth))
    except KeyError:
        print("Birth year data not available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def view_raw(df):
    "Displays raw data of the dataframe requested"
    view_ans = input("\nWould you like to view the raw data? Enter yes or no. \n").lower()
    call_start = 0
    call_stop = 5
    if view_ans == 'yes':
        while True:
            print(df.iloc[call_start:call_stop])
            call_start += 5
            call_stop += 5
            restart = input('\nWould you like to view the next 5 lines? Enter yes or no.\n').lower()
            if restart.lower() != 'yes':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            print('There is no data with the current filters')
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            view_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
