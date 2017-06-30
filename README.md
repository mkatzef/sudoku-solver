# sudoku-solver

A tool to help with (or outright solve) sudoku puzzles. Written in Python, with a Tkinter GUI.

## Getting Started

This project consists of a single module.
* `SudokuSolver.py` - A class for sudoku operations and a GUI to interact with it.

### Prerequisites

To run sudoku-solver, the host machine must have the following installed:
* `Python3` - The programming language in which sudoku-solver was written. Available [here](https://www.python.org/).
* `Tkinter` - The Python library required for the sudoku-solver user interface.\*

\*Included with the standard Python3 installation on Windows and MacOS, requires separate installation on Linux. For Debian-based systems, this is achieved through the following command:
`apt-get install python3-tk`

### Running

The tool may be started by running the script as follows:
`python3 SudokuSolver.py` 

This will open a window with a blank sudoku board and a group of options.

### Use

A sudoku puzzle may be given to sudoku-solver in two different ways:
* Typing the numbers of the sudoku puzzle in each corresponding cell.
* Typing a single string of 81 (9 \* 9) numbers in the import text box\*.

\* In these strings, empty cells are represented as `0`. The import and export features use the same simple format, allowing one to quickly revert to a previous version of the board.

With a sudoku puzzle entered in the solver, two major options are available:
* To solve the puzzle outright.
* To fill in all of the cells that only have one option, and display each cell's resulting options (suggestions).

These are respectively achieved through the "Solve" and "Iterate" buttons. At any time, the "Check" button will test if the entered board is valid and full. The "Advanced" button expands the options menu.

The expanded options menu allows the iteration suggestions to be disabled, and the sudoku solver to be fine tuned. "Path depth" refers to the number of cell decisions to be made based on the first decision. "Path number" refers to the number of times "path depth" may be reached before conceding. Increasing either variable (by slider or text box) increases the chance of solving the given puzzle, but also increases the run time for other puzzles.

## Authors

* **Marc Katzef** - [mkatzef](https://github.com/mkatzef)
