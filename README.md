# Ronny Rubbish Maze Problem

## Description
The Ronny Rubbish Maze Problem is a Python program that solves a maze-like problem of collecting rubbish nodes and disposing of them in designated rooms. The program uses the A* search algorithm to find the optimal path for collecting the rubbish nodes while considering the capacity and volume constraints of the rubbish bin.

The program consists of two main files:

1. AssignmentFinal.py: This file contains the implementation of the A* search algorithm, the main logic for navigating the maze and the execution of the program.

2. gui.py: This file contains the GUI implementation using the Tkinter library. It visualizes the hexagonal grid and animates the movement of the rubbish collector along the optimal path.

Different configurations files: 

1. NewConfiguration.py: This file contains the implementation of the A* search algorithm with different configurations.

2. NewConfigurationGUI.py: This file contains the GUI implementation for different configurations to visualize the hexagonal grid and animates the movement of the rubbish collector along the optimal path.

## Installation
To run the program, follow these steps:

1. Put the both python script files AssignmentFinal.py and gui.py in the same folder.

2. Run AssignmentFinal.py script.

## Usage
Upon running the program, it will solve the Ronny Rubbish Maze Problem and display the optimal path for collecting the rubbish nodes. The GUI window will open, showing the hexagonal grid and animating the movement of the rubbish collector along the path.

The program will print the current node and the collected rubbish information as it progresses through the maze. Once all the rubbish nodes have been cleared, the program will display the final path and the total cost of the path.