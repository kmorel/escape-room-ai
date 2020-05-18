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
      self._screen.echochar(ch)
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
        simpleaudio.WaveObject.from_wave_file('audio/click.wav').play()
        return ch
      simpleaudio.WaveObject.from_wave_file('audio/error.wav').play()

  def get_command(self, prompt='COMMAND: '):
    if prompt:
      self.typeout(prompt)
    command = ''
    while True:
      ch = self._screen.getch()
      if (chr(ch) == '\n') and (len(command) > 0):
        self._screen.echochar('\n')
        return command
      if ((ch in [ curses.KEY_BACKSPACE, curses.KEY_DC, ord('\b') ]) and
          (len(command) > 0)):
        command = command[0:-1]
        y, x = self._screen.getyx()
        self._screen.delch(y, x-1)
        simpleaudio.WaveObject.from_wave_file('audio/click.wav').play()
        continue
      if re.fullmatch('[a-zA-Z ]', chr(ch)):
        char = str(chr(ch)).upper()
        command = command + char
        self._screen.echochar(char)
        simpleaudio.WaveObject.from_wave_file('audio/click.wav').play()
        continue
      simpleaudio.WaveObject.from_wave_file('audio/error.wav').play()

def _curses_init(curses_screen, user_function):
  user_function(terminal(curses_screen))

def wrapper(function):
  curses.wrapper(_curses_init, function)

def _test(term):
  command = term.get_command()
  term.typeout('Entered command: ' + command)
  time.sleep(10)

if __name__ == '__main__':
  wrapper(_test)
