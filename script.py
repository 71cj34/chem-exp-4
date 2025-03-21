import csv

mass_can = 15.98  # Mass of can (g)
mass_water_can = 100.08  # Mass of water inside can (g)
mass_salt = 4  # Mass of salt (g)
mass_water_cooling = 80.03  # Mass of water in cooling jacket (g)
T_initial = 19.781  # Initial temperature (°C)
T_final = 19.113  # Final temperature (°C)

specific_heat_water = 4.184  # Specific heat of water (J/g°C)
specific_heat_can = 0.9  # Specific heat of can (J/g°C)
molar_mass_salt = 97.94  # Molar mass of salt (g/mol)

# Autoimport csv
try:
    with open("data.csv", "r") as f:
        print("Data found. Loading from file...")
        contents = csv.reader(f)
        header = next(contents)
        T = list(map(lambda row: float(row[1]), contents))
        T_initial = T[0]
        T_final = min(T)
except FileNotFoundError:
    print("Data not found. Using coded values")

delta_T = T_final - T_initial

delta_H_rxn = (
    mass_water_cooling * specific_heat_water * delta_T
    + mass_can * specific_heat_can * delta_T
    + mass_water_can * specific_heat_water * delta_T
)*-1

delta_H_soln = delta_H_rxn / (mass_salt / molar_mass_salt)

print(f"ΔH_rxn (J): {delta_H_rxn:.6f}")
print(f"ΔH_soln (J/mol): {delta_H_soln:.6f}")
