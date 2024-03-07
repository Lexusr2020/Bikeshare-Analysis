


#====================== IMPORTS =========================

from ast import While
from calendar import day_name, month, month_name
from itertools import count
from re import I
from secrets import choice
from tracemalloc import stop
import pandas as pd
import numpy as np
import time
import datetime



#===================== VERIABLES ========================

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['January', 'February', 'March', 'April', 'May', 'June']

day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

is_active = True
is_month = False
is_day = False
is_both = False
next_five = True

#===================== GET FILTERS ========================


def get_city():
    global city
    global month
    
    """ gets city filter and returns city """

    while is_active == True:  
        
        print("Please select a city from the following list:\n")

        for x in CITY_DATA:
            print(x.title())
            print()
        city_input = input("What city would you like to see data from?\n")

        
        if city_input.lower() in CITY_DATA:
            city = city_input.title()
            print("Thanks, You've selected: {}".format(city))
            return city
            
        else:
            print("please try again!\n")
            is_active == False


def get_month(city):
    global month
    global day
    
    choice = input("Would you like to filter by Month, Day or Both:\n")   

    #================= JUST MONTH ====================
    """ if by just month, calls  load_month() function """

    if choice.title() == "Month":
  
        print("You've selected {}.\n".format(choice.title()))
        print("Please select month:\n")
        print(months)
        month = input()
        month = month.title()
        if month.title() in months:
            print()
            print("You've selected {}.\n".format(month))
            print("Here are your choices: {} and {}.\n".format(city, month))
            print("Let's begin!")
            print()
            is_month == True
            load_month()
            


    #================= JUST DAY ====================
    """ if by just day, calls  load_day() function """

    if choice.title() == "Day":
   
        print("You've selected {}.\n".format(choice.title()))
        print("Please select day:\n")
        print(day_of_week)
        day = input()
        day = day.title()
        if day.title() in day_of_week:
            print()
            print("You've selected {}.\n".format(day))
            print("Here are your choices: {} and {}.\n".format(city, day))
            print("Let's begin!")
            print()
            is_day == True
            load_day()
            
            

    #============ Both (MONTH & DAY) ====================
    """ if by both, gets month and calls get_day() function """
    if choice.title() == "Both":
    
        print("You've selected {}.\n".format(choice.title()))
        print("Please select month:\n")
        print(months)
        month = input()
        month = month.title()
        if month.title() in months:
            print()
            print("You've selected {}.\n".format(month))
            is_both == True
            get_day(city, month)
            
            
    else:
        if choice.title() == "":
            print("I didn't quite get that, please try again.")
            is_active == False
    
    return city, month


def get_day(city, month): 
    global day
    
    """ Gathers day input and call"""

    print("Please select day:\n")
    print(day_of_week)
    day = input()
    day = day.title()
    if day.title() in day_of_week:
        print()
        print("You've selected {}.\n".format(day))
        print("Here are your choices: {}, {} and {}.\n".format(city, month, day))
        print("Let's begin!")
        print()
        print('\nCalculating The Most Popular Stations and Trip...\n')

        load_both_df(city, month, day)
    
    return city, month, day


#===================== LOADS ========================


    #LOAD BY MONTH
def load_month():
    global city
    global month
    
    start_time = time.time()

    """load data file into a dataframe"""

    if city.lower() != "new york city":
        df = pd.read_csv("./datasets/{}.csv".format(city.lower()))
    else:
        df = pd.read_csv("./datasets/new_york_city.csv")

    """convert the Start Time column to datetime"""

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    """ extract month and day of week from Start Time to create new columns"""

    df['month'] = df['Start Time'].dt.month

    """ filter by month if applicable"""

    if month != 'all':
        """ use the index of the months list to get the corresponding int"""

        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        """ filter by month to create the new dataframe"""

        df = df[df['month'] == month]


    print("Would you like to see the first 5 rows of raw data?\n")
    print("Type Yes or No")
    choice = input()
    if choice.title() == "Yes":
        print(df.head())
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)  
        load_stats(df)
        

    else:
        print("Ok, no raw data")
        load_stats(df)


    #LOAD BY DAY
def load_day():
    global city
    global day

    start_time = time.time()

    """load data file into a dataframe"""
    if city.lower() != "new york city":
        df = pd.read_csv("./datasets/{}.csv".format(city.lower()))
    else:
        df = pd.read_csv("./datasets/new_york_city.csv")


    """ convert the Start Time column to datetime"""

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    """ extract month and day of week from Start Time to create new columns"""

    df['day_of_week'] = df['Start Time'].dt.day_name()

    """ filter by day of week if applicable"""

    if day != 'all':
        """ filter by day of week to create the new dataframe"""

        df = df[df['day_of_week'] == day.title()]

    print("Would you like to see the first 5 rows of raw data?\n")
    print("Type Yes or NO")
    choice = input()
    if choice.title() == "Yes":
        print(df.head())
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
        load_stats(df)

    else:
        print("Ok, no raw data")
        load_stats(df)

    

    #LOAD BY BOTH
