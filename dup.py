#!/usr/bin/env python3
"""docstring"""

import os
import sys

args = sys.argv[1:]

if len(args) != 2:
    print('Usage: {} ORIGINAL RESULT'.format(os.path.basename(sys.argv[0])))
    sys.exit(1)

original, result = args[0], args[1]

taxa = {}
for line in open(result):
    vals = line.split('; ')
    tax_id = vals[0]
    taxa[tax_id] = line

for line in open(original):
    tax_id = line.rstrip()
    print(taxa[tax_id], end='')
