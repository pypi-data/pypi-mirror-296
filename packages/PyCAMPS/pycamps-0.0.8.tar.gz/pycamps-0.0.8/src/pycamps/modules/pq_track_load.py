from sympy import symbols, Function, simplify, Matrix
from pycamps.modules import Module
from pycamps.simulation import StateSpace

'''
Implementation of a PQ Track Load module. Includes V1 and V2 versions.
'''

class PQTrackLoad(Module):
    """
    Represents a time varying impedance load with filters for P and Q setpoints with time varying voltage being used for impedance calculations.

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
        >>> from pycamps.modules import PQTrackLoad
        >>> load = PQTrackLoad('L1', RefFrameAngle=symbols('phi'), RefFrameSpeed=symbols('dphidt'), BaseSpeed=377)

    Made by Rupa Nov 10, 2017
    """
    def __init__(self, IndexName, RefFrameAngle=None, RefFrameSpeed=None, BaseSpeed=1, ParamMap=None):
        super().__init__()
        self.ModuleName = IndexName
        ParameterNames = ['PL','QL','Tp','Tq']
        StateVariableNames = ['iLd','iLq','P','Q']
        PortInputNames = ['vLd','vLq']
        PortStateNames = ['iLd','iLq']
        ControllableInputNames = ['RL','LL']

        Units = ['A','A','MW','MVAR'] if BaseSpeed == 1 else ['units']*4

        self.RefFrameAngle = RefFrameAngle if RefFrameAngle is not None else symbols('phi', real=True)
        self.RefFrameSpeed = RefFrameSpeed if RefFrameSpeed is not None else symbols('dphidt', real=True)
        self.BaseSpeed = BaseSpeed
        IndexName = '_' + IndexName # TODO: Properly implement index names without leading underscore
        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}
        
        self.Units = Units

        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables =  Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.ControllableInputs =  Matrix(symbols([c + IndexName for c in ControllableInputNames]))
        self.PortInputs =  Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates =  Matrix(symbols([p + IndexName for p in PortStateNames]))

        self.PortCurrents = self.PortStates
        self.PortVoltages = self.PortInputs

        self.StateVariableDerivatives =  Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives =  Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Current', 'Current']
        self.StateSpaceEquations, self.ControlInputEquations = self.dynamics()
        self.StateSpace = StateSpace.from_module(self)

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: iLd,iLq
        this.InputVariables: vLd, vLq
        this.Parameters: RL, LL
            
        Outputs:
        StateSpace = [ diLddt ; diLqdt]
        '''
        iLd, iLq, P, Q = self.StateVariables
        vLd, vLq = self.PortInputs
        PL, QL, Tp, Tq = self.Parameters
        RL, LL = self.ControllableInputs
        
        wb = self.BaseSpeed
        dphidt = self.RefFrameSpeed
        
        # PQTrackLoad Dynamics
        diLddt = wb*(dphidt*iLq + (vLd - RL*iLd)/LL)
        diLqdt = wb*((vLq - RL*iLq)/LL - dphidt*iLd)
        dPdt = -(P-PL)/Tp
        dQdt = -(Q - QL)/Tq
        
        RL = P*(vLd**2 + vLq**2)/(P**2 + Q**2)
        LL = Q*(vLd**2 + vLq**2)/((P**2 + Q**2)*dphidt)
        
        StateSpace = Matrix([diLddt, diLqdt, dPdt, dQdt])
        ControlInputEquations = Matrix([RL, LL])

        return simplify(StateSpace), ControlInputEquations
    
class PQTrackLoadV2(Module):
    """
    Represents a variable current source with filters for P and Q with varying voltage.

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
        >>> from pycamps.modules import PQTrackLoadV2
        >>> load = PQTrackLoadV2('L1', RefFrameAngle=symbols('phi'), RefFrameSpeed=symbols('dphidt'), BaseSpeed=377)

    Made by Rupa Nov 10, 2017
    """
    def __init__(self, IndexName, RefFrameAngle=None, RefFrameSpeed=None, BaseSpeed=1, ParamMap=None):
        super().__init__()
        self.ModuleName = IndexName
        ParameterNames = ['PL','QL','Tp','Tq']
        StateVariableNames = ['P','Q']
        PortInputNames = ['vLd','vLq']
        PortStateNames = ['iLd','iLq']

        self.RefFrameAngle = RefFrameAngle if RefFrameAngle is not None else symbols('phi', real=True)
        self.RefFrameSpeed = RefFrameSpeed if RefFrameSpeed is not None else symbols('dphidt', real=True)
        self.BaseSpeed = BaseSpeed
        Units = ['MW','MVAR'] if BaseSpeed == 1 else ['units']*2

        IndexName = '_' + IndexName # TODO: Properly implement index names without leading underscore
        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}
        
        self.Units = Units

        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables =  Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.PortInputs =  Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates =  Matrix(symbols([p + IndexName for p in PortStateNames]))

        self.PortVoltages = self.PortInputs
        P, Q = self.StateVariables
        vd, vq = self.PortInputs
        id = (P*vd + Q*vq)/(vd**2 + vq**2)
        iq = (P*vq - Q*vd)/(vd**2 + vq**2)
        self.PortCurrents = Matrix([id, iq])

        self.StateVariableDerivatives =  Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives =  Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Current', 'Current']
        self.StateSpaceEquations = self.dynamics()
        self.StateSpace = StateSpace.from_module(self)

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: iLd,iLq
        this.InputVariables: vLd, vLq
            
        Outputs:
        StateSpace = [ diLddt ; diLqdt]
        '''
        P, Q = self.StateVariables
        vLd, vLq = self.PortInputs
        PL, QL, Tp, Tq = self.Parameters
        
        wb = self.BaseSpeed
        dphidt = self.RefFrameSpeed
        
        # PQTrackLoad Dynamics
        dPdt = -(P-PL)/Tp
        dQdt = -(Q - QL)/Tq
        
        StateSpace = Matrix([dPdt, dQdt])

        return simplify(StateSpace)