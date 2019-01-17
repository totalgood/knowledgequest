#!/usr/bin/env python
#!/python -m spacy download en
# import lxml.html
import html2text
import spacy
import gensim
from gensim.summarization.summarizer import summarize

html = open('/Users/hobs/Downloads/The PwC Internal Audit.html').read()
txt = html2text.html2text(html)

nlp = spacy.load('en')
docobj = nlp(txt)
sents = list(docobj.sents)
str([w for w in sents[0]])
tokenized_sents = [[str(w) for w in s] for s in sents]

summarize([str(s) for s in sents].join('\n'))
summarize('\n'.join([str(s).replace(' ', '\n') for s in sents]))
sents
