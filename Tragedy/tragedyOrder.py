#!/usr/bin/env python3
"""
tragedyOrder.py -- the order of the 32 tragedies, as TragedyPrediction.txt
part 1 fixes it: the identifiers sorted, then random.Random(3201).shuffle.

  python tragedyOrder.py
"""
import random

TITLES = {
    'tlg0085.tlg001': ('Aeschylus', 'Suppliants', 'eng2'), 'tlg0085.tlg002': ('Aeschylus', 'Persians', 'eng2'),
    'tlg0085.tlg003': ('Aeschylus', 'Prometheus Bound', 'eng2'), 'tlg0085.tlg004': ('Aeschylus', 'Seven Against Thebes', 'eng2'),
    'tlg0085.tlg005': ('Aeschylus', 'Agamemnon', 'eng3'), 'tlg0085.tlg006': ('Aeschylus', 'Libation Bearers', 'eng2'),
    'tlg0085.tlg007': ('Aeschylus', 'Eumenides', 'eng2'),
    'tlg0011.tlg001': ('Sophocles', 'Trachiniae', 'eng3'), 'tlg0011.tlg002': ('Sophocles', 'Antigone', 'eng2'),
    'tlg0011.tlg003': ('Sophocles', 'Ajax', 'eng2'), 'tlg0011.tlg004': ('Sophocles', 'Oedipus Tyrannus', 'eng2'),
    'tlg0011.tlg005': ('Sophocles', 'Electra', 'eng2'), 'tlg0011.tlg006': ('Sophocles', 'Philoctetes', 'eng2'),
    'tlg0011.tlg007': ('Sophocles', 'Oedipus at Colonus', 'eng2'),
    'tlg0006.tlg002': ('Euripides', 'Alcestis', 'eng2'), 'tlg0006.tlg003': ('Euripides', 'Medea', 'eng2'),
    'tlg0006.tlg004': ('Euripides', 'Heracleidae', 'eng2'), 'tlg0006.tlg005': ('Euripides', 'Hippolytus', 'eng2'),
    'tlg0006.tlg006': ('Euripides', 'Andromache', 'eng2'), 'tlg0006.tlg007': ('Euripides', 'Hecuba', 'eng2'),
    'tlg0006.tlg008': ('Euripides', 'Suppliants', 'eng2'), 'tlg0006.tlg009': ('Euripides', 'Heracles', 'eng2'),
    'tlg0006.tlg010': ('Euripides', 'Ion', 'eng2'), 'tlg0006.tlg011': ('Euripides', 'The Trojan Women', 'eng2'),
    'tlg0006.tlg012': ('Euripides', 'Electra', 'eng2'), 'tlg0006.tlg013': ('Euripides', 'Iphigenia in Tauris', 'eng2'),
    'tlg0006.tlg014': ('Euripides', 'Helen', 'eng2'), 'tlg0006.tlg015': ('Euripides', 'Phoenissae', 'eng2'),
    'tlg0006.tlg016': ('Euripides', 'Orestes', 'eng2'), 'tlg0006.tlg017': ('Euripides', 'Bacchae', 'eng2'),
    'tlg0006.tlg018': ('Euripides', 'Iphigenia in Aulis', 'eng2'), 'tlg0006.tlg019': ('Euripides', 'Rhesus', 'eng3'),
}
PILOT = ('tlg0006.tlg001', ('Euripides', 'Cyclops', 'eng2'))

ids = sorted(TITLES)
assert len(ids) == 32
random.Random(3201).shuffle(ids)
if __name__ == '__main__':
    for n, i in enumerate(ids, 1):
        a, t, e = TITLES[i]
        print('P%02d | %s | %s | %s | %s' % (n, i, a, t, e))
