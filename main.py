from ecosystem import *


def main():
    """
    The main function that simulates the simulation
    :return: None
    """
    size = int(input("Enter INTEGER, which is size of the river: "))
    bear_num = int(input("Enter INTEGER, the number of BEARS in the river: "))
    otter_num = int(input("Enter INTEGER, the number of OTTER in the river: "))
    fish_num = int(input("Enter INTEGER, the number of FISH in the river: "))
    sim = int(input("Enter INTEGER, the number of stages in a simulation: "))
    r = River(size, bear_num, otter_num, fish_num)
    for simulation in range(sim):
        print(f"Stage {simulation + 1}: ", end="")
        r.move()


if __name__ == '__main__':
    main()