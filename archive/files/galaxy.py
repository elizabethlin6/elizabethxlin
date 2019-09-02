# -*- coding: utf-8 -*-
#import matplotlib.pyplot as plt
#import numpy as np
#from sklearn import datasets, linear_model
#from sklearn.metrics import mean_squared_error, r2_score

import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.stats.stats import pearsonr


def extract_galaxy_data(filename, column_names):
    """Takes a filename and a list of column names. Returns a list of integers
    that contains the values in those columns from every row.
    Parameter: * File name and column name *
    Output: * List of given column(s) *
    """   
    
    galaxy_csv = open(filename)               # Reads in CSV file 
    input_file = csv.DictReader(galaxy_csv)   # creates a dictionary for each row
    
    galaxy_list = [] 
    
    for line in input_file:
        
        for column in column_names:
            gal_data = line[column]
            gal_data = gal_data.replace("'", '')
            galaxy_list.append(float(gal_data))
             
    return galaxy_list                        # gets list of desired column


def get_size(list_one, list_two):
    """Produces the difference between two lists.
    Parameter: * two different list of values *
    Output: * difference of value in two list in a new list * """
    
    size_list = []                            # takes the difference between two lists
                                              # returns difference of lists
    for i in range(len(list_one)):
        size = list_one[i] - list_two[i]
        size_list.append(size)
        
    return size_list  
   
    assert len(list_one) == len(list_two)   
    

def average_function(list):                      
    """Returns the average of all values in a list.
    Parameter: * list *
    Output: * float value *"""
    
    init_element = 0.0
    denominator = len(list)
    
    for element in list:                  # gets average value of every element in a list
        init_element += element           # useful when calc value
    
    return float(init_element) / denominator


def galaxy_brightness(brightness_list):
    """Gets a list of brightness values for each list. 
    Parameter: * list *
    Output: * new list *
    
    Total R (red band) magnitude and its error.  This was the band at which the
    basic catalog was constructed.  Magnitudes are inverted logarithmic measures
    of brightness.  A  galaxy with R=21 is 100-times brighter than one with R=26."""
    
    bright_line = []
    
    for brightness in brightness_list:         
        bright_line.append(brightness)      
        
    return bright_line


def get_redshift():
    """Gets redshift value of all galaxies.
    Parameter: * None *
    Output: * List of redshift values * """
    
    redshift_list = extract_galaxy_data('galaxy.csv', ['Mcz'])
    return redshift_list


def galaxy_speed(redshift_column_list):
    """Parameter = red shift list; Output = lists of vals of galaxies with certain
    red shift values."""
    
    #groups separated according to quartiles
    v_slow_gal = [] # 0- first quartile
    slow_gal = [] # first quartile to median
    fast_gal = [] # median to third quartile
    v_fast_gal = [] #third quartile to 1
    
    for redshift_value in redshift_column_list:
        
        if redshift_value <=0.405:
            v_slow_gal.append(redshift_value)
        elif redshift_value <= 0.81:
            slow_gal.append(redshift_value)
        elif redshift_value <= 0.905:
            fast_gal.append(redshift_value)
        else:
            v_fast_gal.append(redshift_value)
    
    print        
    print len(v_slow_gal), "galaxies have a speed between 0 and 0.405."
    print len(slow_gal), "galaxies have a speed between 0.405 and 0.81."
    print len(fast_gal), "galaxies have a speed between 0.81 and 0.905."
    print len(v_fast_gal), "galaxies have a speed between 0.905 and 1."
    print
    
    total = float(len(v_slow_gal) + len(slow_gal) + len(fast_gal) + len(v_fast_gal))
    
    print float(len(v_slow_gal)/total *100), "%", "of galaxies are moving at a very slow pace"
    print float(len(slow_gal)/total *100),  "%", "of galaxies are moving at a slow pace"
    print float(len(fast_gal)/total *100),  "%", "of galaxies are moving at a fast pace"
    print float(len(v_fast_gal)/total *100),  "%", "of galaxies are moving at a very fast pace"
    print
    
    assert float(len(v_slow_gal) + len(slow_gal) + len(fast_gal) + len(v_fast_gal)) == 3462.0
    assert float(len(v_slow_gal)/total *100) + float(len(slow_gal)/total *100) + float(len(fast_gal)/total *100) + float(len(v_fast_gal)/total *100) == 100


def plot_brightness_vs_size():
    """Plots a graph that give info about the correlation between brightness and size
    of a galaxy."""
    
    plt.clf()
    
    rmag = extract_galaxy_data('galaxy.csv', ['Rmag'])
    mu_max = extract_galaxy_data('galaxy.csv', ['mumax'])
    gal = galaxy_brightness(extract_galaxy_data('galaxy.csv', ['Rmag']))
    size = get_size(rmag, mu_max)

    x = [[i] for i in size]
    y = [b for b in gal]
    #y = [i + np.random.uniform(0, 1) for i in range(10)]
    
    plt.xlabel('Size of Galaxy')
    plt.ylabel('Brightness of Galaxy')
    plt.title('Correlation between Size and Brightness of Galaxies')

    # fit a line
    model = LinearRegression(x, y)
    model.fit(x, y)

    line_x = x
    line_y = [model.coef_ * x + model.intercept_ for x in line_x]
   # print "Slope is", model.coef_
   # print "Intercept is", model.intercept_
    
    #scatter_x = range(10)
    
    plt.scatter(size, gal, marker = ".", s=1, color='purple')
    plt.plot(line_x, line_y, color='yellow', marker='+', linestyle='dashed',
        linewidth=1, markersize=1,label='y = 1.875 x + 24.394         r-value = 0.79804859231618086')
    
    # plt.plot(x, y)
    plt.legend()
    
    plt.savefig("graph-brightness-sizes.jpeg")
    plt.show()


