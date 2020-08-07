'''
contains all poplulaion matrrix
'''

from glob import glob
import os
import numpy as np
from animation import get_motion_parameters
from utils import check_folder

def initialize_population(Config, mean_age=45, max_age=105,
                          xbounds=[0, 1], ybounds=[0, 1]):
    '''initialized for the simulation

    15 column in pop matrix the pop matrix for this simulation has the following columns:

    0 :  ID
    1 : x coordinate
    2 : y coordinate
    3 : heading in x
    4 : heading in y
    5 : speed
    6 : state (0=healthy, 1=sick, 2=immune, 3=dead, 4=immune but infectious)
    7 : age
    8 : infected
    9 : recovery factor to determine person die or recover
    10 : in process to get healthy
    11 : active destination
    12 : at destination:0=traveling, 1=arrived
    13 : range_x : wander ranges on x axis for those who are confined to a location
    14 : range_y
'''
    pop = np.zeros((Config.size_pop, 15))

    #initalize unique IDs
    pop[:,0] = [x for x in range(Config.size_pop)]

    #initialize random coordinates
    pop[:,1] = np.random.uniform(low = xbounds[0] + 0.05, high = xbounds[1] - 0.05,
                                        size = (Config.size_pop,))
    pop[:,2] = np.random.uniform(low = ybounds[0] + 0.05, high = ybounds[1] - 0.05,
                                        size=(Config.size_pop,))

    #initialize random headings -1 to 1
    pop[:,3] = np.random.normal(loc = 0, scale = 1/3,
                                       size=(Config.size_pop,))
    pop[:,4] = np.random.normal(loc = 0, scale = 1/3,
                                       size=(Config.size_pop,))

    #initialize random speeds
    pop[:,5] = np.random.normal(Config.speed, Config.speed / 2)

    #initalize ages
    std_age = (max_age - mean_age) / 3
    pop[:,7] = np.int32(np.random.normal(loc = mean_age,
                                                scale = std_age, 
                                                size=(Config.size_pop,)))

    pop[:,7] = np.clip(pop[:,7], a_min = 0,
                              a_max = max_age)

    #build recovery_vector
    pop[:,9] = np.random.normal(loc = 0.5, scale = 0.5 / 2, size=(Config.size_pop,))
    return pop

def initialize_destination_matrix(size_pop, total_destinations):
    destinations = np.zeros((size_pop, total_destinations * 2))
    return destinations


def set_destination_bounds(pop, destinations, xmin, ymin,
                           xmax, ymax, dest_no=1, teleport=True):
    '''teleports all persons in limits
    dest_no : int
        the destination number to set as active (if more than one)

    teleport : bool
        whether to instantly teleport individuals to the defined locations
    '''

    #teleport
    if teleport:
        pop[:,1] = np.random.uniform(low = xmin, high = xmax, size = len(pop))
        pop[:,2] = np.random.uniform(low = ymin, high = ymax, size = len(pop))

    x_center, y_center, x_wander, y_wander = get_motion_parameters(xmin, ymin, 
                                                                   xmax, ymax)
    #destination centers
    destinations[:,(dest_no - 1) * 2] = x_center
    destinations[:,((dest_no - 1) * 2) + 1] = y_center
    #wander bounds
    pop[:,13] = x_wander
    pop[:,14] = y_wander

    pop[:,11] = dest_no #active destination
    pop[:,12] = 1 #destination reached

    return pop, destinations
def save_data(pop, pop_tracker):
    num_files = len(glob('data/*'))
    check_folder('data/%i' %num_files)
    np.save('data/%i/pop.npy' %num_files, pop)
    np.save('data/%i/infected.npy' %num_files, pop_tracker.infectious)
    np.save('data/%i/recovered.npy' %num_files, pop_tracker.recovered)
    np.save('data/%i/fatalities.npy' %num_files, pop_tracker.fatalities)


def save_population(pop, tstep=0, folder='data_tstep'):
    check_folder('%s/' %(folder))
    np.save('%s/population_%i.npy' %(folder, tstep), pop)


class Population_trackers():
    def __init__(self):
        self.susceptible = []
        self.infectious = []
        self.recovered = []
        self.fatalities = []

        self.reinfect = False 

    def update_counts(self, pop):
        size_pop = pop.shape[0]
        self.infectious.append(len(pop[pop[:,6] == 1]))
        self.recovered.append(len(pop[pop[:,6] == 2]))
        self.fatalities.append(len(pop[pop[:,6] == 3]))

        if self.reinfect:
            self.susceptible.append(size_pop - (self.infectious[-1] +
                                                self.fatalities[-1]))
        else:
            self.susceptible.append(size_pop - (self.infectious[-1] +
                                                self.recovered[-1] +
                                                self.fatalities[-1]))
