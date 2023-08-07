#!/usr/bin/env python3  
# -*- coding: utf-8 -*- 
#----------------------------------------------------------------------------
# Created Date: 09/01/2023 13:10
# version = '1.0'
# ---------------------------------------------------------------------------
""" MY470 Computer Programming Final Assignment"""

# ---------------------------------------------------------------------------
import datetime
# ---------------------------------------------------------------------------

def read_kills_data(file_kills = '../assignment-final-data/kills.txt'):
    """A function to read the kills data. It organises it in the form of an dictionary with the stucture:
    {match_id: [[killer1, killed1, time1],  [[killer2, killed2, time2]…[killerN, killed, timeN]]]"""
    kills = {}
    with open(file_kills, 'r') as f:
        lines = f.readlines()
    for line in lines:
        match_id, killer, killed, time = line.strip().split('\t')
        if match_id not in kills:
            kills[match_id] = []
        kills[match_id].append([killer, killed, time])
    return kills

def read_team_data_id(file_team_data = '../assignment-final-data/team_ids.txt'):
    """A function to read the team ID data. It organises it in the form of an dictionary with the stucture:
    {match_id: [[player1, player2, player3…playerN][[team_id_player1, team_id_player2, team_id_player3…team_id_playerN]"""
    team_id = {}
    with open(file_team_data, 'r') as f:
        for line in f:
            match_id, player_account_id, team_ids = line.strip().split('\t')
            if match_id not in team_id:
                team_id[match_id] = [[player_account_id], [team_ids]]
            else:
                team_id[match_id][0].append(player_account_id)
                team_id[match_id][1].append(team_ids)
    return team_id

def read_cheaters_data(file_cheaters= '../assignment-final-data/cheaters.txt'):
    """A function to read the cheaters data. It organises it in the form of an dictionary with the structure:
    {player_id, start_timestamp, banned_timestamp}"""
    cheaters = {}
    with open(file_cheaters, 'r') as f:
        lines = f.readlines()
    for line in lines:
        player_id, start_timestamp, banned_timestamp, *_ = line.strip().split()
        start_timestamp = datetime.datetime.strptime(start_timestamp, "%Y-%m-%d")
        banned_timestamp = datetime.datetime.strptime(banned_timestamp, "%Y-%m-%d")
        cheaters[player_id] =[start_timestamp,banned_timestamp]
    return cheaters

