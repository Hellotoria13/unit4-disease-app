# App Title and Mode Selection
st.title("Unit 4 Infectious Diseases Study Tool")
mode = st.sidebar.radio("Choose Mode", ["Study Map", "Flashcards", "Quiz"])

# Study Map Mode
if mode == "Study Map":
    category = st.sidebar.selectbox("Select Body System", list(systems.keys()))
    selected_disease = st.sidebar.selectbox("Search Disease", sorted(facts[category].keys()))

    G = nx.DiGraph()
    G.add_node(category)
    for disease in facts[category]:
        G.add_node(disease)
        G.add_edge(category, disease)

    pos = nx.spring_layout(G, k=1.0, iterations=100, seed=42)
    plt.figure(figsize=(12, 10))
    nx.draw(G, pos, with_labels=True, node_size=3000,
            node_color=[systems[category] if node == category else 'white' for node in G.nodes],
            edge_color='gray', font_size=10, font_weight='bold')
    st.pyplot(plt)

    st.subheader(f"📌 Fact about {selected_disease}:")
    st.info(facts[category][selected_disease])


