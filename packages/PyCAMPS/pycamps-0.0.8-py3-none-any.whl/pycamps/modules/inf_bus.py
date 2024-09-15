from sympy import symbols, simplify, Matrix, sin, cos, Function
from pycamps.modules import Module
from pycamps.simulation import StateSpace

class InfBus(Module):
    """
    Represents an infinite bus with a constant voltage source and series impedance.

    Args:
        IndexName (str): A unique identifier for the module. This is used to create names for parameters and state variables.
        RefFrameAngle (Optional[Symbol]): The angle of the reference frame. Defaults to a symbolic variable 'phi' if not provided.
        RefFrameSpeed (Optional[Symbol]): The speed of the reference frame. Defaults to a symbolic variable 'dphidt' if not provided.
        BaseSpeed (float): The base speed of the system. Defaults to 1. This affects the units of the state variables.
        ParamMap (Optional[dict]): A dictionary mapping parameter names to their values. Keys should be in the format '[ParameterName]_IndexName'.

    Attributes:
        Refer to the attributes of the Module class.
    
    Example:
        >>> from sympy import symbols
        >>> from pycamps.modules import InfBus
        >>> inf_bus = InfBus('Bus1', RefFrameAngle=symbols('phi'), RefFrameSpeed=symbols('dphidt'), BaseSpeed=377)
    """
    def __init__(self, IndexName, RefFrameAngle=None, RefFrameSpeed=None, BaseSpeed=1, ParamMap=None):
        super().__init__()
        self.ModuleName = IndexName
        ParameterNames = ['Rinf', 'Linf', 'vInfd', 'vInfq']
        StateVariableNames = ['Id', 'Iq']
        PortInputNames = ['Vd', 'Vq']
        PortStateNames = ['Id', 'Iq']
        ControllableInputNames = []

        self.RefFrameAngle = RefFrameAngle if RefFrameAngle is not None else symbols('phi', real=True)
        self.RefFrameSpeed = RefFrameSpeed if RefFrameSpeed is not None else symbols('dphidt', real=True)
        self.BaseSpeed = BaseSpeed
        Units = ['A', 'A'] if BaseSpeed == 1 else ['units', 'units']

        IndexName = '_' + IndexName # TODO: Properly implement index names without leading underscore
        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}

        self.Units = Units
        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables = Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.ControllableInputs = Matrix(symbols([ci + IndexName for ci in ControllableInputNames]))
        self.PortInputs = Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates = Matrix(symbols([p + IndexName for p in PortStateNames]))
        self.PortVoltages = self.PortInputs
        self.PortCurrents = -self.PortStates
        self.StateVariableDerivatives = Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives = Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Current', 'Current']
        self.StateSpaceEquations = InfBus.dynamics(self)
        self.StateSpace = StateSpace.from_module(self)

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: Id,Iq
        this.PortInputs: Vd,Vq
        this.Parameters: Rinf,Linf,vInfd,vInfq
        this.RefFrameAngle: angle of rotating reference frame
        this.RefFrameSpeed: speed of rotating reference frame
        this.BaseSpeed: Base speed

        Outputs:
        StateSpace: [dIddt ; dIqdt]
        '''

        Id, Iq = self.StateVariables
        Vd, Vq = self.PortInputs
        Rinf, Linf, vInfd, vInfq = self.Parameters

        wb = self.BaseSpeed
        dphidt = self.RefFrameSpeed
        
        # InfBus Dynamics
        dIddt = dphidt * Iq + (vInfd - Vd - Rinf * Id) / Linf
        dIqdt = (vInfq - Vq - Rinf * Iq) / Linf - dphidt * Id

        StateSpace = wb * Matrix([dIddt, dIqdt])
        return StateSpace
    