import os, io
from tqdm import tqdm
from hanziconv import HanziConv as cc

filter_rules = ['Wikipedia:', 'Help:', 'Topic:', 'Draft:', 'Portal:', 'Fichier:', 'Wikiprojekt:']

#Remove ill-formed articles from the copora
data_dir = 'dataset_original'
for f in os.listdir(data_dir):
    if f.split('.')[-1] == 'rel':

        source, target = f.split('.')[0].split('2')
        source_file = os.path.join('dataset', 'wiki_%s.queries' % source)
        target_file = os.path.join('dataset', 'wiki_%s.documents' % target)

        queries = {}
        with open(source_file) as sourcef:
            for l in sourcef:
                id, title, query = l[:-1].split('\t')
                queries[int(id)] = (title, query) 

        documents = {}
        with open(target_file) as targetf:
            for l in targetf:
                id, title, doc = l[:-1].split('\t')
                documents[int(id)] = (title, doc) 


        outf = open(os.path.join('dataset', f), 'w')
        with open(os.path.join(data_dir, f)) as relf:
            #l = relf.readlines() 
            

