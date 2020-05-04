import time

import simpleaudio

def typeout(output):
  sound = simpleaudio.WaveObject.from_wave_file('audio/floppy-write.wav').play()
  for ch in output:
    print(ch, end='', flush=True)
    time.sleep(0.025)
  sound.stop()

if __name__ == '__main__':
  typeout('''
This is some test text.
Is this working well?
''')
