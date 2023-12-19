import time
import pandas as pd
import numpy as np


CITY_DATA = {
    'Chicago': 'chicago.csv',
    'New York City': 'new_york_city.csv',
    'Washington': 'washington.csv'
}

def get_user_input(prompt, valid_options):
    """
    Helper function to get valid user input for city, month, and day.
    """
    while True:
        user_input = input(prompt).title()
        if user_input in valid_options:
            break
        else:
            print("Sorry, I didn't catch that. Try again.")
    return user_input

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

    city = get_user_input("\nWhich city would you like to filter by? New York City, Chicago or Washington?\n",
                          ['New York City', 'Chicago', 'Washington'])

    month = get_user_input("\nWhich month would you like to filter by? January, February, March, April, May, June or type 'all' if you do not have any preference?\n",
                           ['January', 'February', 'March', 'April', 'May', 'June', 'all'])

    day = get_user_input("\nAre you looking for a particular day? If so, kindly enter the day as follows: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'all' if you do not have any preference.\n",
                         ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'all'])

    print('-'*40)
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
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month)

    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Day:', popular_day)

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    start_station = df['Start Station'].value_counts().idxmax()
    print('Most Commonly Used Start Station:', start_station)

    end_station = df['End Station'].value_counts().idxmax()
    print('Most Commonly Used End Station:', end_station)

    combination_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most Commonly Used Combination of Start Station and End Station Trip:', combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = np.sum(df['Trip Duration'])
    print('Total Travel Time:', total_travel_time / 86400, 'Days')

    mean_travel_time = np.mean(df['Trip Duration'])
    print('Mean Travel Time:', mean_travel_time / 60, 'Minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """
    Displays statistics on bikeshare users.
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    if 'Gender' in df.columns:
        gender_types = df['Gender'].value_counts()
        print('\nGender Types:\n', gender_types)
    else:
        print('\nGender Types:\nNo data available for this month.')

    if 'Birth Year' in df.columns:
        earliest_year = np.min(df['Birth Year'])
        most_recent_year = np.max(df['Birth Year'])
        most_common_year = df['Birth Year'].mode()[0]

        print('\nEarliest Year:', earliest_year)
        print('Most Recent Year:', most_recent_year)
        print('Most Common Year:', most_common_year)
    else:
        print('\nBirth Year Statistics:\nNo data available for this month.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
