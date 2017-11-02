# -*- coding: utf-8 -*- 
import os, io
from tqdm import tqdm
from hanziconv import HanziConv as cc

with open("filter_rules.txt") as f:
        filter_rules = [l[:-1] for l in f.readlines()]

frs = {}


#Remove ill-formed articles from the copora
data_dir = 'dataset_original'
for f in os.listdir(data_dir):
    if f.split('.')[-1] == 'documents':

        src_file = os.path.join('dataset_original', '%s' % f)
        good_file = os.path.join('dataset', '%s' % f)
        bad_file = os.path.join('dataset_original', '%s.bad' % f)

        #print good_file, bad_file

        outf1 = open(good_file, 'w')
        outf2 = open(bad_file, 'w')

        print src_file
        with open(src_file) as f:
            for l in tqdm(f.readlines()):
                id, title, doc = l.split('\t')
                good = True
                for fr in filter_rules:
                    if fr in title:
                        good = False
                        continue

                if ':' in title and len(doc.split()) <= 20:
                    fr = title.split(':')[0] + ':'
                    if ' ' not in fr:
                        frs[fr] = 1

                if good:
                    doc = doc.lower().replace(title.lower(), '', 1)

                    #remove "external links" and "related items" from japanese database
                    x = doc.find('関連項目')
                    if x != -1:
                        doc = doc[:x]
                    x = doc.find('外部リンク')
                    if x != -1:
                        doc = doc[:x]
                   
                    outf1.write('\t'.join([id, title, doc]))
                else:
                    outf2.write(l)

filter_file = open('filter_rules.txt', 'w')
for f in frs:
    filter_file.write('%s\n' % f)
