#!/usr/bin/env python3
"""
extract.py -- Frazer's translation of Apollodorus, text only.

Reads the Perseus TEI files in source/ and writes one line per section,
"citation | text", with every <note> (Frazer's commentary) removed and its
tail kept. Library sections are cited book.chapter.section, Epitome
sections E.chapter.section, as Perseus cites them. A <gap> in the text is
written [...].
"""
import re
import xml.etree.ElementTree as ET

TEI = '{http://www.tei-c.org/ns/1.0}'


def text_of(el):
    out = [el.text or '']
    for ch in el:
        tag = ch.tag.replace(TEI, '')
        if tag == 'note':
            pass
        elif tag == 'gap':
            out.append(' [...] ')
        else:
            out.append(text_of(ch))
        out.append(ch.tail or '')
    return ''.join(out)


def sections(path, prefix):
    root = ET.parse(path).getroot()
    body = root.find('.//' + TEI + 'body')
    rows = []

    def walk(el, path_n):
        for ch in el:
            if ch.tag != TEI + 'div':
                continue
            sub = ch.get('subtype')
            n = path_n + ([ch.get('n')] if sub in ('book', 'chapter', 'section') else [])
            if sub == 'section':
                txt = re.sub(r'\s+', ' ', text_of(ch)).strip()
                rows.append((prefix + '.'.join(n), txt))
            else:
                walk(ch, n)
    walk(body, [])
    return rows


if __name__ == '__main__':
    for src, prefix, out in (('source/tlg0548.tlg001.perseus-eng2.xml', '', 'Library.txt'),
                             ('source/tlg0548.tlg002.perseus-eng2.xml', 'E.', 'Epitome.txt')):
        rows = sections(src, prefix)
        with open(out, 'w', encoding='utf-8') as fh:
            for c, t in rows:
                fh.write('%s | %s\n' % (c, t))
        words = sum(len(t.split()) for _, t in rows)
        print(out, len(rows), 'sections', words, 'words')
