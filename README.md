# 🐮 AI eating grass

This simulation is a simplified representation of the life of a virtual cow that feeds on grass. The goal is to demonstrate how an AI can interact with its environment to survive and reproduce.

![Simulation Animation](gif.gif)

## Simulation Rules

1. A virtual cow 🐮 is present on the screen, starting with an energy level of 2 units.
2. Grass 🌿 appears randomly adjacent to other tufts of grass.
3. The cow gains 2 units of energy by eating grass.
4. The cow dies if it runs out of energy.
5. The cow can reproduce if it has more than 2 units of energy, creating a new cow.
6. At each iteration, the cow loses 1 unit of energy.

## Controls

- Press "P" to pause the simulation.
- Press "N" to regenerate a new simulation with fresh cows and grass.

## Prerequisites

Before running the project, make sure you have the following dependencies installed:

- Python
- Necessary Python libraries (you can install them using `pip`):
  - [Pygame](https://www.pygame.org/)

## Running the Project

1. Clone this repository to your computer:

   ```bash
   git clone https://github.com/corederu/ai-eating-grass.git

2. run `main.py`

   ```bash
   python3 main.py
   ```