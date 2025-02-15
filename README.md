# 2D Platformer Game

A simple 2D platformer game built with Python and OpenGL where you navigate through floating platforms to collect keys while avoiding falling into water and enemies.

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
- **SPACE**: Jump (Map 1 only)
- **E**: Vine swing (Map 2 only)
- **F**: Toggle pause menu

## Game Mechanics

### Map 1: Water Platforms
- Player can move in all directions using WASD
- Jump with spacebar to reach higher platforms
- Player appears larger when jumping (closer to camera)
- Brown circular platforms float in the water
- Some platforms move vertically, others horizontally
- Stand on platforms AND move with them to avoid falling in water
- Red triangular enemies patrol vertically
- Contact with enemies deals 5 damage per second
- Enemies continue moving even when player is on platforms
- Strategic timing needed to avoid enemy contact
- Player starts with 100 health points
- Enemies reduce health by 5 HP/second on contact
- Health resets to 100 when losing a life
- Dying from enemy damage respawns player at left bank
- Yellow diamond-shaped keys are placed
- Collect all 3 keys to win
- Keys can be collected by touching them
- Blue water is deadly - instant death on contact
- Player respawns at left bank after death
- Three lives before game over
- Start with 3 lives
- Lose a life when touching water or losing all health
- Game over when all lives are lost
- Save/Load System
- Save your progress through the pause menu
- Load saved games from either main menu or pause menu
- Save files store:
  - Current lives and health
  - Keys collected
  - Platform positions
  - Enemy positions and states
  - Game progress
- Screens
1. **Main Menu**
   - Start new game
   - Load saved game
   - Quit
2. **Game Screen**
   - Shows lives remaining
   - Shows health bar
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

### Map 2: Jungle Vines
- Complete Map 1 to unlock Map 2
- Different mechanics and challenges from Map 1

#### Vine Swinging
- Press E to swing to nearest active leaf platform
- Can't jump in this map - rely on vine swinging
- Can only swing to active leaves
- Can't swing to the leaf you're currently on

#### Leaf Platforms
- 8 leaf platforms scattered across the map
- Leaves alternate between active and inactive states
- Active leaves rise slightly and can be swung to
- Inactive leaves lower and cannot be targeted
- Each leaf has its own timing for active/inactive cycle

#### Oxygen System
- Limited oxygen that depletes over 100 seconds
- Oxygen depletes regardless of being in or out of water
- Losing all oxygen costs one life
- No health damage from water (unlike Map 1)
- Still move slower in water

#### Victory Condition
- Collect 3 keys placed on specific leaf platforms
- Reach the right bank using the rightmost leaf
- Must time swings carefully with leaf activation cycles

## Objective
Collect all three keys and reach the right bank to win the game. Avoid falling into the water and enemies while using the platforms strategically to reach your goal.

## Tips
- Use platforms as safe zones
- Time your jumps carefully
- Watch enemy movement patterns
- Save frequently in challenging sections
- Watch platform movement patterns
- Collect keys in a strategic order
- Keep track of your health when near enemies

Map 2 Specific Tips:
- Watch leaf activation patterns
- Plan your route between active leaves
- Manage your oxygen timer
- Use the rightmost leaf to reach the bank
- Time your swings to match leaf activation