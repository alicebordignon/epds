import rdflib

# create an empty Graph
g = rdflib.ConjunctiveGraph()

# parse a local RDF file by specifying the format
result = g.parse("C:\\Users\\bordi\\OneDrive\\Desktop\\dhdk_epds\\resources\\artchives_birthplaces.nq", format='nquads')


#Write a SPARQL query to retrieve in ARTchives all the historians that were born in Berlin (wd:Q64). *
queryResults = g.query("""
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
SELECT ?historian ?label
WHERE {  ?historian wdt:P19 wd:Q64;
                    rdfs:label ?label .
}
""")
'''
for i in queryResults:
    print(i[0], i[1])
'''
#Write the SPARQL query to retrieve in Wikidata all the art historians (that are both in ARTchives and Wikidata!)
#that were born in Germany. Copy paste the query that returns a table: <historian URI> <historian label> <city URI> <city label>.
#Tip: A german city in Wikidata has the pattern wdt.P17 (country) > wd:Q183 (Germany).
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Namespace , Literal , URIRef
from rdflib.namespace import RDF , RDFS
# bind the uncommon namespaces
wd = Namespace("http://www.wikidata.org/entity/") # remember that a prefix matches a URI until the last slash (or hashtag #)
wdt = Namespace("http://www.wikidata.org/prop/direct/")
art = Namespace("https://w3id.org/artchives/")

# get the endpoint API
wikidata_endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"

# Get the list of art historians in our graph "g"
arthistorians = set()

# iterate over the triples in the graph
for s,p,o in g.triples(( None, wdt.P170, None)):   # people "o" are the creator "wdt.P170" of a collection "s"
    if "wikidata.org/entity/" in str(o):           # look for the substring to filter wikidata entities only
        arthistorians.add('<' + str(o) + '>')     # remember to transform them in strings!

# prepare the values to be queried
historians = ' '.join(arthistorians) # <uri1> <uri2> <uri3> ... <uriN>

# prepare the query
germanyQuery = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?historian ?historian_label ?birthplace ?birthplace_label
WHERE {
    VALUES ?historian {"""+historians+"""} .
    ?historian rdfs:label ?historian_label .
    ?historian wdt:P19 ?birthplace .
    ?birthplace rdfs:label ?birthplace_label .
    ?birthplace wdt:P17 wd:Q183 .
    FILTER (langMatches(lang(?birthplace_label), "EN"))
    FILTER (langMatches(lang(?historian_label), "EN"))
    }
"""
# set the endpoint
sparql_wd = SPARQLWrapper(wikidata_endpoint)
# set the query
sparql_wd.setQuery(germanyQuery)
# set the returned format
sparql_wd.setReturnFormat(JSON)
# get the results
results = sparql_wd.query().convert()


for result in results["results"]["bindings"]:
    print(result["historian"]["value"], result["historian_label"]["value"], result["birthplace"]["value"], result["birthplace_label"]["value"])
