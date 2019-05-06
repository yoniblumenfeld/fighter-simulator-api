import json
import os
import random

#Each martial art has name as a key and min to max value tuple as value
FIGHTING_STATS_FILE_PATH = "fighting_stats.json"
MARTIAL_ARTS = {
    "kungfu":(80,100),
    "thaibox":(90,98),
    "boxing":(80,100),
    "kravmaga":(92,95)
}

def get_fighter_total_power(fighter):
    """
    Gets a fighter dictionary containing:
    stamina,
    strength,
    speed,
    martial_art
    Returns the fighter total power considering all aspects
    """
    martial_art_min,martial_art_max = MARTIAL_ARTS[fighter['martial_art']]
    martial_art_rand_res = random.randint(martial_art_min,martial_art_max)
    return(fighter['stamina']*0.20 +
           fighter['strength']*0.25 +
           fighter['speed']*0.25 +
           martial_art_rand_res*0.30)


def create_stats_file():
    fileobj = open(FIGHTING_STATS_FILE_PATH,"w")
    json.dump(MARTIAL_ARTS,fileobj)
    fileobj.close()

def get_stats_json():
    with open(FIGHTING_STATS_FILE_PATH,"r") as fileobj:
        return json.load(fileobj)


if __name__ == "__main__":
    create_stats_file()
    print(get_stats_json())