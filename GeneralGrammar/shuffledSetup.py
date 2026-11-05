"""shuffledSetup.py -- ShuffledProtocol.md (frozen 2026-11-04): batches, key, rules, prompts, in TaleCoding under lines/. The key stays here."""
import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
TC = 'C:/Users/Steve1/TaleCoding'
SEED = 20261104
BATCHES = 6
TITLE = {'wonder': 'Russian folktales', 'east': 'East Asian tales'}


def rd(p):
    return open(p, encoding='utf-8', newline='').read().replace('\r\n', '\n')


def wr(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8', newline='\n').write(t)


def rules():
    pk = json.load(open(os.path.join(HERE, 'PilotKey.json'), encoding='utf-8'))
    k = pk['symbols']
    s = rd(os.path.join(TC, 'wonder/Rules.md'))
    card = s[s.index('| Symbol | What happens |'):s.index('## Transcription formats')].rstrip()
    return """# Coding rules: single events

You will code events from tales, one line at a time. Each line stands alone. Work only from these rules and your lines. Do not open other files or search the web. Where a rule leaves you unsure, mark the line `?`; do not invent a rule.

**Code each line by itself.** The lines come from many tales, in no order. Do not try to work out which lines belong together, or what came before or after.

**Each act in an event gets one entry: a symbol from the card, or X.** A symbol stands for an act of a character, defined from the point of view of its significance for the course of the action. Most events narrate one act and get one entry. Where a line narrates two or more distinct acts, give each act that fits a symbol its own entry, in the order the line gives them. A line none of whose acts fits a symbol gets one X.

**Assign the symbol whoever performs it.** The acts on the card are stable elements, independent of how and by whom they are fulfilled. A harmful act by the hero is judged like any other. Read "hero" and "villain" as the roles an act gives, not as fixed characters. Each line names its tale's hero.

**When in doubt between a symbol and X, write X.** A high share of X is a finding, not a failure.

**An act only threatened or intended, and not carried out, is X.**

**A request or demand is the asker's want, not a villainy.** Until something harmful is actually done, a request or demand is the asker's lack (%s).

**The hero asking another for help is not %s.** The answer to it is %s when help is given and %s− when it is refused.

**A minus marks a negative result:** %s− for a test the hero fails, %s− where nothing is given, %s− where the hero loses the fight, and likewise on any symbol. Use the minus sign − (U+2212).

## The card

%s

## Format

Write one line for each of your lines, in the order given:

```
e0000 | <entries, separated by spaces, or X> | <? if unsure, or -> | <a note of at most six words, or ->
```

Write nothing else in the file. Your report: only the identifiers of any lines you could not code, then the two closing lines your prompt asks for.
""" % (k['a'], k['D'], k['F'], k['F'], k['E'], k['F'], k['I'], card)


def main():
    key = {}
    rng = random.Random(SEED)
    ids = rng.sample(range(1000, 9999), 900)
    pos = 0
    r = rules()
    wr(os.path.join(TC, 'lines/Rules.md'), r)
    wr(os.path.join(HERE, 'ShuffledRules.md'), r)
    pk = json.load(open(os.path.join(HERE, 'PilotKey.json'), encoding='utf-8'))
    stages = []
    for name in ('wonder', 'east'):
        back = {v: k for k, v in pk['tales'][name].items()}
        heroes = {}
        for l in rd(os.path.join(TC, name, 'Heroes.txt')).splitlines():
            p = l.split(' | ')
            heroes[p[0]] = p[1].replace('hero: ', '').strip()
        by = {}
        for l in rd(os.path.join(TC, name, 'Events.txt')).splitlines():
            p = l.split(' | ', 2)
            by.setdefault(p[0], []).append((int(p[1]), p[2]))
        bat = [[] for _ in range(BATCHES)]
        for t in sorted(by):
            st = rng.randrange(BATCHES)
            for i, (e, text) in enumerate(sorted(by[t])):
                eid = 'e%04d' % ids[pos]
                pos += 1
                key[eid] = [name, back[t], e]
                bat[(st + i) % BATCHES].append('%s | hero: %s | %s' % (eid, heroes[t], text))
        for b, lines in enumerate(bat):
            rng.shuffle(lines)
            wr(os.path.join(TC, 'lines', name, 'batch%d.txt' % (b + 1)), '\n'.join(lines) + '\n')
            for rr in 'AB':
                wr(os.path.join(TC, 'prompts', 'lines-%s-%s%d.txt' % (name, rr, b + 1)),
                   "You are coding single events from tales with a card. You start with no background on the project, and you should not look for any.\n\n"
                   "Read lines/Rules.md in this repository in full and follow it exactly. Your lines are in lines/%s/batch%d.txt. Open only those two files and your own output folder. Do not open, list or search anything else in this repository, and do not search the web.\n\n"
                   "Write one file, and nothing else, lines/%s/coded/%s/b%d/Coded.txt (create the folder), in the rules' format, one line for each of your lines.\n\n"
                   "Then reply with: the identifiers of any lines you could not code; then one line saying whether the card reminded you of any published scheme, and if so whose; then one line saying whether you could tell where events fell in their tales.\n" % (name, b + 1, name, rr, b + 1))
        stages.append(name)
    run = rd(os.path.join(TC, 'RUN.md')).rstrip('\n')
    if 'lines-wonder' not in run:
        rows = ''.join("| `lines-%s` | `prompts/lines-%s-A1.txt` to `-A6`, `-B1` to `-B6` | `-A`: Opus; `-B`: Sonnet | `lines/%s/coded/<A or B>/b<N>/Coded.txt` | `Report.md` in that folder | `run-lines-%s` |\n" % (n, n, n, n) for n in stages)
        run = run.replace("\n1. Work from the latest", rows + "\n1. Work from the latest", 1) if False else run
        a = run.index('\n\n1. Work from')
        run = run[:a] + '\n' + rows.rstrip('\n') + run[a:]
        wr(os.path.join(TC, 'RUN.md'), run + '\n')
    json.dump(key, open(os.path.join(HERE, 'ShuffledKey.json'), 'w', encoding='utf-8'), indent=0)
    print('events', len(key), {n: [len(rd(os.path.join(TC, 'lines', n, 'batch%d.txt' % (b + 1))).splitlines()) for b in range(BATCHES)] for n in stages})


if __name__ == '__main__':
    main()
