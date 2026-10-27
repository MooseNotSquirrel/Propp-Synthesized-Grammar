#!/usr/bin/env python3
"""
parityReports.py -- reports 10 and 11 of Data/ParityProtocol.md (frozen 2026-10-21): the spheres of action and the
values on the animal tales, reported and not judged, as their first looks were.

  python parityReports.py selftest   the table-backed spheres reader must equal Spheres/explore.py's on the wondertales
  python parityReports.py dry        counts only: stories per corpus, acts per genre, per transcriber
  python parityReports.py run        writes Data/Parity/spheres-animal.txt, spheres-animal-strict.txt, values-animal.txt

Each runs the first look's own main(), unchanged, with only its reader and its output folder replaced:
Spheres/explore.py on the animal tales beside the wondertales on card C (and the strict reading, the villain's
sphere without struggle, as SpheresExplore-strict.txt); Values/explore.py on its three genres and the animal tales'
significance layer (Animal/layers.py's described_animal()).
"""
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, 'Parity')
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'Animal'))
import importlib.util  # noqa: E402
import tables as DT  # noqa: E402


def load(name, path):
    """the two first looks share the module name explore, so each is loaded from its own path"""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SX = load('spheres_explore', os.path.join(ROOT, 'Spheres', 'explore.py'))
VX = load('values_explore', os.path.join(ROOT, 'Values', 'explore.py'))
import layers as LY  # noqa: E402

TS = SX.TS
PATS = {'tale-U': ['Afanasyev/transcriptions/U/%s/b*/Notes.txt'], 'tale-C': ['Afanasyev/transcriptions/C/%s/b*/Notes.txt'],
        'animal': ['AnimalTales/transcriptions/%s/b*/Notes.txt']}


def read_tables(L, corpora):
    """Spheres/explore.py's read() from the normalized tables: {corpus: {story: [(function, performer, undergoer)]}}"""
    out = {}
    for g in corpora:
        st = collections.OrderedDict()
        for r in DT.files('functions', PATS[g], L):
            base = DT.local(r['story'])
            if not re.match(r'^([PFA]\d{2}|L\d-\d{3})', base):
                continue
            st.setdefault(base, collections.OrderedDict()).setdefault(r['version'] or '1', []).append(
                (TS.base(r['raw']), r['performer'].strip(), r['undergoer'].strip()))
        out[g] = {s: [e[:3] for x in SX.first_reading(vs) for e in SX.expand(*x)] for s, vs in st.items()}
    return out


def selftest():
    ok = True
    for L in 'AB':
        old, new = SX.read(L)['tale'], read_tables(L, ['tale-U'])['tale-U']
        same = list(old.items()) == list(new.items())
        ok &= same
        print('self-test %s spheres reader, wondertales card U: %d stories, %d entries, %s' % (
            L, len(new), sum(map(len, new.values())), 'IDENTICAL' if same else 'DIFFERS'))
    print('PARITY SELF-TEST PASSES' if ok else 'PARITY SELF-TEST FAILS')
    return ok


def animal_values():
    return {L: [x for xs in LY.described_animal()[L].values() for x in xs] for L in 'AB'}


def dry():
    for L in 'AB':
        d = read_tables(L, ['animal', 'tale-C'])
        print('dry run %s spheres: animal tales %d stories, wondertales card C %d stories' % (L, len(d['animal']), len(d['tale-C'])))
    E, A = VX.entries(), animal_values()
    for L in 'AB':
        print('dry run %s values: acts with significance, %s, animal %d' % (L, ', '.join('%s %d' % (g, len(E[L][g])) for g in VX.GENRES), len(A[L])))


def run():
    os.makedirs(OUT, exist_ok=True)
    # report 10, the spheres
    SX.CORPORA = collections.OrderedDict([('animal', None), ('tale-C', None)])
    SX.read = lambda L: read_tables(L, ['animal', 'tale-C'])
    SX.HERE = OUT
    for name, villain in (('spheres-animal.txt', None), ('spheres-animal-strict.txt', {'A', 'Pr'})):
        saved = SX.SPHERES['villain']
        if villain:
            SX.SPHERES['villain'] = villain
        SX.OUT[:] = []
        SX.main()
        SX.SPHERES['villain'] = saved
        os.replace(os.path.join(OUT, 'SpheresExplore.txt'), os.path.join(OUT, name))
    # report 11, the values
    base = VX.entries
    A = animal_values()

    def with_animal():
        E = base()
        for L in 'AB':
            E[L]['animal'] = A[L]
        return E
    VX.entries = with_animal
    VX.GENRES = VX.GENRES + ('animal',)
    VX.HERE = OUT
    VX.OUT[:] = []
    VX.main()
    os.replace(os.path.join(OUT, 'ValuesExplore.txt'), os.path.join(OUT, 'values-animal.txt'))


if __name__ == '__main__':
    a = sys.argv[1:]
    cmds = {'selftest': selftest, 'dry': dry, 'run': run}
    if len(a) == 1 and a[0] in cmds:
        cmds[a[0]]()
    else:
        sys.exit(__doc__)
