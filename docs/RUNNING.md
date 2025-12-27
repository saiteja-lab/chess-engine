# How to Run the Chess Engine - Complete Guide

This guide provides detailed step-by-step instructions for running the chess engine in different modes.

## Prerequisites

Before starting, ensure you have the following installed:
- **Python 3.8+** (Check: `python --version`)
- **Node.js 16+** (Check: `node -v`)
- **npm** (Check: `npm -v`)
- **pip** (Check: `pip --version`)

---

## Option 1: Play via Terminal CLI (Simplest)

This is the quickest way to test the engine - play directly in your terminal.

### Step 1: Navigate to the chess-engine directory
```bash
cd c:/Users/saite/Desktop/test/chess_eng/chess-engine
```

### Step 2: Install Python dependencies
```bash
pip install -r requirements.txt
```

This installs:
- `numpy` - For numerical operations
- `pytest` - For running tests
- `flask` and `flask-cors` - For the web API (not needed for CLI but installed anyway)

### Step 3: Run the CLI player
```bash
python ui/cli/play.py
```

### Step 4: Play the game
- The board will be displayed in text format
- You play as **White** (lowercase letters like 'p', 'r', etc.)
- The engine plays as **Black**
- Enter moves in UCI format: `e2e4` (from square to square)
  - First two characters: starting square (file + rank, e.g., 'e2')
  - Last two characters: destination square (e.g., 'e4')
- Type `quit` to exit

**Example moves:**
- `e2e4` - Move pawn from e2 to e4
- `g1f3` - Move knight from g1 to f3
- `e7e8q` - Promote pawn to queen

---

## Option 2: Play via Web Browser (Graphical UI)

This provides a beautiful graphical interface with a chessboard you can click.

### Part A: Start the API Server (Backend)

The Python engine needs to run as a server that the React app can talk to.

#### Step 1: Open a terminal/command prompt
Navigate to the chess-engine directory:
```bash
cd c:/Users/saite/Desktop/test/chess_eng/chess-engine
```

#### Step 2: Ensure dependencies are installed
```bash
pip install -r requirements.txt
```

#### Step 3: Start the Flask server
```bash
python ui/server.py
```

You should see output like:
```
 * Serving Flask app 'server'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

**Keep this terminal window open!** The server must keep running.

---

### Part B: Start the React Frontend

#### Step 1: Open a NEW terminal/command prompt
Keep the previous terminal running the server!

Navigate to the React app directory:
```bash
cd c:/Users/saite/Desktop/test/chess_eng/chess-engine/ui/react-app
```

#### Step 2: Install Node.js dependencies (first time only)
```bash
npm install
```

This may take a few minutes. It installs React, Vite, Tailwind CSS, and other packages.

#### Step 3: Start the development server
```bash
npm run dev
```

You should see output like:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

#### Step 4: Open your browser
Click the link or manually navigate to:
```
http://localhost:5173
```

#### Step 5: Play the game!
- Click on a piece to select it (square turns yellow)
- Click on a destination square to move
- The engine will automatically respond
- Click "New Game" to restart
- The status message shows whose turn it is and what the engine played

---

## Option 3: Use with UCI-Compatible Chess GUIs

The engine supports the Universal Chess Interface (UCI) protocol, allowing it to work with standard chess GUIs like Arena, Cutechess, or Lichess.

### Step 1: Navigate to the chess-engine directory
```bash
cd c:/Users/saite/Desktop/test/chess_eng/chess-engine
```

### Step 2: Run the UCI interface
```bash
python -m engine.uci
```

### Step 3: Configure your chess GUI
In your chess GUI software:
1. Add a new engine
2. Point it to: `python -m engine.uci` (or create a batch file that runs this command)
3. Set the working directory to: `c:/Users/saite/Desktop/test/chess_eng/chess-engine`

### Example UCI Commands (for manual testing):
```
uci
isready
position startpos moves e2e4
go depth 3
quit
```

---

## Troubleshooting

### Issue: "Module not found" errors
**Solution:** Make sure you've installed Python dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Cannot connect to engine" in web UI
**Solution:** 
1. Make sure the Flask server (`python ui/server.py`) is running in another terminal
2. Check that it's running on port 5000
3. Check for firewall issues

### Issue: React app won't start
**Solution:**
1. Delete `node_modules` folder and `package-lock.json`
2. Run `npm install` again
3. Try `npm run dev`

### Issue: Port already in use
**Solution:**
- Flask server (port 5000): Stop the other process or change the port in `ui/server.py`
- React app (port 5173): Vite will automatically try the next available port

### Issue: Moves are invalid
**Solution:**
- Make sure you're using correct UCI notation (e.g., `e2e4`, not `e4`)
- The move must be legal - check the available moves in the CLI if needed

---

## Running Tests

To verify everything is working correctly:

```bash
cd c:/Users/saite/Desktop/test/chess_eng/chess-engine
python -m pytest engine/tests/
```

You should see output like:
```
=========== test session starts ===========
collected 3 items

engine/tests/test_moves.py ...         [100%]

=========== 3 passed in 0.XX s ===========
```

---

## Performance Tips

- The engine searches to **depth 3** by default (can see 3 moves ahead)
- To make it stronger (slower), edit `ui/server.py` and change:
  ```python
  best_move = search(board, 3, 2.0)  # Change 3 to 4 or 5
  ```
- To make it faster (weaker), reduce the depth to 2

---

## Quick Reference: File Structure

```
chess-engine/
├── engine/              # Core chess engine
│   ├── board.py        # Board representation & move generation
│   ├── move.py         # Move class
│   ├── search.py       # Alpha-beta search
│   ├── eval.py         # Position evaluation
│   └── uci.py          # UCI protocol
├── ui/
│   ├── cli/
│   │   └── play.py     # Terminal-based game
│   ├── server.py       # Flask API server
│   └── react-app/      # React frontend
└── requirements.txt    # Python dependencies
```

---

## Summary of Commands

**CLI Mode:**
```bash
cd c:/Users/saite/Desktop/test/chess_eng/chess-engine
pip install -r requirements.txt
python ui/cli/play.py
```

**Web UI Mode (2 terminals needed):**

Terminal 1 (Backend):
```bash
cd c:/Users/saite/Desktop/test/chess_eng/chess-engine
python ui/server.py
```

Terminal 2 (Frontend):
```bash
cd c:/Users/saite/Desktop/test/chess_eng/chess-engine/ui/react-app
npm install  # First time only
npm run dev
```

Then open `http://localhost:5173` in your browser.

---

Enjoy playing chess! 🎯♟️
