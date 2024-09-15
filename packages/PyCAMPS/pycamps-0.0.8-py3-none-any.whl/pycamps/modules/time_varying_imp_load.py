from sympy import symbols, Function, simplify, Matrix, sin, cos, pprint
import numpy as np
from pycamps.modules import Module
from pycamps.simulation import StateSpace

class TimeVaryingImpLoad(Module):
    """
    Represents a time-varying impedance load as setpoints of P and Q (with filter) change but assumes nominal voltage.

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
        >>> import numpy as np
        >>> from pycamps.modules import TimeVaryingImpLoad
        >>> t = np.linspace(0, 10, 100) # sample signal array
        >>> data = np.array([[0, 1, 1], [1, 2, 2], [2, 3, 3]]) # example data for P and Q
        >>> load = TimeVaryingImpLoad('L1', RefFrameAngle=symbols('phi'), RefFrameSpeed=symbols('dphidt'), BaseSpeed=377, data=data, t=t)

    Made by Rupa Nov 10 2017
    """
    def __init__(self, IndexName, RefFrameAngle=None, RefFrameSpeed=None, BaseSpeed=1, ParamMap=None, data=None, t=None):
        super().__init__()
        self.ModuleName = IndexName
        ParameterNames = ['PL','QL']
        StateVariableNames = ['iLd','iLq']
        PortInputNames = ['vLd','vLq']
        PortStateNames = ['iLd','iLq']
        ControllableInputNames = ['RL','LL']

        Units = ['A','A'] if BaseSpeed == 1 else ['units']*2

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

        self.PortCurrents = self.PortStates
        self.PortVoltages = self.PortInputs
        self.StateVariableDerivatives =  Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives =  Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Current', 'Current']
        self.StateSpaceEquations, self.ControlInputEquations = self.dynamics(data, t)
        self.StateSpace = StateSpace.from_module(self)

    def dynamics(self, data, t):
        '''
        Inputs:
        this.StateVariables: iLd,iLq
        this.InputVariables: vLd, vLq
        this.Parameters: RL, LL
            
        Outputs:
        StateSpace = [ diLddt ; diLqdt]
        ControlInputEquations
        '''
        iLd, iLq = self.StateVariables
        vLd, vLq = self.PortInputs

        if not data:
            P, Q = self.Parameters
        Ts = self.Parameters[2] if len(self.Parameters) > 2 else 10
        
        wb = self.BaseSpeed
        dphidt = self.RefFrameSpeed

        RL, LL = self.ControllableInputs
        
        if data:
            # Assuming data is a numpy array and t is defined
            tStep = data[1, 0] - data[0, 0]

            zohImpl = np.ones(int(Ts / tStep)) # zero-order hold (ZOH) implementation array
            nsamples = data.shape[0]
            tEnd = data[-1, 0]

            samples = np.arange(nsamples)

            # Sampled signal
            xSampled = np.zeros((len(t), 2))
            xSampled[::int(Ts / tStep), :] = data[samples * int(Ts), 1:3]

            # Convolution with impulse response
            xZohP = np.convolve(zohImpl, xSampled[:, 0])
            xZohQ = np.convolve(zohImpl, xSampled[:, 1])

            xZohP = xZohP[:len(t)]
            xZohQ = xZohQ[:len(t)]

            P = np.interp(t, np.arange(data[0, 0], tEnd, tStep), xZohP)
            Q = np.interp(t, np.arange(data[0, 0], tEnd, tStep), xZohQ)
        
        RL = P*(vLd**2 + vLq**2)/(P**2 + Q**2)
        LL = Q*(vLd**2 + vLq**2)/(P**2 + Q**2)
        
        # TimeVaryingImpLoad Dynamics
        diLddt = wb*(dphidt*iLq + (vLd - RL*iLd)/LL)
        diLqdt = wb*((vLq - RL*iLq)/LL - dphidt*iLd)

        StateSpace = Matrix([diLddt, diLqdt])
        ControlInputEquations = Matrix([RL, LL])

        StateSpace = simplify(StateSpace)
        return StateSpace, ControlInputEquations