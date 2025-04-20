import streamlit as st
from utilities import sparql

def show():
    st.title("🔍 Study Area Lookup")
    if "study_terms" not in st.session_state:
        with st.spinner("Loading study concepts..."):
            study_links = sparql.query_study()
            study_terms = [term.replace('http://dbpedia.org/resource/', '') for term in study_links]
            st.session_state.study_terms = study_terms
    option = st.selectbox(
        f"🔍 Search from {len(st.session_state.study_terms)} concepts",
        (None, *st.session_state.study_terms),
    )
    
    if option is None:
        st.info('Please select a concept to view.')
    else:
        st.success(f"You selected: {option}")
        data = sparql.query_info(option)

        st.markdown(f'🌐 [Wikipedia Page](https://en.wikipedia.org/wiki/{option})')

        ### Abstract 
        abstract = data.get("http://dbpedia.org/ontology/abstract", "No abstract available.")
        if isinstance(abstract, list):
            abstract = abstract[0]  
        st.markdown("#### 🧠 Abstract")
        st.write(abstract)

        ### Thumbnail 
        image_url = data.get("http://dbpedia.org/ontology/thumbnail") or data.get("http://xmlns.com/foaf/0.1/depiction")
        if isinstance(image_url, list):
            image_url = image_url[0]
        
        if image_url:
                st.markdown(
                    f"""
                    <div style='text-align: center;'>
                        <img src="{image_url}" alt="{option}" style="max-height:300px; width:auto;"/>
                        <p style="font-size: 0.9em;">Wikipedia image of {option}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.warning("No image available.")
        
        ### link to
        st.markdown("#### 🔗 Knowledge Links")

        links_to = sparql.query_link_to(option)
        links_from = sparql.query_link_from(option)

        import pandas as pd

        # Normalize to same length
        max_len = max(len(links_to), len(links_from))
        links_to += [None] * (max_len - len(links_to))
        links_from += [None] * (max_len - len(links_from))

        markdown_table = "| 👉 Link To | 👈 Link From |\n|:--|:--|\n"

        for to, frm in zip(links_to, links_from):
            to_label = to.split("/")[-1].replace("_", " ") if to else ""
            from_label = frm.split("/")[-1].replace("_", " ") if frm else ""
            to_md = f"[{to_label}]({to})" if to else ""
            from_md = f"[{from_label}]({frm})" if frm else ""
            markdown_table += f"| {to_md} | {from_md} |\n"

        st.markdown(markdown_table)
        
