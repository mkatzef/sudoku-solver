""" A module designed to either; help solve a sudoku puzzle by carrying out the
    steps that require little thought (use the iterate button for this), or 
    solve the puzzle outright (use the solve button for this).
    Author: Marc Katzef
    Date: 28/12/2015
"""

from tkinter import *
from tkinter.ttk import *
import time

STANDARD = frozenset([str(number) for number in range(1, 10)])

class Sudoku_engine:
    """Holds the variables for; the current board, the possible suggestions, and
    the status of the solution, along with the functions used to get closer to
    a solution."""
    def __init__(self):
        self.current_board = '0' * 81
        self.suggestions = {}
        self.suggestion_lengths = []
        self.status_var = ""
        self.time_taken = 0
     
        
    def iterate(self, suggestions_flag, *others):
        """Figures out which digits are possible for each box. If only one is,
        this character is included in the next board string. If more than one
        character is, the sorted list is added to a list of lists (and the 
        length of the sorted list is added to a list of lengths, which is used 
        to find a more direct path to a solution)"""
        rows, columns, blocks = self.board_parser(self.current_board)
        
        if suggestions_flag:
            suggestion_marker = '_'
        else:
            suggestion_marker = '0' 
            
        self.suggestion_lengths = []
        iterated_string = ''
        for index in range(81):
            digit = self.current_board[index]
            if digit == '0' or digit == '_': #if empty square
                column = index % 9
                row = index // 9
                if row <= 2:
                    block = column // 3
                elif row <= 5:
                    block = 3 + column // 3
                elif row <= 8:
                    block = 6 + column // 3
                    
                taken_digits = set(rows[row] + columns[column] + blocks[block]) 
                remaining_digits = sorted(list(STANDARD - taken_digits))
                
                if len(remaining_digits) == 0:
                    iterated_string += '0'
                    suggestion_length = 11 #can't continue with this board
                elif len(remaining_digits) == 1:
                    iterated_string += remaining_digits[0]
                    suggestion_length = 10 #might be able to continue with this board, but not with this square
                else:
                    iterated_string += suggestion_marker #indicates suggestions exist for this square depending on suggestions_flag
                    suggestion_length = len(remaining_digits)
            else:
                remaining_digits = [0]
                iterated_string += digit
                suggestion_length = 10
                
            self.suggestions[index] = remaining_digits[:]
            self.suggestion_lengths.append(suggestion_length)

        self.current_board = iterated_string
        
            
    def check_complete(self, *others):
        """Tests if every row, column, and block obeys the rules as a completed 
        sudoku board. Updates the status label to inform the user of its 
        findings, and returns true/false depending or complete/not complete"""
        rows, columns, blocks = self.board_parser(self.current_board)
        every_combination = rows + columns + blocks
        
        check_flag = True
        for combination in every_combination:
            if set(combination) != STANDARD:
                check_flag = False

        if check_flag:
            message = 'Completed Board' #if altered, update display_solution with new marker
        else:
            message = 'Incomplete Board'
        
        self.status_var = message
        return check_flag
    
    
    def solve(self, path_depth=150, path_number=5, *others):
        """Solves a sudoku by finding the squares with the fewest possible
        available choices for the current board, choosing the first option, then
        analysing the resulting board. Decisions are built upon until the board
        becomes unsolvable. In which case, the most recent choice gets made
        (differently) and the exploration continues. If no more options exist
        for a board, the previous working board is brought back, and the
        remaining suggestions are tested. In most cases (where the board is not
        solved immediately) the choices made will be a series of choices between
        only two options.
        Should solve any valid board (quite quickly)."""
        start = time.time()
        given_board_copy = self.current_board
        
        if not self.check_ok():
            self.status_var = "Repeated Values"
            return
            
        self.get_furthest()
        if not(self.check_complete()):
            step_boards = [self.current_board] #list to store boards 
            min_suggestion_number = min(self.suggestion_lengths)
            min_suggestion_index = self.suggestion_lengths.index(min_suggestion_number)
            first_branch = (min_suggestion_index, self.suggestions[min_suggestion_index]) #2-tuple for the square index and its suggestions
            decision_tree = [first_branch] #list of branches

        run = 1
        trial = 1
        
        while not(self.check_complete()) and trial <= path_number:
            run += 1
            if run > path_depth: #most likely only met if a bad choice is made
                trial += 1 #increase trial count
                run = 0 #reset run count
                index = 0
                while len(decision_tree[index][1]) == 0: #find earliest choice set of size greater than one
                    index += 1
                step_boards = step_boards[:index + 1] #shorten the lists to this choice
                decision_tree = decision_tree[:index + 1]
                self.current_board = step_boards[-1]
                self.iterate(False) #update suggestions and continue with from this point again
            
            if 11 in self.suggestion_lengths: #if there's a square with no suggestions
                if len(step_boards) == 1: #if this is the only board
                    break
                self.current_board = step_boards[-1] #take on the previous board, this time choosing the next suggestion
                
            if step_boards[-1] != self.current_board: #if a new board is introduced, find its suggestions
                step_boards.append(self.current_board)
                min_suggestion_number = min(self.suggestion_lengths)
                min_suggestion_index = self.suggestion_lengths.index(min_suggestion_number)
                new_branch = (min_suggestion_index, self.suggestions[min_suggestion_index])
                decision_tree.append(new_branch)
            
            next_change_index, change_list = decision_tree[-1]
            if len(change_list) != 0:
                new_digit = change_list.pop(0) #take the next value for this square out from the suggestions
                self.update(next_change_index, str(new_digit))
                self.get_furthest()
            elif len(step_boards) == 1:
                break
            else:                      
                step_boards.pop()
                decision_tree.pop()
                self.current_board = step_boards[-1]
                self.iterate(False) #update suggestions (used instead of get_furthest as this should have already been performed)
                
        if not self.check_complete():
            self.current_board = given_board_copy
            self.status_var = "No Solution Found, Try The Advanced Options"
            
        end = time.time()
        self.time_taken = end - start


    def get_furthest(self):
        """Performs the iteration step until no more progress is made"""
        current_state = self.current_board
        self.iterate(False)
        while current_state != self.current_board:
            current_state = self.current_board
            self.iterate(False)


    def update(self, entry_box, entry_value):
        """Updates the sudoku board string with the new character, or a
        placeholder ('0') if input is invalid"""
        if not(entry_value.isdigit() and int(entry_value) in range(1, 10)):
            entry_value = '0'

        new_state = self.current_board[:entry_box] + entry_value
        if entry_box < 81:
            new_state += self.current_board[entry_box + 1:]
        self.current_board = new_state    


    def board_parser(self, the_board):
        """Returns 3 lists of 9 lists of 9 digits. One list for rows (from top to 
        bottom), one for columns, from left to right, and one for blocks (from top 
        left to bottom right)"""
        rows = []
        for i in range(9):
            row = []
            for j in range(9):
                row.append(the_board[9 * i + j])
            rows.append(row)
            
        columns = []
        for i in range(9):
            column = []
            for j in range(9):
                column.append(the_board[i + 9 * j])
            columns.append(column)
            
        blocks = []
        for i in range(3):
            for j in range(3):
                block = []
                for k in range(3):
                    for l in range(3):
                        block.append(the_board[27 * i + 3 * j + 9 * k + l])
                blocks.append(block)
    
        return (rows, columns, blocks)


    def check_ok(self):
        """Ensures that the entered board is not obviously un-solvable"""
        rows, columns, blocks = self.board_parser(self.current_board)
        every_combination = rows + columns + blocks
        
        all_ok = True
        for item in every_combination:
            non_zero_values = [digit for digit in item if digit != '0' and digit != '_']
            if len(set(non_zero_values)) < len(non_zero_values): #if there are duplicate digits
                all_ok = False
                self.status_var = "Invalid Board"
        
        return all_ok    
            

