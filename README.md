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

After running the system, the population is evolved until the target fitness is reached. The resulting (best) member of the population is saved into a midi file (currently just named `mga_best.mid`).

## Fitness

The principle behind the current fitness function is to punish for "ugly" notes and patterns and "reward" for nice ones.

For example, "ugly" patterns include:

- Jumps larger than 7 semitones between two consecutive notes.
- A single note repeated more than 3 times in a row.
- Multiple subtonic and supertonic notes.

And some "nice" patterns include:

- Ending note is the same as the starting note (for easier looping).
- Three consecutive rising notes (do-re-mi).
- Three consecutive notes forming a "hat" (do-re-do). 
- Multiple tonic, mediant and dominant notes.

Most of these patterns were chosen almost completely by feeling alone and for this reason they should be reconsidered.

Much more testing is also required to balance out the amount of punishment and reward in each of these cases.
