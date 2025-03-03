# Space Heist

A 3D space exploration game created with OpenGL and Python.

## Game Overview

Space Heist is a thrilling first-person space navigation game where you pilot a spacecraft through a solar system. Your mission is to navigate to a designated space station while defending yourself against hostile pirate ships. Master the controls of your ship in a physics-based 3D environment and use your weapons to neutralize threats.

## Controls

### Ship Movement

- **W/S**: Pitch up/down
- **A/D**: Yaw left/right
- **Q/E**: Roll clockwise/counterclockwise
- **SPACE**: Thrust forward in the direction the ship is facing

### Camera Control

- **LSHIFT**: Toggle between third-person and first-person view
- **Mouse Movement**: When in first-person mode, look around in any direction
- **Left Click**: When in first-person mode, shoot lasers to destroy pirate ships

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

### Combat System

- Red pirate ships constantly pursue your vessel
- Destroy pirate ships by hitting them with your lasers
- If a pirate ship collides with your vessel, it's destroyed but damages your health
- Monitor your health bar in the top-left corner of the screen
- Game ends if your health reaches zero

### Camera

- Third-person camera follows behind your ship
- Camera adapts to ship orientation, giving you a clear view of where you're heading
- First-person camera positions you on top of the ship with a crosshair for aiming
- Lasers can be fired in first-person mode using left-click

### Weapons

- Red laser beams can be fired in first-person mode
- Lasers travel in the direction you're facing
- Use the crosshair in the center of the screen to aim
- Lasers disappear after a few seconds
- One hit from a laser will destroy a pirate ship

## Objectives

1. Start a new game from the main menu
2. Locate the green space station (your destination)
3. Navigate to the destination using the direction indicator
4. Defend yourself against pirate ships along the way
5. Successfully dock with the space station to complete the mission
6. Return to the main menu to play again

## Game Environment

- **Planets**: Large celestial bodies with gravity (visual only)
- **Space Stations**: Orbital installations, one of which is your destination
- **Your Ship**: A maneuverable spacecraft with full 3D control
- **Lasers**: Projectiles that can be fired in first-person mode
- **Pirate Ships**: Hostile spacecraft that pursue you and attempt to damage your ship

## Technical Features

- Built using Python with OpenGL for 3D rendering
- Custom shader-based rendering pipeline
- ImGui-based user interface for menus and HUD elements
- 3D model loading from OBJ files
- Collision detection for combat and mission completion
- Enemy AI for pirate ships that pursue the player
- Health system with visual health bar
- First-person camera with mouse look controls
- Crosshair HUD and projectile system

## Tips for New Players

- Take time to get familiar with the controls before attempting high-speed maneuvers
- Switch to first-person mode for better accuracy when engaging pirate ships
- Keep moving to avoid pirate ships while aiming for your destination
- Use short bursts of thrust rather than continuous acceleration for precise control
- Keep an eye on the distance indicator to gauge how close you are to your target
- The direction indicator points to your destination in world-space, not relative to your ship's orientation
- Switch to first-person mode for a more immersive experience and to shoot lasers
- The crosshair helps aim your lasers in first-person mode
- Monitor your health - if it reaches zero, your mission fails

## Development

This game was developed as part of a computer graphics project, demonstrating various 3D rendering techniques, physics simulations, and game development principles.

---

Enjoy your space adventure!
