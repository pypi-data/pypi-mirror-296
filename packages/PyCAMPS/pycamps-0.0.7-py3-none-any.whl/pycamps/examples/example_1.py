import os
import matplotlib.pyplot as plt

from pycamps.modules import long_line, rl_load, type4_1
from pycamps.simulation import power_system, dynamics
from pycamps.logger import configure_logging

# Specify name of power system (for saving files)
system_name = "Type4_1_LL_RLLoad"

# Configure logging
os.environ['LOG_LEVEL'] = 'INFO'
logger = configure_logging(log_file=f'{system_name}.log', log_to_console=True, log_to_file=True)

# Define base speed
wb = 377
SM1 = type4_1.Type4_1('G1', BaseSpeed=wb)
TL1 = long_line.LongLine('TL_1_2', BaseSpeed=wb)
L1 = rl_load.RLLoad('L1', BaseSpeed=wb)

Modules = [SM1, TL1, L1]
Bus1 = [[SM1], [TL1,'L']]
Bus2 = [[L1], [TL1,'R']]
Buses = [Bus1, Bus2]
PS = power_system.PowerSystem(system_name, Modules, Buses)

# 1: Writes state space equations and vector x
StateSpace = PS.StateSpace
StateSpace.write_equations()
StateSpace.write_vector_x()

params_dictionary = {'J_G1': 76531.33492530156, 
                     'D_G1': 1, 
                     'xdprime_G1': 0.005, 
                     'RS_G1': 0.0001, 
                     'eqprime_G1': -1.35, 
                     'Pm_G1': 1.4786690000000817, 
                     'RTL_TL_1_2': 0.02978336677167938, 
                     'CTL_TL_1_2': 0.001, 
                     'LTL_TL_1_2': 0.40681749584779936, 
                     'RL_L1': 2.3125, 
                     'LL_L1': 0.9588}

# 2. Solve for system equilibrium
Simulator = dynamics.Dynamics(PS, params_directory='parameters')
xf = Simulator.solve_equilibrium(method='hybr')

# 3. Perform linearized analysis
Simulator.linearized_analysis(xf=xf)

# 4. Simulate system trajectory
time, states = Simulator.simulate_trajectory(xf=xf, simulation_time=0.1, method='LSODA')

# 5. Plot the results
plt.figure()
for variable_name, array in states.items():
    plt.plot(time, array, label=variable_name)

plt.legend()
plt.show()

