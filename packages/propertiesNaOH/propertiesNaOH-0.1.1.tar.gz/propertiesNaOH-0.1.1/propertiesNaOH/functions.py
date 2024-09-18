import numpy as np
import matplotlib.pyplot as plt

from pyXSteam.XSteam import XSteam
steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)  # m/kg/sec/°C/bar/W

# NaOH property functions
def saturation_temperature(P, x1):
    """
    last change: brought to python by Dorian Höffner
    author: 16.7.2012 Anna Jahnke */
    Berechnung nach J. Olsson et. al "Thermophysical Properties of Aqueous NaOH-H2O Solutions at High Concentrations",
    International Journal of Thermophysics, Vol. 18, No. 3, 1997
    Boiling point temperature of aqueous NaOH-H2O Solution in °C
    
    Gültigkeitsbereich:
    T in [°C]
    MassFraction X[:]
    X[1]: [kg [NaOH)/ kg [H2O + NaOH)] 
    X[2]: [kg [H2O)/ kg [H2O + NaOH)]
    0<=T<20     0.582<=X[2]<=1
    20<=T<60    0.500<=X[2]<=1
    60<=T<70    0.353<=X[2]<=1
    70<=T<150    0.300<=X[2]<=1
    150<=T<=200  0.200<=X[2]<=1
    p in [Pa]"""

    # x X[1]
    x = 1 - x1 # X[2]

    k=[-113.93947, 209.82305, 494.77153, 6860.8330, 2676.6433, -21740.328, -34750.872, -20122.157, -4102.9890]
    l=[16.240074, -11.864008, -223.47305, -1650.3997, -5997.3118, -12318.744, -15303.153, -11707.480, -5364.9554, -1338.5412, -137.96889]
    m=[-226.80157, 293.17155, 5081.8791, 36752.126, 131262.00, 259399.54, 301696.22, 208617.90, 81774.024, 15648.526, 906.29769]

    a1=k[0] + k[1]*np.log(x) + k[2]*(np.log(x))**2 + k[3]*(np.log(x))**3 + k[4]*(np.log(x))**4 + k[5]*(np.log(x))**5 + k[6]*(np.log(x))**6 + k[7]*(np.log(x))**7 + k[8]*(np.log(x))**8
    a2=l[0] + l[1]*np.log(x) + l[2]*(np.log(x))**2 + l[3]*(np.log(x))**3 + l[4]*(np.log(x))**4 + l[5]*(np.log(x))**5 + l[6]*(np.log(x))**6 + l[7]*(np.log(x))**7 + l[8]*(np.log(x))**8 + l[9]*(np.log(x))**9 + l[10]*(np.log(x))**10
    a3=m[0] + m[1]*np.log(x) + m[2]*(np.log(x))**2 + m[3]*(np.log(x))**3 + m[4]*(np.log(x))**4 + m[5]*(np.log(x))**5 + m[6]*(np.log(x))**6 + m[7]*(np.log(x))**7 + m[8]*(np.log(x))**8 + m[9]*(np.log(x))**9 + m[10]*(np.log(x))**10

    p_kPa=P/1000  # Druck in [kPa]
    # Die Gleichung für den Dampfdruck der Lösung wurde umgestellt nach der Siedetemperatur T
    T = (a1 + a3 * np.log(p_kPa)) / (np.log(p_kPa) - a2)
    
    return float(T)

