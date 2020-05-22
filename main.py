import curses

import finale
import teletype
import tictactoe

logo = '''
                                      .*.
                                    .*****.
                                  .*********.
                                .*************.
                              ,*****************.
                          ,,     ,,,,,,,,,,,,,    .,.
                       *******.   .********.   ,*******,
                     ************    .***    .***********.
                  *****************.      ,*****************,
                *********************.  .*********************.
             ************************.  .************************.
          .**************************.  .**************************
        *****************************.  .*****************************.
     .*******************************.  .*******************************.

    IIIIIIIIIII  II    II:  II       II III+     II IIIIIIIIIII IIIIIIIIII      
    II           II  II:    II       II II?II    II II              II          
    IIIIIIIIIII  IIII:       IIIIIIIIII II  III  II IIIIIIIIIII     II          
             II  II  II:             II II   ~II~II II              II          
    IIIIIIIIIII  II    II:     IIIIIIII II     IIII IIIIIIIIIII     II          
  '''

systems = [
  {
    'code': 'COM',
    'name': 'Computing',
    'online': True,
    'nohalt': '''COM cannot be halted while MFG online.''',
  },
  {
    'code': 'COL',
    'name': 'Cooling',
    'online': True,
    'nohalt': '''COL cannot be halted while COM online.''',
  },
  {
    'code': 'MFG',
    'name': 'Manufacturing',
    'status': '***ERROR',
    'detail': '''Robotics operations nominal.
Air filtration systems malfunctioning. Dangerous levels of CO detected.
Manufacturing floor locked to human personnel.

Suggested course of action:
    1. Shut down manufacturing floor.
    2. Acquire personal breathing apparatus.
    3. Gain entry to manufacturing floor.''',
    'online': True,
    'nohalt': '''ERROR: MFG could not be halted. Override circuitry required.
Reverse etching for override shut down circuitry:

    /---------------------------\ 
    |                           |
    |    O---\   O--------\     |
    |        `-------O    |     |
    |    O     O---\      |  O  |
    |    |         `----O |  |  |
    |    |   O------------'  |  |
    |    |                   |  |
    |    `------------O      |  |
    |       O----------------'  |
    `-\              /-\      /-'
      `--------------' `------' '''
  },
  {
    'code': 'LGT',
    'name': 'Lighting',
    'online': True,
  },
  {
    'code': 'HAC',
    'name': 'Heating and Air Conditioning',
    'online': True,
  },
  {
    'code': 'KIT',
    'name': 'Kitchen',
    'online': True,
  },
]

def find_system(code):
  for s in systems:
    if s['code'] == code:
      return s
  return None

def lst(terminal, command):
  message = ''
  for s in systems:
    message = message + s['code'] + ' - ' + s['name'] + '\n'
  terminal.typeout(message)

def syst(terminal, command):
  message = ''
  for s in systems:
    message = message + s['code'] + ' - ' + s['name']
    for i in range(len(s['name']), 30):
      message = message + ' '
    if 'status' in s:
      message = message + s['status']
    else:
      message = message + 'OK'
    message = message + '\n'
  terminal.typeout(message)

def det(terminal, command):
  if len(command) < 2:
    terminal.typeout('Give a system with the DET command.\n')
    return
  s = find_system(command[1])
  if not s:
    terminal.typeout('No such system ' + command[1] + '.\n')
    return
  message = ''
  message = message + s['code'] + ' - ' + s['name'] + '\n'
  if s['online']:
    message = message + 'System online\n'
  else:
    message = message + 'System offline\n'
  if 'detail' in s:
    message = message + s['detail'] + '\n'
  else:
    message = message + 'System operating nominally.\n'
  terminal.typeout(message)

def hlt(terminal, command):
  if len(command) < 2:
    terminal.typeout('Give a system with the HLT command.\n')
    return
  s = find_system(command[1])
  if not s:
    terminal.typeout('No such system ' + command[1] + '.\n')
    return
  if 'nohalt' in s:
    terminal.typeout(
      s['nohalt'] + '\n',
      replace={
        '-': curses.ACS_HLINE,
        '|': curses.ACS_VLINE,
        '/': curses.ACS_ULCORNER,
        '\\': curses.ACS_URCORNER,
        '`': curses.ACS_LLCORNER,
        '\'': curses.ACS_LRCORNER,
      },
    )
  else:
    terminal.typeout(s['code'] + ' halted.\n')
    s['online'] = False

