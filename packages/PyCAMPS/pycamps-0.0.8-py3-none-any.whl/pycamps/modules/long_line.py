from sympy import symbols, Function, simplify, Matrix
from pycamps.modules import Module
from pycamps.simulation import StateSpace

class LongLine(Module):
    """
    Represents a long transmission line model with resistance, capacitance, and inductances.

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
        >>> from pycamps.modules import LongLine
        >>> long_line = LongLine('TL_1_2', RefFrameAngle=symbols('phi'), RefFrameSpeed=symbols('dphidt'), BaseSpeed=377)
    """
    def __init__(self, IndexName, RefFrameAngle=None, RefFrameSpeed=None, BaseSpeed=1, ParamMap=None):
        super().__init__()
        self.ModuleName = IndexName
        ParameterNames = ['RTL', 'CTL', 'LTL']
        StateVariableNames = ['vTLLd', 'vTLLq', 'iTLMd', 'iTLMq', 'vTLRd', 'vTLRq']
        PortInputNames = ['iInLd', 'iInLq', 'iInRd', 'iInRq']
        PortStateNames = ['vTLLd', 'vTLLq', 'vTLRd', 'vTLRq']
        ControllableInputNames = []

        Units = ['A', 'A'] if BaseSpeed == 1 else ['units', 'units']

        IndexName = '_' + IndexName # TODO: Properly implement index names without leading underscore
        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}

        self.RefFrameAngle = RefFrameAngle if RefFrameAngle is not None else symbols('phi', real=True)
        self.RefFrameSpeed = RefFrameSpeed if RefFrameSpeed is not None else symbols('dphidt', real=True)
        self.BaseSpeed = BaseSpeed
        self.Units = Units
        
        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables =  Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.ControllableInputs =  Matrix(symbols([c + IndexName for c in ControllableInputNames]))
        self.PortInputs =  Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates =  Matrix(symbols([p + IndexName for p in PortStateNames]))
        
        self.PortCurrents = self.PortInputs
        self.PortVoltages = self.PortStates
        self.StateVariableDerivatives =  Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives =  Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Voltage', 'Voltage', 'Voltage', 'Voltage']
        self.StateSpaceEquations = self.dynamics()
        self.StateSpace = StateSpace.from_module(self)

    def dynamics(self):
        vTLLd, vTLLq, iTLMd, iTLMq, vTLRd, vTLRq = self.StateVariables
        iInLd, iInLq, iInRd, iInRq = self.PortInputs
        RTL, CTL, LTL = self.Parameters

        wb = self.BaseSpeed
        dphidt = self.RefFrameSpeed

        # Transmission Line Dynamics
        dvTLLddt = (iInLd - iTLMd) / CTL + dphidt * vTLLq
        dvTLLqdt = (iInLq - iTLMq) / CTL - dphidt * vTLLd
        diTLMddt = dphidt * iTLMq - (vTLRd - vTLLd + RTL * iTLMd) / LTL
        diTLMqdt = -dphidt * iTLMd - (vTLRq - vTLLq + RTL * iTLMq) / LTL
        dvTLRddt = (iInRd + iTLMd) / CTL + dphidt * vTLRq
        dvTLRqdt = (iInRq + iTLMq) / CTL - dphidt * vTLRd

        # StateSpace = wb * simplify([dvTLLddt, dvTLLqdt, diTLMddt, diTLMqdt, dvTLRddt, dvTLRqdt])
        StateSpace = [dvTLLddt, dvTLLqdt, diTLMddt, diTLMqdt, dvTLRddt, dvTLRqdt]
        StateSpace = Matrix([wb * expr for expr in StateSpace])
        StateSpace = simplify(StateSpace)
        return StateSpace