def enthalpy(x, T):
    """
    Last Change: brought to python by Dorian Höffner
    Autor: 	Roman Ziegenhardt
    Quelle: 	Thermophysical Properties of Aqueous NaOH-H2O Solutions at High Concentrations, J. OIsson, A. Jernqvist, G. Aly, 
    		International Journal of Thermophysics Vol. 18. No. 3. 1997
    zuletzt geändert: Elisabeth Thiele: Temperatur in °C und salt mass
    fraction statt water mass fraction
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    Parameter:
     T in [°C]
     x = m_NaOH/(m_H2O + m_NaOH)
     h in [kJ/kg]

    Wertebereich: t in Grad Celsius!
    0<=t<4			0.780 <=xi<=1
    4=<t<10	    0.680<=xi<=1
    10=<t<15		0.580<=xi<=1
    15=<t<26		0.540<=xi<=1
    26 =<t<37		0.440<=xi<=1
    37=<t<48		0.400<=xi<=1
    48=<t<60		0.340<=xi<=1
    60=<t<71		0.300<=xi<=1
    71=<t<82		0.280<=xi<=1
    82=<t<93		0.240<=xi<=1
    93=< t=<204	0.220<=xi<=1 """

    # Convert NaOH mass fraction to water mass fraction
    xi = 1 - x

    # Coefficients
    k = np.array([1288.4485, -0.49649131, -4387.8908, -4.0915144, 4938.2298, 7.2887292, -1841.1890, -3.0202651])
    l = np.array([2.3087919, -9.0004252, 167.59914, -1051.6368, 3394.3378, -6115.0986, 6220.8249, -3348.8098, 743.87432])
    m = np.array([0.02302860, -0.37866056, 2.4529593, -8.2693542, 15.728833, -16.944427, 9.6254192, -2.2410628])
    n = np.array([-8.5131313e-5, 136.52823e-5, -875.68741e-5, 2920.0398e-5, -5488.2983e-5, 5841.8034e-5, -3278.7483e-5, 754.45993e-5])

    # Calculation of coefficients
    c1 = (k[0] + k[2]*xi + k[4]*(xi**2) + k[6]*(xi**3)) / (1 + k[1]*xi + k[3]*(xi**2) + k[5]*(xi**3) + k[7]*(xi**4))
    c2 = l[0] + l[1]*xi + l[2]*(xi**2) + l[3]*(xi**3) + l[4]*(xi**4) + l[5]*(xi**5) + l[6]*(xi**6) + l[7]*(xi**7) + l[8]*(xi**8)
    c3 = m[0] + m[1]*xi + m[2]*(xi**2) + m[3]*(xi**3) + m[4]*(xi**4) + m[5]*(xi**5) + m[6]*(xi**6) + m[7]*(xi**7)
    c4 = n[0] + n[1]*xi + n[2]*(xi**2) + n[3]*(xi**3) + n[4]*(xi**4) + n[5]*(xi**5) + n[6]*(xi**6) + n[7]*(xi**7)

    # Calculate enthalpy
    h = c1 + c2*T + c3*(T**2) + c4*(T**3)

    return float(h)

def saturation_pressure(x, T):
    """
    Calculates the pressure of aqueous NaOH-H2O solutions at high concentrations.
    
    Last Change: Dorian Höffner 2024-04-26 (translated to Python, changed input T to [°C], changed return value to [Pa])
    Author: Anna Jahnke, Roman Ziegenhardt
    Source: Thermophysical Properties of Aqueous NaOH-H2O Solutions at High Concentrations, J. Olsson, A. Jernqvist, G. Aly,
            International Journal of Thermophysics Vol. 18, No. 3, 1997
    
    Parameters:
    T (array-like): Temperature in [°C].
    x (array-like): Mass fraction, defined as m_NaOH / (m_H2O + m_NaOH).
    
    Returns:
    p (float or array-like): Pressure in [Pa]

    Notes:
    Wertebereich: t in Grad Celsius!
    0<=t<20    		0.582<=x<=1
    20<=t<60		0.500<=x<=1
    60<=t<70       	0.353<=x<=1
    70<=t<150		0.300<=x<=1
    150<=t<=200		0.200<=x<=1
    """

    # convert NaOH mass fraction to water mass fraction
    x = 1 - x
    
    if isinstance(x, (int, float)) or isinstance(T, (int, float)):
        pass
    elif len(x) != len(T):
        raise ValueError('x and T must have the same length')

    # Constants
    k = np.array([-113.93947, 209.82305, 494.77153, 6860.8330, 2676.6433,
                  -21740.328, -34750.872, -20122.157, -4102.9890])
    l = np.array([16.240074, -11.864008, -223.47305, -1650.3997, -5997.3118,
                  -12318.744, -15303.153, -11707.480, -5364.9554, -1338.5412,
                  -137.96889])
    m = np.array([-226.80157, 293.17155, 5081.8791, 36752.126, 131262.00,
                  259399.54, 301696.22, 208617.90, 81774.024, 15648.526,
                  906.29769])

    # Calculate pressure
    log_x = np.log(x)
    a1 = np.polyval(k[::-1], log_x)
    a2 = np.polyval(l[::-1], log_x)
    a3 = np.polyval(m[::-1], log_x)

    logP = (a1 + a2 * T) / (T - a3)
    p = np.exp(logP) * 1000

    return float(p) # pressure in Pa

