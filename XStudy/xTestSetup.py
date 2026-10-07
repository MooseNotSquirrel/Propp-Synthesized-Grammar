#!/usr/bin/env python3
"""
xTestSetup.py -- the X study's stage 5 material (XStudyProtocol.md): the
held-out stories, the genres' rules with the candidate acts added, and the
prompts, written into Story Language/XStudy/test/ and prompts/.

  python xTestSetup.py

The rules are each genre's rules as the original transcriptions used them,
unchanged, with one section inserted before "## Transcription formats": the
candidate acts of Candidates.md and their rule of use. The transcribers'
workspace holds no original transcription.
"""
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PARENT = os.path.dirname(ROOT)
X = os.path.join(PARENT, 'XStudy')
T = os.path.join(X, 'test')
SPLIT = {l.split('|')[0].strip(): [int(x) for x in l.split('|')[1].split()]
         for l in open(os.path.join(ROOT, 'Calibration', 'Split.txt'), encoding='utf-8') if '|' in l}
MODELS = {'A': 'transcriber A', 'B': 'transcriber B'}


def candidate_section():
    table = [l.rstrip('\n') for l in open(os.path.join(HERE, 'Candidates.md'), encoding='utf-8') if l.startswith('|')]
    return '\n'.join([
        '## Candidate acts',
        '',
        '**In this run, sixteen candidate acts stand beside Propp\'s functions.**',
        'They are not Propp\'s functions; they are kinds of act that earlier readings of other stories found in events where no function fitted.',
        'Write a candidate act only for an act that none of the functions on the card fits, as the card defines them.',
        'An act that a function fits takes the function, never a candidate act.',
        'This changes one rule of Stage 3: an event none of whose acts fulfills a function, but one of whose acts is a candidate act, takes the candidate act\'s symbol instead of X.',
        'An event none of whose acts is a function or a candidate act is X, as before.',
        'A candidate act is written like a function: its symbol in the symbol field, marked Y or N for whether it matters, with its note quoting the text; in the stream it stands where its event stands.',
        '',
    ] + table + ['', ''])


def rules(src, dst):
    text = open(src, encoding='utf-8').read()
    i = text.index('## Transcription formats')
    open(dst, 'w', encoding='utf-8', newline='\n').write(text[:i] + candidate_section() + text[i:])


def subset(src, dst, ids):
    with open(dst, 'w', encoding='utf-8', newline='\n') as out:
        for line in open(src, encoding='utf-8'):
            if line.split('|')[0].strip() in ids:
                out.write(line)


def prompt(name, text):
    open(os.path.join(X, 'prompts', name), 'w', encoding='utf-8', newline='\n').write(text)


