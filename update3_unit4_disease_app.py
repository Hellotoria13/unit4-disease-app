# Flashcard Mode
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