class Gui:
    """Builds the sudoku assistant gui in a given window/frame"""
    
    def __init__(self, window):
        """Initializes the variables for; the board, board import/export, board
        status, and suggestion preferences. Sets a title and frame for each 
        component then calls relevant Sudoku_engine functions to produce content
        for each frame."""
        self.window = window
        self.sudoku = Sudoku_engine()
        self.import_var = StringVar()
        self.export_var = StringVar()
        self.status_var = StringVar()
        self.status_var.set("In Progress")
        self.suggestions_flag = IntVar()
        self.suggestions_flag.set(1)
        self.advanced_flag = IntVar()
        self.advanced_flag.set(0)
        self.path_number_s = DoubleVar()
        self.path_number_s.set(5)        
        self.path_number_e = DoubleVar()
        self.path_number_e.set(5)        
        self.path_depth_s = DoubleVar()
        self.path_depth_s.set(150)
        self.path_depth_e = DoubleVar()
        self.path_depth_e.set(150)
        self.full_width = 1     
        
        import_frame = Frame(window)
        import_frame.grid(row=12, column=0, columnspan=self.full_width)
        self.import_components(import_frame)

        self.board_frame = Frame(self.window)
        self.board_frame.grid(row=0, column=0, columnspan=self.full_width)
        
        #self.placeholder_frame()
        #self.clean_board()
        self.squares = self.initial_board(self.board_frame)

        export_frame = Frame(window)
        export_frame.grid(row=13, column=0, columnspan=self.full_width)
        self.export_components(export_frame)
        
        options_frame = Frame(window, height=50)
        options_frame.grid(row=14, column=0, columnspan=self.full_width, sticky=W+E)
        self.options(options_frame)

      
    def advanced(self, *args):
        if not(self.advanced_flag.get()):
            self.advanced_flag.set(1)
            self.advanced_frame = Frame(self.window, height=80)
            self.advanced_frame.grid(row=15, column=0, columnspan=self.full_width, sticky=W+E)
            suggestions_toggle = Checkbutton(self.advanced_frame, text='Iteration Suggestions', variable=self.suggestions_flag)
            suggestions_toggle.place(relx=0.5, rely=0.2, anchor='c')
            
            run_label = Label(self.advanced_frame, text='Path Depth')
            run_label.place(relx=0.15, rely=0.5, anchor='c')
            run_scale = Scale(self.advanced_frame, from_=1, to=1000, orient=HORIZONTAL, variable=self.path_depth_s, length=200)
            run_scale.place(relx=0.5, rely=0.5, anchor='c')
                      
            trials_label = Label(self.advanced_frame, text='Path Number')
            trials_label.place(relx=0.15, rely=0.8, anchor='c')
            trials_scale = Scale(self.advanced_frame, from_=1, to=15, orient=HORIZONTAL, variable=self.path_number_s, length=200)
            trials_scale.place(relx=0.5, rely=0.8, anchor='c')
            
            depth_entry = Entry(self.advanced_frame, textvariable=self.path_depth_e, width=7)
            depth_entry.place(relx=0.85, rely=0.5, anchor='c')
            self.path_depth_s.trace('w', self.round_entry)
            depth_entry.bind('<Return>', lambda event: self.path_depth_s.set(self.path_depth_e.get()))
            
            path_number_entry = Entry(self.advanced_frame, textvariable=self.path_number_e, width=7)
            path_number_entry.place(relx=0.85, rely=0.8, anchor='c')
            self.path_number_s.trace('w', self.round_entry2)
            path_number_entry.bind('<Return>', lambda event: self.path_number_s.set(self.path_number_e.get()))
            
            self.status_var.set("Advanced Options Displayed")
            self.window.update()            
            
        else:
            self.advanced_flag.set(0)
            self.advanced_frame.destroy()
            self.status_var.set("Advanced Options Hidden")
            self.window.update()            
        
    
    def round_entry(self, *args):
        self.path_depth_e.set(round(self.path_depth_s.get()))
    
    def round_entry2(self, *args):
            self.path_number_e.set(round(self.path_number_s.get()))
    
    def import_components(self, import_frame):
        """Produces an entry box and a button for importing sudoku boards"""
        import_field = Entry(import_frame, textvariable=self.import_var, width=35)
        import_field.grid(row=1, column=1, columnspan=8, sticky=W+E)
        
        import_button = Button(import_frame, text='Import', command=self.import_board)
        import_button.grid(row=1, column=9)
    
    
    def import_board(self, *others):
        """Checks import string once import is pressed, then updates the
        sudoku board if the input is valid"""
        imported_board = ''
        for character in self.import_var.get():
            if character.isdigit():
                imported_board += character
            else:
                imported_board += '0'
            
        imported_board += '0' * (81 - len(imported_board))
        self.sudoku.current_board = imported_board
        self.display_solution(imported_board)
        self.status_var.set("Board Imported")
        self.window.update()        
    
        
    def clean_board(self):
        """Forms the board frame (again), and creates the row/column labels"""
        for square in self.squares:
            square.delete('1.0', 'end-1c')
            

    def initial_board(self, frame):
        """Decides on appropriate placement and padding for the 81 text boxes
        and passes this information to the square function"""
        
        for column in range(1, 10):
            column_label = Label(frame, text=str(column))
            column_label.grid(row=0, column=column)
        
        for row in range(1, 10):
            row_label = Label(frame, text=str(row))
            row_label.grid(row=row, column=0)          
        
        squares = []
        for entry in range(81):
            current_row = entry // 9 + 1
            current_column = entry % 9 + 1
            pad_x = (0, 5) if entry % 9 in [2, 5, 8] else (0,0)
            pad_y = (0, 5) if entry // 9 in [2, 5, 8] else (0,0)
            square = self.square(frame, entry)#, current_row, current_column, pad_x, pad_y)
            square.grid(row=current_row, column=current_column, padx=pad_x, pady=pad_y)
            squares.append(square)
        return squares
            
        
    def export_components(self, export_frame):
        """Produces an entry box and a button for exporting sudoku boards"""
        export_field = Entry(export_frame, textvariable=self.export_var, width=35)
        export_field.grid(row=13, column=0, columnspan=8, sticky=W+E)
        export_button = Button(export_frame, text='Export', command=self.export_board)
        export_button.grid(row=13, column=9)


    def export_board(self, *others):
        """Produces a string that represents the board in its current state
        and places it in the export entry box (for saving a board in its current
        state)"""
        exported_board = ''# get from engine
        for character in self.sudoku.current_board:
            if character == '_':
                exported_board += '0'
            else:
                exported_board += character
        self.export_var.set(exported_board)
        self.status_var.set("Board Exported")
        self.window.update()        
    
    
    def options(self, options_frame):
        """Places the Iterate, Check, and Solve buttons in the given window/
        frame"""
        row_centers = [0.1,0.25,0.75,0.85]
        iterate_button = Button(options_frame, text='Iterate', command=self.iterate)
        iterate_button.place(relx=0.2, rely=row_centers[1], anchor='c')
        check_button = Button(options_frame, text='Check', command=self.check_complete)
        check_button.place(relx=0.4, rely=row_centers[1], anchor='c')
        solve_button = Button(options_frame, text='Solve', command=self.solve)
        solve_button.place(relx=0.6, rely=row_centers[1], anchor='c')
        status_label = Label(options_frame, textvariable=self.status_var)
        status_label.place(relx=0.5, rely=row_centers[2], anchor='c')        
        advanced_button = Button(options_frame, text='Advanced', command=self.advanced)
        advanced_button.place(relx=0.8, rely=row_centers[1], anchor='c')         
        

    def square(self, window, entry):
        """Places a text box in the input position with the input padding, with
        a binding to update the board string whenever a key is released with the
        text box active"""
        current_entry = Text(window, width=5, height=3)
        current_entry.bind('<KeyRelease>', lambda event: self.update(entry, current_entry.get('1.0', 'end-1c')))
        current_entry.bind('<Tab>', self.change_focus)
        return current_entry
    
    
    def change_focus(self, event):
        """Moves the cursor to the next sudoku square"""
        event.widget.tk_focusNext().focus()
        return("break")
    
    
    def display_solution(self, solution):
        """Divides the information held in the board string into the 81 text
        boxes, and imports the suggestions when the character has any"""
        self.clean_board()
        
        for entry in range(81):
            digit = solution[entry]
            if digit == '_' and self.suggestions_flag.get():
                digit = ''
                for number in self.sudoku.suggestions[entry]:
                    digit += str(number)
            elif digit == '0' or digit == '_':
                digit = ''
                
            self.squares[entry].insert('end', digit)
        
        self.window.update()

    
    def update(self, entry_box, entry_value):
        """Updates the sudoku board string with the new character, or a
        placeholder ('0') if input is invalid"""
        self.sudoku.update(entry_box, entry_value)
        self.status_var.set("In Progress")
        
        
    def iterate(self, *args):
        """Calls the sudoku engine's iterate method"""
        self.sudoku.iterate(self.suggestions_flag.get())
        self.display_solution(self.sudoku.current_board)
        if self.sudoku.check_ok():
            message = "In Progress"
        else:
            message = "Invalid Board"
        self.status_var.set(message)
        
    
    def solve(self, *args):
        """Calls the sudoku engine's solve method"""
        self.status_var.set("Attempting to Solve the Given Puzzle...")
        self.window.update()
        self.sudoku.solve(self.path_depth_e.get(), self.path_number_e.get())
        if self.sudoku.status_var == 'Completed Board':
            self.status_var.set("Board Completed in {:.3f} seconds".format(self.sudoku.time_taken))
            self.display_solution(self.sudoku.current_board)
        else:
            self.status_var.set(self.sudoku.status_var)

        
    def check_complete(self, *args):
        """Calls the sudoku engine's check_complete method"""
        if self.sudoku.check_ok():
            self.sudoku.check_complete()
        self.status_var.set(self.sudoku.status_var)
    
    

def main():
    """Sets everything in motion"""
    window = Tk()
    window.title("Sudoku Assistant")
    window.resizable(width=False, height=False)
    Gui(window)
    window.mainloop()


if __name__ == '__main__':
    main()
    
