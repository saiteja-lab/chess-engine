import React, { useState, useRef } from 'react';

const PIECES = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
};

const ChessBoard = ({ fen, onMove, disabled }) => {
    const [draggedFrom, setDraggedFrom] = useState(null);
    const [selectedSquare, setSelectedSquare] = useState(null);
    const [lastMove, setLastMove] = useState(null);
    const [hoveredSquare, setHoveredSquare] = useState(null);
    const boardRef = useRef(null);

    // Parse FEN
    const parseBoard = () => {
        const board = [];
        const rows = fen.split(' ')[0].split('/');
        for (let r = 0; r < 8; r++) {
            const row = rows[r];
            for (let i = 0; i < row.length; i++) {
                const char = row[i];
                if (!isNaN(char)) {
                    for (let k = 0; k < parseInt(char); k++) board.push(null);
                } else {
                    board.push(char);
                }
            }
        }
        return board;
    };

    const board = parseBoard();

    const squareToAlgebraic = (index) => {
        const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
        const ranks = ['8', '7', '6', '5', '4', '3', '2', '1'];
        return files[index % 8] + ranks[Math.floor(index / 8)];
    };

    const handleSquareClick = (index) => {
        if (disabled) return;

        const piece = board[index];

        if (selectedSquare === null) {
            // Only select if it's a white piece (user's piece)
            if (piece && piece === piece.toUpperCase()) {
                setSelectedSquare(index);
            }
        }
        else if (selectedSquare !== null) {
            if (index === selectedSquare) {
                setSelectedSquare(null);
            } else if (piece && piece === piece.toUpperCase()) {
                setSelectedSquare(index);
            } else {
                const from = squareToAlgebraic(selectedSquare);
                const to = squareToAlgebraic(index);
                setLastMove({ from: selectedSquare, to: index });
                onMove(from + to);
                setSelectedSquare(null);
            }
        }
    };

    const handleDragStart = (e, index) => {
        if (disabled) return;
        const piece = board[index];
        if (!piece || piece !== piece.toUpperCase()) {
            e.preventDefault();
            return;
        }

        setDraggedFrom(index);
        e.dataTransfer.effectAllowed = 'move';

        // Custom Drag Image
        const dragImage = document.createElement('div');
        dragImage.textContent = PIECES[piece];
        dragImage.style.fontSize = '48px';
        dragImage.style.color = '#fff';
        dragImage.style.textShadow = '0 0 5px #000';
        dragImage.style.position = 'absolute';
        dragImage.style.top = '-9999px';
        document.body.appendChild(dragImage);

        e.dataTransfer.setDragImage(dragImage, 25, 25);
        setTimeout(() => document.body.removeChild(dragImage), 0);
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
    };

    const handleDrop = (e, toIndex) => {
        e.preventDefault();
        if (disabled || draggedFrom === null) return;

        const from = squareToAlgebraic(draggedFrom);
        const to = squareToAlgebraic(toIndex);

        setLastMove({ from: draggedFrom, to: toIndex });
        onMove(from + to);
        setDraggedFrom(null);
    };

    const handleDragEnd = () => {
        setDraggedFrom(null);
    };

    const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
    const ranks = ['8', '7', '6', '5', '4', '3', '2', '1'];

    return (
        <div className="select-none">
            <div
                ref={boardRef}
                className="grid grid-cols-8 w-full max-w-[560px] aspect-square rounded-lg overflow-hidden ring-8 ring-surface-800/80 shadow-2xl"
            >
                {board.map((piece, index) => {
                    const row = Math.floor(index / 8);
                    const col = index % 8;
                    const isLight = (row + col) % 2 === 0;
                    const isSelected = selectedSquare === index;
                    const isDragSource = draggedFrom === index;
                    const isLastMoveSquare = lastMove && (lastMove.from === index || lastMove.to === index);

                    // Specific highlight colors
                    let bgColorClass = isLight ? 'bg-indigo-100' : 'bg-indigo-300 shadow-inner';

                    if (isLastMoveSquare) {
                        bgColorClass = isLight ? 'bg-amber-100' : 'bg-amber-200';
                    }
                    if (isSelected) {
                        bgColorClass = 'bg-emerald-200'; // High visibility for selection
                    }

                    return (
                        <div
                            key={index}
                            className={`
                                relative flex items-center justify-center
                                transition-colors duration-150
                                ${bgColorClass}
                            `}
                            onClick={() => handleSquareClick(index)}
                            onDragOver={handleDragOver}
                            onDrop={(e) => handleDrop(e, index)}
                        >
                            {/* Rank Number (Left side) */}
                            {col === 0 && (
                                <span className={`absolute top-1 left-1 text-[10px] sm:text-xs font-bold leading-none select-none
                                    ${isLight ? 'text-indigo-400' : 'text-indigo-100'}
                                `}>
                                    {ranks[row]}
                                </span>
                            )}

                            {/* File Letter (Bottom side) */}
                            {row === 7 && (
                                <span className={`absolute bottom-0.5 right-1 text-[10px] sm:text-xs font-bold leading-none select-none
                                    ${isLight ? 'text-indigo-400' : 'text-indigo-100'}
                                `}>
                                    {files[col]}
                                </span>
                            )}

                            {/* Piece */}
                            {piece && !isDragSource && (
                                <div
                                    draggable={!disabled && piece === piece.toUpperCase()}
                                    onDragStart={(e) => handleDragStart(e, index)}
                                    onDragEnd={handleDragEnd}
                                    className={`
                                        text-4xl sm:text-5xl lg:text-6xl cursor-grab active:cursor-grabbing z-10
                                        transition-transform duration-200
                                        ${piece === piece.toUpperCase() ? 'hover:scale-110' : ''}
                                    `}
                                    style={{
                                        color: piece === piece.toUpperCase() ? '#ffffff' : '#0f172a', /* White / Slate-900 */
                                        filter: piece === piece.toUpperCase()
                                            ? 'drop-shadow(0 2px 3px rgba(0,0,0,0.5))'
                                            : 'drop-shadow(0 2px 3px rgba(255,255,255,0.5))',
                                        textShadow: '0 4px 6px rgba(0,0,0,0.1)'
                                    }}
                                >
                                    {PIECES[piece]}
                                </div>
                            )}

                            {/* Hover Effect Marker (Circle) */}
                            {piece === null && !disabled && (
                                <div className="absolute w-3 h-3 rounded-full bg-black/10 opacity-0 hover:opacity-100 transition-opacity"></div>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default ChessBoard;
