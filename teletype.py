import curses
import re
import simpleaudio
import time

class terminal:
  # Thus curses screen
  _screen = None

  def __init__(self, stdscr):
    self._screen = stdscr
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    self._screen.scrollok(True)
    self._screen.attron(curses.color_pair(1))

  def curses_screen(self):
    return self._screen

  def clear(self):
    self._screen.clear()
    self._screen.refresh()

  def typeout(self, output):
    self._screen.refresh()
    sound = \
      simpleaudio.WaveObject.from_wave_file('audio/floppy-write.wav').play()
    for ch in output:
      #print(ch, end='', flush=True)
      self._screen.addstr(ch)
      self._screen.refresh()
      time.sleep(0.025)
    sound.stop()

  def get_char(self, valid=r'.', prompt=None):
    if prompt:
      self.typeout(prompt)
    while True:
      ch = self._screen.getch()
      if re.fullmatch(valid, chr(ch)):
        ch = chr(ch)
        self._screen.addstr('{}\n'.format(ch))
        self._screen.refresh()
        return ch
      curses.beep()

def _curses_init(curses_screen, user_function):
  user_function(terminal(curses_screen))

def wrapper(function):
  curses.wrapper(_curses_init, function)

def _test(term):
  term.typeout('''
This is some test text.
Is this working well?
''')
  for i in range(50):
    term.typeout('{}\n'.format(i))

if __name__ == '__main__':
  wrapper(_test)
