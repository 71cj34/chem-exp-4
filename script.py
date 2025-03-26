import csv
import pandas as pd
from matplotlib import pyplot as plt
import asyncio
import datetime
import re

show_plot = 0
export_plot = 0
log = 0

salt_name = "nh4br"
mass_can = 14.83  # Mass of can (g)
mass_water_can = 100.04  # Mass of water inside can (g)
mass_salt = 4  # Mass of salt (g)
mass_water_cooling = 80.15  # Mass of water in cooling jacket (g)
delta_H_lit = 16800  # Literature value
T_initial = 19.781  # Initial temperature (°C)
T_final = 19.113  # Final temperature (°C)

specific_heat_water = 4.184  # Specific heat of water (J/g°C)
specific_heat_can = 0.9  # Specific heat of can (J/g°C)

# Autoimport csv
try:
    with open("NH4Br - Copy.csv", "r") as f:
        print("Data found. Loading from file...")
        contents = csv.reader(f)
        header = next(contents)
        T = list(map(lambda row: float(row[1]), contents))
        T_initial = T[0]
        T_final = min(T)
except FileNotFoundError:
    print("Data not found. Using coded values")

salts = {"KNO3": 101.1032, "NH4Br": 97.94, "LiCl": 42.394, "KBr": 119.02}

for k, v in salts.items():
    if k.lower() == salt_name.lower():
        norm_salt_name = k
        molar_mass_salt = v
        print(f"Salt: {norm_salt_name}; Molar mass: {molar_mass_salt}")

delta_T = T_final - T_initial

delta_H_rxn = (
            (mass_water_cooling + mass_salt) * specific_heat_water * delta_T
            + mass_can * specific_heat_can * delta_T
            + mass_water_can * specific_heat_water * delta_T
              ) * -1

# alternative formula (NON WORKING)
# delta_H_rxn = (specific_heat_water * (mass_water_cooling + mass_water_can)
#             + mass_can * specific_heat_can) * delta_T * -1 

if molar_mass_salt is not None:
    delta_H_soln = delta_H_rxn / (mass_salt / molar_mass_salt)
else:
    raise ValueError("Salt not found")

if log:
    # we loggin
    with open("log.txt", "a+") as f:
        var = globals()
        antiobject = re.compile(r'^[a-zA-Z0-9_.]+$')  # anti objects/methods
        antidunder = re.compile(r'^(?!.*__).+$')  # anti global variable
        savedvars = {
            key: value for key, value in var.items()
            if (antiobject.match(str(key)) and antidunder.match(str(key)) and
                antiobject.match(str(value)) and antidunder.match(str(value)))
        }
        f.write(f"Log taken {datetime.datetime.now().strftime('%c')}\n\n"
                f"# Saved variables:\n")
        for key, value in savedvars.items():
            f.write(f"{key}={value}\n")
        f.write("\nLOG END\n----------\n")


print(f"ΔT: {T_final} - {T_initial} = {delta_T:.6f}\n")
print(f"ΔH_rxn (J): {delta_H_rxn:.6f}")
print(f"ΔH_soln (J/mol): {delta_H_soln:.6f}")
print(f"%Error: {(abs(delta_H_soln - delta_H_lit)*100)/delta_H_lit}")


async def plot_data():
    if show_plot:
        df = pd.read_csv('data.csv')
        x = df.iloc[:, 0]
        y = df.iloc[:, 1]
        plt.figure(figsize=(16, 6))
        plt.plot(x, y, marker='o', linestyle='-', color='b')
        plt.xlabel('Time')
        plt.ylabel('Temp')
        plt.title('We Made a Chart')
        plt.grid(True)
        plt.show()


async def main():
    plot_task = asyncio.create_task(plot_data())

    # code should be done by now so just wait for the plot
    await plot_task

asyncio.run(main())
