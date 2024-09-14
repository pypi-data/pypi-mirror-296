import os
import matplotlib.pyplot as plt

from pycamps.modules import type4_2, short_line, inf_bus
from pycamps.simulation import power_system, dynamics
from pycamps.logger import configure_logging

# Specify name of power system (for saving files)
system_name = "Type4_2_SL_InfBus"

# Configure logging
os.environ['LOG_LEVEL'] = 'INFO'
logger = configure_logging(log_file=f'{system_name}.log', log_to_console=True, log_to_file=True)

# Define base speed
wb = 377
SM1 = type4_2.Type4_2('G1', BaseSpeed=wb)
TL1 = short_line.ShortLine('TL_1_2', BaseSpeed=wb)
L1 = inf_bus.InfBus('I1', BaseSpeed=wb)

Modules = [SM1, TL1, L1]
Bus1 = [[SM1], [TL1,'L']]
Bus2 = [[L1], [TL1,'R']]
Buses = [Bus1, Bus2]
PS = power_system.PowerSystem(system_name, Modules, Buses)

# 1: Writes state space equations and vector x
StateSpace = PS.StateSpace
StateSpace.write_equations()
StateSpace.write_vector_x()

# 2. Solve for system equilibrium
Simulator = dynamics.Dynamics(PS, params_directory='params')
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

