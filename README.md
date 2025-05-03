# EduMap: Interactive Study Area Network from DBpedia

🧑🏻‍💻 **Project Author:** Chotanansub Sophaken  
📚 **Course:** CS 43016 – Big Data Analytics  
🏢 **Institution:** Kent State University  
🗓️ **Term:** Spring 2025
<img src="asset/short-demo.gif" alt="Short Demor" width="1000"/>
This project presents the development of **EduMap**, an interactive web-based platform for exploring semantically linked academic concepts derived from DBpedia. The system is designed to support intuitive navigation and structured querying of educational content through Linked Open Data technologies. 

The application integrates SPARQL-based knowledge extraction, subgraph pruning strategies, and graph-based user interface design to facilitate dynamic exploration of interdisciplinary study areas. By enabling users to query and visualize concept networks, the platform supports both self-directed learning and pedagogical planning.

---

## 🌐 Live Application

Access the deployed app here:  
**🔗 [studynet.streamlit.app](https://studynet.streamlit.app/)**

---

## 📁 Project Structure

```
├── README.md
├── deploy
│   └── app
│       ├── data
│       │   └── relation_labels.json        # Label mappings for RDF relation types
│       ├── lookup_concept.py               # Handles concept lookup logic and enrichment
│       ├── main.py                         # Streamlit entry point for the web application
│       ├── query_network.py                # Graph construction and SPARQL query logic
│       └── utilities
│           ├── __pycache__
│           │   └── sparql.cpython-39.pyc   # Cached compiled SPARQL utility
│           └── sparql.py                   # Utility functions for SPARQL interaction
├── notebook
│   └── Edumap_Experiment.ipynb             # Performance evaluation and visualization notebook
└── requirements.txt                        # Python dependencies
```

---

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/edumap.git
cd edumap/deploy/app
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

### 3. Install Dependencies

```bash
pip install -r ../../requirements.txt
```

### 4. Run the Streamlit App

```bash
streamlit run main.py
```

This will launch the application locally at `http://localhost:8501`.

---

## 📊 Experimental Notebook

The `notebook/Edumap_Experiment.ipynb` file contains all experimental results, including:

- Implementation of query strategies
- Performance comparisons
- Visualizations of query efficiency

---

## 🧠 Key Features

- **Concept Lookup**: Retrieve summaries and linked data from DBpedia
- **Graph-Based Querying**: Explore semantic relationships between academic topics
- **Configurable Graph Views**: Choose layout, depth, and filtering strategies
- **SPARQL Optimization**: Efficient querying using Subquery Pruning and other strategies