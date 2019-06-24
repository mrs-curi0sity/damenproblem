import pandas as pd
import time
import random

alphabet = []
for letter in range(65, 91):
    alphabet.append(chr(letter))

# abort execution after TIMEOUT many seconds
TIMEOUT = 8

# TBV 
# I copied this from stackoverflow 'Kill python function after a given amount of time'
import signal

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException

class board():

    def __init__(self, size):
        self.size = size

        #initialize empty board
        self.fields = pd.DataFrame(columns = alphabet[:size], index = range(0, size))
        self.fields.fillna(0, inplace=True)

    def show_fields(self):
        print(self.fields)

    def place_queen(self, x, y):
        self.fields.iloc[x,y] = 1

    # indices starting from 0 to size-1
    def is_valid_new_position(self,x, y):
        is_valid = True

        # Fall1 : Zeile enthaelt bereits eine Dame
        if (self.fields.iloc[x,:]==1).any():
            is_valid = False
        
        # Fall 2: Spalte enthaelt bereits eine Dame
        elif (self.fields.iloc[:,y]==1).any():
            is_valid = False
        
        else:
            diagonale_1, diagonale_2 = self.get_diagonal_values(x, y)
            # print(f'[INFO] diagonale_1: {diagonale_1}')
            # print(f'[INFO] diagonale_2: {diagonale_2}')
            if 1 in diagonale_1:
                is_valid = False
            elif 1 in diagonale_2:
                is_valid = False
        
        return is_valid

    # returns the values on the field for both diagnoals crossing (x,y)
    def get_diagonal_values(self, x,y):
        diagonale_1 = []
        for offset in range(-self.size, self.size):
            x_pos_1 = x + offset
            y_pos_1 = y + offset
            # check if position inside board
            if (0 <= x_pos_1 <= self.size-1) & (0 <= y_pos_1 <= self.size -1):
                # print(f'[DEBUG] diag1 {x_pos_1}, {y_pos_1}')
                diagonale_1.append(self.fields.iloc[x_pos_1, y_pos_1])
        
        # could be unified into one loop, but use extra loop for the sake of clarity
        diagonale_2 = []
        for offset in range(-self.size, self.size):
            x_pos_2 = x + offset
            y_pos_2 = y - offset
            # check if position inside board
            if (0 <= x_pos_2 <= self.size-1) & (0 <= y_pos_2 <= self.size -1):
                # print(f'[DEBUG] diag2 {x_pos_2}, {y_pos_2}')
                diagonale_2.append(self.fields.iloc[x_pos_2, y_pos_2])
        
        return diagonale_1, diagonale_2

    # besser als nichts
    # bei (n over n**2) vielen Kombinationen aber nicht empfehlenswert
    def find_positions(self):

        x_random = random.randint(0,self.size-1)
        y_random = random.randint(0,self.size-1)
        print(f'initializing with random position: {x_random}, {y_random}')
        self.place_queen(x_random, y_random)
        nr_done = 1

        while nr_done <= self.size:
            x,y = self.find_new_position_brute_force()
            if (x,y) == (-1, -1):
                print(f'sorry, no position left. will return after {nr_done} steps')
                return

            print(f'new position found: {x}, {y}')
            self.place_queen(x,y)
            self.show_fields()
            nr_done += 1
        print ('HOOORAY, we found a solition!!!')
        self.fields.to_csv(f'results/damen_{self.size}.csv')

    def find_new_position_brute_force(self):
        x_list = list(range (0,self.size-1))
        random.shuffle(x_list)
        # print(f'[DEBUG] {x_list}')
        for x in x_list:
            y_list = list(range(0,self.size-1))
            random.shuffle(y_list)
            # print(f'[DEBUG] {y_list}')
            for y in y_list:
                if self.is_valid_new_position(x, y):
                    print(f'[INFO] found new position {x}, {y}')
                    return x, y
        # no valid position found
        return -1, -1


def main():
    size = int(input("what size should de board be? : "))
    myboard = board(size=size)
    myboard.show_fields()
    signal.signal(signal.SIGALRM, timeout_handler)

    signal.alarm(TIMEOUT)    
    try:
         myboard.find_positions()
    except TimeoutException:
        print('function terminated due to timeout')

if __name__ == '__main__':
    main()