def pTDiagram(log=True, invT=True, editablePlot=False, show_percentages=True):
    steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)  # m/kg/sec/°C/bar/W
    
    # Temperature range
    temperaturesC = np.arange(0, 100, 1)
    temperaturesK = temperaturesC + 273.15
    concentrations = np.arange(0.2, 0.601, 0.01)
    
    # Prepare the plot
    plt.figure()
    
    # these temperatures are used for the x-axis
    plotTemperatures = np.arange(0, 101, 10) + 273.15
    
    # Calculate water vapor pressure using XSteam
    waterPressure = [steamTable.psat_t(T - 273.15) * 1e5 for T in temperaturesK]  # convert bar to Pa
    
    # Plot the data
    for x in concentrations:
        p = []
        for T in temperaturesC:
            p.append(saturation_pressure(x, T))  # Assuming PressureNaOH is defined elsewhere
    
        # Set color and line width
        color = "black" if int(np.round(x * 100)) % 10 == 0 else "grey"
        lw = 1.0 if color == "black" else 0.25
        
        # Plotting based on conditions
        temp_plot = -1/temperaturesK if invT else temperaturesK
        ylabel = 'Dampfdruck [Pa]' if log else 'Dampfdruck [Pa]'
        xlabel = 'Temperature [°C] (scaled -1/T)' if invT else 'Temperatur [°C]'
        
        if log:
            plt.semilogy(temp_plot, p, color=color, lw=lw)
        else:
            plt.plot(temp_plot, p, color=color, lw=lw)
        
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.xticks(-1/plotTemperatures if invT else plotTemperatures, plotTemperatures - 273.15)
        
        # Label concentrations
        if show_percentages and int(np.round(x * 100)) % 10 == 0:
            label_pos = temp_plot[-1] + 1e-5 if invT else temp_plot[-1]+2
            plt.text(label_pos, p[-1], f'{x * 100:.0f} %', fontsize=8, color='black')

    # Plotting water line
    if log:
        plt.semilogy(temp_plot, waterPressure, color="grey", linestyle='--',
                     label='Pure Water')
    else:
        plt.plot(temp_plot, waterPressure, color="grey", linestyle='--', label='Pure Water')
    

    # Setting axis limits
    if invT:
        plt.xlim(-1/temperaturesK[0], -1/temperaturesK[-1])
    else:
        plt.xlim(temperaturesK[0], temperaturesK[-1])
    
    if log:
        plt.ylim(50, 1e5)
    else:
        plt.ylim(0, max(waterPressure) * 1.1)  # Adjust as needed to make sure all data is visible



    plt.legend()
    
    if not editablePlot:
        plt.show()

def density(x, T):
    """
    DensityNaOH calculates the density of NaOH solution based on concentration and temperature.

    Source: "Thermophysical Properties of Aqueous NaOH-H2O Solutions at High Concentrations,
    J. OIsson, A. Jernqvist, G. Aly, International Journal of Thermophysics Vol. 18. No. 3. 1997"

    Parameters:
    x (array-like): Mole fraction of NaOH in the solution. [m_NaOH / (m_h2o+m_naoh)]
    T (array-like): Temperature in °C.

    Returns:
    rho (numpy array): Density in kg/m^3.
    """

    # transform x=x_NaOH to x=x_h2o

    if isinstance(x, (int, float)) or isinstance(T, (int, float)):
        x = 1 - x
        pass
    elif len(x) != len(T):
        raise ValueError('x and T must have the same length')
    else:
        x = 1 - np.array(x)
        T = np.array(T)

    # Coefficients
    k = np.array([5007.2279636, -25131.164248, 74107.692582, -104657.48684, 69821.773186, -18145.911810])
    l = np.array([-64.786269079, 525.34360564, -1608.4471903, 2350.9753235, -1660.9035108, 457.6437435])
    m = np.array([0.24436776978, -1.9737722344, 6.04601497138, -8.9090614947, 6.37146769397, -1.7816083111])

    x = np.array(x)
    
    b1 = k[0] + k[1] * (x ** (1/2)) + k[2] * x + k[3] * (x ** (3/2)) + k[4] * (x ** 2) + k[5] * (x ** (5/2))
    b2 = l[0] + l[1] * (x ** (1/2)) + l[2] * x + l[3] * (x ** (3/2)) + l[4] * (x ** 2) + l[5] * (x ** (5/2))
    b3 = m[0] + m[1] * (x ** (1/2)) + m[2] * x + m[3] * (x ** (3/2)) + m[4] * (x ** 2) + m[5] * (x ** (5/2))

    rho = b1 + b2 * T + b3 * (T ** 2)

    return float(rho)

