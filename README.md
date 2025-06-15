# Arena Blitz

A collection of mini-games built with Pygame, organized in a unified game launcher.

## Games

- **Cyber Ninja Assault**: A fast-paced ninja action game set in a futuristic world.
- **Shadow Ops**: A tactical stealth game with strategic gameplay elements.

## Project Structure

The project follows a modular structure:

```
arena-blitz/
├── launcher.py           # Main entry point
├── assets/               # Shared resources
├── games/                # Individual games
│   ├── cyber_ninja_assault/  # Cyber Ninja Assault game
│   ├── shadow_ops/       # Shadow Ops game
│   └── ...               # Other games
├── common/               # Shared code
└── README.md             # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.6+
- Pygame

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/Md-Zubair677/arena-blitz.git
   cd arena-blitz
   ```

2. Install dependencies:
   ```
   pip install pygame
   ```

3. Run the launcher:
   ```
   python launcher.py
   ```

## Controls

### Launcher
- Use the mouse to select a game
- ESC to quit

### Cyber Ninja Assault
- WASD: Movement
- Space: Jump/Double jump
- Shift: Dash/Slide
- Mouse: Aim
- Left Click: Attack
- Right Click: Special ability
- E: Interact
- Q: Switch weapons
- ESC: Return to launcher

### Shadow Ops
- WASD: Movement
- Space: Interact/Action
- Shift: Stealth mode
- E: Use equipment
- Q: Switch equipment
- ESC: Return to launcher

## Development

To add a new game:

1. Create a new directory under `games/`
2. Implement the game with a `main.py` file that contains a `run()` function
3. Add the game to the list in `launcher.py`

## License

This project is licensed under the MIT License - see the LICENSE file for details.
