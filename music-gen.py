"""Generating Simple Musical Compositions Using Genetic Algorithms
 
Algorithmics 2022/23
(Group) Project

Team: Anton Slavin


Sources used and viewed:
 - https://github.com/tonysln/py-ga/blob/main/genpixel.py
 - https://dev.to/rpalo/python-s-random-choices-is-awesome-46ii
"""

from midiutil import MIDIFile
from random import choice, choices, random
#import matplotlib.pyplot as plt


def rand_note_stream(n, scale, lens):
    notes = []
    durs  = []
    for i in range(n):
        notes.append(choice(scale))
        durs.append(choice(lens))
    
    times = [0]
    for i,d in enumerate(durs):
        times.append(times[i] + d)
        
    return (notes,durs,times)


def create_midi(notes, durs, times, fname):
    track    = 0
    channel  = 0
    tempo    = 150
    volume   = 100
    
    midi = MIDIFile(1)
    midi.addTempo(track, 0, tempo)
    
    for i,pitch in enumerate(notes):
        midi.addNote(track, channel, pitch, times[i], durs[i], volume)

    with open(fname, 'wb') as bf:
        midi.writeFile(bf)
 


class Composition():
    """Miniature musical composition class
    
    Represented by a stream of MIDI note values and durations.
    """
    
    def __init__(self, n, scale, lens=[0.5, 1, 1.5]):
        n_,d_,t_ = rand_note_stream(n, scale, lens)
        self.notes = n_
        self.durations = d_
        self.times = t_
        self.scale = scale
        self.lens = lens
    
    
    def fitness(self):
        score = 2.0
        
        # Does not end on root
        if self.notes[-1] != self.scale[0]:
            score -= 0.15
        
        for i,n in enumerate(self.notes):
            # Repeating notes
            if i > 1 and (self.notes[i-2] == self.notes[i-1] == n):
                score -= 0.15
            if abs(n - self.notes[i-1]) > 6:
                score -= 0.25
            if abs(n - self.notes[i-1]) > 8:
                score -= 0.35
        
            # Lick 1
            if i > 1 and (0 < self.notes[i-2] == n) and (n != self.notes[i-1]) and (0 < abs(n - self.notes[i-1]) < 3):
                score += 0.1
            # Lick 2
            if i > 1 and (0 < abs(self.notes[i-2] - self.notes[i-1]) < 3) and (0 < abs(n - self.notes[i-1]) < 3):
                score += 0.12
                
        # Encourage "good" notes
        for _ in range(self.notes.count(self.scale[4])):
            score += 0.15
        for _ in range(self.notes.count(self.scale[2])):
            score += 0.25
        for _ in range(self.notes.count(self.scale[0])):
            score += 0.15
        for _ in range(self.notes.count(self.scale[-1])):
            score += 0.1
            
        # "bad" notes
        for _ in range(self.notes.count(self.scale[1])):
            score -= 0.15
        for _ in range(self.notes.count(self.scale[6])):
            score -= 0.15
        
        return max(0.000001, score)
    
    
    def mutate(self, mutrate):
        for i,n in enumerate(self.notes):
            if random() < mutrate:
                self.notes[i] = choice(self.scale)
    
    
    def crossover(self, other):
        p = choice(range(len(self.notes)))
        self.notes = other.notes[:p] + self.notes[p:]
    
    
    def save_midi(self, fname):
        create_midi(self.notes, self.durations, self.times, fname)
    
    
    def __repr__(self):
        s = [f'{n},{d}' for n,d in zip(self.notes, self.durations)]
        return f'<Composition {" ".join(s)}>'
    
    
    
class MusicGA():
    """Musical composition evolver using a genetic algorithm"""
    
    def __init__(self, clen, poplen, mutrate, targetfit):
        self.pop = []
        self.pool = []
        self.clen = clen
        self.poplen = poplen
        self.mutrate = mutrate
        self.best = None
        self.worst = None
        self.targetfit = targetfit    
    

    def populate(self, scale):
        self.pop = []
        for _ in range(self.poplen):
            c = Composition(self.clen, scale)
            self.pop.append((c, c.fitness()))
    
    
    def make_pool(self):
        self.pool = []
        best = None
        bestf = -10e7
        fsum = 0.0
        worst = None
        worstf = 10e7
        
        for c,f in self.pop:
            if f > bestf:
                best = c
                bestf = f
            if f < worstf:
                worst = c
                worstf = f
            fsum += f
        
        # https://dev.to/rpalo/python-s-random-choices-is-awesome-46ii
        
        ws = [f / fsum for c,f in self.pop]
        for _ in range(self.poplen):
            r = random()
            acc = 0
            idx = -1
            while acc < r: 
                idx += 1 
                acc += ws[idx] 
            
            self.pool.append(self.pop[idx])
        
#         fns = [f for c,f in self.pop]
#         self.pool = choices(population=self.pop, 
#                             weights=fns,
#                             k=self.poplen)

        self.best = (best,bestf)
        self.worst = (worst,worstf)
        
    
    def evolve(self):
        # self pop updated as a result, ready to run make_pool()
        for i in range(self.poplen):
            p1,p2 = choices(self.pool, k=2)
            p1,_ = p1
            p2,_ = p2
            p1.crossover(p2)
            p1.mutate(self.mutrate)
            self.pop[i] = (p1, p1.fitness())
    
    
    def run(self):
        it = 1
        while True:
            it += 1
            mga.evolve()
            mga.make_pool()
            b,f = mga.best
            if f > self.targetfit:
                print(self.targetfit, f, it)
                b.save_midi('mga_best.mid')
                print('Midi saved')
                break
                
            if it % 500 == 0:
                #self.targetfit -= 0.01
                print(it, f)
                

                
A_DORIAN = [57, 59, 60, 62, 64, 66, 67, 69]
A_MINOR  = [57, 59, 60, 62, 64, 65, 67, 68]
C_MAJOR  = [60, 62, 64, 65, 67, 69, 71, 72]

if __name__ == '__main__':
    mga = MusicGA(clen=48, poplen=110, mutrate=0.21, targetfit=6.0)
    mga.populate(C_MAJOR)
    mga.make_pool()
    mga.run()
