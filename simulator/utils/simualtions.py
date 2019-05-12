from fighter_simulator_api.utils import fighting_stats_data
import random

def simualte_fight(fighter1,fighter2):
    """
    Accepts two fighter objects.
    returns True if first fighter passed wins.
    returns False otherwise.
    """
    f1_total_rank = int(fighting_stats_data.get_fighter_total_power(fighter1))
    f2_total_rank = int(fighting_stats_data.get_fighter_total_power(fighter2))
    total_ranks = f1_total_rank + f2_total_rank
    rand_num = random.randint(1,total_ranks)
    return True if 1 <= rand_num <= f1_total_rank else False
