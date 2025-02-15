# 2D Platformer Game

A simple 2D platformer game built with Python and OpenGL where you navigate through floating platforms to collect keys while avoiding falling into water.

## Installation

1. Ensure you have Python 3.x installed
2. Install required dependencies:

```bash
pip install glfw
pip install imgui
pip install numpy
```

## How to Run

1. Clone the repository
2. Navigate to the game directory
3. Run the main file:

```bash
python main.py
```

## Game Controls

- **A/D**: Move left/right
- **W/S**: Move up/down
- **SPACE**: Jump
- **F**: Toggle pause menu

## Game Mechanics

### Basic Movement
- Player can move in all directions using WASD
- Jump with spacebar to reach higher platforms
- Player appears larger when jumping (closer to camera)

### Platforms
- Brown circular platforms float in the water
- Some platforms move vertically, others horizontally
- Stand on platforms to avoid falling in water

### Keys
- Yellow diamond-shaped keys are placed
- Collect all 3 keys to win
- Keys can be collected by touching them

### Water Hazard
- Blue water is deadly - instant death on contact
- Player respawns at left bank after death
- Three lives before game over

### Lives System
- Start with 3 lives
- Lose a life when touching water
- Game over when all lives are lost

### Save/Load System
- Save your progress through the pause menu
- Load saved games from either main menu or pause menu
- Save files store:
  - Current lives and health
  - Keys collected
  - Platform positions
  - Game progress

### Screens
1. **Main Menu**
   - Start new game
   - Load saved game
   - Quit

2. **Game Screen**
   - Shows lives remaining
   - Shows keys collected
   - Shows elapsed time

3. **Pause Menu (Press F)**
   - Save game
   - Load game
   - Return to main menu
   - Resume game

4. **Game Over Screen**
   - Shows time survived
   - Option to try again
   - Return to main menu
   - Quit game

## Objective
Collect all three keys and reach the right bank to win the game. Avoid falling into the water and use the platforms strategically to reach your goal.

## Tips
- Use platforms as safe zones
- Time your jumps carefully
- Save frequently in challenging sections
- Watch platform movement patterns
- Collect keys in a strategic order