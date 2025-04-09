potentials = {
    "mg": -2.372,
    "cu": 0.34,
    "pb": -0.1262,
    "ni": -0.257,
    "sn": -0.1375,
    "zn": -0.7618,
}

salts = {
    "cu": 0.34,
    "zn": -0.7618,
    "sn": -0.1375
}


def error_pct(exp, theory):
    # DO NOT EDIT THIS FUNCTION
    return abs((exp - theory) / theory) * 100


def serial_dilute(starting_m, goal_m, dilute_amt, max_keep):
    # DO NOT EDIT THIS FUNCTION

    # uses a brute force approach
    # function assumes max_keep only increments by 0.1
    deltas_all = {}
    # max_keep only supports 1 decimal point
    decimalized = [round(j / 10, 1) for j in range(1, int(max_keep * 10) + 1)]

    def focus_range(starting_amt_1, starting_m_2):
        # deltas format: {(k1, k2, k3, k4): v1} where:
        # k1=round 1 amt, k2=starting molarity, k3=round 2 amt, k4=final molarity, v1=error
        deltas = {}
        for i in decimalized:
            final_dilution = (i * starting_m_2) / dilute_amt
            deltas[(starting_amt_1, starting_m_2, i, final_dilution)] = error_pct(final_dilution, goal_m)
        return deltas

    for i in decimalized:
        m_2 = (i * starting_m) / dilute_amt
        deltas_all.update(focus_range(i, m_2))
    # his ass is NOT O(n)!!!!!
    # as long as this delta list isn't a bajillion things long O(nlogn) is fine
    return sorted(deltas_all.items(), key=lambda item: item[1])[:10]


def task_1():
    # Write your four provided anode/cathode pairs in that order
    e_pairs = [
        ["cu", "mg"],
        ["pb", "mg"],
        ["mg", "zn"],
        ["sn", "zn"]
    ]

    # Write the corresponding experimental enthalpies
    e_exp = [
        -2.598,
        -2.165,
        1.527,
        -0.601,
    ]

    print("Pair\t\tCalculated\tExperimental\t% Error")
    print("------------------------------------------------")
    for i in range(len(e_pairs)):
        anode, cathode = e_pairs[i]
        calculated = potentials[cathode] - potentials[anode]
        experimental = e_exp[i]

        percent_error = error_pct(experimental, calculated)

        print(
            f"{'-'.join(map(str, e_pairs[i]))}\t{abs(calculated):.4f}\t\t{abs(experimental):.4f}\t\t{percent_error:.2f}%")


def task_2():
    # add the concentration of the undiluted solution
    undiluted_conc = 0.05
    # add the goal dilution
    diluted_conc = 0.00005
    # amount (in ml) the solution is diluted to at each serial dilution step
    dilute_amt = 50
    # maximum amount (in ml) that can be taken via pipette each serial dilution step
    max_pipetted = 2

    # use the %error cmdlet after you do the simulation

    # DO NOT EDIT ANYTHING AFTER THIS

    current_index = 0
    # this should be abstracted ngl
    t10 = serial_dilute(undiluted_conc, diluted_conc, dilute_amt, max_pipetted)
    print("Rnk\t\tAmount-1\tExpected Molarity after 1\tAmount-2\tFinal Molarity\t% Error")
    print("-----------------------------------------------------------------------------------")
    for k1, v1 in t10:
        current_index += 1
        print(f"{current_index}\t\t{k1[0]:.1f}\t\t\t{k1[1]:.8f}\t\t\t\t\t{k1[2]:.1f}\t\t\t{k1[3]:.8f}\t\t{v1:.2f}%")


def task_3():
    # your goal ecell value
    wanted_ecell = 0.611
    # the initial molarity of both solutions
    molarity_of_solutions = 0.05
    # amount (in ml) the solution is diluted to at each serial dilution step
    dilute_amt = 50
    # maximum amount (in ml) that can be taken via pipette each serial dilution step
    max_pipetted = 2

    # use the %error cmdlet after you do the simulation

    # DO NOT EDIT ANYTHING PAST THIS LINE
    metals = list(salts.keys())
    valid_ms = {}
    exit = 0
    while not exit:
        invalids = 0
        for first_metal in metals:
            for second_metal in metals:
                if first_metal != second_metal:
                    print("--------------------------")
                    print(f"Pair: {first_metal}-{second_metal}")
                    e1 = salts[first_metal]
                    e2 = salts[second_metal]
                    print(f"Values: {salts[first_metal]}, {salts[second_metal]}")
                    e_cell = e2 - e1
                    required_molarity = (10 ** ((wanted_ecell - e_cell) / -0.0296)) * molarity_of_solutions
                    if 2e-7 < required_molarity < 0.00008:
                        exit = 1
                        print(
                            f"\033[1;32mVALID MOLARITY FOUND\033[0m: pairing {first_metal}-{second_metal}, "
                            f"molarity required {required_molarity}\n")
                        print(f"Ecell: {e_cell:.5f}")
                        print(f"Target - Ecell: {(wanted_ecell - e_cell):.5f}")
                        valid_ms[str(first_metal + "-" + second_metal)] = required_molarity
                        print(
                            f"The molarity except not multiplied by the molarity of the solution ({molarity_of_solutions}) : "
                            f"{(10 ** ((wanted_ecell - e_cell) / -0.0296))})")
                    else:
                        invalids += 1
                        print(
                            f"\033[1;31mINVALID MOLARITY FOUND\033[0m: pairing {first_metal}-{second_metal}, molarity {required_molarity}, "
                            f"{'too big!' if required_molarity > 0.00008 else 'too small!'}")

        if invalids == 6:
            print("\n\nAll combinations were invalid! Reducing V...")
            wanted_ecell -= round(0.01, 2)
            print(f"New target E value: {wanted_ecell}\n\n")

    a = input("\n\nOne or more valid molarit(ies) was found. Scroll up to find it.\n"
              "Continue with serial dilution calculator (y/n)? ")
    if a == "y":
        for k, v in valid_ms.items():
            current_index = 0
            print(
                f"\nExecuting command \'serial_dilute({molarity_of_solutions}, {v}, {dilute_amt}, {max_pipetted})\'...\n")
            t10 = serial_dilute(molarity_of_solutions, v, dilute_amt, max_pipetted)
            print(f"RESULTS FOR PAIRING {k}")
            print("Rnk\t\tAmount-1\tExpected Molarity after 1\tAmount-2\tFinal Molarity\t% Error")
            print("-------------------------------------------------------------------------------------")
            for k1, v1 in t10:
                current_index += 1
                print(
                    f"{current_index}\t\t{k1[0]:.1f}\t\t\t{k1[1]:.8f}\t\t\t\t\t{k1[2]:.1f}\t\t\t{k1[3]:.8f}\t\t{v1:.2f}%")

    else:
        pass


if __name__ == "__main__":
    while True:
        try:
            a = int(input("Which task to run (0 for error % cmdlet, 4 for all three): "))
            if a == 4:
                task_1()
                # task_2()
                # task_3()
            elif a == 0:
                print(f'{error_pct(float(input("Experimental value: ")), float(input("Theoretical Value: "))):.4f}%')
            else:
                try:
                    exec(f"task_{a}()")
                except NameError:
                    print(f"Function \'task_{a}()\' could not be found. Are you sure your input is correct?")
        except ValueError:
            print("Input only accepts integers.")
