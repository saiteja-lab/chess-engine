# Architecture

## Engine (`engine/`)
- **board.py**: 1D array (64 squares) representation. Generates pseudo-legal moves and filters for legality.
- **search.py**: Iterative deepening with Alpha-Beta pruning.
- **eval.py**: Material + Piece-Square Tables.
- **uci.py**: UCI protocol adapter.

## UI (`ui/`)
- **react-app/**: Vite + React + Tailwind frontend.
- **server.py**: Flask API to bridge React and Python engine.
