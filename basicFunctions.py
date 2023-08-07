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
from readData import read_kills_data, read_team_data_id, read_cheaters_data
# ---------------------------------------------------------------------------

def count_cheaters(l, cheaters):
    """The function takes a list and a dictionary as input, 
    it counts the number of items in the list that are in the dictionary and returns the total count."""
    cheater_count = 0
    for item in l:
        if item in cheaters:
            cheater_count += 1
    return cheater_count

def estimate_expected_counts(team_id, cheaters, randomise = False, n = None):
    """The function takes in a dictionary of match IDs, 
    a dictionary of cheater accounts, and two optional arguments; a boolean indicating whether to 
    shuffle team IDs and an integer indicating number of iterations. It counts the number of cheaters in 
    each team and returns the expected counts by averaging over the number of iterations."""
    match_ids = set(list(team_id.keys()))
    teams_with_cheaters = {0:0, 1:0, 2:0, 3:0}

    if not randomise:
        for match in match_ids:
            accounts = team_id[match][0]
            team_ids = team_id[match][1].copy()

            temp_team_dict = {}
            for t in range(len(team_ids)):
                if team_ids[t] in temp_team_dict.keys(): 
                    temp_team_dict[team_ids[t]].append(accounts[t])
                else:
                    temp_team_dict[team_ids[t]] = [accounts[t]]

            for team, players in temp_team_dict.items():
                cheaters_per_team = count_cheaters(players, cheaters)
                if cheaters_per_team in [0, 1, 2, 3]:
                    teams_with_cheaters[cheaters_per_team]+=1

        counts = teams_with_cheaters
        
        return counts

    else:
        teams_with_cheaters_randomised={0:[], 1:[], 2:[], 3:[]}

        for i in range(n):
            teams_with_cheaters = {0:0, 1:0, 2:0, 3:0}
            for match in match_ids:
                accounts = team_id[match][0]
                team_ids = team_id[match][1].copy()
                np.random.shuffle(team_ids)

                temp_team_dict = {}
                for t in range(len(team_ids)):
                    if team_ids[t] in temp_team_dict.keys(): 
                        temp_team_dict[team_ids[t]].append(accounts[t])
                    else:
                        temp_team_dict[team_ids[t]] = [accounts[t]]

                cheaters_per_team = {}       
                for team, player in temp_team_dict.items():
                    cheaters_per_team = count_cheaters(player, cheaters)
                    if cheaters_per_team in [0, 1, 2, 3]:
                        teams_with_cheaters[cheaters_per_team]+=1
                        
            for k, v in teams_with_cheaters.items():
                teams_with_cheaters_randomised[k].append(v)

    
        counts_randomised = {k: [np.mean(v), [np.mean(v) - 1.96 * np.std(v) / np.sqrt(n), np.mean(v) + 1.96 * np.std(v) / np.sqrt(n)]] for k, v in teams_with_cheaters_randomised.items()}

        return counts_randomised

def is_cheater_yet(cheaters, p, date):
    """The function takes a player and a date as input, and checks if the player was a cheater at the given date 
    by checking the player's existence in a dictionary called 'cheaters' and the date of the input is after the date 
    the player became a cheater. 
    It returns True if the player was a cheater at the given date and False otherwise."""
    if p in cheaters.keys():
        if date > cheaters[p][0]:
            return True
        else:
            return False
    else:
        return False

def shuffle_players(kills, match_id):
    """The function shuffles player IDs for a selected match in the kills dictionary 
    and relabels the match kills with the shuffled player IDs""" 
    match_kills = kills[match_id]
    players_in_match = get_players_in_match(kills, match_id, offset=0)
    players_shuffled = players_in_match.copy()
    np.random.shuffle(players_shuffled)
    relabelled_ids = dict(zip(players_in_match, players_shuffled))
    
    return [[relabelled_ids[kill[0]], relabelled_ids[kill[1]], kill[2]] for kill in match_kills]


def get_players_in_match(kills, match_id, offset=0):
    """This function takes in match kills data, a match id and an optional offset, and returns a list of unique players in the match, 
    after skipping over a certain number of elements in the kills data, as specified by the offset."""
    match_kills = kills[match_id]
    players_in_match = []

    for i in range(offset, len(match_kills)):
        item = match_kills[i]
        players_in_match.append(item[0])
        players_in_match.append(item[1])

    players_in_match = list(set(players_in_match))
    return players_in_match

