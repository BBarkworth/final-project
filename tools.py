import math
# for log and round down calcs

def rating(func_dict):
    log_dict = {}
    for key, value in func_dict.items():
        log_num = math.log10(value)
        log_dict[key] = log_num
    final_dict = {}
    max_num = 0
    min_num = 0
    counter = 0
    for key, value in log_dict.items():
        if value > max_num:
            max_num = value
        if counter < 1:
            min_num = value
        if min_num > value:
            min_num = value
        counter += 1
    for key, value in log_dict.items():
        new_max = 5
        new_min = 1 
        new_value = (new_max - new_min) / (max_num - min_num) * (value - max_num) + 5
        new_value = round(new_value)
        final_dict[key] = new_value
    return(final_dict)
    # function to convert the data from large values to rating out of 5 via log10 and data normalising

def rating_change(winner, loser):
    K_factor = 75
    l = 10 ** (winner/400)
    r = 10 ** (loser/400)
    l2 = l / (l+r)
    r2 = r / (l+r)
    lfinal = round(winner + K_factor*(1-l2))
    rfinal = round(loser + K_factor*(0-r2))
    return(lfinal, rfinal)
# function to work out rating change for each match 

def ties(team1, team2):
    K_factor = 75
    t1 = 10 ** (team1/400)
    t2 = 10 ** (team2/400)
    t1divide = t1 / (t1+t2)
    t2divide = t2 / (t1+t2)
    team1final = round(team1 + K_factor*(0.5-t1divide))
    team2final = round(team2 + K_factor*(0.5-t2divide))
    return(team1final, team2final)
# function to work out rating change for each match for ties

def carry_over(rating):
    new_rating = (0.75 * rating) + (0.25 * 1500)
    return new_rating
# function to reduce how much of an effect previous season's data has