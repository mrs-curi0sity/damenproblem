import unittest
from damenproblem import board
 

class TestPlacement(unittest.TestCase):

    def test_placement(self):
        size = 4
        myboard =board(size=size)
        myboard.place_queen(3,'A')
        myboard.place_queen(3,'C')
        myboard.place_queen(2,'B')
        myboard.place_queen(2,'A')
        myboard.show_fields()
        diag_1, diag_2 = myboard.get_diagonal_values(0,0)
        self.assertEqual(diag_1, [0,0,0,0])
        self.assertEqual(diag_2, [0])

        diag_1, diag_2 = myboard.get_diagonal_values(2,0)
        print(diag_1, diag_2)
        self.assertEqual(diag_1, [1,0])
        self.assertEqual(diag_2, [0,0,1])

        diag_1, diag_2 = myboard.get_diagonal_values(1,2)
        self.assertEqual(diag_1, [0,0,0])
        self.assertEqual(diag_2, [0,0, 1,1])


    def test_valid_moves(self):
        size = 4
        myboard =board(size=size)
        myboard.place_queen(3,'A')
        myboard.show_fields()
        self.assertEqual(False, myboard.is_valid_new_position(3,0))
        self.assertEqual(False, myboard.is_valid_new_position(2,1))
        self.assertEqual(True, myboard.is_valid_new_position(2,2))

if __name__ == '__main__':
     unittest.main()
