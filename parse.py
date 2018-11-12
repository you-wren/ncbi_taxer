#!/usr/bin/env python3

import sys
from xml.etree.ElementTree import ElementTree

args = sys.argv[1:]

if not args:
    print('Usage: {} TAX.XML'.format(sys.argv[0]))
    sys.exit(1)

file = args[0]
tree = ElementTree()
tree.parse(file)
taxon = list(tree.findall('Taxon'))

if not taxon:
    print('Found no <Taxon> in "{}"'.format(file))
    sys.exit(1)

for tax in taxon:
    tax_id = tax.find('TaxId')
    name = tax.find('ScientificName')
    lineage = tax.find('Lineage')
    print('; '.join([tax_id.text, lineage.text, name.text]))
