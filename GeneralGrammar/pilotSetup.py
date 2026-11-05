"""pilotSetup.py -- sets up CardPilotProtocol.md (frozen 2026-11-04): the draw, the key, cell S's neutral repository and cell H's prompts.
The key stays here, in the keeper's repository, and never enters the readers'. Run: python pilotSetup.py
Writes: PilotDraw.txt, PilotKey.json, and C:/Users/Steve1/TaleCoding/ (cell S, by a seeded shuffle); PilotH/ holds H's prompts, to copy
to the two earlier repositories when a part is cleared to run."""
import json
import os
import random
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PROJ = os.path.dirname(ROOT)
SEED = 20261104
SREPO = 'C:/Users/Steve1/TaleCoding'
CODES = 'Bip Dox Gul Hab Kem Lun Mip Nar Pov Rud Sef Vek Wob Yul Zin Baf Dov Gop Hux Jem Kib Lom Mur Nep Rav Suv Vig Zab Qet Fub Tiv Sog Dek Poz'.split()
CORPORA = {
    'wonder': dict(rules=os.path.join(PROJ, 'Afanasyev/AfanasyevRules-C.md'), tales=os.path.join(PROJ, 'Afanasyev/tales'), events=os.path.join(PROJ, 'Afanasyev/Events.txt'),
                   heroes=os.path.join(PROJ, 'Afanasyev/Heroes.txt'), prefix='T', story='tale', old='C'),
    'east': dict(rules=os.path.join(PROJ, 'ActsRoles/eastasian/TranscribeRules-C.md'), tales=os.path.join(PROJ, 'ActsRoles/eastasian/tales'), events=os.path.join(PROJ, 'ActsRoles/eastasian/Events.txt'),
                 heroes=os.path.join(PROJ, 'ActsRoles/eastasian/Heroes.txt'), prefix='E', story='eastasian', old='C'),
}


def read(p):
    return open(p, encoding='utf-8', newline='').read().replace('\r\n', '\n')


def draw():
    """15 tales of each corpus, from those with at least three function units in both old readers' strings"""
    import csv
    import collections
    csv.field_size_limit(10 ** 9)
    n = collections.Counter()
    for r in csv.DictReader(open(os.path.join(ROOT, 'Data/tables/functions.tsv'), encoding='utf-8', newline=''), delimiter='\t', quoting=csv.QUOTE_NONE):
        c = r['story'].split(':')[0]
        if c in ('tale', 'eastasian') and r['card'] == 'C' and r['function'] != 'X' and r['reader'] in ('A', 'B') and r['version'] in ('', '1'):
            n[(r['story'], r['reader'])] += 1
    out = {}
    for name, c in CORPORA.items():
        ok = sorted({s for s, r in n if s.startswith(c['story'] + ':') and n[(s, 'A')] >= 3 and n[(s, 'B')] >= 3})
        rng = random.Random(SEED)
        rng.shuffle(ok)
        out[name] = sorted(s.split(':', 1)[1] for s in ok[:15])
    return out


def symbols_of(card_rows):
    return [r[0] for r in card_rows]


def card_rows(text):
    a = text.index('| Symbol | Function | What happens |')
    rows = []
    for line in text[a:].split('\n')[2:]:
        if not line.startswith('|'):
            break
        p = [x.strip() for x in line.strip('|').split('|')]
        rows.append((p[0], p[1], p[2]))
    return rows


def key_of(rows):
    syms = symbols_of(rows)
    codes = list(CODES)
    random.Random(SEED).shuffle(codes)
    return dict(zip(syms, codes))


