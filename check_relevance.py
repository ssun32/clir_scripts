import sys, os, random
if len(sys.argv) is not 3:
    print "Usage: %s %s" % (sys.argv[0], "[wikipedia_language_code] [relevance level]")
    print "e.g zh - chinese, ja -japanese"
    print "Relevance level is either 1 or 2, 2 is more relevant"

else:
    source = 'en'
    target = str(sys.argv[1])

    source_file = os.path.join('dataset','wiki_%s.queries' % source)
    target_file = os.path.join('dataset','wiki_%s.documents' % target)
    rel_file = os.path.join('dataset','%s2%s.rel' % (source, target))

    def check_file(file):
        if not os.path.exists(file):
            print "%s not found." % file
            sys.exit(0)

    # if any of the files do not exists, quit
    check_file(source_file)
    check_file(target_file)
    check_file(rel_file)

    queries = {}
    print "loading query file..."
    with open(source_file) as f:
        for l in f:
            id, title, query = l[:-1].split('\t')
            queries[int(id)] = (title, query)

    documents = {}
    print "loading document file..."
    with open(target_file) as f:
        for l in f:
            id, title, doc = l[:-1].split('\t')
            documents[int(id)] = (title, doc)

    relevance_level1 = {}
    relevance_level2 = {}
    print "loading relevance file..."
    with open(rel_file) as f:
        for l in f:
            src, target, rel = l[:-1].split('\t')
            rel = int(rel)
            src = int(src)
            target = int(target)

            if rel is 2:
                relevance_level2[(src, target)] = rel
            else:
                relevance_level1[(src, target)] = rel

    def random_next():
        os.system('clear')
        if int(sys.argv[2]) is 2: 
            k = random.choice(relevance_level2.keys())
        elif int(sys.argv[2]) is 1: 
            k = random.choice(relevance_level1.keys())

        source_index, target_index = k

        print "Query ID: %s" % source_index
        print "Title: %s" % queries[source_index][0]
        print "Query (%s):" % source
        print queries[source_index][1] + '\n'

        print "Document ID: %s" % target_index
        print "Title: %s" % documents[target_index][0]
        print "Document (%s):" % target
        print documents[target_index][1]


    random_next()
    n = raw_input("Press enter to quit (q to quit):")
    while n != 'q' and n != 'Q':
        random_next()
        n = raw_input("Press enter to quit (q to quit):")

