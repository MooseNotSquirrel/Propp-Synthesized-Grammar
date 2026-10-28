#!/usr/bin/env python3
"""
setupTranscribe.py -- the transcription stages of the two new corpora, Propp's functions on card C (CrossCultureProtocol.md
section 3), set up in Propp-ActsRoles: native-transcribe and eastasian-transcribe.

  python setupTranscribe.py dry      say what would be written, and change nothing
  python setupTranscribe.py write    write it (refused if a file it writes exists with different content)

Modelled on animal-transcribe (2026-10-20): two blind transcribers, A on Opus and B on Sonnet, three batches each, the
batches of the event lists (setupEvents.py). Writes:
  ActsRoles/<native or eastasian>/TranscribeRules-C.md   animal/AfanasyevRules-C.md with the definitions card and every stage
      unchanged; only its title, its opening sentence and its paragraph on language change, the last taking the event rules'
      wording for these corpora (English as it stands; matter that is not the tale; for the native tales the Latin passages,
      for the East Asian the frame story), with the card's sentence on quoting kept: notes quote the text as it is printed.
  ActsRoles/prompts/<native or eastasian>-transcribe-<A or B>-b1.txt to -b3.txt   animal-transcribe's prompts word for word,
      but for the corpus, the rules' name, the tales and the language.
  ActsRoles/RUN.md   the two stages added, set up and not cleared to run.
"""
import os
import sys

import setupEvents as SE

AR, CORPORA, BATCHES = SE.AR, SE.CORPORA, SE.BATCHES
STAGES = {'native': 'native-transcribe', 'eastasian': 'eastasian-transcribe'}
RULES = 'TranscribeRules-C.md'
OLD_LANG = ('**Read each tale in its original language; write in English.**\n'
            'The tales are in Russian, one in Belarusian and one in a strongly dialectal speech. Read them as they stand. Write your '
            'event lists, entries, notes and reports in English, but where a note quotes the words of the text, quote them in the '
            'original.\n')
LIST_LANG = 'Read them as they stand, and do not supply what a translator may have left out.'


def read(*p):
    return open(os.path.join(AR, *p), encoding='utf-8').read()


def rules(c):
    base = read('animal', 'AfanasyevRules-C.md')
    lr = read(c, 'ListRules.md')
    lang = lr[lr.index('**Read each tale as it stands, in English; write in English.**'):lr.index('## Listing the events')]
    lang = lang.rstrip('\n') + '\n'
    assert lang.count(LIST_LANG) == 1
    lang = lang.replace(LIST_LANG, LIST_LANG + ' Write your entries, notes and reports in English; where a note quotes the '
                                               'words of the text, quote them as the text prints them.')
    title = 'the Native American tales' if c == 'native' else 'the East Asian tales'
    reps = [("# Transcriber rules: Afanasyev's tales in Propp's notation", "# Transcriber rules: %s in Propp's notation" % title),
            ("These rules turn tales from Aleksandr Afanasyev's collection of Russian folktales, read in their original language, into",
             'These rules turn tales from %s, into' % CORPORA[c]['what']),
            (OLD_LANG, lang)]
    for a, b in reps:
        assert base.count(a) == 1, a[:60]
        base = base.replace(a, b)
    return base


def prompt(c, L, k, ids):
    t = read('prompts', 'animal-transcribe-%s-b1.txt' % L)
    first = ', '.join('animal/tales/A%03d.txt' % i for i in range(1, 18))
    reps = [("some tales from Aleksandr Afanasyev's collection of Russian folktales", 'some tales from %s' % CORPORA[c]['short']),
            ('Your tales are these 17, one per file, read in their original language: ' + first,
             'Your tales are these %d, one per file, read as they stand: %s' % (len(ids), ', '.join('%s/tales/%s.txt' % (c, i) for i in ids))),
            ('in the original language.', 'as the text prints them.'),
            ('transcriptions/%s/b1/' % L, 'transcriptions/%s/b%d/' % (L, k)),
            ('AfanasyevRules-C.md', RULES),
            ('animal/', c + '/')]
    for a, b in reps:
        assert a in t, a[:60]
        t = t.replace(a, b)
    return t


def run_md():
    t = read('RUN.md')
    if 'native-transcribe' in t:
        return t
    row = ("| `%s` | `%s-A-b1.txt` to `-b3`, `%s-B-b1.txt` to `-b3` | `-A-`: Opus; `-B-`: Sonnet | "
           "`%s/transcriptions/<A or B>/<batch>/Streams.txt` and `Notes.txt` | `Report.md` in that folder | `run-%s` |\n")
    reps = [('native-events, eastasian-events, native-latin,',
             'native-events, eastasian-events, native-latin, native-transcribe, eastasian-transcribe,'),
            ("It was cleared to run at the owner's word the same day.\n",
             "It was cleared to run at the owner's word the same day.\n"
             "The stages `native-transcribe` and `eastasian-transcribe` were set up on 2026-10-28 (`CrossCulture/setupTranscribe.py`), "
             "after the event lists were joined, and are not yet cleared: they run only at the owner's word. They need nothing from "
             "each other and may run in one session.\n"),
            ('| `run-native-latin` |\n',
             '| `run-native-latin` |\n' + ''.join(row % (STAGES[c], STAGES[c], STAGES[c], c, STAGES[c]) for c in CORPORA)),
            ('`native/ListRules.md` and the files `native/tales/T01.txt`, `O09.txt` and `O19.txt`; ',
             '`native/ListRules.md` and the files `native/tales/T01.txt`, `O09.txt` and `O19.txt`; ' +
             ''.join('for `%s`, `%s/%s`, `%s/Events.txt`, `%s/Heroes.txt` and the folder `%s/tales/`; ' % (STAGES[c], c, RULES, c, c, c)
                     for c in CORPORA))]
    for a, b in reps:
        assert t.count(a) == 1, a[:60]
        t = t.replace(a, b)
    return t


def outputs():
    out = {}
    for c, d in CORPORA.items():
        out[os.path.join(c, RULES)] = rules(c)
        for L in 'AB':
            for k, (a, b) in enumerate(BATCHES, 1):
                out[os.path.join('prompts', '%s-%s-b%d.txt' % (STAGES[c], L, k))] = prompt(c, L, k, d['ids'][a:b])
    out['RUN.md'] = run_md()
    return out


def main(mode):
    out = outputs()
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
