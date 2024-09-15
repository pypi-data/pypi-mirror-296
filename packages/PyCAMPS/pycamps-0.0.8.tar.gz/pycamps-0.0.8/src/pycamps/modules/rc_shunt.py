from sympy import symbols, Function, simplify, Matrix, sin, cos, pprint
from pycamps.modules import Module
from pycamps.simulation import StateSpace

class RCShunt(Module):
    """
    Represents an RC shunt module in a power system.

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
        >>> from pycamps.modules import RCShunt
        >>> shunt = RCShunt('SH1', RefFrameAngle=symbols('phi'), RefFrameSpeed=symbols('dphidt'), BaseSpeed=377)
    """
    def __init__(self, IndexName, RefFrameAngle=None, RefFrameSpeed=None, BaseSpeed=1, ParamMap=None):
        super().__init__()
        self.ModuleName = IndexName
        ParameterNames = ['Rsh','Csh']
        StateVariableNames = ['vcd','vcq']
        PortInputNames = ['iInd', 'iInq']
        PortStateNames = ['vcd','vcq']

        Units = ['V','V'] if BaseSpeed == 1 else ['units']*2

        self.RefFrameAngle = RefFrameAngle if RefFrameAngle is not None else symbols('phi', real=True)
        self.RefFrameSpeed = RefFrameSpeed if RefFrameSpeed is not None else symbols('dphidt', real=True)
        self.BaseSpeed = BaseSpeed
        IndexName = '_' + IndexName # TODO: Properly implement index names without leading underscore

        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}
        
        self.Units = Units

        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables =  Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.PortInputs =  Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates =  Matrix(symbols([p + IndexName for p in PortStateNames]))

        self.PortCurrents = self.PortInputs
        self.PortVoltages = self.PortStates

        self.StateVariableDerivatives =  Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives =  Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Voltage']*2
        self.StateSpaceEquations = self.dynamics()
        self.StateSpace = StateSpace.from_module(self)

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: vcd; vcq
        this.InputVariables: iInd, iInq
        this.Parameters: RSh, Csh
            
        Outputs:
        StateSpace = [dvcddt, dvcqdt]
        '''
        vcd, vcq = self.StateVariables
        iInd, iInq = self.PortInputs
        Rsh, Csh = self.Parameters
        
        wb = self.BaseSpeed
        dphidt = self.RefFrameSpeed
        
        # Transmission Line Dynamics
        dvcddt = ( - vcd/(Rsh*Csh) + iInd/Csh + dphidt*vcq);         
        dvcqdt = (- vcq/(Rsh*Csh) + iInq/Csh - dphidt*vcd)
        
        StateSpace = Matrix([dvcddt, dvcqdt])
        StateSpace = simplify(StateSpace)
        return StateSpace