#!/usr/bin/env python
from pandocfilters import toJSONFilter, Str

"""
Pandoc filter that removes links.
"""

def delink(k, v, f, meta):
    if k == 'Link':
        return v[0]

if __name__ == "__main__":
  toJSONFilter(delink)
