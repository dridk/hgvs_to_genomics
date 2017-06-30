
#!/usr/bin/env/ python

import gzip
import re
import argparse


parser = argparse.ArgumentParser(description='Convert HGSV Snp (only) to genomics coordinate')
parser.add_argument("-r", "--refGene", dest="refGene", help="Path to refGene (txt.gz)", metavar="FILE")
parser.add_argument("-s", "--snp", dest="hgvs", help="HGVS snp (NM_001277962:c.1595G>A)")

args = parser.parse_args()


REFGENE=args.refGene
HGVS =args.hgvs


m = re.search("(?P<transcript>.+):c.(?P<pos>\d+)(?P<ref>\w)>(?P<alt>\w)", HGVS)

transcript = m.group("transcript")
pos = int(m.group("pos"))
ref = m.group("ref")
alt = m.group("alt")



# Search Transcripts 
with gzip.open(REFGENE, 'r') as f:
    for line in f:
        row = line.decode().rstrip().split("\t")

        if row[1] == transcript:
            selection = row
            break

chromosome = selection[2]
cdsStart   = int(selection[6])
cdsEnd     = int(selection[7])
exonCount  = int(selection[8])
exonStarts = selection[9].split(",")
exonEnd    = selection[10].split(",")
exons      = [(int(exonStarts[i]), int(exonEnd[i])) for i in range(exonCount)]


cpos = 0

for i in range(0, len(exons)):
    exon = exons[i]
    for st in range(exon[0], exon[1]):
        if cpos > 0 and cpos <= cdsEnd:
            cpos += 1  

        if st == cdsStart:
            cpos = 1

        if cpos == pos:
            pos_genomic = st + 1
            break

print(chromosome,pos_genomic,ref,alt, sep=":")






#print(exonCount)