def specific_heat_capacity(x, T):
    """
    Calculate the specific heat capacity of a NaOH solution as a function of temperature and concentration.
    The function is based on the following publication:
    Alexandrov 2004 - "The Equations for Thermophysical Properties of Aqueous Solutions of Sodium Hydroxide"
    ---
    x: float
        Concentration of NaOH in the solution [kg/kg]
    T: float
        Temperature of the solution [°C]
    ---
    returns: float
        Specific heat capacity of the solution [kJ/kgK]
    ---
    Author: Dorian Höffner
    Date: 2024-08-19
    """

    # Constants
    a01=9.8555259e1
    a11=-3.4501318e2
    a21=4.8180532e2
    a31=-3.3440616e2
    a41=1.1516735e2
    a51=-1.5708814e1

    a02=-3.4357815e1
    a12=1.1674552e2
    a22=-1.5776854e2
    a32=1.0577045e2
    a42=-3.5099188e1
    a52=4.5935013
    
    a03=1.9791083
    a13=-5.3828966
    a23=5.5124212
    a33=-2.5430046
    a43=4.5943595e-1
    
    a04=-5.6191575e-2
    a14=8.5936388e-2
    a24=-1.6966718e-2
    a34=-1.4864492e-2
    
    a05=7.9944152e-3
    a15=-1.5444457e-2
    a25=7.5030322e-3


    cp_water = steamTable.CpL_t(T) # [kJ/kgK]

    # calculate molality (mol/kg) from concentration (kg/kg)
    M = 39.9971e-3          # [kg/mol]
    m = x / M               # [mol/kg]

    # calculate relative temperature
    t = (T + 273.15) / 273.15

    cp_diff = m    * (a01 + a11 * t + a21 * t**2 + a31 * t**3 + a41 * t**4 + a51 * t**5) + \
              m**2 * (a02 + a12 * t + a22 * t**2 + a32 * t**3 + a42 * t**4 + a52 * t**5) + \
              m**3 * (a03 + a13 * t + a23 * t**2 + a33 * t**3 + a43 * t**4) + \
              m**4 * (a04 + a14 * t + a24 * t**2 + a34 * t**3) + \
              m**5 * (a05 + a15 * t + a25 * t**2)

    if x <= 0.0001:
        cp = cp_water
    else:
        cp = cp_water - cp_diff * 1e-3 # [kJ/kgK]

    return cp

def dynamic_viscosity(x, T, p):
    """
    Calculate the dynamic viscosity of a NaOH solution as a function of temperature and concentration.
    The function is based on the following publication:
    Alexandrov 2004 - "The Equations for Thermophysical Properties of Aqueous Solutions of Sodium Hydroxide"
    ---
    x: float
        Concentration of NaOH in the solution [kg/kg]
    T: float
        Temperature of the solution [°C]
    p: float
        Pressure of the solution [Pa]
    ---
    returns: float
        Dynamic viscosity of the solution [Pa s]
    """

    # prepare inputs
    M = 39.9971e-3                      # [kg/mol]
    m = x / M                           # [mol/kg]
    T0 = 293.15                         # [K] (yes 293.15, not 273.15)
    t = T0 / (T + 273.15)               # [-]
    t1 = t - 1                          # [-]

    p = p / 1e6                         # [Pa]  -> [MPa]
    p_sw = steamTable.psat_t(T) / 1e1   # [bar] -> [MPa]
    
    # coeffs from cited publicatiosn
    c = np.array([np.nan, 5.17341030, 9.81838817, 2.83021985e1, 7.02071954e1, -9.92041252e2, -1.13267055e4, -5.10988292e4, -1.18863488e5, -1.41053273e5, -6.78490604e4])
    d = np.array([-3.18833435e-1, -1.07314454e1, -8.61347656e1, -6.50268842e2, -6.06767730e3, -4.07022741e4, -1.59650983e5, -3.53438962e5, -4.11357235e5, -1.96118714e5, np.nan])

    expression1 =        c[1] * t1 + c[2] * t1**2 + c[3] * t1**3 + c[4] * t1**4 + c[5] * t1**5 + c[6] * t1**6 + c[7] * t1**7 + c[8] * t1**8 + c[9] * t1**9 + c[10] * t1**10
    expression2 = d[0] + d[1] * t1 + d[2] * t1**2 + d[3] * t1**3 + d[4] * t1**4 + d[5] * t1**5 + d[6] * t1**6 + d[7] * t1**7 + d[8] * t1**8 + d[9] * t1**9
    my_water    = 1001.6 * (t1 + 1)**2 * np.exp(expression1) + (p-p_sw) * expression2 # [µPa s]

    # coeffs from actual publication
    b11 =  5.7070102e-1
    b21 =  4.9395013e-1
    b31 = -2.0417183
    b41 =  1.1654862

    b12 = -2.9922166e-1
    b22 =  3.7957782e-1
    b32 = -7.423751e-2

    b13 =  4.9815412e-2
    b23 = -4.8332728e-2

    expression3 = m    * (b11 * t + b21 * t**2 + b31 * t**3 + b41 * t**4) + \
                  m**2 * (b12 * t + b22 * t**2 + b32 * t**3) + \
                  m**3 * (b13 * t + b23 * t**2)
    
    my_rel = np.exp(expression3)

    my = my_water * np.exp(expression3) # [µPa s]

    return float(my * 1e-6) # [Pa s]

