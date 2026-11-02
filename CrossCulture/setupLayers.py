#!/usr/bin/env python3
"""
setupLayers.py -- the act and free-verb stages of the two new corpora (CrossCultureProtocol.md section 3: every layer from the
start, the instruments unchanged), set up in Propp-ActsRoles: native-acts, eastasian-acts, native-free and eastasian-free.

  python setupLayers.py dry      say what would be written, and change nothing
  python setupLayers.py write    write it (refused if a file it writes exists with different content)

Modelled on animal-acts and animal-free (Animal/layers.py, 2026-10-20): describers A on Opus and B on Sonnet, the batches of the
transcription stages (setupTranscribe.py: four native, three East Asian). The rules are ActsRules.md and free/FreeRules.md,
unchanged; they say nothing of language, which the animal prompts carried. The prompts are animal-acts' and animal-free's
(Animal/layers.py), word for word, but for the corpus, the tales, and their reading: where the animal prompts say the tales are
read in their original language, these give the event rules' reading of these corpora (English as it stands; Latin passages
translated; scanning matter passed over; for the East Asian tales, the collector's frame story not part of the tale), and
notes quote the text as it prints it. Writes the 28 prompts and RUN.md's four stages, set up and not cleared.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'Animal'))
import layers as LY  # noqa: E402
import setupTranscribe as ST  # noqa: E402

AR, CORPORA, BATCHES = ST.AR, ST.CORPORA, ST.BATCHES
LAYERS = {'acts': LY.ACTS_PROMPT, 'free': LY.FREE_PROMPT}
READING = {
    'native': ('They are English translations from scanned books. Where a passage is printed in Latin, '
               'translate it as you read and describe it as plainly as the rest. Page headings, page numbers, captions, '
               'footnote marks and scanning errors are not part of the tale.'),
    'eastasian': ('They are English translations from scanned books. Page headings, page numbers, '
                  'captions, footnote marks and scanning errors are not part of the tale; nor, in the Chinese tales '
                  '(identifiers beginning C), is the collector\'s story of the children and their teacher in which the '
                  'tales are told.'),
}


def stage(c, layer):
    return '%s-%s' % (c, layer)


def prompt(c, layer, L, k, ids):
    t = LAYERS[layer]
    files = ', '.join('%s/tales/%s.txt' % (c, i) for i in ids)
    reps = [('read in their original language: {files}.', 'read as they stand: {files}. ' + READING[c]),
            ('in the original language.', 'as the text prints them.'),
            ('animal/', c + '/')]
    for a, b in reps:
        assert a in t, a
        t = t.replace(a, b)
    return t.format(what=CORPORA[c]['short'], n=len(ids), files=files, L=L, b='b%d' % k)


def run_md():
    t = open(os.path.join(AR, 'RUN.md'), encoding='utf-8').read()
    if 'native-acts' in t:
        return t
    names = [stage(c, layer) for layer in LAYERS for c in CORPORA]
    row = ("| `{s}` | `{s}-A-b1.txt` to `-b{n}`, `{s}-B-b1.txt` to `-b{n}` | `-A-`: Opus; `-B-`: Sonnet | "
           "`{c}/{layer}/<A or B>/<batch>/Notes.txt` | `Report.md` in that folder | `run-{s}` |\n")
    rows = ''.join(row.format(s=stage(c, layer), n=len(BATCHES[c]), c=c, layer=layer) for layer in LAYERS for c in CORPORA)
    inputs = ''.join('for `%s`, `%s`, `%s/Events.txt` and the folder `%s/tales/`; '
                     % (stage(c, layer), 'ActsRules.md' if layer == 'acts' else 'free/FreeRules.md', c, c)
                     for layer in LAYERS for c in CORPORA)
    anchor_list = 'native-transcribe, eastasian-transcribe,'
    anchor_clear = ("and were cleared to run at the owner's word on 2026-11-01. They need nothing from each other and may run "
                    "in one session.\n")
    anchor_row = '| `run-eastasian-transcribe` |\n'
    anchor_in = 'the folder `eastasian/tales/`; for `animal-transcribe`, '
    for a in (anchor_list, anchor_row, anchor_in):
        assert t.count(a) == 1, a
    assert anchor_clear in t
    t = t.replace(anchor_list, anchor_list + ' ' + ', '.join(names) + ',')
    i = t.index(anchor_clear) + len(anchor_clear)
    t = t[:i] + ("The stages %s were set up on 2026-11-02 (`CrossCulture/setupLayers.py`), after the new corpora's "
                 "transcriptions were merged, and are not yet cleared: they run only at the owner's word. They need nothing "
                 "from each other and may run in one session.\n" % ', '.join('`%s`' % n for n in names)) + t[i:]
    t = t.replace(anchor_row, anchor_row + rows)
    t = t.replace(anchor_in, 'the folder `eastasian/tales/`; ' + inputs + 'for `animal-transcribe`, ')
    return t


def outputs():
    out = {}
    for layer in LAYERS:
        for c, d in CORPORA.items():
            for L in 'AB':
                for k, (a, b) in enumerate(BATCHES[c], 1):
                    out[os.path.join('prompts', '%s-%s-b%d.txt' % (stage(c, layer), L, k))] = prompt(c, layer, L, k, d['ids'][a:b])
    out['RUN.md'] = run_md()
    return out


def main(mode):
    out = outputs()
    read = lambda p: open(os.path.join(AR, p), encoding='utf-8').read()
    clash = [p for p, s in out.items() if p != 'RUN.md' and os.path.exists(os.path.join(AR, p)) and read(p) != s]
    if clash:
        raise SystemExit('refusing: these exist with different content: %s' % clash)
    for p in sorted(out):
        old = read(p) if os.path.exists(os.path.join(AR, p)) else ''
        print('%s: %s' % (p, 'unchanged' if old == out[p] else 'new' if not old else 'changed, %+d characters' % (len(out[p]) - len(old))))
    if mode == 'write':
        for p, s in out.items():
            open(os.path.join(AR, p), 'w', encoding='utf-8', newline='\n').write(s)
        print('written to %s' % AR)
    else:
        print('dry run: nothing written')


if __name__ == '__main__':
    a = sys.argv[1:]
    if a not in (['dry'], ['write']):
        sys.exit(__doc__)
    main(a[0])
