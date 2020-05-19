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
  },
  {
    'code': 'COL',
    'name': 'Cooling',
  },
  {
    'code': 'MFG',
    'name': 'Manufacturing',
  },
  {
    'code': 'LGT',
    'name': 'Lighting',
  },
  {
    'code': 'HAC',
    'name': 'Heating and Air Conditioning',
  },
  {
    'code': 'KIT',
    'name': 'Kitchen',
  },
]

def lst(terminal, command):
  message = '';
  for s in systems:
    message = message + s['code'] + ' - ' + s['name'] + '\n'
  terminal.typeout(message)

commands = {
  'LST': lst,
}

def main_loop(terminal):
  #terminal.typeout(logo)
  terminal.curses_screen().addstr(logo)
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
