from termcolor import colored

colours = {0: "magenta",
                        1: "blue",
                        2: "cyan",
                        3: "green",
                        4: "yellow",
                        5: "red",
                        }

print(colored("0:", colours[0]))
print(colored("0:", colours[1]))
print(colored("0:", colours[2]))
print(colored("0:", colours[3]))
print(colored("0:", colours[4]))
print(colored("0:", colours[5]) + colored("0:", colours[5]))
