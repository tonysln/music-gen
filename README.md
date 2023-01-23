# music-gen
Generating Simple Musical Compositions Using Genetic Algorithms.

## Usage

*Please use either Python 3.11 or pypy3 to run the program for best performance.*

```
pypy3 music-gen.py
```

All configurable parameters are given to the main `MusicGA` class constructor:

```
clen      - composition length
poplen    - population size
mutrate   - mutation rate
targetfit - target fitness
```

After initializing the GA system, it has to be populated with the given scale as parameter. A valid scale is just an array of integers, representing MIDI note numbers, from which the GA system generates compositions and chooses random notes for mutation.

For example, a single octave of the C Major scale:

```
C_MAJOR  = [60, 62, 64, 65, 67, 69, 71, 72]
```

