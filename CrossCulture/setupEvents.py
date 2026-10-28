#!/usr/bin/env python3
"""
setupEvents.py -- the event-list stages of the two new corpora (CrossCultureProtocol.md section 3: every layer from the start,
as the animal tales were run), set up in Propp-ActsRoles: native-events and eastasian-events.

  python setupEvents.py dry      say what would be written, and change nothing
  python setupEvents.py write    write it (refused if a file it writes exists with different content)
  python setupEvents.py latin dry|write   the rule on Latin passages, and the stage native-latin relisting T01, O09, O19
  python setupEvents.py merge    join each corpus's checked batches into <corpus>/Events.txt and Heroes.txt
  python setupEvents.py merge latin   join native-latin's relisted T01, O09, O19 into native/Events.txt and Heroes.txt

Modelled on the stage animal-events (2026-10-20): one reader on Opus a batch, three batches of 17, 17 and 16 tales; the
rules file is animal/ListRules.md, changed only where the new corpora differ, as each change below says. Writes:
  ActsRoles/<native or eastasian>/tales/<id>.txt   each tale of tales/ in its corpus repository, its header line in the
                                                   animal tales' form "identifier | title | revision", the revision naming
                                                   the source file and its lines; the keeper's provenance lines dropped
  ActsRoles/<native or eastasian>/ListRules.md     the rules
  ActsRoles/prompts/<native or eastasian>-events-e1.txt to -e3.txt
  ActsRoles/RUN.md                                 the two stages added, set up and not cleared to run
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SL = os.path.dirname(os.path.dirname(HERE))
AR = os.path.join(SL, 'ActsRoles')
CORPORA = {
    'native': {'repo': 'NativeAmerican', 'ids': ['T%02d' % i for i in range(1, 26)] + ['O%02d' % i for i in range(1, 26)],
               'what': 'two collections of Native American narratives, Tlingit (recorded at Sitka) and Omaha and Ponca, in the '
                       'English of their collectors',
               'short': 'two collections of Native American narratives, in English translation',
               'extra': ''},
    'eastasian': {'repo': 'EastAsian', 'ids': ['C%02d' % i for i in range(1, 26)] + ['J%02d' % i for i in range(1, 26)],
                  'what': 'two collections of East Asian tales, Chinese (told at Swatow) and Japanese, in the English of their '
                          'collectors',
                  'short': 'two collections of East Asian tales, in English translation',
                  'extra': '\nIn the Chinese tales (identifiers beginning C), the collector tells the tales inside a story of her own, '
                           'about a group of children and their teacher, in which the tales are told. Passages of that story stand '
                           'between the tales and may fall at the end of a tale\'s file. They are not part of the tale: list only the '
                           'tale itself, from its title to its end.\n'},
}
BATCHES = [(0, 17), (17, 34), (34, 50)]
STAGES = {'native': 'native-events', 'eastasian': 'eastasian-events'}

RULES = '''# Rules for listing events: {title}

These rules turn tales from {what}, into lists of their events.
They are fixed before any tale is listed.
Follow them exactly.
Where a rule leaves you unsure what to write, say so in your report; do not invent a rule.

## Where you may look

**Work only from the material you are given.**
Your prompt gives you these rules and the tales you are to work on.
Do not open other files, do not search the web, and do not use any published analysis of these tales.

**Keep each tale at its own length.**
Do not fill in what other versions of a tale add, even when you know them; some tales here are versions of one another, and each is listed as it stands.

**Read each tale as it stands, in English; write in English.**
The tales are English translations, made by collectors of the late nineteenth and early twentieth centuries. Read them as they stand, and do not supply what a translator may have left out.

**Some files carry matter that is not the tale.**
The texts come from scans of printed books. A file may hold the book's page headings and page numbers, captions of its pictures, footnote marks such as [1], and words broken or misspelt by the scanning. These are not part of the tale: pass over them, and read a broken word as the sentence plainly needs it. Where you cannot tell what a passage says, say so in your report.
{extra}
## Listing the events

**An event is a clause that narrates an action or a change of state.**
These are not events:
- descriptions of how things habitually are, such as "the Wolf was always hungry";
- general statements, such as "the tyrant will always find a pretext";
- the moral, wherever it stands.

Speech counts as an event when the speaking is itself an act that the tale turns on: a plea, a promise, a lie, a boast, a refusal, a command.

**Mark the moral apart.**
Some tales end with a general statement of their point, sometimes as the last sentence of the tale, sometimes spoken by a character; most have none.
Record such a statement on its own line as the moral; it is not an event.
A tale with no such statement has no moral line.

**The hero is the character whose fortunes the tale follows.**
In practice, the hero is the character who takes part, as doer or as sufferer, in the most events.
If two characters tie, the hero is the one who takes part in the last event.
If they still tie, write both.

**Event formats.**
`Events.txt` has one line per event: tale identifier, event number, and a short plain paraphrase in everyday words.

```
X000 | 1 | A Mouse runs over a sleeping Lion's face and wakes him
```

`Heroes.txt` has one line per tale: identifier, hero, and the moral, or `-`.

```
X000 | hero: the Mouse | moral: -
```
'''

PROMPT = '''You are listing the events of some tales from {short}. You start with no background on the project, and you should not look for any.

Read {c}/ListRules.md in this repository in full; it is your rules, and you follow them exactly.

Your tales are these {n}, one per file, each beginning with a line "identifier | title | revision": {files}. Read each tale in full, as it stands, then list its events in order, work out its hero by the rule given, and note its moral if it has one.

Open only {c}/ListRules.md and these tale files. Do not open any other file or folder, and do not search the web or use what folklorists or scholars have written about these tales: work from each tale's words.

Write two files, and nothing else, in {c}/events/: Events-e{k}.txt and Heroes-e{k}.txt, in the formats of the rules' section "Event formats", using each tale's identifier (such as {first}). Keep any working file you make inside {c}/events/ and delete it before you finish.

Then reply with a short report: the number of events per tale, each tale's hero, and every place where a rule left you unsure, with the tale and event.
'''


def tale(c, tid):
    """the reader's file: the identifier line, then the tale's text as extract.py cut it"""
    text = open(os.path.join(SL, CORPORA[c]['repo'], 'tales', tid + '.txt'), encoding='utf-8').read().split('\n')
    head = [l for l in text[:4]]
    assert all(l.startswith('# ') for l in head) and text[4] == '', tid
    title = head[0].split('. ', 1)[1]
    m = re.search(r'source/(\S+) .*lines (\d+) to (\d+)', ' '.join(head))
    rev = 'source %s, lines %s to %s' % (m.group(1), m.group(2), m.group(3))
    return '%s | %s | %s\n\n%s' % (tid, title, rev, '\n'.join(text[5:]))


def outputs():
    out = {}
    for c, d in CORPORA.items():
        for tid in d['ids']:
            out[os.path.join(c, 'tales', tid + '.txt')] = tale(c, tid)
        title = 'the Native American tales' if c == 'native' else 'the East Asian tales'
        out[os.path.join(c, 'ListRules.md')] = RULES.format(title=title, what=d['what'], extra=d['extra'])
        for k, (a, b) in enumerate(BATCHES, 1):
            ids = d['ids'][a:b]
            out[os.path.join('prompts', '%s-e%d.txt' % (STAGES[c], k))] = PROMPT.format(
                short=d['short'], c=c, n=len(ids), k=k, first=ids[0], files=', '.join('%s/tales/%s.txt' % (c, t) for t in ids))
    out['RUN.md'] = run_md()
    return out


def run_md():
    t = open(os.path.join(AR, 'RUN.md'), encoding='utf-8').read()
    if 'native-events' in t:
        return t
    reps = [
        ('animal-events, animal-transcribe, animal-acts, animal-free, animal-sig, animal-heroes,',
         'animal-events, animal-transcribe, animal-acts, animal-free, animal-sig, animal-heroes, native-events, eastasian-events,'),
        ('The stage `animal-events` is cleared to run (2026-10-20).\n',
         'The stage `animal-events` is cleared to run (2026-10-20).\n'
         'The stages `native-events` and `eastasian-events` were set up on 2026-10-28 (Propp-Synthesized-Grammar, '
         '`CrossCulture/CrossCultureProtocol.md` and `CrossCulture/setupEvents.py`), and are not yet cleared: they run only at the '
         'owner\'s word. They need nothing from each other and may run in one session.\n'),
        ("| `animal-transcribe` |",
         "| `native-events` | `native-events-e1.txt` to `-e3.txt` | Opus | `native/events/Events-eN.txt`, `native/events/Heroes-eN.txt` | `native/events/Report-eN.md` | `run-native-events` |\n"
         "| `eastasian-events` | `eastasian-events-e1.txt` to `-e3.txt` | Opus | `eastasian/events/Events-eN.txt`, `eastasian/events/Heroes-eN.txt` | `eastasian/events/Report-eN.md` | `run-eastasian-events` |\n"
         "| `animal-transcribe` |"),
        ('for `animal-transcribe`, ',
         'for `native-events`, `native/ListRules.md` and the folder `native/tales/`; for `eastasian-events`, '
         '`eastasian/ListRules.md` and the folder `eastasian/tales/`; for `animal-transcribe`, '),
    ]
    for a, b in reps:
        assert t.count(a) == 1, a
        t = t.replace(a, b)
    return t


def main(mode):
    out = outputs()
    clash = [p for p, s in out.items() if p != 'RUN.md' and os.path.exists(os.path.join(AR, p))
             and open(os.path.join(AR, p), encoding='utf-8').read() != s]
    if clash:
        raise SystemExit('refusing: these exist with different content: %s' % clash)
    for c, d in CORPORA.items():
        print('%s: %d tale files, %d characters in all; the longest %s' % (
            c, len(d['ids']), sum(len(out[os.path.join(c, 'tales', t + '.txt')]) for t in d['ids']),
            max(d['ids'], key=lambda t: len(out[os.path.join(c, 'tales', t + '.txt')]))))
        for k, (a, b) in enumerate(BATCHES, 1):
            ids = d['ids'][a:b]
            print('  %s-e%d: %d tales, %s to %s, %d characters' % (STAGES[c], k, len(ids), ids[0], ids[-1],
                                                                   sum(len(out[os.path.join(c, 'tales', t + '.txt')]) for t in ids)))
    print('files: %d (%s)' % (len(out), ', '.join(sorted({p.split(os.sep)[0] for p in out}))))
    if mode == 'write':
        for p, s in out.items():
            path = os.path.join(AR, p)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, 'w', encoding='utf-8', newline='\n').write(s)
        print('written to %s' % AR)
    else:
        print('dry run: nothing written')


# ---------------------------------------------------------------- the Latin passages (2026-10-28, the owner's ruling)
# Swanton and Dorsey printed some passages in Latin. The readers of native-events paraphrased them politely; the owner ruled
# that they are to be translated instead. The rule is added to native/ListRules.md, and the three tales whose readers
# reported Latin are listed again by a fresh reader in the stage native-latin. The first lists stay on record in events/.
LATIN_TALES = ['T01', 'O09', 'O19']
LATIN_AFTER = 'Read them as they stand, and do not supply what a translator may have left out.\n'
LATIN_RULE = ('\n**Passages in Latin are part of the tale.** (Added 2026-10-28.)\n'
              'The collectors printed some passages in Latin rather than English. Translate each such passage into plain English as '
              'you read it, and list its events as plainly as the rest of the tale, saying in everyday words what happens, without '
              'softening it or leaving it out.\n')
LATIN_PROMPT = PROMPT.replace('Events-e{k}.txt and Heroes-e{k}.txt', 'Events-l1.txt and Heroes-l1.txt')


def latin_outputs():
    rules = open(os.path.join(AR, 'native', 'ListRules.md'), encoding='utf-8').read()
    if LATIN_RULE not in rules:
        assert rules.count(LATIN_AFTER) == 1
        rules = rules.replace(LATIN_AFTER, LATIN_AFTER + LATIN_RULE)
    d = CORPORA['native']
    prompt = LATIN_PROMPT.format(short=d['short'], c='native', n=len(LATIN_TALES), k=1, first=LATIN_TALES[0],
                                 files=', '.join('native/tales/%s.txt' % t for t in LATIN_TALES))
    t = open(os.path.join(AR, 'RUN.md'), encoding='utf-8').read()
    if 'native-latin' not in t:
        reps = [
            ('native-events, eastasian-events,', 'native-events, eastasian-events, native-latin,'),
            ("the same day. They need nothing from each other and may run in one session.\n",
             "the same day. They need nothing from each other and may run in one session.\n"
             "The stage `native-latin` was set up on 2026-10-28 (`CrossCulture/setupEvents.py`): three tales listed again under the "
             "rule on Latin passages added to `native/ListRules.md`. It is not yet cleared: it runs only at the owner's word.\n"),
            ("| `run-eastasian-events` |\n",
             "| `run-eastasian-events` |\n"
             "| `native-latin` | `native-latin-l1.txt` | Opus | `native/events/Events-l1.txt`, `native/events/Heroes-l1.txt` | "
             "`native/events/Report-l1.md` | `run-native-latin` |\n"),
            ('for `eastasian-events`, `eastasian/ListRules.md` and the folder `eastasian/tales/`; ',
             'for `eastasian-events`, `eastasian/ListRules.md` and the folder `eastasian/tales/`; for `native-latin`, '
             '`native/ListRules.md` and the files `native/tales/T01.txt`, `O09.txt` and `O19.txt`; '),
        ]
        for a, b in reps:
            assert t.count(a) == 1, a
            t = t.replace(a, b)
    return {os.path.join('native', 'ListRules.md'): rules, os.path.join('prompts', 'native-latin-l1.txt'): prompt, 'RUN.md': t}


def latin(mode):
    out = latin_outputs()
    for p, s in out.items():
        old = open(os.path.join(AR, p), encoding='utf-8').read() if os.path.exists(os.path.join(AR, p)) else ''
        print('%s: %s' % (p, 'unchanged' if old == s else 'new' if not old else 'changed, %+d characters' % (len(s) - len(old))))
    print('native-latin-l1: %d tales, %s, %d characters' % (len(LATIN_TALES), ', '.join(LATIN_TALES),
                                                            sum(len(tale('native', t)) for t in LATIN_TALES)))
    if mode == 'write':
        for p, s in out.items():
            open(os.path.join(AR, p), 'w', encoding='utf-8', newline='\n').write(s)
        print('written')
    else:
        print('dry run: nothing written')
    return out


# ---------------------------------------------------------------- the joined lists
def merge():
    """<corpus>/Events.txt and Heroes.txt, the batches joined in order, as animal/Events.txt was; the native tales listed again
    in native-latin are left out until that stage is merged, and the first lists stay in events/"""
    for c in CORPORA:
        skip = set(LATIN_TALES) if c == 'native' and not os.path.exists(os.path.join(AR, c, 'events', 'Events-l1.txt')) else set()
        for name in ('Events', 'Heroes'):
            lines = []
            for k in range(1, len(BATCHES) + 1):
                lines += [l.rstrip('\n') for l in open(os.path.join(AR, c, 'events', '%s-e%d.txt' % (name, k)), encoding='utf-8')
                          if l.strip()]
            lines = [l for l in lines if l.split(' |')[0] not in skip]
            if not skip and c == 'native':
                raise SystemExit('the native-latin lists are to be joined by a later command')
            path = os.path.join(AR, c, name + '.txt')
            text = '\n'.join(lines) + '\n'
            if os.path.exists(path) and open(path, encoding='utf-8').read() != text:
                raise SystemExit('refusing to overwrite %s' % path)
            open(path, 'w', encoding='utf-8', newline='\n').write(text)
            print('%s: %d lines, %d tales%s' % (path, len(lines), len({l.split(' |')[0] for l in lines}),
                                               '; left out until relisted: ' + ', '.join(sorted(skip)) if skip else ''))


def merge_latin():
    """native/Events.txt and Heroes.txt rebuilt from the batches in tale order, the lines of T01, O09 and O19 taken from
    native-latin's lists (Events-l1.txt, Heroes-l1.txt) in place of the first lists'; replaces only the 47-tale joined files
    that merge wrote"""
    ev = os.path.join(AR, 'native', 'events')
    for name in ('Events', 'Heroes'):
        first = []
        for k in range(1, len(BATCHES) + 1):
            first += [l.rstrip('\n') for l in open(os.path.join(ev, '%s-e%d.txt' % (name, k)), encoding='utf-8') if l.strip()]
        relisted = [l.rstrip('\n') for l in open(os.path.join(ev, '%s-l1.txt' % name), encoding='utf-8') if l.strip()]
        got = sorted({l.split(' |')[0] for l in relisted})
        if got != sorted(LATIN_TALES):
            raise SystemExit('%s-l1.txt holds %s, not %s' % (name, got, LATIN_TALES))
        path = os.path.join(AR, 'native', name + '.txt')
        held = '\n'.join(l for l in first if l.split(' |')[0] not in LATIN_TALES) + '\n'
        if open(path, encoding='utf-8').read() != held:
            raise SystemExit('refusing: %s is not the 47-tale file that merge wrote' % path)
        by = {}
        for l in first:
            t = l.split(' |')[0]
            if t not in LATIN_TALES:
                by.setdefault(t, []).append(l)
        for l in relisted:
            by.setdefault(l.split(' |')[0], []).append(l)
        lines = [l for t in CORPORA['native']['ids'] for l in by.get(t, [])]
        open(path, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
        print('%s: %d lines, %d tales; %s from native-latin' % (path, len(lines), len(by), ', '.join(LATIN_TALES)))


if __name__ == '__main__':
    a = sys.argv[1:]
    cmds = {('dry',): lambda: main('dry'), ('write',): lambda: main('write'), ('latin', 'dry'): lambda: latin('dry'),
            ('latin', 'write'): lambda: latin('write'), ('merge',): merge, ('merge', 'latin'): merge_latin}
    if tuple(a) not in cmds:
        sys.exit(__doc__)
    cmds[tuple(a)]()
