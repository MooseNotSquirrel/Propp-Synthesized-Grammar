#!/usr/bin/env python3
"""
postHoc.py -- after the verdict: departure to return in Propp's own moves, with the
reader's fault mended. The corpus runner's reducer names departure `up` and return
`down`, which the frozen reader did not map, so the frozen run found no departure in
Propp's moves. Reported, not judged; the frozen result stands.

  python postHoc.py      writes Links/PostHoc.txt
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import links as K  # noqa: E402


def main():
    moves = [[{'up': '↑', 'down': '↓'}.get(t, t) for t in m] for m in K.propp_moves()]
    r = K.Moves(moves).test(('↑',), '↓')
    line = '↑ -> ↓ in Propp\'s moves, the reader mended: %s%s' % (K.fmt(r), '  HOLDS' if K.holds(r) else '')
    open(os.path.join(HERE, 'PostHoc.txt'), 'w', encoding='utf-8', newline='\n').write(
        '# PostHoc.txt -- postHoc.py, after the verdict; reported, not judged.\n\n' + line + '\n')
    print(line)


if __name__ == '__main__':
    main()