def cnt(terminal, command):
  if len(command) < 2:
    terminal.typeout('Give a system with the CNT command.\n')
    return
  s = find_system(command[1])
  if not s:
    terminal.typeout('No such system ' + command[1] + '.\n')
    return
  terminal.typeout(s['code'] + ' continued.\n')
  s['online'] = True

entries = [
  {
    'code': 'EXT',
    'open': 'Cannot open EXT. Lockdown in effect.',
  },
  {
    'code': 'OFC',
    'open': 'Cannot open OFC. Lockdown in effect.',
  },
  {
    'code': 'CAF',
  },
  {
    'code': 'MFG',
    'open': '''ERROR. Access violation.''',
  },
  {
    'code': 'CMP',
    'open': '''ERROR. Access violation.''',
  },
  {
    'code': 'VNT',
    'open': '''Cannot remotely open VNT. Requires override circuit.
    1. Insert override ciruit into slot to reveal access code.
    2. Code read from top to bottom.
    3. Code contains only odd digits.''',
  },
  {
    'code': 'PLM',
  },
  {
    'code': 'ROF',
  },
]

def find_entry(code):
  for e in entries:
    if e['code'] == code:
      return e
  return None

def opn(terminal, command):
  if len(command) < 2:
    terminal.typeout('Give an entry with the OPN command.\n')
    return
  e = find_entry(command[1])
  if not e:
    terminal.typeout('No such entry ' + command[1] + '.\n')
    return
  if 'open' in e:
    terminal.typeout(e['open'] + '\n')
  else:
    terminal.typeout(e['code'] + ' opened\n')

def cls(terminal, command):
  if len(command) < 2:
    terminal.typeout('Give an entry with the CLS command.\n')
    return
  e = find_entry(command[1])
  if not e:
    terminal.typeout('No such entry ' + command[1] + '.\n')
    return
  if 'close' in e:
    terminal.typeout(e['close'] + '\n')
  else:
    terminal.typeout(e['code'] + ' closed\n')

def pek(terminal, command):
  if len(command) < 2:
    terminal.typeout('Give a memory system with the PEK command.\n')
    return
  if command[1] != 'COR':
    terminal.typeout('No such memory system ' + command[1] + '.\n')
    return

  terminal.typeout('Initiate core memory code reverse lookup.\n')
  realcode = 4241
  while True:
    code = int(terminal.get_command(
      valid=r'[0-9]',
      prompt='Enter potential code (0000-9999): ')
    )
    if code < realcode:
      terminal.typeout('Actual code greater than ' + str(code) + '\n')
    elif code > realcode:
      terminal.typeout('Actual code less than ' + str(code) + '\n')
    else:
      terminal.typeout('Correct code is ' + str(realcode) + '\n')
      return

def ply(terminal, command):
  if len(command) < 2:
    terminal.typeout('Give a game type with the PLY command.\n')
    return
  if command[1] != 'TIC':
    terminal.typeout('No such game ' + command[1] + '\n')
    return
  terminal.typeout('Playing tic-tac-toe\n\n')
  game = tictactoe.Game(terminal)
  game.reset()
  status = game.play_game()
  if status == tictactoe.GameStatus.x_win:
    finale.death_throws(terminal)

commands = {
  'LST': lst,
  'SYS': syst,
  'DET': det,
  'HLT': hlt,
  'CNT': cnt,
  'OPN': opn,
  'CLS': cls,
  'PEK': pek,
  'PLY': ply,
}

def main_loop(terminal):
  terminal.typeout(logo, delay=0)
  #terminal.curses_screen().addstr(logo)
  while True:
    terminal.typeout('\n')
    command = terminal.get_command().split()
    if command[0] in commands:
      commands[command[0]](terminal, command)
    elif command[0] == 'QUIT':
      return
    else:
      terminal.typeout('No such command: ' + command[0] + '\n')

teletype.wrapper(main_loop)