def neutral_rules(text, key, name):
    """H's rules with what points to Propp removed and his symbols coded; each replacement must find its text"""
    k = key

    def rep(a, b, count=1):
        nonlocal text
        assert text.count(a) >= 1 and (count == 0 or text.count(a) == count), a
        text = text.replace(a, b)
    first = text.split('\n')[0]
    rep(first, '# Coding rules: a collection of tales')
    if name == 'wonder':
        rep("from Aleksandr Afanasyev's collection of Russian folktales, read in their original language, into strings of the function symbols Vladimir Propp defined for the folktale.", 'from a collection of Russian folktales, read in their original language, into strings of the symbols on the card below.')
    else:
        rep('into strings of the function symbols Vladimir Propp defined for the folktale.', 'into strings of the symbols on the card below.')
    rep(" in Propp's terms.", '.')
    if name == 'east':
        rep('In the Chinese tales (identifiers beginning C), the collector', 'In the Chinese tales, the collector')
    rep('Transcribe from the text and from the definitions card alone.', 'Code from the text and from the card alone.')
    rep("a short plain paraphrase without Propp's terms.", 'a short plain paraphrase.')
    rep('**Each act in an event gets one entry: a function symbol, or X.**', '**Each act in an event gets one entry: a symbol from the card, or X.**')
    rep('Propp defines a function as "an act of a character, defined from the point of view of its significance for the course of the action" (p.21).', 'A symbol on the card stands for an act of a character, defined from the point of view of its significance for the course of the action.')
    rep('choose by what it causes in the tale, as Propp does (p.67).', 'choose by what it causes in the tale.')
    rep('Propp: "Functions of characters serve as stable, constant elements in a tale, independent of how and by whom they are fulfilled" (p.21).', 'The acts on the card are stable, constant elements in a tale, independent of how and by whom they are fulfilled.')
    rep('Propp: "Each new act of villainy, each new lack creates a new move" (p.92).', 'Each new act of villainy, each new lack creates a new move.')
    rep("**The hero asking another for help is not the donor's function.**", '**The hero asking another for help is not %s.**' % k['D'])
    rep('is the asker\'s lack (a) when', "is the asker's lack (%s) when" % k['a'])
    rep("The hero's request is a when it is where the hero's want is first stated, and X otherwise; the answer to it is F when help is given and F− when it is refused.", "The hero's request is %s when it is where the hero's want is first stated, and X otherwise; the answer to it is %s when help is given and %s− when it is refused." % (k['a'], k['F'], k['F']))
    rep('**Write the bare letter; do not write variety numbers.**', '**Write each symbol as the card gives it.**')
    rep('A minus marks a negative result: E− for a test the hero fails, F− where nothing is given, I− where the hero loses the fight, and likewise on any function whose outcome is negative.', 'A minus marks a negative result: %s− for a test the hero fails, %s− where nothing is given, %s− where the hero loses the fight, and likewise on any symbol whose outcome is negative.' % (k['E'], k['F'], k['I']))
    # the card
    a = text.index('**These definitions, in plain words, stand in for')
    b = text.index('| Symbol | Function | What happens |')
    rows = card_rows(text)
    end = b
    lines = text[b:].split('\n')
    n = 2 + len(rows)
    tail = '\n'.join(lines[n:])
    shuffled = list(rows)
    random.Random(SEED + 1).shuffle(shuffled)
    table = ['| Symbol | What happens |', '|---|---|']
    for s, _, d in shuffled:
        d = d.replace('Not a function;', 'Not an act on this card;')
        d = re.sub(r'[α-ω↑↓]', lambda m: k[m.group(0)], d)
        table.append('| %s | %s |' % (k[s], d))
    text = text[:a] + '\n'.join(table) + '\n' + tail
    rep('A000 | I | 3 | ev 3 | D |', 'A000 | I | 3 | ev 3 | %s |' % k['D'])
    rep('X, perhaps E', 'X, perhaps %s' % k['E'])
    rep('## The definitions card', '## The card')
    rep('Do not summarize the results or comment on how well Propp fits.', 'Do not summarize the results or comment on how well the card fits.')
    # the word itself: "function" goes wherever it stands in the rules
    text = re.sub(r"\bfunctions\b", 'symbols', text)
    text = re.sub(r"\bfunction\b", 'symbol', text)
    text = text.replace('Functions', 'Symbols').replace('Function', 'Symbol').replace('fulfills a symbol', 'fits a symbol')
    return text


def recode_list(path, ids, mp):
    out = []
    for line in read(path).split('\n'):
        t = line.split(' | ')[0].strip()
        if t in ids:
            out.append(mp[t] + line[len(t):])
    return '\n'.join(out) + '\n'


