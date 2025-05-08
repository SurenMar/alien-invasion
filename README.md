# Alien Invasion  
An Alien Invasion game with a built-in database, developed in Python using Pygame.

<img width="500" alt="ainv_game screenshot" src="https://github.com/user-attachments/assets/e6dc3ccb-0412-4370-b62f-1c79d885042c" />

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

## 🚀 Installation (via Bash)

### 🖥️ For Mac Users Only:
   1. Download the file `install.sh` into a folder where you like the game to be.
   2. Make the script executable: `chmod +x install.sh`.
   3. Run the file: `./install.sh`.
   4. If you are missing any required programs, the script will notify you. Download these programs and re-run `install.sh`.
   5. Follow the steps provided once the script finishes.
   6. To play again, go into the `alien-invasion` directory and run: `./run.sh`.
   7. Do **NOT** run `install.sh` again, otherwise it will download a new copy alien_invasion.

### 🌍 For All Users (Including Mac):
   1. Download a ZIP file of **alien_invasion**.
   2. Unzip the file.
   3. The game files will be in a folder called `alien-invasion-main`.
   4. Go into this file and ensure you have python and pip installed (installation steps vary depending on OS).
   5. Install the required library, **pygame**, via pip (installation steps vary depending on OS).
   6. Make `run.sh` executable: `chmod +x run.sh`.
   7. Play the game: `./run.sh`
      

## ▶️ Usage

- On launch, you're greeted with a **username textbox** and **Sign In/Sign Up** buttons.
- Enter a username to play. If it's already taken (during sign-up), you'll see an error.
- After signing in, you’ll see the **Play button** at the center and your high score below it.
- Click **Play** to start the game!
- After losing all your lives, you’ll return to the main screen and your new high score will be displayed (if it's higher).
- Whenever you wish to exit, simply press the `q` key on your keyboard
- Upon exit, your high score is saved and will appear next time you log in.
- If you exit mid-game after beating your high score, it still gets saved.

## ✅ To-Do List

1. Replace the JSON-based database with **MySQL** for better scalability and reliability.
   
