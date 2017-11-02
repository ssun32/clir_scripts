# encoding: utf-8
import sys, re, io
from nltk.tokenize import sent_tokenize as st
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

qids = {}
stopwords = set(stopwords.words('english'))
stemmer = SnowballStemmer('english')

with open('dataset/wiki_en.queries.ids', 'r') as f:
    for l in f:
        qids[float(l[:-1])] = 1

wiki_en_data_path = '/export/a14/shuo/wikiclir17/wiki/extracted_wiki/wiki_en.dat'

fgood = io.open('dataset/wiki_en.queries', 'w', encoding='utf-8')
fbad = io.open('dataset/wiki_en.queries.bad', 'w', encoding='utf-8')

with io.open(wiki_en_data_path, 'r', encoding='utf-8', errors='ignore') as f:
    for l in f:
        l = l.split('\t')
        try:
            did = int(l[0])
        except:
            continue
        title = l[1]
        doc = l[-1]
        sys.stdout.write('\rHandling doc id: ' + str(did))
        sys.stdout.flush() # important

        if did in qids:
            #do sentence boundary detection
            if '\\n' in doc:
                doc = '\\n'.join(doc.split('\\n')[1:])
            doc = st(doc)[0]

            if '\\n' in doc:
                 doc = doc.split('\\n')[0]

            doc = doc.lower()

            title_tokens = title.split()
            if len(title_tokens) > 1:
                doc = doc.replace(title.lower(), '')

            title_tokens = [stemmer.stem(t.lower()) for t in title_tokens if t not in stopwords]

            keep = []
            for t in doc.split():

                if stemmer.stem(t) not in title_tokens:
                    keep.append(t)

            doc = ' '.join(keep)
            output = '\t'.join([str(did), title, doc])+'\n'

            if 'can refer to' in doc or 'may refer to' in doc or 'disambiguation' in title:
                fbad.write(output)
            else:
                fgood.write(output)
