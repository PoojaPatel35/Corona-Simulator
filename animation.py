'''
file that contains all function related to pop mobility
'''

import numpy as np

def update_positions(pop):
    pop[:,1] = pop[:,1] + (pop[:,3] * pop[:,5])
    pop[:,2] = pop[:,2] + (pop [:,4] * pop[:,5])
    return pop
def out_of_bounds(pop, xbounds, ybounds):

    #determine number of elements that need to be updated

    shp = pop[:,3][(pop[:,1] <= xbounds[:,0]) &
                            (pop[:,3] < 0)].shape
    pop[:,3][(pop[:,1] <= xbounds[:,0]) &
                    (pop[:,3] < 0)] = np.clip(np.random.normal(loc = 0.5,
                                                                        scale = 0.5/3,
                                                                        size = shp),
                                                        a_min = 0.05, a_max = 1)

    shp = pop[:,3][(pop[:,1] >= xbounds[:,1]) &
                            (pop[:,3] > 0)].shape
    pop[:,3][(pop[:,1] >= xbounds[:,1]) &
                    (pop[:,3] > 0)] = np.clip(-np.random.normal(loc = 0.5,
                                                                        scale = 0.5/3,
                                                                        size = shp),
                                                        a_min = -1, a_max = -0.05)

    #update y heading
    shp = pop[:,4][(pop[:,2] <= ybounds[:,0]) &
                            (pop[:,4] < 0)].shape
    pop[:,4][(pop[:,2] <= ybounds[:,0]) &
                    (pop[:,4] < 0)] = np.clip(np.random.normal(loc = 0.5,
                                                                        scale = 0.5/3,
                                                                        size = shp),
                                                        a_min = 0.05, a_max = 1)

    shp = pop[:,4][(pop[:,2] >= ybounds[:,1]) &
                            (pop[:,4] > 0)].shape
    pop[:,4][(pop[:,2] >= ybounds[:,1]) &
                    (pop[:,4] > 0)] = np.clip(-np.random.normal(loc = 0.5,
                                                                        scale = 0.5/3,
                                                                        size = shp),
                                                        a_min = -1, a_max = -0.05)

    return pop


def update_randoms(pop, size_pop, speed=0.5, heading_update_chance=0.02,
                   speed_update_chance=0.02, heading_multiplication=1,
                   speed_multiplication=1):

    #randomly update heading
    #x
    update = np.random.random(size=(size_pop,))
    shp = update[update <= heading_update_chance].shape
    pop[:,3][update <= heading_update_chance] = np.random.normal(loc = 0,
                                                        scale = 1/3,
                                                        size = shp) * heading_multiplication
    #y
    update = np.random.random(size=(size_pop,))
    shp = update[update <= heading_update_chance].shape
    pop[:,4][update <= heading_update_chance] = np.random.normal(loc = 0,
                                                        scale = 1/3,
                                                        size = shp) * heading_multiplication
    #randomize speeds
    update = np.random.random(size=(size_pop,))
    shp = update[update <= heading_update_chance].shape
    pop[:,5][update <= heading_update_chance] = np.random.normal(loc = speed,
                                                        scale = speed / 3,
                                                        size = shp) * speed_multiplication

    pop[:,5] = np.clip(pop[:,5], a_min=0.0001, a_max=0.05)
    return pop


def get_motion_parameters(xmin, ymin, xmax, ymax):
    x_center = xmin + ((xmax - xmin) / 2)
    y_center = ymin + ((ymax - ymin) / 2)

    x_wander = (xmax - xmin) / 2
    y_wander = (ymax - ymin) / 2

    return x_center, y_center, x_wander, y_wander
