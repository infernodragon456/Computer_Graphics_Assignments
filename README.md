# Space Heist

A 3D space exploration game created with OpenGL and Python.

## Game Overview

Space Heist is a thrilling first-person space navigation game where you pilot a spacecraft through a solar system. Your mission is to navigate to a designated space station while mastering the controls of your ship in a physics-based 3D environment.

## Controls

### Ship Movement

- **W/S**: Pitch up/down
- **A/D**: Yaw left/right
- **Q/E**: Roll clockwise/counterclockwise
- **SPACE**: Thrust forward in the direction the ship is facing

### Other Controls

- **1**: Start a new game from the main menu
- **2**: Exit the game from the main menu
- **4**: To go to the main menu from YOU WON or GAME OVER screens

## Gameplay Mechanics

### Physics System

- The ship has realistic momentum and inertia
- Velocity-based movement with gradual acceleration and deceleration
- Drag effect slows the ship when not actively thrusting
- Frame-rate independent physics ensure consistent gameplay regardless of hardware

### Navigation

- A red arrow in the bottom-right corner acts as a compass, pointing toward your destination
- Distance to the destination is displayed below the arrow
- The green-colored space station is your destination

### Camera

- Third-person camera follows behind your ship
- Camera adapts to ship orientation, giving you a clear view of where you're heading

## Objectives

1. Start a new game from the main menu
2. Locate the green space station (your destination)
3. Navigate to the destination using the direction indicator
4. Successfully dock with the space station to complete the mission
5. Return to the main menu to play again

## Game Environment

- **Planets**: Large celestial bodies with gravity (visual only)
- **Space Stations**: Orbital installations, one of which is your destination
- **Your Ship**: A maneuverable spacecraft with full 3D control

## Technical Features

- Built using Python with OpenGL for 3D rendering
- Custom shader-based rendering pipeline
- ImGui-based user interface for menus and HUD elements
- 3D model loading from OBJ files
- Collision detection for mission completion

## Tips for New Players

- Take time to get familiar with the controls before attempting high-speed maneuvers
- Use short bursts of thrust rather than continuous acceleration for precise control
- Keep an eye on the distance indicator to gauge how close you are to your target
- The direction indicator points to your destination in world-space, not relative to your ship's orientation

## Development

This game was developed as part of a computer graphics project, demonstrating various 3D rendering techniques, physics simulations, and game development principles.

---

Enjoy your space adventure!