def load_both_df(city, month, day):


    start_time = time.time()

    """ load data file into a dataframe"""

    if city.lower() != "new york city":
        df = pd.read_csv("./datasets/{}.csv".format(city.lower()))
    else:
        df = pd.read_csv("./datasets/new_york_city.csv")

    """ convert the Start Time column to datetime"""
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    """ extract month and day of week from Start Time to create new columns"""

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    """ filter by month if applicable"""
    if month != 'all':
        
        """ use the index of the months list to get the corresponding int"""

        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        """ filter by month to create the new dataframe"""

        df = df[df['month'] == month]

    """ filter by day of week if applicable"""
    if day != 'all':
        """ filter by day of week to create the new dataframe"""

        df = df[df['day_of_week'] == day.title()]

    
    print("Would you like to see the first 5 rows of raw data?\n")
    print("Type Yes or NO")
    choice = input()
    if choice.title() == "Yes":
        print(df.head())
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
        load_stats(df)
        return df

    else:
        print("Ok, no raw data")
        load_stats(df)
        return df


#===================== STATS ========================


    #LOAD STATS
def load_stats(df):
    global new_df
    global s
    global e
    s = 0
    e = 5
    global next_five
    global start_time

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    """========== eliminate NaN Values====================="""

    df.dropna(axis = 1)

    """ display the most common start hour"""

    df['Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Hour'].mode().values[0]

    print('Most Frequent Start Hour is:', popular_hour)
    print()

    """ display the most common day of week"""

    df['Day'] = df['Start Time'].dt.day_name()
    popular_day = df['Day'].mode().values[0]

    print('Most popular day is: ', popular_day)
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    """============  STATION STATS =================="""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    """ display most commonly used start station"""

    start_station = df['Start Station'].mode().values[0]
    print("The most popular start station is: ")
    print(start_station)
    print()

    """ display most commonly used end station"""

    end_station = df['End Station'].mode().values[0]
    print("The most popular end station is: ", end_station)
    print()

    """ display most frequent combination of start station and end station trip"""

    start_end = df.groupby(['Start Station','End Station']).size().idxmax()
    print("The most popular start & end stations is: ", start_end)
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    """
    ============  TRIP STATS =================="""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    """display total travel time"""

    travel_sum = df["Trip Duration"].sum()
    print("Total travel time is: ", travel_sum, "seconds")
    print()

    """ display mean travel time"""

    mean_travel = df['Trip Duration'].mean()
    print("The longest trips is: ", mean_travel, "seconds")
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    if city != "Washington":
        user_stats(df)

    if city.lower() == "washington":

        new_df = df[['Start Time','End Time','Trip Duration', 'Start Station', 'End Station', 'User Type']]
        print("Would you like to see 5 rows of data at a time?\n")
        print()
        print("PLEASE NOTE: Gender has been excluded\n")
        print("Type Yes or No")

        choice = input()
        if choice.title() == "Yes":
            print()
            start_time = time.time()      
            new_df = new_df.reset_index()
            print(new_df.iloc[s:e])
            
        while next_five == True:
            s = s + 5
            e = e + 5
            print_five_rows(new_df, s, e)

    
    #LOAD USER STATS
def user_stats(df):
    global new_df
    global s
    global e
    s = 0
    e = 5
    global next_five

    """============  USER STATS =================="""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    """ Display counts of user types"""

    user_counts = df["User Type"].value_counts()
    print("Here is the user count is: \n", user_counts)
    print()

    """ Display counts of gender"""

    gender_counts = df["Gender"].value_counts()
    print("Here is the gender count: \n", gender_counts)
    print()

    """ Display earliest, most recent, and most common year of birth"""

    year_earliest = df["Birth Year"].min()
    print("The oldest person was born in: ", year_earliest)
    print()

    year_recent = df["Birth Year"].max()
    print("The youngest person was born in: ", year_recent)
    print()

    year_common = df["Birth Year"].mode()[0]
    print("The most common birth year si: ", year_common)
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    """ Display 5 rows of raw data at a time"""

    """ Created new DF and Reset row index"""

    if city.lower() == "chicago" or city.lower() == "new york city":

        new_df = df[['Start Time','End Time','Trip Duration', 'Start Station', 'End Station', 'Gender', 'Birth Year']]
        print("Would you like to see 5 rows data at a time?\n")
        print()
        print("PLEASE NOTE: User Type has been excluded\n")
        print("Type Yes or No")
        
        choice = input()
        if choice.title() == "Yes":
            print()
            start_time = time.time()      
            new_df = new_df.reset_index()
            print(new_df.iloc[s:e])
            
        while next_five == True:
            s = s + 5
            e = e + 5
            print_five_rows(new_df, s, e)

              
#===================== PRINT NEXT FIVE ROWS ======================== 


def print_five_rows(new_df, s, e):
    global start_time

    """ loops if you press enter key and prints the next five rows """


    """ exits loop when any other key is pressed and prompts restart """
    
    print("Would you like to continue?")
    print("Press Enter to continue. Type any other key to exit")
    print()
    more = input()
    if more.title() == "":
        print(new_df.iloc[s:e])
        print()
        return new_df, s, e

    elif more.title() != "":
        next_five == False
        restart()
   

 #===================== RESTART PROMPT ========================        


def restart():    
    """ Restart Option """

    is_both == False
    restart = input('\nWould you like to restart? Enter yes or no.\n')
    
    if restart.lower() == 'yes':
        main()

    else:
        """ Exits Program """
        print()
        print("Closing program, goodbye!")
        exit()
    

#===================== CALL FUNCTIONS ========================


def main():
    """ MAIN FUNCTION """
    get_city()
    """ Gets city input returns city """
    get_month(city)
    """ Gets month, day, or both input returns city month and day if applicable """

    while is_both:
        get_day(city, month)
        """ Gets month, day, or both input and call load stats.  If both is chosen, then calls load-both_df  or calls  """
        load_both_df(city, month, day)
        """ Loads df by city month and day. Returns df """

    else:
        restart()
        

if __name__ == "__main__":
	main()


    


