def thermal_conductivity(x, T, p):
    """
    Calculate the thermal conductivity of a NaOH solution as a function of temperature and concentration.
    The function is based on the following publication:
    Alexandrov 2004 - "The Equations for Thermophysical Properties of Aqueous Solutions of Sodium Hydroxide"
    ---
    x: float
        Concentration of NaOH in the solution [kg/kg]
    T: float
        Temperature of the solution [°C]
    ---
    returns: float
        Thermal conductivity of the solution [W/mK]
    ---
    """

    # prepare inputs for water calculation
    p_sw = steamTable.psat_t(T) / 1e1   # [bar] -> [MPa]
    p = p / 1e6                         # [Pa]  -> [MPa]
    T02 = 273.15 + 20                   # [K]
    t = T02 / (T + 273.15) - 1          # [-]

    # coeffs from cited publication (for water)
    g = np.array([5.99454842e-1, -4.82554378e-1, -4.31229616e-1, -8.62555022e-1, -3.80050418e-1, 4.85828450e1, 3.35400696e2, 1.08007806e3, 1.67727081e3, 1.04225629e3])
    q = np.array([5.31492446e-4, 3.46658996e-4, 1.23050434e-2, 1.27873471e-1, -7.40820487e-1, -1.93072528e1, -1.22835056e2, -3.66150909e2, -5.31321978e2, -3.03153185e2])

    expression1 = g[0] + g[1] * t**1 + g[2] * t**2 + g[3] * t**3 + g[4] * t**4 + g[5] * t**5 + g[6] * t**6 + g[7] * t**7 + g[8] * t**8 + g[9] * t**9
    expression2 = q[0] + q[1] * t**1 + q[2] * t**2 + q[3] * t**3 + q[4] * t**4 + q[5] * t**5 + q[6] * t**6 + q[7] * t**7 + q[8] * t**8 + q[9] * t**9
    lambda_water = expression1 + (p-p_sw) * expression2  # [kW/mK]

    
    # prepare inputs for NaOH calculation
    T0 = 403.0 # [K]
    t1 = (T+273.15) / T0
    M = 39.9971e-3          # [kg/mol]
    m = x / M               # [mol/kg]
    
    # coeffs from actual publication (for NaOH)
    e01 = 3.2900544e-1
    e11 = -1.1048583
    e21 = 1.2503803
    e31 = -4.4228179e-1

    e02 = -2.1990820e-2
    e12 = 5.9100989e-2
    e22 = -4.4407173e-2
    
    e03 = 1.5069324e-3
    e13 = -4.3273501e-3
    e23 = 3.3763248e-3

    expression3 = m    * (e01 + e11 * t1 + e21 * t1**2 + e31 * t1**3) + \
                  m**2 * (e02 + e12 * t1 + e22 * t1**2) + \
                  m**3 * (e03 + e13 * t1 + e23 * t1**2)
    
    lambda_NaOH = lambda_water + expression3 # [kW/mK]

    return float(lambda_NaOH * 1e3) # [W/mK]


def dhdx(x,T):
    # Author: Elisabeth Thiele
    # brought to python by Dorian Höffner
    # partielles Differential dh/dx

    # Variables:
    # T:        Temperatur            in °C
    # x:        NaOH concentration in kg NaOH/kg solution
    # dhdx:     partielle Ableitung Enthalpie nach Massenanteil in [kJ/kg]

    delta = 0.000001
    x1 = x - delta
    x2 = x + delta

    dhdx = (enthalpy(x2,T) - enthalpy(x1,T)) / (2*delta)
    return dhdx


def dhdT(x,T):
    # Author: Elisabeth Thiele
    # partielles Differential dh/dx

    # Variables:
    # T:        Temperatur [°C]
    # x:        NaOH concentration [kg NaOH/kg solution]
    # dhdx:     partielle Ableitung Enthalpie nach Temperatur in [kJ/kgK] EINHEIT?

    delta = 0.0001
    T1 = T - delta
    T2 = T + delta

    dhdT = (enthalpy(x,T1) - enthalpy(x,T2)) / (2*delta)
    return dhdT