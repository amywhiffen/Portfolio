#!/usr/bin/env python3  
# -*- coding: utf-8 -*- 
#----------------------------------------------------------------------------
# Created Date: 20/01/2023 13:54
# version = '1.0'
# ---------------------------------------------------------------------------
""" MY470 Computer Programming Final Assignment"""
# ---------------------------------------------------------------------------
import random
import copy
import numpy as np
from collections import Counter
import datetime
import time
# ---------------------------------------------------------------------------
from basicFunctions import count_cheaters, estimate_expected_counts, is_cheater_yet, shuffle_players, get_players_in_match, get_victims_turn_cheaters, count_observers_start_cheating
from readData import read_kills_data, read_team_data_id, read_cheaters_data
# ---------------------------------------------------------------------------

def study_estimate_expected_counts(file_team_data, file_cheaters, n=20):
    """The function takes in 3 input arguments, reads team and cheater 
    data from files, calls the estimate_expected_counts() function to obtain the empirical mean and 
    randomised mean with a 95% confidence interval of the number of cheaters in each team, 
    prints these results and returns them as output."""
    cheaters = read_cheaters_data()
    team_id = read_team_data_id()
    
    empirical_mean = estimate_expected_counts(team_id, cheaters, randomise = False, n = None)
    randomised_mean_confidence_interval = estimate_expected_counts(team_id, cheaters, randomise = True, n = n)
    
    print("Empirical count is:", empirical_mean)
    print("Randomised mean and confidence interval is:", randomised_mean_confidence_interval)
    
    return empirical_mean, randomised_mean_confidence_interval

def study_victims_turn_cheaters(file_cheaters, file_kills, n=20):
    """This function reads cheaters and kills data from the given files and 
    calls get_victims_turn_cheaters function to calculate the number of victims that turn into cheaters. 
    It also shows the results of empirical mean, randomised mean, and confidence interval."""
    cheaters = read_cheaters_data()
    kills = read_kills_data()
    
    empirical_mean,_ = get_victims_turn_cheaters(cheaters, kills)
    randomised_mean, confidence_interval = get_victims_turn_cheaters(cheaters, kills, randomised = True, n = n)
    
    print("Empirical count is:", empirical_mean)
    print("Randomised mean is:", randomised_mean)
    print("Confidence Interval is:", confidence_interval)
    
    return empirical_mean, randomised_mean, confidence_interval

def study_count_observers_start_cheating(file_cheaters, file_kills, n=20):
    """This function reads cheaters and kills data from the given files and calls count_observers_start_cheating 
    function to calculate the number of observers that start cheating. 
    It also returns and shows the results of empirical mean, randomised mean, and confidence interval."""
    cheaters = read_cheaters_data()
    kills = read_kills_data()
    
    empirical_mean,_ = count_observers_start_cheating(cheaters, kills)
    randomised_mean, confidence_interval = count_observers_start_cheating(cheaters, kills, randomised = True, n = n)
    
    print("Empirical count is:", empirical_mean)
    print("Randomised mean is:", randomised_mean)
    print("Confidence Interval is:", confidence_interval)
    
    return empirical_mean, randomised_mean, confidence_interval