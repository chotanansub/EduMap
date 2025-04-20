import streamlit as st
from streamlit_option_menu import option_menu
import lookup_concept, query_network


with st.sidebar:
    selected = option_menu(
        menu_title="📚 EduMap",
        options=["Home", "Concept Look Up", "Concept Query"],
        icons=['house', 'search', 'diagram-2'],
        menu_icon="book",
        default_index=0,
        
    )

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.8em; color: #6c757d; line-height: 1.5;">
            <span>🧑🏻‍💻 <em>Chotanansub Sophaken</em></span><br>
            📝 CS 43016: Big Data Analytics<br>
            🏫 Kent State University<br>
            🗓️ Spring, 2025<br>
            🔗 <a href="https://github.com/chotanansub/EduMap" target="_blank">GitHub Repository</a>
        </div>
        """,
        unsafe_allow_html=True
    )

# Routing
if selected == "Home":
    st.title("👋🏻 Welcome to **EduMap**! ")
    st.info("👈🏻 Use the sidebar to explore the available tools and features.")
    st.markdown(
    """
    **EduMap** is an interactive tool for exploring connections between academic concepts and study areas.  
    For example, a subject like *American Urban History* might link to *Sociology* or indirectly relate to *English Local History*.  
    
    With EduMap, you can visually discover and interpret these relationships through a dynamic concept network.
    """
)
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
elif selected == "Concept Look Up":
    lookup_concept.show()
elif selected == "Concept Query":
    query_network.show()


