from sympy import symbols, Function, simplify, Matrix
from pycamps.modules.module import Module
from pycamps.simulation.state_space import StateSpace

class PQLoad(Module):
    def __init__(self, IndexName, RefFrameAngle=None, RefFrameSpeed=None, BaseSpeed=1, ParamMap=None):
        super().__init__()
        self.ModuleName = IndexName
        ParameterNames = ['PL','QL']
        StateVariableNames = ['iLd','iLq']
        PortInputNames = ['vLd','vLq']
        PortStateNames = ['iLd','iLq']
        ControllableInputNames = ['LL']

        if BaseSpeed == 1:
            Units = ['V', 'V', 'A', 'A', 'V', 'V']
        else:
            Units = ['units']*6

        self.RefFrameAngle = RefFrameAngle if RefFrameAngle is not None else symbols('phi', real=True)
        self.RefFrameSpeed = RefFrameSpeed if RefFrameSpeed is not None else symbols('dphidt', real=True)
        self.BaseSpeed = BaseSpeed
        IndexName = '_' + IndexName # TODO: Properly implement index names without leading underscore
        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}

        self.Units = Units
        
        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables = Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.ControllableInputs = Matrix(symbols([c + IndexName for c in ControllableInputNames]))
        self.PortInputs = Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates = Matrix(symbols([p + IndexName for p in PortStateNames]))
        
        self.PortVoltages = self.PortInputs
        self.PortCurrents = self.PortStates
        self.StateVariableDerivatives = Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives = Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        
        self.PortOutputTypes = ['Current','Current']
        self.StateSpaceEquations, self.ControlInputEquations = self.dynamics()
        self.StateSpace = StateSpace.from_module(self)

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: iLd,iLq
        this.InputVariables: vLd, vLq
        this.Parameters: PL, QL
        
        Outputs:
        StateSpace = [ diLddt ; diLqdt];
        NOTE: TO BE USED ONLY IN THE ABSENCE OF INDUCTOR CUTSETS
        '''
        iLd, iLq = self.StateVariables
        vLd, vLq = self.PortInputs
        PL, QL = self.Parameters
        # LL = (QL*(vLd**2 + vLq**2))/(PL**2 + QL**2)
        LL = self.ControllableInputs[0]

        wb = self.BaseSpeed
        dphidt = self.RefFrameSpeed

        # PQLoad Dynamics
        diLddt = (-PL/QL * iLd) + vLd/LL + dphidt*iLq
        diLqdt = (-PL/QL * iLq) + vLq/LL - dphidt*iLd
            
        LL = (QL*(vLd**2 + vLq**2))/(PL**2 + QL**2)

        StateSpace = wb * Matrix([diLddt, diLqdt])
        StateSpace = simplify(StateSpace)
        ControlInputEquations = Matrix([LL])
        return StateSpace, ControlInputEquations