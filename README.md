# Chess Game (Pygame GUI)

A simple chess game built with **Pygame** and **python-chess**, featuring a graphical interface and a toggleable board view (white/black).

---

## 🧩 Features

- Interactive chessboard with legal move highlighting
- Flip the board view (`F` key) — background stays fixed while pieces rotate
- Move history navigation (left arrow key)
- Built using `pygame` and `python-chess`

---

## 🛠️ Setup

Clone the repository and install dependencies inside the `source` directory using **Pipenv**:

```bash
cd source
pipenv install -r requirements.txt
```

---

## ▶️ Run the Game

Once dependencies are installed, start the GUI by running:

```bash
pipenv run python main.py
```

---

## 🎮 Controls

| Key / Action | Description |
|---------------|-------------|
| **Left Click** | Select or move a piece |
| **F** | Flip board view |
| **← (Left Arrow)** | Go back one move in history |
| **Close Window** | Quit game |

---

## 📁 Structure

```
.
├── source/
│   ├── main.py
│   ├── gui.py
│   ├── chessgame.py
│   ├── requirements.txt
│   └── pictures/
│       ├── white_pawn.png
│       ├── black_queen.png
│       └── ... etc.
└── README.md
```

---

## 🧠 Notes

- The images for pieces must be located in `source/pictures/` as `white_pawn.png`, `black_king.png`, etc.
- The game uses `python-chess` for move validation and game logic.
- Works on Python 3.10+.

---

## 📜 License

MIT License — feel free to use and modify.
