import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import matplotlib.pyplot as plt
from ast import literal_eval

# Read csv and make genre column arrays
title_df = pd.read_csv('titles.csv', converters = {'genres': literal_eval})

# Function to bin dataframe by decade
def bin(title_df):
    # Check the min and max years to check which decades to bin
    temp = title_df.min(numeric_only = True)
    text = ['Minimum Release Year: ' + str(int(temp[0]))]

    temp = title_df.max(numeric_only = True)
    text += ['Maximum Release Year: ' + str(int(temp[0]))]

    # As we want to bin each decade, start from 1950 and finish at 2020
    title_df['decades'] = pd.cut(x = title_df['release_year'], 
                                 bins = [1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2030],
                                 labels = [40, 50, 60, 70, 80, 90, 100, 110, 120]) #100, 110 and 120 are our 2000's bins
    
    # Save as csv to use in other programs
    title_df.to_csv('output/binned_table.csv', index=False)

    # Remove unwanted decades
    title_df = title_df[(title_df['release_year'] > 1950) & (title_df['release_year'] < 2021)]

    # Write to text file
    with open('output/prelim_info.txt', 'w') as f:
        for line in text:
            f.write(line)
            f.write('\n')
    
    return title_df

# Reference: https://www.geeksforgeeks.org/python-program-for-binary-search/
# Edited binary search function that performs reverse process and returns the index of element with higher alphabetical value
def binary_search(arr, low, high, x):
 
    # Check base case
    if high >= low:
 
        mid = (high + low) // 2
 
        # If element is present at the middle itself
        if arr[mid] == x:
            return -1
 
        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)
 
        # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x)
 
    else:
        # Element is not present in the array so output index of element that has higher alphabetical value
        return low

# Function to find all genres
def find_genres(binned_df):
    # Iterate through rows of dataframe
    genres = []

    # Iterate through dataframe rows
    for index, row in binned_df.iterrows():
        # Iterate through each array of genres column
        for element in row['genres']:

            # Check if the element is contained within genres list
            output = binary_search(genres, 0, len(genres) - 1, element)
            if (output != -1):
                # If so insert in alphabetical order
                genres.insert(output, element)
    
    return genres

# Function to count total number of genres
def count_genres(binned_df, genres):
    count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Iterate through dataframe rows
    for index, row in binned_df.iterrows():
        # Iterate through each array of genres column
        for element in row['genres']:
            # Count the genre
            count[genres.index(element)] = count[genres.index(element)] + 1
    
    # Make a dataframe
    genre_count_df = pd.DataFrame(data = {'genre': genres, 'count': count})

    #print(genre_count_df['genre'][0])
    with open('output/prelim_info.txt', 'a') as f:
        f.write('\nGenre Count\n')
        for row in genre_count_df.index:
            f.write(genre_count_df['genre'][row])
            f.write(': ')
            f.write(str(genre_count_df['count'][row]))
            f.write('\n')

# Function to calculate proportions of a list
def calc_proportion(count):
    list = []
    sum_count = sum(count)
    for element in count:
        list.append(element/sum_count)
    return list

# Function to count total number of genres for each decade
def count_genres_decades(binned_df, genres, bin, check):
    # Get only value of specific bin
    binned_df = binned_df[binned_df['decades'] == bin]

    count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Iterate through dataframe rows
    for index, row in binned_df.iterrows():
        # Iterate through each array of genres column
        for element in row['genres']:
            # Count the genre
            count[genres.index(element)] = count[genres.index(element)] + 1
    
    # Make a list which will be our row
    if (check == True):
        list = [bin] + calc_proportion(count)
    # This case is for making dataframe with raw numbers
    else:
        list = [bin] + count

    return list

# Function that creates new dataframe of values to plot
def make_final_df(binned_df, genres, check):
    # Make empty dataframe
    decade_prop_df = pd.DataFrame( columns = ['decade', 'action', 'animation', 'comedy',
                                            'crime', 'documentation', 'drama', 'european',
                                            'family', 'fantasy', 'history', 'horror', 'music',
                                            'reality', 'romance', 'scifi', 'sport',
                                            'thriller', 'war', 'western'])

    # Iterate by number of decades we have chosen to make dataframe
    for count in range(7):
        list = count_genres_decades(binned_df, genres, 50 + 10*count, check)
        # Append new list to dataframe
        decade_prop_df.loc[len(decade_prop_df)] = list

    if (check == True):
        decade_prop_df.to_csv('output/decade_prop_df.csv', index=False)
    # This case is for making dataframe with raw numbers
    else:
        decade_prop_df.to_csv('output/decade_count_df.csv', index=False)
    return decade_prop_df

# Function to change decade category values to be more visually appealing
def change_decade_values(decade_prop_df):
    # Iterate through rows
    for row in range(len(decade_prop_df)):
        str1 = ''
        # Calculate the decade
        num = float(80 + 10*row)
        #num = float(50 + 10*row)
        # If bin is in the 2000's
        if (num >= 100):
            num = num - 100
            if (num == 0):
                str1 = '200' + str(int(num))
            else:
                str1 = '20' + str(int(num))
        # If bin is in 1900s
        else:
            str1 = '19' + str(int(num))
        # Replace the old bins with proper decades
        decade_prop_df.replace(float(80 + 10*row), str1 + 's', inplace = True)
        #decade_prop_df.replace(float(50 + 10*row), str1 + 's', inplace = True)

# Plot data
def plot_data(decade_prop_df):
    decade_prop_df.plot(x = 'decade', kind = 'barh', stacked = True, title = 'Genre Trends for Each Decade', 
                         mark_right = True, figsize=(15,5))
    plt.legend(bbox_to_anchor = (1.05, 1.0), loc = 'upper left')
    plt.xlabel("Proportion")
    plt.ylabel("Decade")
    plt.tight_layout()
    plt.savefig('output/trend_graph.png')

# Call functions

binned_df = bin(title_df)

genres = find_genres(binned_df)

count_genres(binned_df, genres)

decade_prop_df = make_final_df(binned_df, genres, True)

# For teammates
decade_count_df = make_final_df(binned_df, genres, False)

# There are too few data points for the 50s, 60s and 70s so remove them
decade_prop_df = decade_prop_df[decade_prop_df['decade'] > 70]

change_decade_values(decade_prop_df)

plot_data(decade_prop_df)