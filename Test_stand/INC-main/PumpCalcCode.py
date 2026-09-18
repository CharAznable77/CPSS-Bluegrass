"""
pump_sizing.py — Python translation of the provided MATLAB "Pump version 2 calcs".
Run directly or import pump_calcs()/PumpInputs in notebooks or scripts.
"""
 
import math
from dataclasses import dataclass, asdict
from typing import Dict, Any
 
@dataclass
class PumpInputs:
    Q_gpm: float = 4.0
    H_psi: float = 400.0
    N_rpm: float = 30000.0
    n_bla: int = 10
    n_dif: int = 1
    k6_m: float = 0.001
    g_ft_s2: float = 32.2
    psi_coef: float = 0.7
    spec_g: float = 0.79
    eta: float = 0.2
    eta_d: float = 0.8
    phi: float = 0.8
    rho: float = 1000.0
    mu: float = 523.1e-6
 
def pump_calcs(inp: PumpInputs) -> Dict[str, Any]:
    H_ft = 2.31 * inp.H_psi
    omega = inp.N_rpm * 2*math.pi / 60.0  # rad/s
 
    Ns = inp.N_rpm * (inp.Q_gpm ** 0.5) * (H_ft ** -0.75)
    D2_in = 1300.0/(Ns * (H_ft**0.25)) * ((inp.Q_gpm/inp.psi_coef) ** 0.5)
    d1_in = 0.268 * ((inp.Q_gpm/inp.phi) ** 0.5) * ((inp.psi_coef/H_ft) ** 0.25)
    De_in = 5.1 * ((inp.Q_gpm/inp.N_rpm) ** (1.0/3.0))
    b2_in = d1_in
    b1_in = b2_in * 1.25
 
    P_req_hp = (inp.Q_gpm * H_ft * inp.spec_g) / (3956.0 * inp.eta)
    P_req_W = P_req_hp * 745.7
 
    T_req_lb_in = 63025.0 * (P_req_W/745.7) / inp.N_rpm
    T_req_Nm = T_req_lb_in * 0.11298482933333
 
    D1_in = 1.0 * De_in
    D3_in = 0.75 * D1_in
 
    D1_m = D1_in * 0.0254
    D2_m = D2_in * 0.0254
    d1_m = d1_in * 0.0254
    R3_in = D3_in / 2.0
    R3_m = R3_in * 0.0254
    b1_m = b1_in * 0.0254
    b2_m = b2_in * 0.0254
 
    R1_m = D1_m/2.0
    R2_m = D2_m/2.0
 
    k1 = 1.055 * (1.0 - (1.0 / (inp.n_bla ** 0.903))) * (1.0 - (R1_m/R2_m) ** 4.401)
    k2 = 1.42 * (1.0 - (1.0 / (inp.n_bla ** 0.49)))
 
    omega_2 = k1 * omega
 
    q_v_m3s = k2 * inp.n_dif * math.pi * ((d1_m/2.0) ** 2) * omega_2 * R2_m
    q_v_GPM = q_v_m3s * 15850.323140625
 
    dP_Pa = 0.5 * inp.rho * (omega_2 * R2_m) ** 2 + 0.5 * inp.eta_d * inp.rho * (omega_2 * R2_m) ** 2
    dP_psi = dP_Pa * 0.000145038
 
    L_m = R2_m - R1_m
    S_solidity = L_m * inp.n_bla / (math.pi * D2_m)
 
    Re = inp.rho * omega_2 * ((R3_m ** 2) / inp.mu)
    b_bar_m = (b1_m + b2_m)/2.0
    k3 = inp.k6_m * (0.134/(Re ** 0.246)) * ((b_bar_m/R3_m) ** 0.0655)
    k4 = inp.k6_m * (0.0105/(Re ** 0.193))
    P_f_W = 0.5 * inp.rho * (omega ** 3) * (R3_m ** 4) * ((2.0 * k3 * R3_m) + (2.0 * math.pi * b2_m * k4))
 
    denom_W = q_v_m3s * inp.rho * omega * R2_m * omega_2 * R2_m + P_f_W
    eta_calc = (dP_Pa * q_v_m3s) / denom_W if denom_W != 0 else float('nan')
 
    P_req_calc_W = (q_v_m3s * dP_Pa * inp.spec_g) / (eta_calc if eta_calc != 0 else float('nan'))
 
    return {
        "inputs": asdict(inp),
        "derived": {
            "H_ft": H_ft,
            "omega_rad_s": omega,
            "Ns": Ns,
            "D2_in": D2_in,
            "d1_in": d1_in,
            "De_in": De_in,
            "b1_in": b1_in,
            "b2_in": b2_in,
            "P_req_W": P_req_W,
            "T_req_Nm": T_req_Nm,
            "D1_in": D1_in,
            "D3_in": D3_in,
            "D2_m": D2_m,
            "d1_m": d1_m,
            "R3_m": R3_m,
            "b1_m": b1_m,
            "b2_m": b2_m,
            "k1": k1,
            "k2": k2,
            "omega_2_rad_s": omega_2,
            "q_v_m3s": q_v_m3s,
            "q_v_GPM": q_v_GPM,
            "dP_Pa": dP_Pa,
            "dP_psi": dP_psi,
            "S_solidity": S_solidity,
            "Re": Re,
            "k3": k3,
            "k4": k4,
            "P_f_W": P_f_W,
            "eta_calc": eta_calc,
            "P_req_calc_W": P_req_calc_W
        }
    }
 
def demo():
    res = pump_calcs(PumpInputs())
    print(" - Results from input factors -")
    print(f" - Specific Speed (Ns) = {res['derived']['Ns']:.6g}")
    print(f" - Impeller Diameter (D2) = {res['derived']['D2_in']:.6g} [in]")
    print(f" - Volute Outlet Diameter (d1) = {res['derived']['d1_in']:.6g} [in]")
    print(f" - Eye Diameter (De) = {res['derived']['De_in']:.6g} [in]")
    print(f" - Impeller Eye Tip Height (b1) = {res['derived']['b1_in']:.6g} [in]")
    print(f" - Impeller Edge Tip Height (b2) = {res['derived']['b2_in']:.6g} [in]")
    print(f" - Required Power (P_req) = {res['derived']['P_req_W']:.6g} [W]")
    print(f" - Required Torque (T_req) = {res['derived']['T_req_Nm']:.6g} [N·m]")
    print("")
    print(" - Estimated metrics @BEP -")
    print(f" - Head rise (dP_calculated) = {res['derived']['dP_psi']:.6g} [psi]")
    print(f" - Flowrate (q_v_calculated) = {res['derived']['q_v_GPM']/3.75:.6g} [GPM]")
    print(f" - Efficiency (eta_calculated) = {100.0*res['derived']['eta_calc']:.6g} [%]")
    print(f" - Efficiency (P_req_calc) = {res['derived']['P_req_calc_W']:.6g} [W]")
 
if __name__ == "__main__":
    demo()
 