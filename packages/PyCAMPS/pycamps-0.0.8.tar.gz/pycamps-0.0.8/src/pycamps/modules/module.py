import sympy as sp

class Module:
    """
    This module serves as a superclass to all dynamic component modules in the power system. 

    Attributes:
        ModuleName (str): The name of the module.
        RefFrameAngle (Symbol): The anglular position of the DQ reference frame.
        RefFrameSpeed (Symbol): The angular speed of the DQ reference frame.
        BaseSpeed (float): The base speed of the system (inverse of time units).
        ParameterMap (dict): A dictionary mapping parameter names to their values or functions.
        Parameters (Matrix): A matrix of symbolic parameters for the module (inductances, capacitances, etc).
        ControllerGains (Matrix): Gains of controllers.
        SetPoints (Matrix): Set points for controllers.
        StateVariables (Matrix): A matrix of symbolic state variables for the module.
        StateSpaceEquations (Matrix): A matrix of state space equations.
        StateVariableDerivatives (Matrix): A matrix of derivatives of state variables.
        PortInputs (Matrix): Inputs to the module from other modules.
        PortStates (Matrix): States of the module.
        PortVoltages (Matrix): Voltages at the ports.
        PortCurrents (Matrix): Currents at the ports.
        PortStates_Time (Matrix): Time-dependent states of the module.
        PortStateDerivatives (Matrix): Derivatives of the port states.
        PortOutputTypes (Matrix): Types of outputs from the ports (current or charge).
        ControllableInputs (Matrix): Inputs that can be controlled, typically for passivity-based control.
        InternalInputs (Matrix): Inputs that are internal to the module.
        ControlInputEquations (Matrix): Mathematical equations for controllable inputs.
        InternalEquations (Matrix): Internal equations of the module.
        DesiredStateVariables (Matrix): Desired state variables for underactuated systems.
        DesiredStateVariableDerivatives (Matrix): Derivatives of the desired state variables.
        DesiredStateSpace (Matrix): Desired state space representation.
        SetPointOutputs (Matrix): Outputs that are sent to another module.
        SetPointOutputEquations (Matrix): Equations for set point outputs.
        GTemp (Matrix): Temporary matrix for calculations.
        Units (list of str): The units of the state variables, which depend on the base speed.
        Data (Matrix): Additional data related to the module.
        StateSpace (StateSpace): State space representation of the module.
    """

    def __init__(self):
        self.ModuleName = ''
        self.RefFrameAngle = sp.Matrix([])
        self.RefFrameSpeed = sp.Matrix([])
        self.BaseSpeed = sp.Matrix([])
        self.Parameters = sp.Matrix([])
        self.ControllerGains = sp.Matrix([])
        self.SetPoints = sp.Matrix([])
        self.StateVariables = sp.Matrix([])
        self.StateSpaceEquations = sp.Matrix([])
        self.StateVariableDerivatives = sp.Matrix([])
        self.ParameterMap = {}
        self.PortInputs = sp.Matrix([])
        self.PortStates = sp.Matrix([])
        self.PortVoltages = sp.Matrix([])
        self.PortCurrents = sp.Matrix([])
        self.PortStates_Time = sp.Matrix([])
        self.PortStateDerivatives = sp.Matrix([])
        self.PortOutputTypes = sp.Matrix([])
        self.ControllableInputs = sp.Matrix([])
        self.InternalInputs = sp.Matrix([])
        self.ControlInputEquations = sp.Matrix([])  # in PBC, mathematical equations for controllable inputs
        self.InternalEquations = sp.Matrix([])
        self.DesiredStateVariables = sp.Matrix([])  # with PBC, for underactuated systems, there will be desired state variables
        self.DesiredStateVariableDerivatives = sp.Matrix([])
        self.DesiredStateSpace = sp.Matrix([])
        self.SetPointOutputs = sp.Matrix([])  # set point outputs that are sent to another module
        self.SetPointOutputEquations = sp.Matrix([])  # set point
        self.GTemp = sp.Matrix([])
        self.Units = []
        self.Data = sp.Matrix([])
        self.StateSpace = None