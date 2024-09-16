# Conway's Game of Life Interactive Simulation

This project provides an interactive simulation of **Conway's Game of Life**, a well-known cellular automaton, implemented using Python, `matplotlib`, and `numpy`. It allows users to add initial conditions using predefined patterns (like a **Glider**, **Blinker**, or **Still Life Block**) or to manually click on cells to create custom patterns. Once the grid is set up, the simulation runs according to the rules of Conway's Game of Life.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [How to Run the Program](#how-to-run-the-program)
- [Predefined Patterns](#predefined-patterns)
- [Manual Grid Configuration](#manual-grid-configuration)
- [Game of Life Rules](#game-of-life-rules)
- [Boundary Conditions](#boundary-conditions)
- [How the Code Works](#how-the-code-works)
- [Acknowledgements](#acknowledgements)

## Introduction

Conway's Game of Life is a cellular automaton devised by mathematician John Horton Conway in 1970. It's a zero-player game, meaning that its evolution is determined by its initial state, with no further input required from players. The game takes place on an infinite grid of square cells, but in this implementation, the grid is finite.

Each cell in the grid can be in one of two states:
- Alive (represented by `1`).
- Dead (represented by `0`).

The game evolves based on the states of each cell and the number of live neighbors it has.

This project provides:
- An interactive grid where users can toggle cell states.
- Predefined buttons for adding **Glider**, **Blinker**, and **Still Life Block** patterns.
- A **Start** button to run the simulation after grid setup.
- Real-time visualization of the grid as it evolves according to Conway's rules.

## Installation

### Prerequisites
- Python 3.x
- Libraries:
  - `numpy`
  - `matplotlib`

### Install Required Packages
To install the required libraries, run the following command:

```bash
pip install numpy matplotlib
```

## How to Run the Program
1. Clone or Download the Repository to your local machine.
2. Navigate to the project directory in your terminal or command prompt.
3. Run the program using Python:

```bash
python  game_of_life.py
```
4. The program will launch a GUI window displaying the grid.
5. Interact with the grid by clicking on cells to toggle their states.
6. Use the predefined buttons to add patterns to the grid.
7. Click the **Start** button to begin the simulation.  

8. Observe the grid's evolution in real-time.

## Predefined Patterns
- **Glider**: A pattern that moves diagonally down and to the right.
```bash
Pattern:
  0 1 0
  0 0 1
  1 1 1
```

- **Blinker**: A pattern that oscillates between three states.
```bash
Pattern:
  Initial state (Horizontal):
  0 0 0
  1 1 1
  0 0 0

  Next state (Vertical):
  0 1 0
  0 1 0
  0 1 0
```
- **Still Life Block**: A static pattern that remains unchanged.
```bash
Pattern:
  1 1
  1 1
```

## Manual Grid Configuration

You can also manually configure the grid by clicking on individual cells. Each click toggles the cell between alive and dead. This allows you to create custom patterns for your own experiments.

## Game of Life Rules

Conway's Game of Life operates under the following simple rules:

1. Underpopulation: Any live cell with fewer than two live neighbors dies, as if caused by underpopulation.
2. Survival: Any live cell with two or three live neighbors lives on to the next generation.
3. Overpopulation: Any live cell with more than three live neighbors dies, as if by overpopulation.
4. Reproduction: Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

## Boundary Conditions

This implementation uses fixed boundary conditions. The grid edges do not wrap around, meaning that cells on the edges of the grid have fewer neighbors.

### Boundary Condition Types:
- **Fixed**: The grid edges do not wrap around. Cells on the edges have fewer neighbors.
    - For example, the top-left corner cell will only have 3 neighbors instead of 8.
- **No Periodic Boundary**: In this simulation, there is no wrapping from one edge to the opposite edge. Cells at the edges have fewer neighbors, and their behavior differs from cells in the center.

## How the code works

### 1. Initialisation 
The program initializes a grid of size 50x50 where each cell is set to `0` (dead). The user can either toggle the state of individual cells or use predefined patterns (Glider, Blinker, Block).

### 2. Interactive Grid
The grid is interactive, allowing users to:
- Toggle cell states between alive and dead by clicking on the grid.
- Insert predefined patterns using buttons.

### 3. Game Logic (Conway's Rules)
After setting up the grid, the user starts the simulation by clicking the Start button. The grid then evolves over time according to Conway’s rules, which are applied to each cell based on the number of live neighbors.

### 4. Animation

The simulation is animated using `matplotlib.animation`, and the grid is updated in real-time.

### 5. Termination

The simulation runs for a fixed number of steps (by default, 200). This number can be adjusted within the `animate` function.

## Acknowledgements 

This project was inspired by Conway's Game of Life and various open-source Python visualizations of cellular automata.

- **John Horton Conway** for devising the Game of Life.
- **Matplotlib** for the animation library.
