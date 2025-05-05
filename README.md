# Alien Invasion  
An Alien Invasion game with a built-in database, developed in Python using Pygame.

## Features

### 🎮 Gameplay Overview
- A simple Alien Invasion game that tracks your **score** and **current level** at the top of the screen.
- As the game progresses, the **aliens**, **ship**, and **bullets** all increase in speed.
- Before the game begins, your **current high score** is displayed.

### ❤️ Lives
- The player starts with **3 lives**, shown in the top-left corner.
- A life is lost if an alien reaches the bottom of the screen or collides with the ship.

### 🔐 Login Page
- The home screen includes a working **textbox**, along with **Sign In** and **Sign Up** buttons.
- Error messages are shown in specific cases, such as trying to sign up with an already-used username.

### 🗃️ Database
- User data is currently stored in a **JSON file** (to be upgraded to SQL).
- Each user’s **high score** is saved and restored upon logging in again.

## 🚀 Installation

_Work in Progress_

## ▶️ Usage

- On launch, you're greeted with a **username textbox** and **Sign In/Sign Up** buttons.
- Enter a username to play. If it's already taken (during sign-up), you'll see an error.
- After signing in, you’ll see the **Play button** at the center and your high score below it.
- Click **Play** to start the game!
- After losing all your lives, you’ll return to the main screen and your new high score will be displayed (if it's higher).
- Upon exit, your high score is saved and will appear next time you log in.
- If you exit mid-game after beating your high score, it still gets saved.

## ✅ To-Do List

1. Modify the display to work with different devices.
2. Refactor the button system into a single file:
   - A general `Button` class.
   - Subclasses for `PlayButton` and `LoginButton`.
3. Replace the JSON-based database with **MySQL** for better scalability and reliability.
   
