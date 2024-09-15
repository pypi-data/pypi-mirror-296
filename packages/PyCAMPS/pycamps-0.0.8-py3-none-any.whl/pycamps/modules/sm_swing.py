from sympy import symbols, Function, simplify, Matrix, sin, cos, pprint, sqrt
from pycamps.modules import Module
from pycamps.simulation import StateSpace

class SMSwing(Module):
    """
    Represents a synchronous machine with the swing equation.

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
        >>> from pycamps.modules import SMSwing
        >>> sm = SMSwing('G1', RefFrameAngle=symbols('phi'), RefFrameSpeed=symbols('dphidt'), BaseSpeed=377)
    """
    def __init__(self, IndexName, RefFrameAngle=None, RefFrameSpeed=None, BaseSpeed=1, ParamMap=None):
        super().__init__()
        self.ModuleName = IndexName
        ParameterNames = ['J','D','xdprime','RS']
        StateVariableNames = ['iSd','iSq','delta','omega']
        PortInputNames = ['vSd','vSq']
        PortStateNames = ['iSd','iSq']
        SetPointNames = ['omega', 'Pm','V']

        Units = ['A','A','radians','rad/s'] if BaseSpeed == 1 else ['units']*4

        IndexName = '_' + IndexName # TODO: Properly implement index names without leading underscore
        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}
        
        self.RefFrameAngle = RefFrameAngle if RefFrameAngle is not None else symbols('phi', real=True)
        self.RefFrameSpeed = RefFrameSpeed if RefFrameSpeed is not None else symbols('dphidt', real=True)
        self.BaseSpeed = BaseSpeed
        self.Units = Units

        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables =  Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.PortInputs =  Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates =  Matrix(symbols([p + IndexName for p in PortStateNames]))

        self.PortCurrents = -self.PortStates
        self.PortVoltages = self.PortInputs

        self.StateVariableDerivatives =  Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives =  Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.SetPoints =  Matrix(symbols([p + IndexName + '_ref' for p in SetPointNames]))
        self.PortOutputTypes = ['Current']*2
        self.StateSpaceEquations = self.dynamics()
        self.StateSpace = StateSpace.from_module(self)

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: delta,omega, eqprime
        this.InputVariables: iSd,iSq
        this.Parameters: J,D,Td0,xd,xdprime,RS,Pm,efd
        this.RefFrameAngle: angle of rotating reference frame
        this.RefFrameSpeed: speed of rotating reference frame
        this.BaseSpeed: Base speed
            
        Outputs:
        StateSpace: [diSddt ; diSqdt ; diRdt ; domegadt ; dthetadt]

        Refer Ilic, Marija D and Zaborszky, John, Dynamics and control
        of large electric power systems,2000, Wiley New York for
        detailed model derivation
        '''
        iSd, iSq, delta, omega  = self.StateVariables
        vSd, vSq = self.PortInputs
        J, D, xdprime, Rs = self.Parameters         
        omega_ref, Pm_ref, E_ref = self.SetPoints
        
        wb = self.BaseSpeed
        dphidt = self.RefFrameSpeed
        
        # Reference Transformation matrix: From network to machine  
        TN2M = Matrix([[sin(delta), -cos(delta)], [cos(delta), sin(delta)]])
        E_net = simplify((TN2M.inv() * Matrix([0, E_ref])))

        # State space of machine in network reference frame
        diSddt = (E_net[0] - vSd - 0*Rs*iSd)/xdprime + omega*iSq
        diSqdt = (E_net[1] - vSq - 0*Rs*iSq)/xdprime - omega*iSd
        
        Emag = E_ref
        Imag = sqrt(iSd**2 + iSq**2)
        
        ddeltadt = (omega-dphidt) 
        domegadt = 1/J*(Pm_ref - Emag*Imag - D*(omega-omega_ref))   # Rotor dynamics
        
        StateSpace = Matrix([diSddt, diSqdt, ddeltadt, domegadt])
        return StateSpace