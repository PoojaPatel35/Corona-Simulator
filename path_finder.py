
# contains methods related to path planning


import numpy as np

from animation import get_motion_parameters, update_randoms

def go_to_location(patient, destination, location_bounds, dest_no=1):

    x_center, y_center, x_wander, y_wander = get_motion_parameters(location_bounds[0],
                                                                    location_bounds[1],
                                                                    location_bounds[2],
                                                                    location_bounds[3])
    patient[13] = x_wander
    patient[14] = y_wander
    
    destination[(dest_no - 1) * 2] = x_center
    destination[((dest_no - 1) * 2) + 1] = y_center
    patient[11] = dest_no
    return patient, destination

def set_destination(pop, destinations):
    active_dests = np.unique(pop[:,11][pop[:,11] != 0])

    #set destination
    for d in active_dests:
        dest_x = destinations[:,int((d - 1) * 2)]
        dest_y = destinations[:,int(((d - 1) * 2) + 1)]
        #compute new headings
        head_x = dest_x - pop[:,1]
        head_y = dest_y - pop[:,2]

        #reinsert headings into pop of those not at destination yet
        pop[:,3][(pop[:,11] == d) &
                        (pop[:,12] == 0)] = head_x[(pop[:,11] == d) &
                                                            (pop[:,12] == 0)]
        pop[:,4][(pop[:,11] == d) &
                        (pop[:,12] == 0)] = head_y[(pop[:,11] == d) &
                                                            (pop[:,12] == 0)]
        #set speed to 0.01
        pop[:,5][(pop[:,11] == d) &
                        (pop[:,12] == 0)] = 0.02

    return pop


def check_at_destination(pop, destinations, wander_factor=1.5, speed = 0.5):
    active_dests = np.unique(pop[:,11][(pop[:,11] != 0)])

    #see who is at destination
    for d in active_dests:
        dest_x = destinations[:,int((d - 1) * 2)]
        dest_y = destinations[:,int(((d - 1) * 2) + 1)]

        #see who arrived at destination and filter out who already was there
        at_dest = pop[(np.abs(pop[:,1] - dest_x) < (pop[:,13] * wander_factor)) &
                                (np.abs(pop[:,2] - dest_y) < (pop[:,14] * wander_factor)) &
                                (pop[:,12] == 0)]

        if len(at_dest) > 0:
            #mark those as arrived
            at_dest[:,12] = 1
            #insert random headings and speeds for those at destination
            at_dest = update_randoms(at_dest, size_pop = len(at_dest), speed = speed,
                                     heading_update_chance = 1, speed_update_chance = 1)

            #at_dest[:,5] = 0.001

            #reinsert into pop
            pop[(np.abs(pop[:,1] - dest_x) < (pop[:,13] * wander_factor)) &
                        (np.abs(pop[:,2] - dest_y) < (pop[:,14] * wander_factor)) &
                        (pop[:,12] == 0)] = at_dest
    return pop

def keep_at_destination(pop, destinations, wander_factor=1):

    #how many destinations are active
    active_dests = np.unique(pop[:,11][(pop[:,11] != 0) &
                                                (pop[:,12] == 1)])

    for d in active_dests:
        dest_x = destinations[:,int((d - 1) * 2)][(pop[:,12] == 1) &
                                                    (pop[:,11] == d)]
        dest_y = destinations[:,int(((d - 1) * 2) + 1)][(pop[:,12] == 1) &
                                                        (pop[:,11] == d)]

        #see who is marked as arrived
        arrived = pop[(pop[:,12] == 1) &
                                (pop[:,11] == d)]

        ids = np.int32(arrived[:,0]) # find unique IDs of arrived persons

        shp = arrived[:,3][arrived[:,1] > (dest_x + (arrived[:,13] * wander_factor))].shape

        arrived[:,3][arrived[:,1] > (dest_x + (arrived[:,13] * wander_factor))] = -np.random.normal(loc = 0.5,
                                                                scale = 0.5 / 3,
                                                                size = shp)


        #where x smaller than destination - wander, set heading positive
        shp = arrived[:,3][arrived[:,1] < (dest_x - (arrived[:,13] * wander_factor))].shape
        arrived[:,3][arrived[:,1] < (dest_x - (arrived[:,13] * wander_factor))] = np.random.normal(loc = 0.5,
                                                            scale = 0.5 / 3,
                                                            size = shp)
        #where y larger than destination + wander, set heading negative
        shp = arrived[:,4][arrived[:,2] > (dest_y + (arrived[:,14] * wander_factor))].shape
        arrived[:,4][arrived[:,2] > (dest_y + (arrived[:,14] * wander_factor))] = -np.random.normal(loc = 0.5,
                                                                scale = 0.5 / 3,
                                                                size = shp)
        #where y smaller than destination - wander, set heading positive
        shp = arrived[:,4][arrived[:,2] < (dest_y - (arrived[:,14] * wander_factor))].shape
        arrived[:,4][arrived[:,2] < (dest_y - (arrived[:,14] * wander_factor))] = np.random.normal(loc = 0.5,
                                                            scale = 0.5 / 3,
                                                            size = shp)

        #slow speed
        arrived[:,5] = np.random.normal(loc = 0.005,
                                        scale = 0.005 / 3, 
                                        size = arrived[:,5].shape)

        #reinsert into pop
        pop[(pop[:,12] == 1) &
                    (pop[:,11] == d)] = arrived
                                
    return pop
def reset_destinations(pop, ids=[]):

    if len(ids) == 0:
        #if ids empty, reset everyone
        pop[:,11] = 0
    else:
        pass
        #else, reset id's

    pass
