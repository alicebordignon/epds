import rdflib
from rdflib import Namespace , Literal , URIRef
from rdflib.namespace import RDF , RDFS

# bind the uncommon namespaces
wd = Namespace("http://www.wikidata.org/entity/") # remember that a prefix matches a URI until the last slash (or hashtag #)
wdt = Namespace("http://www.wikidata.org/prop/direct/")
art = Namespace("https://w3id.org/artchives/")

# create an empty Graph
g = rdflib.ConjunctiveGraph()

# parse a local RDF file by specifying the format
result = g.parse("C:\\Users\\bordi\\OneDrive\\Desktop\\dhdk_epds\\resources\\artchives.nq", format='nquads')

colls_and_people = []

# get all the collections
for coll,isA,coll_class in g.triples(( None, RDF.type , wd.Q9388534)):
    # create a list for each collection
    coll_list = []
    # get all the periods for that collection
    for this_coll, hasSubj, people in g.triples(( coll, art.hasSubjectPeople, None)):
        # get the labels of the periods
        for this_people, hasLabel, people_label in g.triples((people , RDFS.label, None )):
            # get only the last label
            people_label = str(people_label).strip()
        # append periods to the related collection
        coll_list.append(people_label)
    # append collections to the initial list
    colls_and_people.append(coll_list)

print(colls_and_people)

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
import pandas as pd

dataset = colls_and_people

te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_ary, columns=te.columns_)

frequent_itemsets = apriori(df, min_support=0.05, use_colnames=True)
frequent_itemsets

from mlxtend.frequent_patterns import association_rules
association_rules(frequent_itemsets, metric="confidence", min_threshold=0.9)


#(Alessandro Contini Bonacossi) - (Bernard Berenson)
#RULES = IF {Alessandro Contini Bonacossi} THEN {Bernard Berenson}
