import React, { useState, useEffect } from 'react';
import ChessBoard from './components/Board';

function App() {
  const [fen, setFen] = useState("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");
  const [gameStatus, setGameStatus] = useState("ready");
  const [statusMessage, setStatusMessage] = useState("Click 'New Game' to start!");
  const [moveHistory, setMoveHistory] = useState([]);
  const [thinking, setThinking] = useState(false);
  const [gameOver, setGameOver] = useState(false);

  const API_URL = "http://localhost:5000/api";

  const startNewGame = async () => {
    setThinking(true);
    setGameOver(false);
    setMoveHistory([]);
    setGameStatus("loading");
    setStatusMessage("Starting new game...");

    try {
      const res = await fetch(`${API_URL}/new_game`, { method: 'POST' });
      const data = await res.json();
      setFen(data.fen);
      setGameStatus("playing");
      setStatusMessage("Your move! Drag a piece or click to select.");
    } catch (e) {
      console.error(e);
      setGameStatus("error");
      setStatusMessage("Cannot connect to engine. Is server.py running?");
    }
    setThinking(false);
  };

  const handleMove = async (moveStr) => {
    if (thinking || gameOver || gameStatus !== "playing") return;

    setThinking(true);
    setStatusMessage("Processing move...");

    try {
      const res = await fetch(`${API_URL}/move`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ move: moveStr })
      });
      const data = await res.json();

      if (data.error) {
        setStatusMessage(`⚠️ Illegal move! Try again.`);
        setThinking(false);
        return;
      }

      setMoveHistory(prev => [...prev, {
        number: Math.floor(prev.length / 2) + 1,
        white: moveStr,
        black: data.engine_move || null
      }]);
      setFen(data.fen);

      if (data.game_over) {
        setGameStatus("finished");
        setStatusMessage("🎉 Victory! You won the game!");
        setGameOver(true);
        setThinking(false);
        return;
      }

      setStatusMessage("🤖 Engine is thinking...");

      setTimeout(() => {
        if (data.engine_move) {
          setStatusMessage("✅ Your turn!");
        } else {
          setGameStatus("finished");
          setStatusMessage("Game Over!");
          setGameOver(true);
        }
        setThinking(false);
      }, 500);

    } catch (e) {
      console.error(e);
      setStatusMessage("❌ Connection error!");
      setThinking(false);
    }
  };

  useEffect(() => {
    startNewGame();
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center p-4 lg:p-8 relative overflow-hidden">
      {/* Decorative background elements */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary-500/20 rounded-full blur-[120px] pointer-events-none animate-pulse-slow"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-secondary-500/20 rounded-full blur-[120px] pointer-events-none animate-pulse-slow" style={{ animationDelay: '1.5s' }}></div>

      <div className="w-full relative z-10 flex flex-col xl:flex-row gap-8 items-start justify-center animate-fade-in">

        {/* Left Panel: Controls & Info */}
        <section className="w-full max-w-md xl:w-80 flex-shrink-0 space-y-6 mx-auto xl:mx-0">
          <div className="glass-panel rounded-3xl p-8 text-center border-t border-white/60">
            <div className="mb-2 inline-block px-3 py-1 rounded-full bg-indigo-50 text-indigo-600 text-xs font-bold tracking-widest uppercase">
              Grandmaster AI
            </div>
            <h1 className="text-5xl font-extrabold text-surface-900 tracking-tight font-display bg-clip-text text-transparent bg-gradient-to-br from-slate-900 to-slate-600">
              Chess
            </h1>
          </div>

          <div className="glass-panel rounded-3xl p-6 space-y-4">
            <div className="flex items-center justify-between mb-2">
              <h2 className="text-xl font-bold text-surface-800 font-display">Status</h2>
              <div className={`flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium ${thinking ? 'bg-amber-100 text-amber-700' :
                gameStatus === 'playing' ? 'bg-emerald-100 text-emerald-700' :
                  'bg-slate-100 text-slate-600'
                }`}>
                <span className={`w-2 h-2 rounded-full ${thinking ? 'bg-amber-500 animate-pulse' :
                  gameStatus === 'playing' ? 'bg-emerald-500' :
                    'bg-slate-400'
                  }`}></span>
                {thinking ? 'Thinking...' : gameStatus === 'playing' ? 'Active' : 'Idle'}
              </div>
            </div>

            <div className="bg-white/50 rounded-xl p-4 border border-white/40 min-h-[80px] flex items-center justify-center text-center">
              <p className="text-surface-700 font-medium leading-relaxed">
                {statusMessage}
              </p>
            </div>

            <button
              onClick={startNewGame}
              disabled={thinking}
              className="w-full py-4 bg-surface-900 text-white font-bold text-lg rounded-xl
                       hover:bg-indigo-600 transition-all transform hover:-translate-y-1 active:translate-y-0
                       disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none
                       shadow-xl shadow-slate-900/10 hover:shadow-indigo-500/25 flex items-center justify-center gap-2"
            >
              {thinking ? (
                <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
              ) : (
                <>
                  <span>New Game</span>
                </>
              )}
            </button>
          </div>

          <div className="glass-panel rounded-3xl p-6">
            <h3 className="text-sm font-bold text-surface-400 uppercase tracking-wider mb-4">Instructions</h3>
            <ul className="space-y-3 text-sm font-medium text-surface-600">
              <li className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center text-lg">🖱️</div>
                <span>Drag & Drop to move</span>
              </li>
              <li className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center text-lg">💡</div>
                <span>Highlights show valid moves</span>
              </li>
            </ul>
          </div>
        </section>

        {/* Center Panel: Board */}
        <section className="flex-1 flex justify-center items-start lg:pt-8 w-full min-w-[300px]">
          <div className="relative">
            <div className="absolute inset-0 bg-indigo-500/5 blur-3xl transform scale-110 -z-10 rounded-full"></div>
            <div className="glass-panel p-4 rounded-2xl shadow-2xl shadow-indigo-900/10 transition-all duration-500 hover:shadow-indigo-900/20">
              <ChessBoard
                fen={fen}
                onMove={handleMove}
                disabled={thinking || gameOver || gameStatus !== 'playing'}
              />
            </div>
          </div>
        </section>

        {/* Right Panel: History */}
        <section className="w-full max-w-md xl:w-80 flex-shrink-0 h-[600px] lg:h-[800px] glass-panel rounded-3xl overflow-hidden flex flex-col mx-auto xl:mx-0">
          <div className="p-6 border-b border-white/50 bg-white/30 backdrop-blur-md sticky top-0 z-10 flex justify-between items-center">
            <h2 className="text-xl font-bold text-surface-800 font-display">History</h2>
            <span className="bg-white/50 px-3 py-1 rounded-full text-xs font-bold text-surface-500 border border-white/50">
              {moveHistory.length} Moves
            </span>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-2 custom-scrollbar-light scroll-smooth">
            {moveHistory.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-surface-400 opacity-60">
                <div className="text-4xl mb-2">📜</div>
                <p>No moves recorded</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 gap-2">
                {moveHistory.map((move, i) => (
                  <div key={i} className="flex text-sm animate-slide-up" style={{ animationDelay: `${i * 50}ms` }}>
                    <div className="w-10 py-3 text-surface-400 font-mono text-xs flex items-center justify-center">{move.number}.</div>
                    <div className="flex-1 flex gap-2">
                      <div className="flex-1 bg-white/60 rounded-lg py-2 px-3 font-medium text-surface-700 shadow-sm border border-transparent hover:border-indigo-100 transition-colors">
                        {move.white}
                      </div>
                      {move.black && (
                        <div className="flex-1 bg-surface-100/50 rounded-lg py-2 px-3 font-medium text-surface-700 shadow-inner border border-transparent">
                          {move.black}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>
      </div>
    </div>
  );
}

export default App;
