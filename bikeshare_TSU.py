import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# create lists to be used in function: get_filters
months = ['january', 'february', 'march', 'april', 'mai', 'june', 'july', 'august', 'september', 'oktober', 'november', 'december']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nWould you like to analyze bikeshare data for chicago, new york city or washington? ')
        if city in CITY_DATA.keys():
            re_check = input('\nIf you are sure press "enter" or type another city name!')
            if re_check == '':
                print('\nYou have decided for: ', city.title())
                break
            else:
                if re_check in CITY_DATA.keys():
                    city = re_check
                    print('\nYou have decided for: ', city.title())
                    break
                else:
                    print(re_check.title(),'is not in database or city name is typed wrong')
        else:
            print(city.title(),'is not in database or city name is typed wrong')

    #get user input to display the raw data upon. I have included this function before the filters for month and day, so that the user can see the original data
    while True:
        raw_data_request = input('\nWould you like to see 5 lines of the raw bikeshare data for the selected city? Press "enter" for yes, "no" if not. ')
        if raw_data_request == '':
            df_raw = pd.read_csv(CITY_DATA[city])
            print('\n', df_raw.head(), '\n')
            break
        elif raw_data_request == 'no':
            print('Program proceeds for next filters')
            break
        else:
            print('Wrong entry. Next try')

    if raw_data_request == '':
        n = 5
        while True:
            raw_data_request = input('For the next 5 line continue pressing "enter", or "no" if not: ')
            if raw_data_request == '':
                print('\n', df_raw.head(n+5), '\n')
                n += 5
            elif raw_data_request == 'no':
                print('Program proceeds for next filters')
                break
            else:
                print('Wrong entry. Next try')


    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        filter = input('\nWould you like to filter by month, day, both or none? ')
        if filter == 'none':
            month, day = 'all', 'all'
            break
        elif filter == 'both':
            month = input('\nWhich month would you like to analyze? (Enter january, february, ...) ')
            day = input('\nWhich day would you like to analyze? (Enter monday, tuesday, ...) ')
            if month in months and day in days:
                break
        elif filter == 'month':
            day = 'all'
            month = input('\nWhich month would you like to analyze? (Enter january, february, ...) ')
            if month in months:
                break
            else:
                print(month, 'does not exist')
        elif filter == 'day':
            month = 'all'
            day = input('\nWhich day would you like to analyze? (Enter monday, tuesday, ...) ')
            if day in days:
                break
            else:
                print(day, 'does not exist')
        else:
            print('\nYou entered an invalid value!')

    # display information about for which city, month and day filter the dataframe is loading
    if filter == 'none':
        print('\nDataFrame is loading for {} and without filter for month and day.'.format(city.title()))
    elif filter == 'month':
        print('\nDataFrame is loading for {} and with filter for {}.'.format(city.title(), month.title()))
    elif filter == 'day':
        print('\nDataFrame is loading for {} and with filter for {}.'.format(city.title(), day.title()))
    else:
        print('\nDataFrame is loading for {} and filter for {} and {}.'.format(city.title(), month.title(), day.title()))

    print('-'*40)
    return city, month, day, filter


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

    # load Data for the respective city
    df = pd.read_csv(CITY_DATA[city])
    if city == 'washington':
        df = pd.read_csv(CITY_DATA[city])
        df['Gender'] = 'not_available'
        df['Birth Year'] = 'not_available'

    # convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour
    df['month'] = df['Start Time'].dt.month
    df['day of week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month and day of week if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'mai', 'june', 'july', 'august', 'september', 'oktober', 'november', 'december']
        df =  df[df['month'] == months.index(month)+1]

    if day != 'all':
        df =  df[df['day of week'] == day.title()]

    return df


def time_stats(df, filter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel for ...\n')
    start_time = time.time()

    # display the most common month, the most common day of week and the most common start hour, based on the filter applied before
    if filter == 'none':
        print('Time statistics for filter selection: ', 'none\n')
        time_stat = pd.Series(data = [df['month'].mode()[0], df['day of week'].mode()[0], df['hour'].mode()[0]], index = ['Most common month:', 'Most common day:', 'Most common hour:'])
    if filter == 'day':
        print('Time statistics for filter selection: ', 'day\n')
        time_stat = pd.Series(data = [df['month'].mode()[0], df['hour'].mode()[0]], index = ['Most common month:', 'Most common hour:'])
    if filter == 'month':
        print('Time statistics for filter selection: ', 'month\n')
        time_stat = pd.Series(data = [df['day of week'].mode()[0], df['hour'].mode()[0]], index = ['Most common day:', 'Most common hour:'])
    if filter == 'both':
        print('Time statistics for filter selection: ', 'month and ', 'day\n')
        time_stat = pd.Series(data = [df['hour'].mode()[0]], index = ['Most common hour:'])

    print(time_stat)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station, most commonly used end station and most frequent combination of start station and end station trip
    df['Start End Combination'] = df['Start Station'] +' and '+df['End Station']
    stat_stat = pd.Series(data = [df['Start Station'].mode()[0], df['End Station'].mode()[0], df['Start End Combination'].mode()[0]], index = ['The most popular start station:', 'The most popular end station:', 'The most frequent combination of start station and end station trip:'])

    print(stat_stat)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time and mean travel time

    tm_dur_stat = pd.Series(data = [pd.Timedelta(seconds = (df['Trip Duration'].sum())), pd.Timedelta(seconds = (df['Trip Duration'].mean()))], index = ['Total travel time:', 'Mean travel time:'])
    print(tm_dur_stat)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print('\nUser Type Value Counts:\n')
    print(user_type)

    # Display counts of gender
    gender_type = df['Gender'].value_counts()
    print('\nGender Value Counts:\n')
    print(gender_type)

    # Display earliest, most recent, and most common year of birth
    us_age_info = pd.Series(data = [df['Birth Year'].min(), df['Birth Year'].max(), df['Birth Year'].mode()[0]], index = ['Youngest user:', 'Oldest user:', 'Most common year:'])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day, filter = get_filters()
        df = load_data(city, month, day)

        time_stats(df, filter)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
