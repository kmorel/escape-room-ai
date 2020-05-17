import teletype
import time

class GameStatus:
  in_progress = 0
  cat = 1
  x_win = 2
  o_win = 3

class Game:
  '''Manages a TicTacToe game.'''

  _x_image = [
    'X   X',
    ' X X ',
    '  X  ',
    ' X X ',
    'X   X',
  ]

  _o_image = [
    ' OOO ',
    'O   O',
    'O   O',
    'O   O',
    ' OOO ',
  ]

  _xo_image = [
    'XOOOX',
    'OX XO',
    'O X O',
    'OX XO',
    'XOOOX',
  ]

  _none_image = [
    '     ',
    '     ',
    '     ',
    '     ',
    '     ',
    '     ',
  ]

  # Because this is being used in an escape room, we are intentionally
  # indexing the spaces weird. Moreover, these indices are arranged such
  # that every line adds up to 15 (and all triples that add to 15 are in
  # a line).
  _board_numbers = [
    [ 2, 9, 4 ],
    [ 7, 5, 3 ],
    [ 6, 1, 8 ]
  ]

  _x_squares = []
  _o_squares = []

  _empty_squares = [ 1, 2, 3, 4, 5, 6, 7, 8, 9 ]

  _terminal = None

  def __init__(self, terminal):
    self._terminal = terminal

  def _get_image(self, square):
    if square in self._x_squares:
      if square in self._o_squares:
        return self._xo_image
      else:
        return self._x_image
    else:
      if square in self._o_squares:
        return self._o_image
      else:
        return self._none_image

  def _get_row_print(self, row, add_key = False):
    s = ''
    left = self._get_image(row[0])
    center = self._get_image(row[1])
    right = self._get_image(row[2])
    for i in range(5):
      s = s + ' ' + left[i] + ' | ' + center[i] + ' | ' + right[i]
      if add_key:
        s = s + '       '
        if (i % 2) == 0:
          row = i // 2
          s = s + \
            str(self._board_numbers[row][0]) + '|' + \
            str(self._board_numbers[row][1]) + '|' + \
            str(self._board_numbers[row][2])
        else:
          s = s + '-+-+-'
      s = s + '\n'
    return s

  def print_board(self):
    s = ''
    s = s + self._get_row_print(self._board_numbers[0])
    s = s + '-------+-------+-------\n'
    s = s + self._get_row_print(self._board_numbers[1])
    s = s + '-------+-------+-------     Board key:\n'
    s = s + self._get_row_print(self._board_numbers[2], True)
    self._terminal.typeout(s)

  def x_turn(self):
    space = int(self._terminal.get_char(valid=r'[1-9]',
                                        prompt='Pick a space (1-9): '))
    self._x_squares.append(space)
    # Intentional bug: player can pick space already picked
    if space in self._empty_squares:
      self._empty_squares.remove(space)
    self._terminal.typeout('\nYour move:\n')
    self.print_board()

  def _decide_o_space(self):
    # Check to see if o is about to connect 3
    for i in range(len(self._o_squares)):
      for j in range(len(self._o_squares)):
        if i == j:
          continue
        remaining = 15 - self._o_squares[i] - self._o_squares[j]
        if remaining in self._empty_squares:
          return remaining

    # Check to see if x is about to connect 3
    for i in range(len(self._x_squares)):
      for j in range(len(self._x_squares)):
        if i == j:
          continue
        remaining = 15 - self._x_squares[i] - self._x_squares[j]
        if remaining in self._empty_squares:
          return remaining

    # If center is available, take it
    if 5 in self._empty_squares:
      return 5

    preferred_spaces = []
    # If opponent has center, favor corners to prevent corner trap. Otherwise
    # favor sides for the same reason.
    if 5 in self._x_squares:
      preferred_spaces = [ 2, 4, 6, 8, 1, 3, 7, 9 ]
    else:
      preferred_spaces = [ 1, 3, 7, 9, 2, 4, 6, 8 ]

    for space in preferred_spaces:
      if space in self._empty_squares:
        return space

    # If we are here, it is in error. Give up.
    return 5

  def o_turn(self):
    self._terminal.typeout('\nThinking...')
    time.sleep(2)
    space = self._decide_o_space()
    self._o_squares.append(space)
    self._empty_squares.remove(space)
    self._terminal.typeout('\nOpponent\'s move:\n')
    self.print_board()

  def get_status(self):
    for i in range(len(self._o_squares)):
      for j in range(len(self._o_squares)):
        if i == j:
          continue
        for k in range(len(self._o_squares)):
          if (k == i) or (k == j):
            continue
          if self._o_squares[i] + self._o_squares[j] + self._o_squares[k] == 15:
            return GameStatus.o_win

    for i in range(len(self._x_squares)):
      for j in range(len(self._x_squares)):
        if i == j:
          continue
        for k in range(len(self._x_squares)):
          if (k == i) or (k == j):
            continue
          if self._x_squares[i] + self._x_squares[j] + self._x_squares[k] == 15:
            return GameStatus.x_win

    if self._empty_squares:
      return GameStatus.in_progress
    else:
      return GameStatus.cat

  def play_game(self):
    self.print_board()
    while True:
      self.x_turn()
      if self.get_status() != GameStatus.in_progress:
        break
      self.o_turn()
      if self.get_status() != GameStatus.in_progress:
        break

    status = self.get_status()
    if status == GameStatus.cat:
      self._terminal.typeout('Cat game\n')
    elif status == GameStatus.x_win:
      self._terminal.typeout('You won?!?!?!\n')
    elif status == GameStatus.o_win:
      self._terminal.typeout('I win\n')
    else:
      self._terminal.typeout('Internal error\n')

    return status

def _test(term):
  game = Game(term)
  game.play_game()

if __name__ == '__main__':
  teletype.wrapper(_test)
