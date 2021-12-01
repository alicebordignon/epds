#TIPS: Iterate on triples in ARTchives that have as property
#"wdp.P27". The object of this property is the URI identifying
#countries of citizenship. Every country of citizenship has a label,
#which is the object of the property "RDFS.label".
#Remember to strip strings and to remove duplicates from the list.

# all imports
import pprint
import rdflib
from rdflib import URIRef, Literal, Namespace
from rdflib.namespace import XSD, RDFS, DCTERMS

 # remember that a prefix matches a URI until the last slash (or hashtag #)
wdp = Namespace("http://www.wikidata.org/prop/direct/")

g = rdflib.ConjunctiveGraph()
result = g.parse("C:\\Users\\bordi\\OneDrive\\Desktop\\dhdk_epds\\resources\\artchives.nq", format='nquads')

unique_countries = set()

for s, p, o in g.triples((None, wdp.P27, None)):
    for s1, p1, o1 in g.triples((o, RDFS.label, None)):
        unique_countries.add(o1.strip())

count_countries = dict()
for i in unique_countries:
    count_countries[i] = 0
    for s, p, o in g.triples((None, wdp.P27, None)):
        for s1, p1, o1 in g.triples((o, RDFS.label, None)):
            if o1.strip() == i:
                count_countries[i] += 1
print(count_countries)