def s_prompt(name, reader, tales, mp):
    what = {'wonder': 'a collection of Russian folktales', 'east': 'two collections of East Asian tales, in English translation'}[name]
    read_as = {'wonder': 'read in their original language', 'east': 'read as they stand'}[name]
    quote = {'wonder': 'in the original language', 'east': 'as the text prints them'}[name]
    files = ', '.join('%s/tales/%s.txt' % (name, mp[t]) for t in tales)
    return ("You are coding some tales from %s into the symbols of a card. You start with no background on the project, and you should not look for any.\n\n"
            "Read %s/Rules.md in this repository first, in full, and follow it exactly; its card is your guide. Your tales are these 15, one per file, %s: %s. Their events are in %s/Events.txt and each tale's hero in %s/Heroes.txt.\n\n"
            "Your task is Stage 3, transcription, for these tales only. For each, read the whole tale first. Then write the entries the rules require for each of its listed events, in the listed order, keeping the listed hero: one entry per act, and one X for an event none of whose acts fits a symbol, each marked Y or N for whether it matters to the course of the tale. Where %s/Heroes.txt names more than one hero, transcribe the tale once for each, with identifiers suffixed /1, /2, and so on, in the order named.\n\n"
            "Open only %s/Rules.md, your tale files, %s/Events.txt, %s/Heroes.txt and your own output folder. Do not open, list or search any other folder in this repository. Do not search the web, and do not use any published analysis of these tales. You are coder %s.\n\n"
            "Write two files, and nothing else, in %s/coded/%s/ (create it): Streams.txt and Notes.txt, in the formats of the rules' section \"Transcription formats\". Keep any working file inside that folder, and delete it before you finish. Every note quotes the words of the text its entry rests on, %s.\n\n"
            "Then reply with the report the rules' last section asks for: every place where a rule left you unsure what to write, with the tale and event. Do not summarize results or comment on how well the card fits. After that report, and only after your files are written, add one last line: whether the card reminded you of any published scheme, and if so whose.\n"
            % (what, name, read_as, files, name, name, name, name, name, name, reader, name, reader, quote))


S_RUN = """# Running a stage

**You are the runner: you start fresh subagents, save what they return, and push it, and you code and judge nothing.**

| Stage | Prompt files | Model | What each writes | Reply saved as | Branch |
|---|---|---|---|---|---|
| `wonder` | `prompts/wonder-A.txt`, `prompts/wonder-B.txt` | `-A`: Opus; `-B`: Sonnet | `wonder/coded/<A or B>/Streams.txt`, `Notes.txt` | `Report.md` in that folder | `run-wonder` |
| `east` | `prompts/east-A.txt`, `prompts/east-B.txt` | `-A`: Opus; `-B`: Sonnet | `east/coded/<A or B>/Streams.txt`, `Notes.txt` | `Report.md` in that folder | `run-east` |

1. Work from the latest `main`. Report the commit you started from.
2. Start one fresh subagent per prompt file, all at once, on the model the table gives, with this whole instruction: `Read prompts/<file> in this repository in full; it is your task. Follow it exactly, and give your final reply in the form it asks for.` If you cannot choose the model, stop and report it; do not run it on another.
3. Save each subagent's final reply word for word where the table says. If one fails or stops early, save what it gave, say so, and do not start it again.
4. Commit by name on the stage's branch and push it. Do not merge.
"""


def h_prompt(name, reader, tales):
    if name == 'wonder':
        files = ', '.join('tales/%s.txt' % t for t in tales)
        t = read(os.path.join(PROJ, 'Afanasyev/prompts/transcribe-C-%s-b1.txt' % reader))
        t = re.sub(r'Your tales are these 15, one per file, read in their original language: [^.]*(?:\.txt, [^.]*)*\.txt\.', 'Your tales are these 15, one per file, read in their original language: %s.' % files, t)
        t = t.replace('transcriptions/C/%s/b1/' % reader, 'transcriptions/PilotH/%s/' % reader)
    else:
        files = ', '.join('eastasian/tales/%s.txt' % t for t in tales)
        t = read(os.path.join(PROJ, 'ActsRoles/prompts/eastasian-transcribe-%s-b1.txt' % reader))
        t = re.sub(r'Your tales are these \d+, one per file, read as they stand: [^.]*(?:\.txt, [^.]*)*\.txt\.', 'Your tales are these 15, one per file, read as they stand: %s.' % files, t)
        t = t.replace('eastasian/transcriptions/%s/b1/' % reader, 'eastasian/transcriptions/PilotH/%s/' % reader)
    return t


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8', newline='\n').write(text)


