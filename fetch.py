#!/usr/bin/env python3

import os
import sys
import xml.etree.ElementTree as ET
from Bio import Entrez

Entrez.email = "kyclark@email.arizona.edu"
dbname = "BioSample"

args = sys.argv[1:]

if len(args) != 1:
    print('Usage: {} ACCLIST'.format(os.path.basename(sys.argv[0])))
    sys.exit(1)

acclist = args[0]

for i, term in enumerate(open(acclist)):
    term = term.rstrip()
    print('{:4}: {}'.format(i+1, term), file=sys.stderr)
    handle = Entrez.esearch(db=dbname, term=term, idtype="id")
    result = Entrez.read(handle)
    handle.close()

    if len(result['IdList']) == 1:
        id = result['IdList'][0]
        #print('{} => {}'.format(term, id))
        fetch = Entrez.efetch(db=dbname,
                              id=id,
                              retmode="xml",
                              rettype="full")
        xml = ''.join(fetch.readlines())
        #print(xml)
        tree = ET.fromstring(xml)
        orgs = tree.findall('BioSample/Description/Organism')

        if orgs:
            org = orgs[0].attrib
            tax_id = org['taxonomy_id']
            tax_fetch = Entrez.efetch(db="taxonomy",
                                      id=tax_id,
                                      retmode="xml",
                                      rettype="full")
            tax_xml = ET.fromstring(''.join(tax_fetch.readlines()))
            lineage = tax_xml.findall('Taxon/Lineage')[0]
            print('\t'.join([term, lineage.text]))
    else:
        print('"{}" not found'.format(term), file=sys.stderr)

print('Done', file=sys.stderr)
