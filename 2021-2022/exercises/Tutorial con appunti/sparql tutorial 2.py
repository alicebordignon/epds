#1.10 Download and query the JSON result with python
import json, pprint

pp = pprint.PrettyPrinter(indent=1) # just to pretty print results

with open('C:\\Users\\bordi\\OneDrive\\Desktop\\dhdk_epds\\resources\\sparql_query_result.json','r') as results:
    data = json.load(results)
    pprint.pprint(data)


for result in data["results"]["bindings"]:  # enter the list of dictionaries // do you remember "for row in rows"?
    res_class = result['class']['value']    # the value of the cell under column "class"
    res_tot = result['tot']['value']        # the value of the cell under column "tot"
    #print('The class', res_class,'has', res_tot, 'individuals')

#2. Execute SPARQL queries with RDFLib on a local RDF file

import rdflib

# create an empty Graph
g = rdflib.ConjunctiveGraph()

# parse a local RDF file by specifying the format
result = g.parse("C:\\Users\\bordi\\OneDrive\\Desktop\\dhdk_epds\\resources\\artchives.nq", format='nquads')

query_results = g.query(
    """SELECT ?class (COUNT(?individual) AS ?tot)
    WHERE { ?individual a ?class .}
    GROUP BY ?class ?tot""")

for query_res in query_results:
    print(query_res[0], query_res["tot"])

#3. Query a SPARQL endpoint with RDFLib and SPARQLWrapper libraries

#we create a wrapper on top of the request. we don't see all the code we show here, but
#we use a template code for querying all possible sparql points. you wrap the end point, uou send the query
#and you get the jason result

from SPARQLWrapper import SPARQLWrapper, JSON
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# get the endpoint API
wikidata_endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
#these are the sparql points for wikidata

# prepare the query : 10 random triples
my_SPARQL_query = """
SELECT *
WHERE {?s ?p ?o}
LIMIT 10
"""

# set the endpoint
sparql_wd = SPARQLWrapper(wikidata_endpoint)   #assign a variable to an instance of a class. every time i have to create a new variable
# set the query
sparql_wd.setQuery(my_SPARQL_query) #i prepare the wrapper, and i said what query i want to work
# set the returned format
sparql_wd.setReturnFormat(JSON)  #decide to HOW to return our data (we chose jason)
# get the results
results = sparql_wd.query().convert()  #now that i told you everything, go. that convert means convert the jason file in a dictionary.
#now that results is a dictionary i can iterate over it.

# manipulate the result, how to access the results
for result in results["results"]["bindings"]:
    print(result["s"]["value"], result["p"]["value"], result["o"]["value"])

#3.1 Integrate art historians' birth places from Wikidata
from rdflib import Namespace , Literal , URIRef
from rdflib.namespace import RDF , RDFS

# bind the uncommon namespaces
wd = Namespace("http://www.wikidata.org/entity/") # remember that a prefix matches a URI until the last slash (or hashtag #)
wdt = Namespace("http://www.wikidata.org/prop/direct/")
art = Namespace("https://w3id.org/artchives/")

# Get the list of art historians in our graph "g"
arthistorians_list = set()

# iterate over the triples in the graph
for s,p,o in g.triples(( None, wdt.P170, None)):   # people "o" are the creator "wdt.P170" of a collection "s"
    if "wikidata.org/entity/" in str(o):           # look for the substring to filter wikidata entities only
        arthistorians_list.add('<' + str(o) + '>')     # remember to transform them in strings!

print(arthistorians_list)

#INTEGRATE THE DATA INTO THE GRAPH Once the wrapper and the query are set we manipulate results:

# prepare the values to be queried
historians = ' '.join(arthistorians_list) # <uri1> <uri2> <uri3> ... <uriN>

# prepare the query
birthplace_query = """
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
SELECT DISTINCT ?historian ?birthplace ?birthplace_label
WHERE {
    VALUES ?historian {"""+historians+"""} . # look how we include a variable in a query string!
    ?historian wdt:P19 ?birthplace .
    ?birthplace rdfs:label ?birthplace_label .
    FILTER (langMatches(lang(?birthplace_label), "EN"))
    }
"""

# set the endpoint
sparql_wd = SPARQLWrapper(wikidata_endpoint)
# set the query
sparql_wd.setQuery(birthplace_query)
# set the returned format
sparql_wd.setReturnFormat(JSON)
# get the results
results = sparql_wd.query().convert()

# manipulate the result
for result in results["results"]["bindings"]:
    historian_uri = result["historian"]["value"]
    print("historian:", historian_uri)
    if "birthplace" in result: # some historians may have no birthplace recorded in Wikidata!
        birthplace = result["birthplace"]["value"]
        if "birthplace_label" in result:
            birthplace_label = result["birthplace_label"]["value"]
            print("found:", birthplace, birthplace_label)

            # only if both uri and label are found we add them to the graph
            g.add(( URIRef(historian_uri) , URIRef(wdt.P19) , URIRef(birthplace) ))
            g.add(( URIRef(birthplace) , RDFS.label , Literal(birthplace_label) ))
    else:
        print("nothing found in wikidata :(")

#STORE
g.serialize(destination='C:\\Users\\bordi\\OneDrive\\Desktop\\dhdk_epds\\resources\\artchives_birthplaces.nq', format='nquads')
