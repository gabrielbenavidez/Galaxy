__author__= 'Haibin Guan'
import argparse
import os
import pandas,numpy

"""Script allows you to convert the taxonomy csv file obtained from collapsing certain level taxonomy file in qiime2 and then convert it to percent abundance and transforms it"""
#-----------Command Line Arguments-----------------
parser=argparse.ArgumentParser(description="Script allows you to convert the taxonomy csv file obtained from collapsing certain level taxonomy file in qiime2")
parser.add_argument('-i','--input', help=' Input csv file you want covnert to percentage',required=True)
parser.add_argument('-o','--out', help='Name of output file: jsut the mae e.g., "Percent_taxa-L7"', required=True)#require later
args = parser.parse_args()
o_file=str(args.out)
csvfile=str(args.input) 

temp= pandas.read_table(csvfile)
#print(temp.columns[0])
if("# Constructed from biom file" in temp.columns[0]):
    # -----------open csv file in with pandas and only include patient and bacteria metadata remove all other metadata information -------
    print("Retrieving percent abundance")
    df = pandas.read_table(csvfile, header=1, index_col=0)
    index = [c for c in df.columns]
    dfp = pandas.pivot_table(df, values=index, index='#OTU ID', aggfunc=sum)
    df = dfp.transpose()
    cols = [c for c in df.columns if c[0] == 'k' or c[0] == 't']
    df = df[cols]
else:
    print("Script has been modified from original")
    df = pandas.read_table(csvfile, header=0, index_col=0)
    index = [c for c in df.columns]
    dfp = pandas.pivot_table(df, values=index, index='taxonomy', aggfunc=sum)
    df = dfp.transpose()
    cols = [c for c in df.columns if c[0] == 'k' or c[0] == 't']
    df = df[cols]

#--------------- Convert raw counts to percentages -------
dft=df
dft[cols] = dft[cols].div(dft[cols].sum(axis=1), axis=0)
dft=dft.transpose()
dft.index.name='taxonomy'
dft.to_csv(o_file+'.tsv',sep='\t')
print ("Done :)")



