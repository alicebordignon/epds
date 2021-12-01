# all imports
import pprint
import rdflib
from rdflib import URIRef, Literal, Namespace
from rdflib.namespace import XSD, RDFS, DCTERMS
from rdflib import Literal
 #All the labels of the keywords associated to Federico Zeri
g = rdflib.ConjunctiveGraph()
result = g.parse("C:\\Users\\bordi\\OneDrive\\Desktop\\dhdk_epds\\resources\\artchives.nq", format='nquads')
#1. Iterate over the triples having (a) as subject the URI identifying Zeri, and (b)
#as predicate wdt.P921 (remember to declare and bind the namespaces to a prefix!)

zeri = URIRef('http://www.wikidata.org/entity/Q1089074')
wd = Namespace("http://www.wikidata.org/entity/")
wdt = Namespace("http://www.wikidata.org/prop/direct/") # remember that a prefix matches a URI until the last slash (or hashtag #)
unique_topics = set()

for s,p,o in g.triples((wd.Q1089074, wdt.P921, None)):
    for s1,p1,o1 in g.triples((o, RDFS.label, None)):
        unique_topics.add(o1.strip())

for topic in unique_topics:
    print(topic) #i strip it because this is a problem of these data, in a way that strings will be unique.

#in this case i made a double loop using a set a prepared. i made 1 and 2 together


#alternative solution
unique_topics = set()
objects = set()
for s, p, o in g.triples((wd.Q1089074, wd.P921, None)):
    objects.add(o)

for s1, p1, o1 in g.triples((None, RDFS.label, None)):
    if s1 in objects:
        print(o1)         #this method is not convenient with normal databases.


#2. Iterate over the objects of the prior triple pattern and lookup for a new triple pattern,
#having now as subject the variable identifying the topic, and as predicate RDFs.label
#(remember to import RDFS along with the built-in namespaces such as DCTERMS).
    for s1, p1, o1 in g.triples((o, RDFS.label, None)):
        unique_topics.add(o1.strip()) #i strip it because this is a problem of these data, in a way that strings will be unique.

#3. print the list
for topic in unique_topics:
    print(topic)
