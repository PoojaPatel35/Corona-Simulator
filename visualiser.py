
# contains all methods for visualisation tasks

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

from environment import build_hospital
from utils import check_folder

def set_style(Config):
    if Config.plot_style.lower() == 'dark':
        mpl.style.use('plot_styles/dark.mplstyle')


def build_fig(Config, figsize=(5,7)):
    set_style(Config)
    figure = plt.figure(figsize=(5,7))
    spec = figure.add_gridspec(ncols=1, nrows=2, height_ratios=[5,2])

    ax1 = figure.add_subplot(spec[0,0])
    plt.title('infection simulation')
    plt.xlim(Config.xbounds[0], Config.xbounds[1])
    plt.ylim(Config.ybounds[0], Config.ybounds[1])

    ax2 = figure.add_subplot(spec[1,0])
    ax2.set_title('number of infected')
    ax2.set_ylim(0, Config.size_pop + 100)
    return figure, spec, ax1, ax2


def draw_tstep(Config, pop, pop_tracker, frame,
               figure, spec, ax1, ax2):

    set_style(Config)
    palette = Config.get_palette()

    spec = figure.add_gridspec(ncols=1, nrows=2, height_ratios=[5,2])
    ax1.clear()
    ax2.clear()
    ax1.set_xlim(Config.x_plot[0], Config.x_plot[1])
    ax1.set_ylim(Config.y_plot[0], Config.y_plot[1])

    if Config.self_isolate and Config.isolation_bounds != None:
        build_hospital(Config.isolation_bounds[0], Config.isolation_bounds[2],
                       Config.isolation_bounds[1], Config.isolation_bounds[3], ax1,
                       addcross = False)
        
    #plot pop segments
    healthy = pop[pop[:,6] == 0][:,1:3]
    ax1.scatter(healthy[:,0], healthy[:,1], color=palette[0], s = 2, label='healthy')
    
    infected = pop[pop[:,6] == 1][:,1:3]
    ax1.scatter(infected[:,0], infected[:,1], color=palette[1], s = 2, label='infected')

    immune = pop[pop[:,6] == 2][:,1:3]
    ax1.scatter(immune[:,0], immune[:,1], color=palette[2], s = 2, label='immune')
    
    fatalities = pop[pop[:,6] == 3][:,1:3]
    ax1.scatter(fatalities[:,0], fatalities[:,1], color=palette[3], s = 2, label='dead')
    ax1.text(Config.x_plot[0],
             Config.y_plot[1] + ((Config.y_plot[1] - Config.y_plot[0]) / 100), 
             'timestep: %i, total: %i, healthy: %i infected: %i immune: %i fatalities: %i' %(frame,
                                                                                             len(pop),
                                                                                             len(healthy), 
                                                                                             len(infected), 
                                                                                             len(immune), 
                                                                                             len(fatalities)),
                fontsize=6)
    
    ax2.set_title('number of infected')
    ax2.text(0, Config.size_pop * 0.05,
                'covid simulator',
                fontsize=6, alpha=0.5)
    #ax2.set_xlim(0, simulation_steps)
    ax2.set_ylim(0, Config.size_pop + 200)

    if Config.treatment_dependent_risk:
        infected_arr = np.asarray(pop_tracker.infectious)
        indices = np.argwhere(infected_arr >= Config.healthcare_capacity)

        ax2.plot([Config.healthcare_capacity for x in range(len(pop_tracker.infectious))], 
                 'r:', label='healthcare capacity')

    if Config.plot_mode.lower() == 'default':
        ax2.plot(pop_tracker.infectious, color=palette[1])
        ax2.plot(pop_tracker.fatalities, color=palette[3], label='fatalities')
    elif Config.plot_mode.lower() == 'sir':
        ax2.plot(pop_tracker.infectious, color=palette[1], label='infectious')
        ax2.plot(pop_tracker.fatalities, color=palette[3], label='fatalities')
        ax2.plot(pop_tracker.susceptible, color=palette[0], label='susceptible')
        ax2.plot(pop_tracker.recovered, color=palette[2], label='recovered')
    else:
        raise ValueError('incorrect plot_style specified, use \'sir\' or \'default\'')

    ax2.legend(loc = 'best', fontsize = 6)
    
    plt.draw()
    plt.pause(0.0001)

    if Config.save_plot:
        try:
            plt.savefig('%s/%i.png' %(Config.plot_path, frame))
        except:
            check_folder(Config.plot_path)
            plt.savefig('%s/%i.png' %(Config.plot_path, frame))