def tale():
    d = os.path.join(T, 'tale')
    os.makedirs(os.path.join(d, 'tales'), exist_ok=True)
    af = os.path.join(PARENT, 'Afanasyev')
    rules(os.path.join(af, 'AfanasyevRules-U.md'), os.path.join(d, 'AfanasyevRules-X.md'))
    ids = ['A%03d' % t for t in SPLIT['test']]
    for i in ids:
        shutil.copy(os.path.join(af, 'tales', i + '.txt'), os.path.join(d, 'tales', i + '.txt'))
    subset(os.path.join(af, 'Events.txt'), os.path.join(d, 'Events.txt'), set(ids))
    subset(os.path.join(af, 'Heroes.txt'), os.path.join(d, 'Heroes.txt'), set(ids))
    batches = {'t1': ids[:12], 't2': ids[12:]}
    for L in 'AB':
        for b, bi in batches.items():
            files = ', '.join('test/tale/tales/%s.txt' % i for i in bi)
            prompt('test-tale-%s-%s.txt' % (L, b), (
                "You are transcribing some tales from Aleksandr Afanasyev's collection of Russian folktales into Vladimir Propp's notation for the functions of the folktale. You start with no background on the project, and you should not look for any.\n\n"
                "Read test/tale/AfanasyevRules-X.md in this repository first, in full, and follow it exactly; its definitions card is your guide to Propp's functions, and its section \"Candidate acts\" adds sixteen acts that are not Propp's. Your tales are these %d, one per file, read in their original language: %s. Their events are in test/tale/Events.txt and each tale's hero in test/tale/Heroes.txt.\n\n"
                "Your task is Stage 3, transcription, for these tales only, under the rules as the section \"Candidate acts\" amends them. For each, read the whole tale first. Then write the entries the rules require for each of its listed events, in the listed order, keeping the listed hero, each marked Y or N for whether it matters to the course of the tale. Where test/tale/Heroes.txt names more than one hero, transcribe the tale once for each, with identifiers suffixed /1, /2, and so on, in the order named.\n\n"
                "Open only test/tale/AfanasyevRules-X.md, your tale files, test/tale/Events.txt, test/tale/Heroes.txt and your own output folder. Do not open, list or search any other file or folder in this repository, in particular nothing under test/tale/transcriptions/ but your own folder. Do not search the web, and do not use any published analysis of these tales in Propp's terms. You are transcriber %s.\n\n"
                "Write two files, and nothing else, in test/tale/transcriptions/%s/%s/ (create it): Streams.txt and Notes.txt, in the formats of the rules' section \"Transcription formats\". Keep any working file inside that folder, and delete it before you finish. Every note quotes the words of the text its entry rests on, in the original language.\n\n"
                "Then reply with the report the rules' last section asks for: every place where a rule left you unsure what to write, with the tale and event. Do not summarize results or comment on how well Propp fits.\n"
            ) % (len(bi), files, L, L, b))
    return {b: len(bi) for b, bi in batches.items()}


def fable():
    d = os.path.join(T, 'fable')
    os.makedirs(d, exist_ok=True)
    fa = os.path.join(PARENT, 'Fables')
    rules(os.path.join(fa, 'AesopRules.md'), os.path.join(d, 'AesopRules-X.md'))
    batches = {}
    for i, b in enumerate(('b1', 'b2', 'b3', 'b4'), 1):
        m = re.search(r'these fables only: ([^.]*)\.', open(os.path.join(fa, 'prompts', 'transcribe-A-%s.txt' % b), encoding='utf-8').read())
        batches['t%d' % i] = [x.strip() for x in m.group(1).split(',')]
    ids = {x for v in batches.values() for x in v}
    for f in ('Fables.txt', 'Events.txt', 'Heroes.txt'):
        subset(os.path.join(fa, f), os.path.join(d, f), ids)
    for L in 'AB':
        for b, bi in batches.items():
            prompt('test-fable-%s-%s.txt' % (L, b), (
                "You are transcribing some of Aesop's fables, in George Fyler Townsend's 1867 translation, into Vladimir Propp's notation for the functions of the folktale. You start with no background on the project, and you should not look for any.\n\n"
                "Read test/fable/AesopRules-X.md in this repository first, in full, and follow it exactly; its definitions card is your guide to Propp's functions, and its section \"Candidate acts\" adds sixteen acts that are not Propp's. The fables are in test/fable/Fables.txt, one per line as \"identifier | title | text\". The events of each fable are in test/fable/Events.txt, and each fable's hero and moral in test/fable/Heroes.txt.\n\n"
                "Your task is Stage 3, transcription, for these fables only, under the rules as the section \"Candidate acts\" amends them: %s. For each, read the whole fable first. Then write the entries the rules require for each of its listed events, in the listed order, keeping the listed hero, each marked Y or N for whether it matters to the course of the fable. Where test/fable/Heroes.txt names more than one hero, transcribe the fable once for each, with identifiers suffixed /1, /2, and so on, in the order named.\n\n"
                "Open only test/fable/AesopRules-X.md, test/fable/Fables.txt, test/fable/Events.txt, test/fable/Heroes.txt and your own output folder. Do not open, list or search any other file or folder in this repository, in particular nothing under test/fable/transcriptions/ but your own folder. Do not search the web, and do not use any published analysis of these fables in Propp's terms. You are transcriber %s.\n\n"
                "Write two files, and nothing else, in test/fable/transcriptions/%s/%s/ (create it): Streams.txt and Notes.txt, in the formats of the rules' section \"Transcription formats\". Keep any working file inside that folder, and delete it before you finish. Every note quotes the words of the text its entry rests on.\n\n"
                "Then reply with the report the rules' last section asks for: every place where a rule left you unsure what to write, with the fable and event. Do not summarize results or comment on how well Propp fits.\n"
            ) % (', '.join(bi), L, L, b))
    return {b: len(bi) for b, bi in batches.items()}


