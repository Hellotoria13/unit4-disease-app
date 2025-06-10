
# Unit 4 Disease App with Rerun-Proof Quiz Questions
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
from unit4_disease_facts import facts

st.set_page_config(layout="wide")

systems = {
    "Skin": "lightcoral",
    "Respiratory": "lightgreen",
    "Cardio/Nervous": "lightskyblue",
    "GI/STI/Urinary": "khaki"
}

st.title("Unit 4 Infectious Diseases Study Tool")
mode = st.sidebar.radio("Choose Mode", ["Study Map", "Flashcards", "Quiz"])

if mode == "Study Map":
    category = st.sidebar.selectbox("Select Body System", list(systems.keys()))
    selected_disease = st.sidebar.selectbox("Search Disease", sorted(facts[category].keys()))
    G = nx.DiGraph()
    G.add_node(category)
    for disease in facts[category]:
        G.add_node(disease)
        G.add_edge(category, disease)
    pos = nx.spring_layout(G, k=1.2, iterations=200, seed=42)
    plt.figure(figsize=(12, 10))
    nx.draw(G, pos, with_labels=True, node_size=3000,
            node_color=[systems[category] if node == category else 'white' for node in G.nodes],
            edge_color='gray', font_size=10, font_weight='bold')
    st.pyplot(plt)
    st.subheader(f"📌 Fact about {selected_disease}:")
    st.info(facts[category][selected_disease])

elif mode == "Flashcards":
    all_diseases = [(cat, dis) for cat in facts for dis in facts[cat]]
    if "flash_index" not in st.session_state:
        st.session_state.flash_index = 0
    category, disease = all_diseases[st.session_state.flash_index % len(all_diseases)]
    st.subheader(f"Flashcard {st.session_state.flash_index + 1} of {len(all_diseases)}")
    st.markdown(f"**Disease**: {disease}")
    if st.button("Show Answer"):
        st.success(facts[category][disease])
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Next"):
            st.session_state.flash_index += 1
            st.experimental_rerun()
    with col2:
        if st.button("Restart"):
            st.session_state.flash_index = 0
            st.experimental_rerun()

elif mode == "Quiz":
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
        st.session_state.quiz_total = 0
    if "quiz_question" not in st.session_state or st.session_state.get("reset_quiz", False):
        st.session_state.quiz_question = random.choice([(cat, dis, facts[cat][dis]) for cat in facts for dis in facts[cat]])
        st.session_state.reset_quiz = False

    q = st.session_state.quiz_question
    options = [q[1]] + random.sample([d for _, d, _ in [(cat, dis, facts[cat][dis]) for cat in facts for dis in facts[cat]] if d != q[1]], 3)
    random.shuffle(options)

    st.subheader("Quiz: Which disease matches this description?")
    st.markdown(f"🧠 **Clue**: {q[2]}")
    answer = st.radio("Choose one:", options, key="quiz_answer")

    if st.button("Submit Answer"):
        if answer:
            st.session_state.quiz_total += 1
            if answer == q[1]:
                st.session_state.quiz_score += 1
                st.success(f"✅ Correct! {q[2]}")
            else:
                st.error(f"❌ Incorrect. Correct answer: {q[1]} — {q[2]}")
            st.write(f"**Score:** {st.session_state.quiz_score}/{st.session_state.quiz_total}")
        else:
            st.warning("Please select an answer before submitting.")

    if st.button("Try Another"):
        st.session_state.reset_quiz = True
        st.experimental_rerun()

    if st.button("Reset Score"):
        st.session_state.quiz_score = 0
        st.session_state.quiz_total = 0
        st.experimental_rerun()