def get_victims_turn_cheaters(cheaters, kills, randomised = False, n = None, global_detected_victims_turn_cheaters=[]):
    """This function calculates the number of victims that turn into cheaters in a given set 
    of matches by iterating through the "kills" dictionary and using the "victims_turn_cheaters_per_match" 
    function. If "randomised" is set to True, it will also calculate the mean number of victims that turned 
    into cheaters with a 95% confidence interval by shuffling players in each match "n" times."""
    victims_turn_cheaters = 0
    detected_victims_turn_cheaters = global_detected_victims_turn_cheaters

    if not randomised:
        for match_id in kills.keys():       
            match_kills = kills[match_id]
            match_date = datetime.datetime.strptime(match_kills[0][2][:10], "%Y-%m-%d") 
            for kill in match_kills:
                killer = kill[0]
                killed = kill[1]
                killed_by_cheater = is_cheater_yet(cheaters, killer, match_date)
                if killed_by_cheater:
                    killed_is_cheater = is_cheater_yet(cheaters, killed, match_date)
                    if killed not in detected_victims_turn_cheaters:
                        if not killed_is_cheater:
                            if killed in cheaters.keys():
                                victims_turn_cheaters += 1
                                detected_victims_turn_cheaters.append(killed)
                                
        return victims_turn_cheaters, detected_victims_turn_cheaters

    else:
        victims_turn_cheaters_counts = []
        for i in range(n):
            detected_victims_turn_cheaters = []
            victims_turn_cheaters=0
            for match_id in kills.keys():        
                match_kills = kills[match_id]
                match_kills = shuffle_players(kills, match_id)
                new_victims_turn_cheaters, detected_victims_turn_cheaters = get_victims_turn_cheaters(cheaters, {match_id: match_kills}, randomised = False, global_detected_victims_turn_cheaters = detected_victims_turn_cheaters)
                victims_turn_cheaters += new_victims_turn_cheaters

            victims_turn_cheaters_counts.append(victims_turn_cheaters)
            
        victims_turn_cheaters_mean = np.mean(victims_turn_cheaters_counts)
        victims_turn_cheaters_std = np.std(victims_turn_cheaters_counts)                              
        confidence_interval_95_positive = victims_turn_cheaters_mean + 1.96 * (victims_turn_cheaters_std) / np.sqrt(n)
        confidence_interval_95_negative =  victims_turn_cheaters_mean - 1.96 * (victims_turn_cheaters_std) / np.sqrt(n)  
                                      
        return victims_turn_cheaters_mean, [confidence_interval_95_negative, confidence_interval_95_positive]


def count_observers_start_cheating(cheaters, kills, randomised = False, n = None, global_observers_start_cheating = []):
    """This function calculates the number of observers that start cheating by iterating through the 
    "kills" dictionary and using the function "is_cheater_yet" and "get_players_in_match". 
    If "randomised" is set to True, it will also calculate the mean number of 
    observers that start cheating with a 95% confidence interval by shuffling players in each match "n" times."""
    observers_start_cheating = 0
    detected_observers_start_cheating = global_observers_start_cheating
    
    if not randomised:
        for match_id in kills.keys():
            match_kills = kills[match_id]
            date = datetime.datetime.strptime(match_kills[0][2][:10], "%Y-%m-%d") 
            cheaters_victim_count = {}
            i=0
            while i < len(match_kills) and  max(cheaters_victim_count.values(), default=0)<3:
                killer = match_kills[i][0]
                killed_by_cheater=is_cheater_yet(cheaters, killer,date)       
                if killed_by_cheater: 
                    if killer in cheaters_victim_count.keys():
                        cheaters_victim_count[killer]+=1
                    else:
                        cheaters_victim_count[killer]=1                      
                i+=1    

            if i==len(match_kills):
                pass
            else:
                observers = get_players_in_match(kills, match_id, offset=i)

                for observer in observers:
                    if not observer in detected_observers_start_cheating:
                        observer_is_cheater = is_cheater_yet(cheaters, observer, date) 
                        if not observer_is_cheater:
                            if observer in cheaters.keys():
                                observers_start_cheating+=1
                                detected_observers_start_cheating.append(observer)
                                
        return observers_start_cheating, global_observers_start_cheating
   
    else:
        count_observers_start_cheating_random = []
        for j in range(n):
            detected_observers_start_cheating = []
            observers_start_cheating = 0

            for match_id in kills.keys():
                match_kills = shuffle_players(kills, match_id)
                new_observers_start_cheating, detected_observers_start_cheating = count_observers_start_cheating(cheaters, {match_id: match_kills}, randomised=False, global_observers_start_cheating = detected_observers_start_cheating) 
                
                observers_start_cheating += new_observers_start_cheating
            
            count_observers_start_cheating_random.append(observers_start_cheating)
        
        count_observers_start_cheating_mean = np.mean(count_observers_start_cheating_random)
        count_observers_start_cheating_std = np.std(count_observers_start_cheating_random)                              
        confidence_interval_95_positive = count_observers_start_cheating_mean + 1.96 * (count_observers_start_cheating_std) / np.sqrt(n)
        confidence_interval_95_negative =  count_observers_start_cheating_mean - 1.96 * (count_observers_start_cheating_std) / np.sqrt(n)  
                                      
        return count_observers_start_cheating_mean, [confidence_interval_95_negative, confidence_interval_95_positive]
   

