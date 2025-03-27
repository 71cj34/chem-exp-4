# Note: this script contains only the calculations for Part B. Part A is done on Stemble (it does it automatically for you so you don't need a script for it).
# The provided values are for test tubes 1, 2, 3 respectively. I highly recommend you get your own values and don't just use mine because I'm 99% sure I did the experiment wrong.

# V_KSCN = 2
# V_FeNO3 = 5
# V_H2O = 3
# Abs = 0.144
# Slope = 4902

# V_KSCN = 3
# V_FeNO3 = 5
# V_H2O = 2
# Abs = 0.263
# Slope = 4902

V_KSCN = 4
V_FeNO3 = 5
V_H2O = 1
Abs = 0.370
Slope = 4902

#######################

V_tot = V_H2O+V_KSCN+V_FeNO3

print(f"V_tot = {V_tot}")
print(f"[SCN-] (initial) = {(V_KSCN*0.002)/V_tot}")
print(f"[Fe3+] (initial) = {(V_FeNO3*0.002)/V_tot}")

print(f"[FeSCN] at equilibrium is {Abs/Slope}")

scn = ((V_KSCN*0.002)/V_tot) - Abs/Slope
fe3 = ((V_FeNO3*0.002)/V_tot) - Abs/Slope
keq = (Abs/Slope)/(scn*fe3)

print(f"[SCN-] at equilibrium is {scn}")
print(f"[Fe3+] at equilibrium is {fe3}")
print(f"[K_eq] is {keq}")