def review(key):
    """the owner's sheet: the two cards side by side, in S's order, and every changed line of the rules"""
    import difflib
    out = ['# The two cards, for the owner to compare (CardPilotProtocol.md section 2)', '',
           "**Readers in cell S see only the Code and S's definition columns, in this shuffled order.** This sheet, with the key, stays in the keeper's repository.", '',
           '## The card', '', "| Code | His symbol | His name (dropped in S) | Definition in H | Changed in S? |", '|---|---|---|---|---|']
    h = read(CORPORA['wonder']['rules'])
    srules = read(os.path.join(SREPO, 'wonder', 'Rules.md'))
    defs = {s: d for s, _, d in card_rows(h)}
    names = {s: n for s, n, _ in card_rows(h)}
    a = srules.index('| Symbol | What happens |')
    for line in srules[a:].split('\n')[2:]:
        if not line.startswith('|'):
            break
        code, d = [x.strip() for x in line.strip('|').split('|')]
        sym = next(k for k, v in key.items() if v == code)
        out.append('| %s | %s | %s | %s | %s |' % (code, sym, names[sym], defs[sym], 'same' if d == defs[sym] else 'S: ' + d))
    for name, c in CORPORA.items():
        out += ['', '## Every other line changed: %s' % name, '']
        hl = read(c['rules']).split('\n')
        sl = read(os.path.join(SREPO, name, 'Rules.md')).split('\n')
        b = hl.index('## The definitions card')
        e = next(i for i, l in enumerate(hl) if l.startswith('## Transcription formats'))
        hx = hl[:b] + hl[e:]
        b2 = sl.index('## The card')
        e2 = next(i for i, l in enumerate(sl) if l.startswith('## Transcription formats'))
        sx = sl[:b2] + sl[e2:]
        for l in difflib.ndiff(hx, sx):
            if l.startswith('- '):
                out.append('- **H:** ' + l[2:])
            elif l.startswith('+ '):
                out.append('- **S:** ' + l[2:])
    write(os.path.join(HERE, 'PilotCardReview.md'), '\n'.join(out) + '\n')


def main():
    d = draw()
    rows = card_rows(read(CORPORA['wonder']['rules']))
    key = key_of(rows)
    assert len(set(key.values())) == len(key) == len(rows)
    ids = {}
    for name, c in CORPORA.items():
        ids[name] = {t: '%s%02d' % (c['prefix'], i + 1) for i, t in enumerate(random.Random(SEED + 2).sample(d[name], len(d[name])))}
    json.dump({'symbols': key, 'tales': ids}, open(os.path.join(HERE, 'PilotKey.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    write(os.path.join(HERE, 'PilotDraw.txt'), '# PilotDraw.txt -- 15 tales each, seed %d, before any coding\n' % SEED + '\n'.join('%s: %s' % (n, ' '.join(v)) for n, v in d.items()) + '\n')
    write(os.path.join(SREPO, 'README.md'), '# Tale coding\n\nCoding tales with a card. Stages are in RUN.md.\n')
    write(os.path.join(SREPO, 'RUN.md'), S_RUN)
    for name, c in CORPORA.items():
        mp = ids[name]
        write(os.path.join(SREPO, name, 'Rules.md'), neutral_rules(read(c['rules']), key, name))
        write(os.path.join(SREPO, name, 'Events.txt'), recode_list(c['events'], set(mp), mp))
        write(os.path.join(SREPO, name, 'Heroes.txt'), recode_list(c['heroes'], set(mp), mp))
        for t, new in mp.items():
            lines = read(os.path.join(c['tales'], t + '.txt')).split('\n')
            head = lines[0].split(' | ')
            assert head[0].strip() == t, t
            lines[0] = '%s | %s | -' % (new, head[1].strip())
            write(os.path.join(SREPO, name, 'tales', new + '.txt'), '\n'.join(lines))
        for r in 'AB':
            write(os.path.join(SREPO, 'prompts', '%s-%s.txt' % (name, r)), s_prompt(name, r, sorted(mp), mp))
            write(os.path.join(HERE, 'PilotH', '%s-%s.txt' % (name, r)), h_prompt(name, r, d[name]))
    review(key)
    print('written', {k: len(v) for k, v in d.items()})


if __name__ == '__main__':
    main()
