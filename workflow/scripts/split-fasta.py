import argparse
import os
from Bio import SeqIO

parser = argparse.ArgumentParser(description="", 
                                 usage="python %(prog)s --input filename.fasta")
parser.add_argument("-i", "--input",  
                    help="Path to Fasta file",
                    metavar="\b",
                    required=True)

parser.add_argument("-o", "--output",  
                    help="Output directory",
                    metavar="\b",
                    required=True)
args = parser.parse_args()

filenumber=1
numseqs=0

with open(os.path.abspath(args.input)) as handle:
    #print(os.path.abspath(args.input))
    #outpath=list(os.path.split(os.path.abspath(args.input)))[0]
    for record in SeqIO.parse(handle, "fasta"):
        filename_ls=list(os.path.splitext(os.path.basename(args.input)))
        outfilename=filename_ls[0] + "_" + str(filenumber)
        outfilename=outfilename + filename_ls[-1]
        #absoutpath=os.path.join(outpath,outfilename)
        absoutpath=os.path.join(os.path.abspath(args.output),outfilename)
        #print(absoutpath)
        with open(absoutpath, "a") as outfile:
            SeqIO.write(record, outfile, "fasta")
            numseqs +=1 
            if numseqs == 50:
                filenumber+=1
                numseqs = 0 