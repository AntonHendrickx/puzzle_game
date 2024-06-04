import os
import unittest
import pygame
from src.puzzle import Puzzle
from src.regular_puzzle_piece import RegularPiece


class MyTestCase(unittest.TestCase):
    def test_save_piece(self):
        test_dir = os.path.dirname(__file__)
        image_path = os.path.join(test_dir, 'puzzle_test.png')
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (50, 50))
        piece = RegularPiece(1, 1, 50, 50, image)
        data = piece.serialize()
        new_piece = RegularPiece.deserialize(data)
        self.assertEqual(new_piece.get_width(), piece.get_width())  # add assertion here

    def test_save_puzzle(self):
        test_dir = os.path.dirname(__file__)
        image_path = os.path.join(test_dir, 'puzzle_test.png')
        screen = pygame.Surface((800, 600))
        puzzle = Puzzle(screen, 600, 300, 8, image_path, False)
        data = puzzle.serialize()
        new_puzzle = Puzzle.deserialize(data, screen)
        self.assertIsNotNone(new_puzzle)


if __name__ == '__main__':
    unittest.main()
