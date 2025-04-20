from SPARQLWrapper import SPARQLWrapper, JSON
import streamlit as st
sparql = SPARQLWrapper("https://dbpedia.org/sparql")

@st.cache_data(show_spinner=False)
def query_study():
    query = """
    PREFIX gold: <http://purl.org/linguistics/gold/>
    PREFIX dbr: <http://dbpedia.org/resource/>

    SELECT DISTINCT ?s WHERE {
      ?s gold:hypernym dbr:Study .
    }
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    subjects = [result["s"]["value"] for result in results["results"]["bindings"]]
    return subjects

@st.cache_data(show_spinner=False)
def query_info(title):
    query = f"""
    PREFIX dbr: <http://dbpedia.org/resource/>
    SELECT DISTINCT ?p ?o WHERE {{
        dbr:{title} ?p ?o .
        FILTER (lang(?o) = 'en' || !isLiteral(?o))
    }}LIMIT 1000
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    info_dict = {}
    for r in results["results"]["bindings"]:
        p = r["p"]["value"]
        o = r["o"]["value"]
        
        if p in info_dict:
            if isinstance(info_dict[p], list):
                info_dict[p].append(o)
            else:
                info_dict[p] = [info_dict[p], o]
        else:
            info_dict[p] = o

    return info_dict

@st.cache_data(show_spinner=False)
def query_link_to(title):
    query = f"""
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX gold: <http://purl.org/linguistics/gold/>

    SELECT DISTINCT ?s ?p ?o
    WHERE {{
    dbr:{title} ?p ?o .
    ?o gold:hypernym dbr:Study .
    BIND(dbr:{title} AS ?s)
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    object = [result["o"]["value"] for result in results["results"]["bindings"]]
    return object

@st.cache_data(show_spinner=False)
def query_link_from(title):
    query = f"""
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX gold: <http://purl.org/linguistics/gold/>

    SELECT DISTINCT ?s ?p ?o
    WHERE {{
        ?s ?p dbr:{title} .
        dbr:{title} gold:hypernym dbr:Study .
    }}LIMIT 20
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    subjects = [result["s"]["value"] for result in results["results"]["bindings"]]
    return subjects

@st.cache_data(show_spinner=False)
def query_thumbnail(uri):
    query = f"""
    SELECT DISTINCT ?thumb WHERE {{
        <{uri}> <http://dbpedia.org/ontology/thumbnail> ?thumb .
    }} LIMIT 1
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    bindings = results["results"]["bindings"]
    if bindings:
        thumb_url = bindings[0]["thumb"]["value"]
        return thumb_url.replace("wiki-commons:", "http://commons.wikimedia.org/wiki/")
    return None