def plot_redshift_vs_size():
    """Plots a graph that give info about the correlation between redshift and size
    of a galaxy."""
    
    plt.clf()
    
    rmag = extract_galaxy_data('galaxy.csv', ['Rmag'])
    speed = extract_galaxy_data('galaxy.csv', ['mumax'])
    
    gal = galaxy_brightness(extract_galaxy_data('galaxy.csv', ['Mcz']))
    size = get_size(rmag, speed)

    x = [[i] for i in size]
    y = [b for b in gal]
    #y = [i + np.random.uniform(0, 1) for i in range(10)]
    
    plt.xlabel('Size of Galaxy')
    plt.ylabel('Redshift of Galaxy')
    plt.title('Correlation between Size and Redshift of Galaxies')

    # fit a line
    model = LinearRegression(x, y)
    model.fit(x, y)

    line_x = x
    line_y = [model.coef_ * x + model.intercept_ for x in line_x]
    horiz_val = line_x
    min = [0.007 for i in range(len(size))]
    max = [1.379 for i in range(len(size))]
         
    plt.scatter(size, gal, marker = ".", s=1, color='blue')
   
    plt.plot(horiz_val, min, color = 'yellow', label='Minimum Redshift')
    plt.plot(horiz_val, max, color = 'green',label='Maximum Redshift')
    plt.legend()

    plt.show()
    plt.savefig("graph-redshift-sizes.jpeg")   


def get_redshift():
    """Gets redshift value of all galaxies
    Parameter: * None *
    Output: statements of the galaxies with the smallest and largest redshift value."""
    
    mn_list = extract_galaxy_data('galaxy.csv', ['Mcz'])
    
    return mn_list


def get_min_max_redshift():
    """Gets redshift value of all galaxies
    Parameter: * None *
    Output: statements of the galaxies with the smallest and largest redshift value."""
    
    mn_list = extract_galaxy_data('galaxy.csv', ['Mcz'])
    
    new_list = sorted(mn_list)

    print "The smallest redshift value is", new_list[0]
    print "The largest redshift value is", new_list[-1]
    
    assert new_list[0] == 0.007
    assert new_list[-1] == 1.379

def get_gal_number():
    """Returns list of names of galaxies.
    Parameter: * None *
    Output: * name list * """
    
    name_list = extract_galaxy_data("galaxy.csv", ["Nr"])
    return name_list


def welcome_intro():
    """Intro to Galaxies Program.
    Parameter: * None *
    Output: * Welcome statements * """
    
    print "**************************************"
    print "** Analyzing Galactic Environments ***"
    print "**************************************"
    
    
def get_red_blue_graph():
    """Plots a graph that give info about how the galaxy is moving and how it 
    affects the 5 traditional broad spectral bands of a galaxy."""
    
    plt.clf()
    bands = extract_galaxy_data('galaxy.csv', ['W420FE', 'W462FE', 'W462FE', 'W518FE', 'W571FS', 'W604FE', 'W646FD', 'W696FE', 'W753FE', 'W815FS','W856FD', 'W914FD', 'W914FE'])
    redshift = extract_galaxy_data('galaxy.csv', ['Mcz','Mcz', 'Mcz', 'Mcz', 'Mcz', 'Mcz', 'Mcz', 'Mcz', 'Mcz', 'Mcz', 'Mcz','Mcz','Mcz'])
    
    # x = color band ( correlated directly 5 traditional broad spectral bands )
    # y = redshift (distance)

    y = [redshift]
    x = [bands]

    plt.scatter(x, y, marker = ".", s=1, color='blue')
    
    #axis labels
    plt.legend()
    plt.xlabel('Redshift Value')
    plt.ylabel('5 traditional broad spectral bands')
    plt.title('The Effects of Speed on Broad Spectral Bands')
    plt.legend(loc = "upper right")

    plt.savefig('red_blue.jpeg', dpi=None, facecolor='w', edgecolor='w',
        orientation='landscape', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)
    
    plt.show()
    
################################################################################  
# Main Function                                                                
################################################################################
def main():   
    welcome_intro()
    print
    print "Problem 1: How does the brightness of galaxies affect the size of the galaxy?"
    print "Result: According to our plot_brightness_vs_size() function, the greater the size of the galaxy, the brighter the galaxy."
    rmag = extract_galaxy_data('galaxy.csv', ['Rmag'])
    mu_max = extract_galaxy_data('galaxy.csv', ['mumax'])
    gal = galaxy_brightness(extract_galaxy_data('galaxy.csv', ['Rmag']))
    size = get_size(rmag, mu_max)
    print "The p-value of our data is:", pearsonr(size,gal)[0]
    plot_brightness_vs_size()
    print 
    print "Problem 2: Categorize galaxies based on their redshift value to analyze the movement/speed in the universe."
    print "Result: A majority of the galaxies (39.83%) are traveling at the fastest speed with"
    print "a redshift value between 0.905 and 1. "
    rs = get_redshift()
    galaxy_speed(rs)
    get_min_max_redshift()
    print
    print "Problem 3: How does the size of the bands of a galaxy affect the red shift values of a galaxy?"
    print "Result: There is no correlation between the size of the bands of a galaxy and the red shift values."
    print "This can be seen in our graph where there is no linear correlation with respect to the data we used to"
    print "plot the points of our graph."
    plot_redshift_vs_size()
    print 
    print "Problem 4: Find the effect of redshift on observed brightnesses in 13 bands."
    print "Result: Galaxies can be observed in other color bands but a majority of them"
    print "resides in 650 - 800 nm which equates to the color red. "
    get_red_blue_graph()
    
    
if __name__ == "__main__":
    main()