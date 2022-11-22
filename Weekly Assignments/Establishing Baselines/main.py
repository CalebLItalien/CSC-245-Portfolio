'''
#Caleb L'Italien
#CSC-245
#Homework 1, Part 1
#Calculates the perceived time to stars based on distance and the speed of light
'''
import math

SPEED_OF_LIGHT = 299792458
LY_TO_METERS_CONVERSION = 9460730472580800
SECONDS_TO_YEARS_CONVERSION = 31556952

def star_travel_time(distance, percentage):
    '''
    Calculates the perceived time of travelers based on distance traveled and speed, a percentage of the speed of light.
    :param distance: Distance in light years
    :param percentage: A percentage of the speed of light
    :return: The percieved time

    HOW TO USE FUNCTION:
        Call the function, entering two arguments. The first argument is the distance in light years, the second
        is the percentage of the speed of light. Percentage can be entered as a whole number or decimal (ie: 50 or 0.5).
        Examples:
        star_travel_time(4.0, 50)
        star_travel_time(2, 0.3)
        star_travel_time(1.0, 65)
    '''
    valid_arguments = True
    if percentage > 1:
        percentage_decimal = percentage / 100
    elif percentage < 0:
        print("Invalid percentage")
        valid_arguments = False
    else:
        percentage_decimal = percentage

    if distance <= 0:
        print("Invalid distance")
        valid_arguments = False

    distance_meters = distance * LY_TO_METERS_CONVERSION

    if valid_arguments:
        velocity = SPEED_OF_LIGHT * percentage_decimal
        factor = 1/(math.sqrt(1 - (velocity**2 / SPEED_OF_LIGHT**2)))

        real_time = distance_meters/velocity
        real_time_years = real_time / SECONDS_TO_YEARS_CONVERSION

        experienced_time = real_time_years / factor
        return experienced_time