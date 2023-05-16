import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS_AVAILABLE = { 'all', 'january', 'february', 'march',
                     'april', 'may', 'june'}

DAYS_AVAILABLE = {'all', 'monday', 'tuesday', 'wednesday',
                  'thursday', 'friday', 'saturday', 'sunday'}

VALID_REPLY = {'yes', 'no'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please enter a city to explore: ').lower()

    while city.lower() not in CITY_DATA:
        city = input("That city is unavailable. Please choose from Chicago, New York City, or Washington: ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Please enter a month or type 'all' for all months: ").lower()

    while month.lower() not in MONTHS_AVAILABLE:
        month = input("This month isn't available. Please choose 'all' or select a month from January - June: ").lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please enter a day of the week: ').lower()

    while day.lower() not in DAYS_AVAILABLE:
        day = input("This wasn't a valid input. Please choose 'all' or select a weekday from Monday - Sunday: ").lower()

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
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    top_month = df['month'].mode()[0]

    print("The most common month is: {} (6 = June, 5 = May, etc.)".format(top_month))

    # display the most common day of week
    top_day = df['day_of_week'].mode()[0]

    print("The most common day of the week: {}".format(top_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    top_hour = df['hour'].mode()[0]

    print("The most common start hour is: {}".format(top_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    top_start = df['Start Station'].mode()[0]
    print("The most commonly used start station is: {}".format(top_start))

    # display most commonly used end station
    top_end = df['End Station'].mode()[0]
    print("The most commonly used end station is: {}".format(top_end))

    # display most frequent combination of start station and end station trip
    top_trip = (df['Start Station'] + " to " + df['End Station']).mode()[0]
    print("The most frequent trip from start to end stations is: {}".format(top_trip))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    hours = round((total_time / 3600))
    print("The total travel time is: {} hours".format(hours))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    mean_minutes = round((mean_time / 60), 2)
    print("The mean travel time is: {} minutes".format(mean_minutes))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print("The counts of user types are: {}".format(user_counts))


    # Display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print("The counts of gender are: {}".format(gender_counts))


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode())
        print("The earliest year of birth is: {}, the most recent is: {}, and the most common is {}".format(earliest, most_recent, common_year))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    Asks user if they would like to see the data used in the analysis

    Args:
        (str) data request - allows user to specify yes or no for data request
    Returns:
        df - Pandas DataFrame containing 5 rows of the raw data used to create summary stats
    """

    i=0
    data_request = input("Would you like to see the data used for this analysis? ").lower()

    while True:
        if data_request not in VALID_REPLY:
            data_request = input("Please enter a valid input (yes or no). ").lower()
        elif data_request == 'no':
            break
        else:
            print(df[i:i+5])
            data_request = input("Would you like to see more data? ").lower()
            i += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
