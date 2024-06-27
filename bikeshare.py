import time
import pandas as pd
import numpy as np

# the only cities with available data are chicago, new york city, and washington
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # extract the list of valid cities from the dictionary keys
    valid_cities = list(CITY_DATA.keys())
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        # get user input and convert it to lowercase
        city = str(input('Would you like to see data for Chicago, New York City, or Washington?')).lower()
        # check if the input is valid
        if city in valid_cities:
            # if valid, break the loop
            break
        else: 
            # if invalid, inform the user
            print("Please enter a valid city name: Chicago, New York City, or Washington.")
     
    # capitalize the first letter of each word for consistent output 
    city = city.title()
    print(f'Looks like you want to hear about {city}! If this is not true, restart the program!')

    # define valid months and valid days
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all'] 
    valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    valid_responses = ['month', 'day', 'both', 'none']
    # get user input for filter type (month, day, both, none)
    while True:
        filter_response = str(input('Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter.')).lower()
        # check if the input is valid
        if filter_response in valid_responses:
            # if valid, break the loop
            break
        else: 
            # if invalid, inform the user
            print("Please enter a valid response: 'month', 'day', 'both', 'none'.")

    # initialize month and day 
    month = 'all'
    day = 'all'
    
    # get user input for month if needed 
    if filter_response in ['month', 'both']:
        while True:
            month = str(input("Which month are you interested in: January, February, March, April, May, June, or 'all'?")).lower()
            if month in valid_months:
                break
            else:
                print("Please enter a valid month: January, February, March, April, May, June or 'all'.")                              
    # get user input for day if needed
    if filter_response in ['day', 'both']:
        while True:
            day = str(input("Which day of the week are you intersted in: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or 'all'?")).lower()
            if day in valid_days:
                break
            else:
                print("Please enter a valid day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or 'all'.")                       
                            
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month != 'all':
        # use index of the months list to get the corresponding int 
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create a new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    #print("DataFrame shape:", df.shape)
    #print("DataFrame head:", df.head())
    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most common Month:', popular_month)
    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most common day of week:', popular_day.title())
    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most common start hour:', popular_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station:', popular_start_station)
    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station:', popular_end_station)
    # TO DO: display most frequent combination of start station and end station trip
    df['Combo Station'] = df['Start Station'] +  " to " + df['End Station']
    popular_start_end_station = df['Combo Station'].mode()[0]
    print('Most frequent combination of start station and end station trip:', popular_start_end_station)
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time)
    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts by user types:", user_types)
    # TO DO: Display counts of gender
    if city.lower() != 'washington':
        gender_counts = df['Gender'].value_counts()
        print("Counts by Gender:", gender_counts) 
        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print('Earliest Year of Birth:', earliest_year)
        print('Most Recent Year of Birth:', most_recent_year)
        print('Most Common Year of Birth:', most_common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Display the data upon request by the user in increments of 5 rows
def display_raw_data(df):
    start_loc = 0
    while True: 
        response = ['yes', 'no']
        view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no: ").lower()
        if view_data in response:
            if view_data == 'yes':
                print(df.iloc[start_loc:start_loc+5])
                start_loc += 5
            else:
                break
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
