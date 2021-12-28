import time
import pandas as pd
pd.set_option('display.max_columns',200)
import numpy as np
import datetime #import datetime to convert dates to numbers https://stackoverflow.com/questions/19934248/nameerror-name-datetime-is-not-defined

#Get cities available for data
#https://www.geeksforgeeks.org/python-get-dictionary-keys-as-a-list/
def getCities(CITY_DATA):

    return [*CITY_DATA]
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Create list of cities we have data for
cities = (getCities(CITY_DATA))

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    #https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response
    city = ''
    while True:
        print ("You can choose to explore data for:", cities)
        city = input("Which city data would you like to see?")
        city = city.lower()
        if not city in cities:
            print("Sorry, please enter a valid city.")
        else:
            print("We will explore data for", city.title())
            break


    #Get user input for month (all, january, february, ... , june)
    month = ''
    while True:
        months = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
        month = input("What month would you like to see data for? January, February, March, April, May, June, or all? Please type out the full month name.")
        month = month.lower()
        if not month in months:
            print("Sorry, please enter a valid month.")
        else:
            print("We will explore data for", month.capitalize())
            break

    #Get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while True:
        days = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
        day = input("What day would you like to see data for? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all? Please type out the full day name.")
        day = day.lower()
        if not day in days:
            print("Sorry, please enter a valid day.")
        else:
            print("We will explore data for", day.capitalize())
            break
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
    print("You are viewing first data for:", city, month, day)

    #load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def data_display(df):
    '''This function will ask the user if they want to see individual trip data 5 lines at a time.
    Your script should prompt the user if they want to see 5 lines of raw data,
    Display that data if the answer is 'yes',
    Continue iterating these prompts and displaying the next 5 lines of raw data at each iteration,
    Stop the program when the user says 'no' or there is no more raw data to display.'''
    show_data = ''
    while True:
        yorn = ('yes', 'no')
        #Ask user if they want to see data
        show_data = input('Do you want to see the first 5 rows of trip data? Enter yes or no.')
        #Check if input is yes or no
        if not show_data in yorn:
            print("Sorry, please answer yes or no.")
        else:
            #if no
            if show_data.lower() != 'yes':
                print('No individual data will be displayed.')
                break
            else:
                #set start and end lines
                start_line = 0 #Begin at first line
                end_line = 5 #Set ending line
                #count rows
                total_rows = df.index   #https://stackoverflow.com/questions/15943769/how-do-i-get-the-row-count-of-a-pandas-dataframe
                rows = len(df.index)
                while ('yes'):
                    print(df.iloc[start_line:end_line])     #https://www.askpython.com/python/built-in-methods/python-iloc-function
                    start_line += 5 #increment by 5
                    end_line += 5   #increment by 5
                    #check if end of dataframe has been reached
                    if end_line >= rows:
                        print('You have reached the end of the file.')
                        break
                    else:
                        #ask user if they want to see another 5 lines
                        show_data = input('Would you like to see another 5 lines of data?:')
                        #quit
                        if show_data.lower() != 'yes':
                            break
        break

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    time.sleep(1) #https://stackoverflow.com/questions/11552320/correct-way-to-pause-a-python-program
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month

    # find the most popular month
    popular_month = df['month'].mode()[0]

    print('Most Popular Start Month:', popular_month)

    # display the most common day of week https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.weekday.html, https://stackoverflow.com/questions/60339049/weekday-name-from-a-pandas-dataframe-date-object
    # extract day from the Start Time column to create a day column
    df['day'] = df['Start Time'].dt.weekday_name

    # find the most popular hour
    popular_day = df['day'].mode()[0]
    #dayname = popular_day.strftime("%A")

    print('Most Popular Start Day:', popular_day)

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    time.sleep(1) #https://stackoverflow.com/questions/11552320/correct-way-to-pause-a-python-program
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    #https://stackoverflow.com/questions/15138973/how-to-get-the-number-of-the-most-frequent-value-in-a-column
    print('Most common start station:')
    print(df['Start Station'].value_counts().idxmax())
    print(df['Start Station'].value_counts().max(), 'trips')
    print()

    # display most commonly used end station
    print('Most common end station:')
    print(df['End Station'].value_counts().idxmax())
    print(df['End Station'].value_counts().max(), 'trips')
    print()

    # display most frequent combination of start station and end station trip
    print('Most common trip:')
    print(df.groupby(['Start Station', 'End Station']).size().idxmax())
    print(df.groupby(['Start Station', 'End Station']).size().max(), 'trips')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    I don't have the time unit displayed as it's not in the data. It would only be an assumption."""
    time.sleep(1) #https://stackoverflow.com/questions/11552320/correct-way-to-pause-a-python-program
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total trip time:')
    print(df['Trip Duration'].sum())
    print()

    # display mean travel time
    print('Mean travel time:')
    round_mean = df['Trip Duration'].mean()
    rounded_mean = round(round_mean)
    print(rounded_mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    time.sleep(1) #https://stackoverflow.com/questions/11552320/correct-way-to-pause-a-python-program

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Count of user types:')
    print(df['User Type'].value_counts())
    print()

    # Display counts of gender
    if 'Gender' in df:
        print('Count of gender:')
        print(df['Gender'].value_counts())
        print()
    else:
        print('There is no gender information available.')

    # Display earliest, most recent, and most common year of birth
    # using groupby() function on Group column  https://www.geeksforgeeks.org/max-and-min-date-in-pandas-groupby/
    if 'Birth Year' in df:
        print('Minimum Birth Year:')
        min_birth_year = int(df['Birth Year'].min())
        print(min_birth_year)
        print()
        print('Maximum Birth Year:')
        max_birth_year = int(df['Birth Year'].max())
        print(max_birth_year)
        print()
        print('Most Common Birth Year:')
        com_birth_year = int(df['Birth Year'].value_counts().idxmax())
        print(com_birth_year)
    else:
        print('There is no birth year data avilable.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        data_display(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #Ask user if they want to run again
        while True:
            yorn = ('yes', 'no')
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            restart = restart.lower()
           #Check if input is yes or no
            if not restart in yorn:
                print("Sorry, please answer yes or no.")
            else:
            #if yes, restart
                if restart == 'yes':
                    print('Restarting...')
                    break
                else:
                #if no, exit program
                    print('Exiting...')
                    exit()


if __name__ == "__main__":
	main()
