# all configration files

import numpy as np

class config_error(Exception):
    pass
class Configuration():
    def __init__(self, *args, **kwargs):
        self.verbose = True #whether to print infections, recoveries and fatalities to the terminal
        self.simulation_steps = 10000 #total simulation steps performed
        self.tstep = 0 #current simulation timestep
        self.save_data = False #whether to dump data at end of simulation
        self.save_pop = False #whether to save pop matrix every 'save_pop_freq' timesteps
        self.save_pop_freq = 10 #pop data will be saved every 'n' timesteps. Default: 10
        self.save_pop_folder = 'pop_data/' #folder to write pop timestep data to
        self.endif_no_infections = True #whether to stop simulation if no infections remain

        #scenario flags
        self.traveling_infects = False
        self.self_isolate = False
        self.lockdown = False
        self.lockdown_percentage = 0.1 #after this proportion is infected, lock-down begins
        self.lockdown_compliance = 0.95 #fraction of the pop that will obey the lockdown

        #world variables, defines where pop can and cannot roam
        self.xbounds = [0.02, 0.98]
        self.ybounds = [0.02, 0.98]

        #visualisation variables
        self.visualise = True #whether to visualise the simulation
        self.plot_mode = 'sir' #default or sir
        #size of the simulated world in coordinates
        self.x_plot = [0, 1]
        self.y_plot = [0, 1]
        self.save_plot = False
        self.plot_path = 'render/' #folder where plots are saved to
        self.plot_style = 'default' #can be default, dark, ...
        self.colorblind_mode = False
        #if colorblind is enabled, set type of colorblindness
        #available: deuteranopia, protanopia, tritanopia. defauld=deuteranopia
        self.colorblind_type = 'deuteranopia'

        #pop variables
        self.size_pop = 2000
        self.mean_age = 45
        self.max_age = 105
        self.age_dependent_risk = True #whether risk increases with age
        self.risk_age = 55 #age where mortality risk starts increasing
        self.critical_age = 75 #age at and beyond which mortality risk reaches maximum
        self.critical_mortality_chance = 0.1 #maximum mortality risk for older age
        self.risk_increase = 'quadratic' #whether risk between risk and critical age increases 'linear' or 'quadratic'
        self.speed = 0.01 #average speed of pop
        self.wander_range = 0.05
        self.wander_factor = 1
        self.wander_factor_dest = 1.5

        #infection variables
        self.infection_range=0.01 #range surrounding sick patient that infections can take place
        self.infection_chance=0.03   #chance that an infection spreads to nearby healthy people each tick
        self.recovery_duration=(200, 500) #how many ticks it may take to recover from the illness
        self.mortality_chance=0.02 #global baseline chance of dying from the disease

        #healthcare variables
        self.healthcare_capacity = 300 #capacity of the healthcare system
        self.treatment_factor = 0.5 #when in treatment, affect risk by this factor
        self.no_treatment_factor = 3 #risk increase factor to use if healthcare system is full
        #risk parameters
        self.treatment_dependent_risk = True #whether risk is affected by treatment

        #self isolation variables
        self.self_isolate_proportion = 0.6
        self.isolation_bounds = [0.02, 0.02, 0.1, 0.98]

        #lockdown variables
        self.lockdown_percentage = 0.1
        self.lockdown_vector = []


    def get_palette(self):
        # returns appropriate color palette

        #palette colors are: [healthy, infected, immune, dead]
        palettes = {'regular': {'default': ['yellow', 'red', 'green', 'black'],
                                'dark': ['#404040', '#ff0000', '#00ff00', '#000000']},
                    'deuteranopia': {'default': ['yellow', '#a50f15', '#08519c', 'black'],
                                     'dark': ['#404040', '#fcae91', '#6baed6', '#000000']},
                    'protanopia': {'default': ['yellow', '#a50f15', '08519c', 'black'],
                                   'dark': ['#404040', '#fcae91', '#6baed6', '#000000']},
                    'tritanopia': {'default': ['yellow', '#a50f15', '08519c', 'black'],
                                   'dark': ['#404040', '#fcae91', '#6baed6', '#000000']}
                    }

        if self.colorblind_mode:
            return palettes[self.colorblind_type.lower()][self.plot_style]
        else:
            return palettes['regular'][self.plot_style]

    def get(self, key):
        '''gets key value from config'''
        try:
            return self.__dict__[key]
        except:
            raise config_error('key %s not present in config' %key)


    def set(self, key, value):
        '''sets key value in config'''
        self.__dict__[key] = value


    def read_from_file(self, path):
        '''reads config from filename'''
        #TODO: implement
        pass


    def set_lockdown(self, lockdown_percentage=0.1, lockdown_compliance=0.9):
        self.lockdown = True

        self.lockdown_percentage = lockdown_percentage
        self.lockdown_vector = np.zeros((self.size_pop,))
        #lockdown vector is 1 for those not complying
        self.lockdown_vector[np.random.uniform(size=(self.size_pop,)) >= lockdown_compliance] = 1


    def set_self_isolation(self, self_isolate_proportion=0.9,
                           isolation_bounds = [0.02, 0.02, 0.09, 0.98],
                           traveling_infects=False):
        '''sets self-isolation scenario to active'''

        self.self_isolate = True
        self.isolation_bounds = isolation_bounds
        self.self_isolate_proportion = self_isolate_proportion
        #set roaming bounds to outside isolated area
        self.xbounds = [0.1, 1.1]
        self.ybounds = [0.02, 0.98]
        #update plot bounds everything is shown
        self.x_plot = [0, 1.1]
        self.y_plot = [0, 1]
        #update whether traveling agents also infect
        self.traveling_infects = traveling_infects


    def set_reduced_interaction(self, speed = 0.001):
        '''sets reduced interaction scenario to active'''

        self.speed = speed


    def set_demo(self, destinations, pop):
        #make C
        #first leg
        destinations[:,0][0:100] = 0.05
        destinations[:,1][0:100] = 0.7
        pop[:,13][0:100] = 0.01
        pop[:,14][0:100] = 0.05

        #Top
        destinations[:,0][100:200] = 0.1
        destinations[:,1][100:200] = 0.75
        pop[:,13][100:200] = 0.05
        pop[:,14][100:200] = 0.01

        #Bottom
        destinations[:,0][200:300] = 0.1
        destinations[:,1][200:300] = 0.65
        pop[:,13][200:300] = 0.05
        pop[:,14][200:300] = 0.01


        #make O
        #first leg
        destinations[:,0][300:400] = 0.2
        destinations[:,1][300:400] = 0.7
        pop[:,13][300:400] = 0.01
        pop[:,14][300:400] = 0.05

        #Top
        destinations[:,0][400:500] = 0.25
        destinations[:,1][400:500] = 0.75
        pop[:,13][400:500] = 0.05
        pop[:,14][400:500] = 0.01

        #Bottom
        destinations[:,0][500:600] = 0.25
        destinations[:,1][500:600] = 0.65
        pop[:,13][500:600] = 0.05
        pop[:,14][500:600] = 0.01

        #second leg
        destinations[:,0][600:700] = 0.3
        destinations[:,1][600:700] = 0.7
        pop[:,13][600:700] = 0.01
        pop[:,14][600:700] = 0.05


        #make V
        #First leg
        destinations[:,0][700:800] = 0.35
        destinations[:,1][700:800] = 0.7
        pop[:,13][700:800] = 0.01
        pop[:,14][700:800] = 0.05

        #Bottom
        destinations[:,0][800:900] = 0.4
        destinations[:,1][800:900] = 0.65
        pop[:,13][800:900] = 0.05
        pop[:,14][800:900] = 0.01

        #second leg
        destinations[:,0][900:1000] = 0.45
        destinations[:,1][900:1000] = 0.7
        pop[:,13][900:1000] = 0.01
        pop[:,14][900:1000] = 0.05

        #Make I
        #leg
        destinations[:,0][1000:1100] = 0.5
        destinations[:,1][1000:1100] = 0.7
        pop[:,13][1000:1100] = 0.01
        pop[:,14][1000:1100] = 0.05

        #I dot
        destinations[:,0][1100:1200] = 0.5
        destinations[:,1][1100:1200] = 0.8
        pop[:,13][1100:1200] = 0.01
        pop[:,14][1100:1200] = 0.01

        #make D
        #first leg
        destinations[:,0][1200:1300] = 0.55
        destinations[:,1][1200:1300] = 0.67
        pop[:,13][1200:1300] = 0.01
        pop[:,14][1200:1300] = 0.03

        #Top
        destinations[:,0][1300:1400] = 0.6
        destinations[:,1][1300:1400] = 0.75
        pop[:,13][1300:1400] = 0.05
        pop[:,14][1300:1400] = 0.01

        #Bottom
        destinations[:,0][1400:1500] = 0.6
        destinations[:,1][1400:1500] = 0.65
        pop[:,13][1400:1500] = 0.05
        pop[:,14][1400:1500] = 0.01

        #second leg
        destinations[:,0][1500:1600] = 0.65
        destinations[:,1][1500:1600] = 0.7
        pop[:,13][1500:1600] = 0.01
        pop[:,14][1500:1600] = 0.05

        #dash
        destinations[:,0][1600:1700] = 0.725
        destinations[:,1][1600:1700] = 0.7
        pop[:,13][1600:1700] = 0.03
        pop[:,14][1600:1700] = 0.01

        #Make 1
        destinations[:,0][1700:1800] = 0.8
        destinations[:,1][1700:1800] = 0.7
        pop[:,13][1700:1800] = 0.01
        pop[:,14][1700:1800] = 0.05


        #Make 9
        #right leg
        destinations[:,0][1800:1900] = 0.91
        destinations[:,1][1800:1900] = 0.675
        pop[:,13][1800:1900] = 0.01
        pop[:,14][1800:1900] = 0.08

        #roof
        destinations[:,0][1900:2000] = 0.88
        destinations[:,1][1900:2000] = 0.75
        pop[:,13][1900:2000] = 0.035
        pop[:,14][1900:2000] = 0.01

        #middle
        destinations[:,0][2000:2100] = 0.88
        destinations[:,1][2000:2100] = 0.7
        pop[:,13][2000:2100] = 0.035
        pop[:,14][2000:2100] = 0.01

        #left vertical leg
        destinations[:,0][2100:2200] = 0.86
        destinations[:,1][2100:2200] = 0.72
        pop[:,13][2100:2200] = 0.01
        pop[:,14][2100:2200] = 0.01

        ###################
        ##### ROW TWO #####
        ###################

        #S
        #first leg
        destinations[:,0][2200:2300] = 0.115
        destinations[:,1][2200:2300] = 0.5
        pop[:,13][2200:2300] = 0.01
        pop[:,14][2200:2300] = 0.03

        #Top
        destinations[:,0][2300:2400] = 0.15
        destinations[:,1][2300:2400] = 0.55
        pop[:,13][2300:2400] = 0.05
        pop[:,14][2300:2400] = 0.01

        #second leg
        destinations[:,0][2400:2500] = 0.2
        destinations[:,1][2400:2500] = 0.45
        pop[:,13][2400:2500] = 0.01
        pop[:,14][2400:2500] = 0.03

        #middle
        destinations[:,0][2500:2600] = 0.15
        destinations[:,1][2500:2600] = 0.48
        pop[:,13][2500:2600] = 0.05
        pop[:,14][2500:2600] = 0.01

        #bottom
        destinations[:,0][2600:2700] = 0.15
        destinations[:,1][2600:2700] = 0.41
        pop[:,13][2600:2700] = 0.05
        pop[:,14][2600:2700] = 0.01

        #Make I
        #leg
        destinations[:,0][2700:2800] = 0.25
        destinations[:,1][2700:2800] = 0.45
        pop[:,13][2700:2800] = 0.01
        pop[:,14][2700:2800] = 0.05

        #I dot
        destinations[:,0][2800:2900] = 0.25
        destinations[:,1][2800:2900] = 0.55
        pop[:,13][2800:2900] = 0.01
        pop[:,14][2800:2900] = 0.01

        #M
        #Top
        destinations[:,0][2900:3000] = 0.37
        destinations[:,1][2900:3000] = 0.5
        pop[:,13][2900:3000] = 0.07
        pop[:,14][2900:3000] = 0.01

        #Left leg
        destinations[:,0][3000:3100] = 0.31
        destinations[:,1][3000:3100] = 0.45
        pop[:,13][3000:3100] = 0.01
        pop[:,14][3000:3100] = 0.05

        #Middle leg
        destinations[:,0][3100:3200] = 0.37
        destinations[:,1][3100:3200] = 0.45
        pop[:,13][3100:3200] = 0.01
        pop[:,14][3100:3200] = 0.05

        #Right leg
        destinations[:,0][3200:3300] = 0.43
        destinations[:,1][3200:3300] = 0.45
        pop[:,13][3200:3300] = 0.01
        pop[:,14][3200:3300] = 0.05

        #set all destinations active
        pop[:,11] = 1
