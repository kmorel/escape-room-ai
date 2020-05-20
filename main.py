import curses
import teletype

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

    +---------------------------+
    |                           |
    |    O---+   O--------+     |
    |        +-------O    |     |
    |    O     O---+      |  O  |
    |    |         +----O |  |  |
    |    |   O------------+  |  |
    |    |                   |  |
    |    +------------O      |  |
    |       O----------------+  |
    +-+              +-+      +-+
      +--------------+ +------+'''
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
    terminal.typeout('Give a system with the DET command.\n')
    return
  s = find_system(command[1])
  if not s:
    terminal.typeout('No such system ' + command[1] + '.\n')
    return
  if 'nohalt' in s:
    terminal.typeout(s['nohalt'] + '\n')
  else:
    terminal.typeout(s['code'] + ' halted.\n')
    s['online'] = False

def cnt(terminal, command):
  if len(command) < 2:
    terminal.typeout('Give a system with the DET command.\n')
    return
  s = find_system(command[1])
  if not s:
    terminal.typeout('No such system ' + command[1] + '.\n')
    return
  terminal.typeout(s['code'] + ' continued.\n')
  s['online'] = True

commands = {
  'LST': lst,
  'SYS': syst,
  'DET': det,
  'HLT': hlt,
  'CNT': cnt,
}

def main_loop(terminal):
  #terminal.typeout(logo)
  terminal.curses_screen().addstr(logo)
  while True:
    terminal.curses_screen().echochar(curses.ACS_BBSS)
    terminal.curses_screen().echochar(ord('a'))
    terminal.typeout('\n')
    command = terminal.get_command().split()
    if command[0] in commands:
      commands[command[0]](terminal, command)
    elif command[0] == 'QUIT':
      return
    else:
      terminal.typeout('No such command: ' + command[0] + '\n')

teletype.wrapper(main_loop)
