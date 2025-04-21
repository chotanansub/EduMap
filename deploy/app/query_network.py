import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from utilities import sparql
import time
import json

def show():
    st.title("🌐 Study Concept Networks")

    # Load study terms once
    if "study_terms" not in st.session_state:
        with st.spinner("Loading study concepts..."):
            study_links = sparql.query_study()
            study_terms = [term.replace('http://dbpedia.org/resource/', '') for term in study_links]
            st.session_state.study_terms = study_terms

    if "relation_labels" not in st.session_state:
        with open("deploy/app/data/relation_labels.json", "r") as f:
            st.session_state.relation_labels = json.load(f)


    display_option_list = [op.replace('_',' ') for op in st.session_state.study_terms]
    display_option = st.selectbox(f"🔍 Search from {len(st.session_state.study_terms)} concepts", (None, *display_option_list))
    if display_option is None:
        st.info("Please select a concept to view.")
        return
    
    
    #st.success(f"You selected: **{display_option}**")
    
    option = display_option.replace(' ','_')
    center_uri = f"http://dbpedia.org/resource/{option}"

    with st.expander("⚙️ Graph Configuration"):
        layout_mode = st.selectbox("Graph Layout Mode", ["Graph (Free)", "Tree (Hierarchical)"])
        bidirectional = st.checkbox("Show bidirectional edges (A → B and B → A)", value=False)
        max_depth = st.number_input("Maximum green node depth", min_value=1, max_value=10, value=2)
        max_total_nodes = st.number_input("Maximum total nodes", min_value=10, max_value=1000, value=30)
        limit_children = st.checkbox("Limit children per node (excluding center)", value=True)
        if limit_children:
            max_child_per_node = st.number_input("Maximum children per node", min_value=1, max_value=100, value=3)
        show_gray = st.checkbox("Enriched node with general concepts", value=False)
        if show_gray:
            max_gray = st.number_input("Maximum enriched nodes", min_value=1, max_value=100, value=20)

    info = sparql.query_info(option)
    study_set = set(f"http://dbpedia.org/resource/{s}" for s in st.session_state.study_terms)
    nodes = []
    edges = []
    edge_pairs = set()
    added_nodes = set()
    gray_count = 0
    node_depths = {center_uri: 0}

    thumbnail = sparql.query_thumbnail(center_uri)
    if thumbnail:
        nodes.append(Node(id=center_uri, label=option, size=45, color={"border": "#f74a4b"}, image=thumbnail, shape="circularImage"))
    else:
        nodes.append(Node(id=center_uri, label=option, size=45, color={"border": "#f74a4b"}))
    added_nodes.add(center_uri)

    def add_study_node(val, depth):
        if depth > max_depth or val in added_nodes or len(nodes) >= max_total_nodes:
            return
        uri_tail = val.split("/")[-1]
        display_label = uri_tail.replace("_", " ")
        color = {"border": "#145A32", "background": "#ffffff"}
        thumb = sparql.query_thumbnail(val)
        if thumb:
            nodes.append(Node(id=val, label=display_label, size=20, color=color, image=thumb, shape="circularImage"))
        else:
            nodes.append(Node(id=val, label=display_label, size=20, color=color))
        added_nodes.add(val)
        node_depths[val] = depth
        info_nested = sparql.query_info(uri_tail)
        child_count = 0
        for p, nested_obj in info_nested.items():
            nested_vals = nested_obj if isinstance(nested_obj, list) else [nested_obj]
            for nested_val in nested_vals:
                is_valid = (
                    isinstance(nested_val, str)
                    and nested_val.startswith("http")
                    and nested_val in study_set
                    and len(nodes) < max_total_nodes
                )
                if layout_mode == "Tree (Hierarchical)":
                    is_valid = is_valid and nested_val not in added_nodes and nested_val not in node_depths
                if not is_valid:
                    continue

                if limit_children and child_count >= max_child_per_node:
                    return

                edge_lbl = st.session_state.relation_labels.get(p, p.split("/")[-1])
                if (val, nested_val) not in edge_pairs:
                    edges.append(Edge(source=val, target=nested_val, label=edge_lbl, type="CURVE_SMOOTH"))
                    edge_pairs.add((val, nested_val))
                if bidirectional and layout_mode == "Graph (Free)" and (nested_val, val) not in edge_pairs:
                    edges.append(Edge(source=nested_val, target=val, label=edge_lbl, type="CURVE_SMOOTH"))
                    edge_pairs.add((nested_val, val))
                node_depths[nested_val] = node_depths[val] + 1
                add_study_node(nested_val, depth + 1)
                child_count += 1

    for predicate, obj in info.items():
        values = obj if isinstance(obj, list) else [obj]
        for val in values:
            if isinstance(val, str) and val.startswith("http"):
                obj_label = val.split("/")[-1].replace("_", " ")
                if val == center_uri or val in added_nodes:
                    continue
                elif val in study_set:
                    color = {"border": "#145A32", "background": "#ffffff"}
                elif show_gray and gray_count < max_gray and val.startswith("http://dbpedia.org/resource/") and val not in study_set:
                    color = {"border": "#AAAAAA", "background": "#dddddd"}
                    gray_count += 1
                else:
                    continue
                if layout_mode == "Tree (Hierarchical)" and val in node_depths:
                    continue
                if val in study_set:
                    add_study_node(val, 1)
                else:
                    nodes.append(Node(id=val, label=obj_label, size=20, color=color))
                    added_nodes.add(val)
                edge_label = st.session_state.relation_labels.get(predicate, predicate.split("/")[-1])
                node_depths[val] = 1
                if (center_uri, val) not in edge_pairs:
                    edges.append(Edge(source=center_uri, target=val, label=edge_label, type="CURVE_SMOOTH"))
                    edge_pairs.add((center_uri, val))
                if bidirectional and layout_mode == "Graph (Free)" and (val, center_uri) not in edge_pairs:
                    edges.append(Edge(source=val, target=center_uri, label=edge_label, type="CURVE_SMOOTH"))
                    edge_pairs.add((val, center_uri))

    config = Config(
        width=800,
        height=650,
        directed=True,
        hierarchical=False,
        physics=True,
        nodeHighlightBehavior=True,
        **{
            "interaction": {"hover": True, "selectable": True},
            "nodes": {
                "borderWidth": 3,
                "font": {"size": 16},
                "margin": 10,
                "color": {
                    "border": "#222222",
                    "background": "#ffffff",
                    "highlight": {"border": "#2B7CE9"},
                    "hover": {"border": "#2B7CE9"}
                }
            },
        }
    )

    if "show_node_info" not in st.session_state:
        st.session_state["show_node_info"] = True

    _, button_col2 = st.columns([2, 1])
    with button_col2:
        toggle = st.button("🧭 Toggle Info Panel")
    if toggle:
        st.session_state["show_node_info"] = not st.session_state["show_node_info"]

    if st.session_state["show_node_info"]:
        col1, col2 = st.columns([2, 1])
    else:
        col1 = st.container()
        col2 = None

    with col1:
         if "graph_ready" not in st.session_state:
            st.session_state.graph_ready = False
 
         if not st.session_state.graph_ready:
            with st.spinner("🔄 Preparing graph..."):
                # This simulates some backend prep delay
                time.sleep(1)  # Optional delay to simulate rendering
                st.session_state.graph_ready = True
                st.rerun()
         else:
            return_value = agraph(nodes=nodes, edges=edges, config=config)
            if return_value:
                node_uri = return_value
                node_label = node_uri.split("/")[-1]

    if st.session_state["show_node_info"] and col2:
        with col2:
            if return_value and isinstance(return_value, str):
                st.subheader(f"📝 {node_label.replace('_',' ')}")
                #st.success(f"🧠 **{node_label.replace('_',' ')}**")
                st.markdown(f"[🌐 View on DBpedia]({node_uri})")
                info = sparql.query_info(node_label)
                thumbnail = sparql.query_thumbnail(node_uri)
                if thumbnail:
                    st.image(thumbnail, width=150)
                abstract = info.get("http://dbpedia.org/ontology/abstract")
                if isinstance(abstract, list):
                    abstract = abstract[0]
                if abstract:
                    st.markdown("##### 📖 Abstract")
                    abstract_limit = 250
                    if len(abstract) > abstract_limit:
                        abstract = abstract[:250] + '...'
                    st.write(abstract)
                    wikipedia_link = f'https://en.wikipedia.org/wiki/{node_label}'
                    st.markdown(f'[read full article (wikipedia)]({wikipedia_link})')
            else:
                st.write("Click a node to see its info here.")