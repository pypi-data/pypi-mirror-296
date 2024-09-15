import os
import numpy as np
import sympy as sp
from pycamps.logger import configure_logging

logger = configure_logging()

class StateSpace:
    """
    Represents a state space model for a power system or module.

    Args:
        system_name (str): The name of the system.
        set_point_outputs (Matrix): A SymPy matrix of set point outputs.
        set_point_output_equations (Matrix): A SymPy matrix of equations for set point outputs.
        controllable_inputs (Matrix): A SymPy matrix of controllable inputs.
        control_input_equations (Matrix): A SymPy matrix of equations for controllable inputs.
        internal_inputs (Matrix): A SymPy matrix of internal inputs.
        internal_equations (Matrix): A SymPy matrix of internal equations.
        state_variable_derivatives (Matrix): A SymPy matrix of state variable derivatives.
        state_space_equations (Matrix): A SymPy matrix of state space equations.
        desired_state_variable_derivatives (Matrix): A SymPy matrix of desired state variable derivatives.
        desired_state_space (Matrix): A SymPy matrix of desired state space equations.
        state_variables (Matrix): A SymPy matrix of state variables.
        desired_state_variables (Matrix): A SymPy matrix of desired state variables.
        units (list of str): A list of units for the state variables.

    Methods:
        from_power_system(PS: PowerSystem): Creates a StateSpace instance from a PowerSystem instance.
        from_module(module: Module): Creates a StateSpace instance from a module.
        print_equations(): Prints the interconnected state space equations.
        write_equations(filename=None): Writes the interconnected state space equations to a file.
        print_vector_x(): Prints the interconnected state space equations (dx) in a form suitable for running the simulation directly.
        write_vector_x(filename=None): Writes the interconnected state space equations (dx) into a file in a form suitable for running the simulation directly.
    
    Example:
        >>> from pycamps.simulation import StateSpace
        >>> ss = StateSpace(system_name='Power System 1', ...)
        >>> ss.print_equations()
    """

    def __init__(self, system_name, set_point_outputs, set_point_output_equations, controllable_inputs, control_input_equations, internal_inputs, internal_equations, state_variable_derivatives, state_space_equations, desired_state_variable_derivatives, desired_state_space, state_variables, desired_state_variables, units):
        self.system_name = system_name
        self.SetPointOutputs = set_point_outputs
        self.SetPointOutputEquations = set_point_output_equations
        self.ControllableInputs = controllable_inputs
        self.ControlInputEquations = control_input_equations
        self.InternalInputs = internal_inputs
        self.InternalEquations = internal_equations
        self.StateVariableDerivatives = state_variable_derivatives
        self.StateSpaceEquations = state_space_equations
        self.DesiredStateVariableDerivatives = desired_state_variable_derivatives
        self.DesiredStateSpace = desired_state_space
        self.StateVariables = state_variables
        self.DesiredStateVariables = desired_state_variables
        self.Units = units

    @classmethod
    def from_power_system(cls, PS):
        return cls(
            system_name=PS.system_name,
            set_point_outputs=PS.SetPointOutputs,
            set_point_output_equations=PS.SetPointOutputEquations,
            controllable_inputs=PS.ControllableInputs,
            control_input_equations=PS.ControlInputEquations,
            internal_inputs=PS.InternalInputs,
            internal_equations=PS.InternalEquations,
            state_variable_derivatives=PS.StateVariableDerivatives,
            state_space_equations=PS.StateSpaceEquations,
            desired_state_variable_derivatives=PS.DesiredStateVariableDerivatives,
            desired_state_space=PS.DesiredStateSpace,
            state_variables=PS.StateVariables,
            desired_state_variables=PS.DesiredStateVariables,
            units=PS.Units
        )

    @classmethod
    def from_module(cls, module):
        return cls(
            system_name=module.ModuleName,
            set_point_outputs=module.SetPoints,
            set_point_output_equations=module.SetPointOutputEquations,
            controllable_inputs=module.ControllableInputs,
            control_input_equations=module.ControlInputEquations,
            internal_inputs=module.InternalInputs,
            internal_equations=module.InternalEquations,
            state_variable_derivatives=module.StateVariableDerivatives,
            state_space_equations=module.StateSpaceEquations,
            desired_state_variable_derivatives=module.DesiredStateVariableDerivatives,
            desired_state_space=module.DesiredStateSpace,
            state_variables=module.StateVariables,
            desired_state_variables=module.DesiredStateVariables,
            units=module.Units
        )

    # TODO: Implement the __eq__ method
    def __str__(self):
        attributes = [
            ("Name", self.system_name),
            ("Set Point Outputs", self.SetPointOutputs),
            ("Set Point Output Equations", self.SetPointOutputEquations),
            ("Controllable Inputs", self.ControllableInputs),
            ("Control Input Equations", self.ControlInputEquations),
            ("Internal Inputs", self.InternalInputs),
            ("Internal Equations", self.InternalEquations),
            ("State Variable Derivatives", self.StateVariableDerivatives),
            ("State Space Equations", self.StateSpaceEquations),
            ("Desired State Variable Derivatives", self.DesiredStateVariableDerivatives),
            ("Desired State Space", self.DesiredStateSpace),
            ("State Variables", self.StateVariables),
            ("Desired State Variables", self.DesiredStateVariables),
            ("Units", self.Units)
        ]

        def value_exists(value):
            return value is not None \
                and not (isinstance(value, list) and len(value) == 0) \
                and not (isinstance(value, str) and value == '') \
                and not (isinstance(value, np.ndarray) and value.size == 0) \
                and not (isinstance(value, sp.Basic) and value.is_zero)
                
        
        return "\n".join(f"{name}: {value}" for name, value in attributes if value_exists(value))
    
    def __eq__(self, other):
        if not isinstance(other, StateSpace):
            return False
        
        def sympy_equal(eq1, eq2):
            return sp.simplify(eq1 - eq2) == 0

        return (
            self.system_name == other.system_name and
            sympy_equal(self.SetPointOutputs, other.SetPointOutputs) and
            sympy_equal(self.SetPointOutputEquations, other.SetPointOutputEquations) and
            sympy_equal(self.ControllableInputs, other.ControllableInputs) and
            sympy_equal(self.ControlInputEquations, other.ControlInputEquations) and
            sympy_equal(self.InternalInputs, other.InternalInputs) and
            sympy_equal(self.InternalEquations, other.InternalEquations) and
            sympy_equal(self.StateVariableDerivatives, other.StateVariableDerivatives) and
            sympy_equal(self.StateSpaceEquations, other.StateSpaceEquations) and
            sympy_equal(self.DesiredStateVariableDerivatives, other.DesiredStateVariableDerivatives) and
            sympy_equal(self.DesiredStateSpace, other.DesiredStateSpace) and
            sympy_equal(self.StateVariables, other.StateVariables) and
            sympy_equal(self.DesiredStateVariables, other.DesiredStateVariables) and
            self.Units == other.Units
        )

    def print_equations(self):
        '''
        Prints out the interconnected state space equations to the log console.
        '''
        logger.info(f'Power System: {self.system_name}\n')
        # Print the set point equations
        logger.info("Set Point Outputs:")
        for output, equation in zip(self.SetPointOutputs, self.SetPointOutputEquations):
            logger.info(f'{output} = {equation}\n')
        # Print the controllable input equations
        logger.info("Controllable Inputs:")
        for input, equation in zip(self.ControllableInputs, self.ControlInputEquations):
            logger.info(f'{input} = {equation}\n')
        # Print the internal input equations
        logger.info("Internal Inputs:")
        for input, equation in zip(self.InternalInputs, self.InternalEquations):
            logger.info(f'{input} = {equation}\n')
        # Print the state space equations
        logger.info("State Space Equations:")
        for derivative, state_space in zip(self.StateVariableDerivatives, self.StateSpaceEquations):
            logger.info(f'{derivative} = {state_space}\n')
        # Print the desired state space equations (used for control)
        logger.info("Desired State Space Equations:")
        for derivative, state_space in zip(self.DesiredStateVariableDerivatives, self.DesiredStateSpace):
            logger.info(f'{derivative} = {state_space}\n')

    def write_equations(self, filename=None):
        '''
        Writes out the interconnected state space equations to a file.
        '''
        if not filename:
            filename = f'{self.system_name}_Equations.txt'
        # Check if directory exists, if not, make it
        os.makedirs(os.path.dirname('results/equations/' + filename), exist_ok=True)

        with open('results/equations/' + filename, 'w') as f: # Empties out file contents before writing!
            # Write the set point equations
            for output, equation in zip(self.SetPointOutputs, self.SetPointOutputEquations):
                f.write(f'{output} = {equation}\n')
            # Write the controllable input equations
            for input, equation in zip(self.ControllableInputs, self.ControlInputEquations):
                f.write(f'{input} = {equation}\n')
            # Write the internal input equations
            for input, equation in zip(self.InternalInputs, self.InternalEquations):
                f.write(f'{input} = {equation}\n')
            # Write the state space equations
            for derivative, state_space in zip(self.StateVariableDerivatives, self.StateSpaceEquations):
                f.write(f'{derivative} = {state_space}\n')
            # Write the desired state space equations (used for control)
            for derivative, state_space in zip(self.DesiredStateVariableDerivatives, self.DesiredStateSpace):
                f.write(f'{derivative} = {state_space}\n')

    def print_vector_x(self):
        '''
        Prints out the interconnected state space equations (dx) in a form suitable for 
        running the simulation directly. Also assigns value of each element of the 
        vector (x) into the respective state variables.
        '''
        logger.info(f'Power System: {self.system_name}\n')
        # State variables
        logger.info('State Variables:')
        for i, variable in enumerate(self.StateVariables):
            logger.info(f'{variable} = x({i})')
        # Desired state variables
        logger.info('Desired State Variables:')
        for i, variable in enumerate(self.DesiredStateVariables):
            logger.info(f'{variable} = x({i+len(self.StateVariables)})')
        # Set Point outputs
        logger.info('Set Point Outputs:')
        for output, equation in zip(self.SetPointOutputs, self.SetPointOutputEquations):
            logger.info(f'{output} = {equation}')
        # Print controllable input expressions
        logger.info('Controllable Inputs:')
        for input, equation in zip(self.ControllableInputs, self.ControlInputEquations):
            logger.info(f'{input} = {equation}')
        # Print internal input expressions
        logger.info('Internal Inputs:')
        for input, equation in zip(self.InternalInputs, self.InternalEquations):
            logger.info(f'{input} = {equation}')
        # Print state space equations
        logger.info('State Space Equations:')
        for derivative, state_space in zip(self.StateVariableDerivatives, self.StateSpaceEquations):
            logger.info(f'{derivative} = {state_space}')
        # Print desired state space equations
        logger.info('Desired State Space Equations:')
        for derivative, state_space in zip(self.DesiredStateVariableDerivatives, self.DesiredStateSpace):
            logger.info(f'{derivative} = {state_space}')
        # Return dx vector
        logger.info('dx = [')
        # State variable derivatives
        for derivative in self.StateVariableDerivatives:
            logger.info(derivative)
        # Desired state variable derivatives
        for derivative in self.DesiredStateVariableDerivatives:
            logger.info(derivative)
        logger.info(']')

    def write_vector_x(self, filename=None):
        '''
        Writes the interconnected state space equations (dx) into a file in a form 
        suitable for running the simulation directly. Also assigns value of each element 
        of the vector (x) into the respective state variables.
        '''
        if not filename:
            filename = f'{self.system_name}_Equations.txt'
            
        # Check if directory exists, if not, make it
        os.makedirs(os.path.dirname('results/equations/' + filename), exist_ok=True)

        with open('results/equations/' + filename, 'a') as f:
            # State variables
            for i, variable in enumerate(self.StateVariables):
                f.write(f'{variable} = x({i})\n')
            # Desired state variables
            for i, variable in enumerate(self.DesiredStateVariables):
                f.write(f'{variable} = x({i+len(self.StateVariables)})\n')
            # Set Point outputs
            for output, equation in zip(self.SetPointOutputs, self.SetPointOutputEquations):
                f.write(f'{output} = {equation}\n')
            # Write controllable input expressions
            for input, equation in zip(self.ControllableInputs, self.ControlInputEquations):
                f.write(f'{input} = {equation}\n')
            # Write internal input expressions
            for input, equation in zip(self.InternalInputs, self.InternalEquations):
                f.write(f'{input} = {equation}\n')
            # Write state space equations
            for derivative, state_space in zip(self.StateVariableDerivatives, self.StateSpaceEquations):
                f.write(f'{derivative} = {state_space}\n')
            # Write desired state space equations
            for derivative, state_space in zip(self.DesiredStateVariableDerivatives, self.DesiredStateSpace):
                f.write(f'{derivative} = {state_space}\n')
            # Return dx vector
            f.write('dx = [')
            # State variable derivatives
            for derivative in self.StateVariableDerivatives:
                f.write(f'{derivative}\n')
            # Desired state variable derivatives
            for derivative in self.DesiredStateVariableDerivatives:
                f.write(f'{derivative}\n')
            f.write(']\n')
