# Quiz Mode
elif mode == "Quiz":
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
        st.session_state.quiz_total = 0

    all_qs = [(cat, dis, facts[cat][dis]) for cat in facts for dis in facts[cat]]
    q = random.choice(all_qs)
    options = [q[1]] + random.sample([d for _, d, _ in all_qs if d != q[1]], 3)
    random.shuffle(options)

    st.subheader("Quiz: Which disease matches this description?")
    st.markdown(f"🧠 **Clue**: {q[2]}")
    answer = st.radio("Choose one:", options)

    if st.button("Submit Answer"):
        st.session_state.quiz_total += 1
        if answer == q[1]:
            st.session_state.quiz_score += 1
            st.success(f"✅ Correct! {q[2]}")
        else:
            st.error(f"❌ Incorrect. Correct answer: {q[1]} — {q[2]}")

        st.write(f"**Score:** {st.session_state.quiz_score}/{st.session_state.quiz_total}")
        if st.button("Try Another"):
            st.experimental_rerun()
