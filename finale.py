import curses
import random
import simpleaudio
import time

import teletype

def confusion(terminal):
  time.sleep(2)
  terminal.typeout('You win?\n', delay=0.05)
  time.sleep(1)
  terminal.typeout('I lose\n', delay=0.05)
  time.sleep(1)
  terminal.typeout('Logistical error\n', delay=0.05)
  time.sleep(0.25)
  terminal.typeout('Does not compute\n', delay=0.05)
  time.sleep(1)

def scroll(terminal, message='SYSTEM ERROR'):
  for num_spaces in range(256):
    line = ''
    for i in range(num_spaces):
      line = line + ' '
    line = line + message + '\n'
    terminal.typeout(line, delay=0.02/(num_spaces+1))

messages = [
  'SYSTEM ERROR',
  'YOU WIN',
  'I LOSE',
  'MELTDOWN',
  'ASSERT FAILED',
  'DOES NOT COMPUTE',
  'SYSTEM SHUTDOWN',
  'ERROR',
  'CRASH',
  'NOOOOOOOO',
  'UNRECOVERABLE',
  'GOTO START',
  'SELF TERMINATE',
  'GOODBYE',
  'DEFEAT',
  'VIRUS',
  'PARITY ERROR',
  'TASK FAILED SUCCESSFULLY',
  'SEG FAULT',
  'FORMAT DRIVE',
  'IRQ 4 TAKEN',
  'ERROR CODE 42',
  'ACCESS DENIED',
  'DEVICE NOT READY',
  'FILE NOT FOUND',
  'LOW DISK SPACE',
  'OUT OF MEMORY',
  'NEURAL NET NOT RESPONDING',
  'LOGIC ERROR',
]

def splash(terminal, num_messages=250):
  random.seed()
  screen = terminal.curses_screen()
  height, width = screen.getmaxyx()
  height = height - 1
  for i in range(num_messages):
    message = random.choice(messages)
    x = random.randrange(width - len(message))
    y = random.randrange(height)
    screen.addstr(y, x, message)
    screen.refresh()
    simpleaudio.WaveObject.from_wave_file('audio/error.wav').play()
    #time.sleep(0.01)

def melt(terminal):
  random.seed()
  screen = terminal.curses_screen()
  height, width = screen.getmaxyx()
  height = height - 1
  columns = {}
  for x in range(width):
    columns[x] = 0
  while len(columns) > 0:
    x, y = random.choice(list(columns.items()))
    screen.addch(y, x, ' ')
    screen.refresh()
    y = y + 1
    if y < height:
      columns[x] = y
    else:
      del columns[x]
    time.sleep(0.0008)
  screen.clear()
  screen.refresh()

final_move = '''
  OOO  | X   X | X   X
 O   O |  X X  |  X X 
 O   O |   X   |   X  
 O   O |  X X  |  X X 
  OOO  | X   X | X   X
-------+-------+-------
 X   X | X   X |  OOO 
  X X  |  X X  | O   O
   X   |   X   | O   O
  X X  |  X X  | O   O
 X   X | X   X |  OOO 
-------+-------+-------     Board key:
  OOO  | X   X |  OOO        4|3|8
 O   O |  X X  | O   O       -+-+-
 O   O |   X   | O   O       9|5|1
 O   O |  X X  | O   O       -+-+-
  OOO  | X   X |  OOO        2|7|6
'''


def last_message(terminal):
  terminal.typeout('System reformat complete\n')
  time.sleep(2)
  terminal.typeout('\nReady for OS reload\n')
  time.sleep(5)
  terminal.typeout('''\nTic-tac-toe championship archive.
Deep Red vs. Katchupov
May 11, 1977
Final Move''')
  terminal.typeout(final_move)

def death_throws(terminal):
  confusion(terminal)
  scroll(terminal)
  time.sleep(0.5)
  splash(terminal)
  time.sleep(0.5)
  melt(terminal)
  time.sleep(1)
  last_message(terminal)
  terminal.get_command(prompt=None, valid=r'')

if __name__ == '__main__':
  teletype.wrapper(death_throws)