def tragedy():
    d = os.path.join(T, 'tragedy')
    tr = os.path.join(PARENT, 'Tragedy')
    os.makedirs(d, exist_ok=True)
    rules(os.path.join(tr, 'TragedyRules.md'), os.path.join(d, 'TragedyRules-X.md'))
    order = {l.split('|')[0].strip(): l.split('|')[2].strip() + "'s " + l.split('|')[3].strip()
             for l in open(os.path.join(ROOT, 'Tragedy', 'PlayOrder.txt'), encoding='utf-8') if l.strip()}
    plays = ['P%02d' % i for i in range(17, 33)]
    for p in plays:
        os.makedirs(os.path.join(d, 'plays', p), exist_ok=True)
        for f in ('Text.txt', 'Events.txt', 'Cast.txt', 'Hero.txt'):
            shutil.copy(os.path.join(tr, 'plays', p, f), os.path.join(d, 'plays', p, f))
    batches = {'t%d' % (i + 1): plays[2 * i:2 * i + 2] for i in range(8)}
    for L in 'AB':
        for b, bi in batches.items():
            names = ' and '.join('%s (%s)' % (order[p], p) for p in bi)
            files = ', '.join('test/tragedy/plays/%s/Text.txt, Events.txt, Cast.txt and Hero.txt' % p for p in bi)
            prompt('test-tragedy-%s-%s.txt' % (L, b), (
                "You are transcribing two Greek plays, %s, in English translation, into Vladimir Propp's notation for the functions of the folktale. You start with no background on the project, and you should not look for any.\n\n"
                "Read test/tragedy/TragedyRules-X.md in this repository first, in full, and follow it exactly; its definitions card is your guide to Propp's functions, and its section \"Candidate acts\" adds sixteen acts that are not Propp's. Each play is in its folder under test/tragedy/plays/: Text.txt, one speech per line; Events.txt, its events; Cast.txt, its cast; and Hero.txt, its hero. Name every performer and undergoer exactly as the play's Cast.txt names them.\n\n"
                "Your task is Stage 3, transcription, for these two plays only, under the rules as the section \"Candidate acts\" amends them. For each, read the whole play first. Then write the entries the rules require for each listed event, in the listed order, keeping the listed hero, each marked Y or N for whether it matters to the course of the play. Where a Hero.txt names more than one hero, transcribe that play once for each, with identifiers suffixed /1, /2, and so on, in the order named.\n\n"
                "Open only test/tragedy/TragedyRules-X.md, %s, and your own output folder. Do not open, list or search any other file or folder in this repository, in particular nothing under test/tragedy/transcriptions/ but your own folder. Do not search the web, and do not use any published analysis of these plays or their myths in Propp's terms. You are transcriber %s.\n\n"
                "Write two files, and nothing else, in test/tragedy/transcriptions/%s/%s/ (create it): Streams.txt and Notes.txt, in the formats of the rules' section \"Transcription formats\", the two plays one after the other. Keep any working file inside that folder, and delete it before you finish. Every note quotes the words of the text its entry rests on.\n\n"
                "Then reply with the report the rules' last section asks for: every place where a rule left you unsure what to write, with the play and event. Do not summarize results or comment on how well Propp fits.\n"
            ) % (names, files, L, L, b))
    return {b: len(bi) for b, bi in batches.items()}


def main():
    os.makedirs(T, exist_ok=True)
    print('tale', tale())
    print('fable', fable())
    print('tragedy', tragedy())


if __name__ == '__main__':
    sys.exit(main())
