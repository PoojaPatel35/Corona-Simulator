import os
import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from criteria import Configuration, config_error
from SEIR import find_nearby, infect, recover_or_die, compute_mortality,\
healthcare_infection_correction
from animation import update_positions, out_of_bounds, update_randoms,\
get_motion_parameters
from path_finder import go_to_location, set_destination, check_at_destination,\
keep_at_destination, reset_destinations
from pop_matrix import initialize_population, initialize_destination_matrix,\
set_destination_bounds, save_data, save_population, Population_trackers
from visualiser import build_fig, draw_tstep, set_style

class Simulation():
    #for lockdwon destination -1 means no motion
    def __init__(self, *args, **kwargs):
        #default data
        self.Config = Configuration()
        self.frame = 0
        # default pop init
        self.population_init()
        self.pop_tracker = Population_trackers()
        #destinations vector init
        self.destinations = initialize_destination_matrix(self.Config.size_pop, 1)
        self.figure, self.spec, self.ax1, self.ax2 = build_fig(self.Config)
    def population_init(self):
        self.pop = initialize_population(self.Config, self.Config.mean_age,
                                                self.Config.max_age, self.Config.xbounds, 
                                                self.Config.ybounds)

    def tstep(self):
        '''
        take time step as days
        '''
        active_dests = len(self.pop[self.pop[:,11] != 0])
        # shows population matrix

        if active_dests > 0 and len(self.pop[self.pop[:,12] == 0]) > 0:
            self.pop = set_destination(self.pop, self.destinations)
            self.pop = check_at_destination(self.pop, self.destinations,
                                                   wander_factor = self.Config.wander_factor_dest,
                                                   speed = self.Config.speed)

        if active_dests > 0 and len(self.pop[self.pop[:,12] == 1]) > 0:
            #keep them at destination
            self.pop = keep_at_destination(self.pop, self.destinations,
                                                  self.Config.wander_factor)

        if len(self.pop[:,11] == 0) > 0:
            _xbounds = np.array([[self.Config.xbounds[0] + 0.02, self.Config.xbounds[1] - 0.02]] * len(self.pop[self.pop[:,11] == 0]))
            _ybounds = np.array([[self.Config.ybounds[0] + 0.02, self.Config.ybounds[1] - 0.02]] * len(self.pop[self.pop[:,11] == 0]))
            self.pop[self.pop[:,11] == 0] = out_of_bounds(self.pop[self.pop[:,11] == 0],
                                                                        _xbounds, _ybounds)
        
        #set randoms
        if self.Config.lockdown:
            if len(self.pop_tracker.infectious) == 0:
                mx = 0
            else:
                mx = np.max(self.pop_tracker.infectious)

            if len(self.pop[self.pop[:,6] == 1]) >= len(self.pop) * self.Config.lockdown_percentage or\
               mx >= (len(self.pop) * self.Config.lockdown_percentage):
                #reduce speed for all population
                self.pop[:,5] = np.clip(self.pop[:,5], a_min = None, a_max = 0.001)
                #set speeds of complying people to 0
                self.pop[:,5][self.Config.lockdown_vector == 0] = 0
            else:
                #random update
                self.pop = update_randoms(self.pop, self.Config.size_pop, self.Config.speed)
        else:
            self.pop = update_randoms(self.pop, self.Config.size_pop, self.Config.speed)

        #dead people: set speed and heading to 0
        self.pop[:,3:5][self.pop[:,6] == 3] = 0
        
        #update positions
        self.pop = update_positions(self.pop)

        #find new infections
        self.pop, self.destinations = infect(self.pop, self.Config, self.frame,
                                                    send_to_location = self.Config.self_isolate, 
                                                    location_bounds = self.Config.isolation_bounds,  
                                                    destinations = self.destinations, 
                                                    location_no = 1, 
                                                    location_odds = self.Config.self_isolate_proportion)

        #set self for recover and die
        self.pop = recover_or_die(self.pop, self.frame, self.Config)

        #send cured back to pop if self isolation active or  put in recover or die class
        self.pop[:,11][self.pop[:,6] == 2] = 0
        self.pop_tracker.update_counts(self.pop)

        #visualise
        if self.Config.visualise:
            draw_tstep(self.Config, self.pop, self.pop_tracker, self.frame,
                       self.figure, self.spec, self.ax1, self.ax2)

        #report stuff to console
        sys.stdout.write('\r')
        sys.stdout.write('%i: healthy: %i, infected: %i, immune: %i, in treatment: %i, \
        dead: %i, of total: %i' %(self.frame, self.pop_tracker.susceptible[-1], self.pop_tracker.infectious[-1],
                        self.pop_tracker.recovered[-1], len(self.pop[self.pop[:,10] == 1]),
                        self.pop_tracker.fatalities[-1], self.Config.size_pop))

        #save popdata if required
        if self.Config.save_pop and (self.frame % self.Config.save_pop_freq) == 0:
            save_population(self.pop, self.frame, self.Config.save_pop_folder)
        #run callback
        self.callback()
        self.frame += 1
    def callback(self):

        if self.frame == 50:
            print('\ninfecting person')
            self.pop[0][6] = 1
            self.pop[0][8] = 50
            self.pop[0][10] = 1
    def run(self):
        '''run simulation'''
        i = 0
        while i < self.Config.simulation_steps:
            try:
                sim.tstep()
            except KeyboardInterrupt:
                print('\nCTRL-C caught, exiting')
                sys.exit(1)
            #check whether to end if no infecious persons remain.
            if self.Config.endif_no_infections and self.frame >= 500:
                if len(self.pop[(self.pop[:,6] == 1) |
                                       (self.pop[:,6] == 4)]) == 0:
                    i = self.Config.simulation_steps

        if self.Config.save_data:
            save_data(self.pop, self.pop_tracker)

        #report outcomes
        print('\n-----stopping-----\n')
        print('total timesteps taken: %i' %self.frame)
        print('total dead: %i' %len(self.pop[self.pop[:,6] == 3]))
        print('total recovered: %i' %len(self.pop[self.pop[:,6] == 2]))
        print('total infected: %i' %len(self.pop[self.pop[:,6] == 1]))
        print('total infectious: %i' %len(self.pop[(self.pop[:,6] == 1) |
                                                          (self.pop[:,6] == 4)]))
        print('total unaffected: %i' %len(self.pop[self.pop[:,6] == 0]))

if __name__ == '__main__':

    #initialize
    sim = Simulation()
    #set number of simulation steps
    sim.Config.simulation_steps = 20000
    sim.Config.plot_style = 'default' #can also be dark

    # #set reduced interaction
    # sim.Config.set_reduced_interaction()
    # sim.population_init()
    #
    # #set lockdown scenario
    # sim.Config.set_lockdown(lockdown_percentage = 0.1, lockdown_compliance = 0.95)
    #
    # set self-isolation scenario
    sim.Config.set_self_isolation(self_isolate_proportion = 0.9,
                                 isolation_bounds = [0.02, 0.02, 0.09, 0.98],
                                 traveling_infects=False)
    sim.population_init()
    sim.run()
