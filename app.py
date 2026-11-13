import streamlit as st
from prepare import prepare_application
from tools import search_remote_jobs, JOB_CACHE

st.set_page_config(page_title="JobHunt Agent", layout="wide")
st.title("JobHunt Agent")

mode = st.sidebar.radio("Job source", ["Paste a job", "Search Remotive"])
min_score = st.sidebar.slider("Skip jobs scoring below", 0, 80, 40)

job_text, job_url = "", ""

if mode == "Paste a job":
    job_text = st.text_area("Paste the job description", height=250)
    job_url = st.text_input("Job link (optional)")
else:
    query = st.text_input("Keyword", "react")
    if st.button("Search"):
        st.session_state["found"] = search_remote_jobs(query)
    found = st.session_state.get("found", [])
    if found:
        labels = [f'{j["title"]} - {j["company"]}' for j in found]
        pick = st.selectbox("Pick a job", range(len(found)), format_func=lambda i: labels[i])
        job_text = JOB_CACHE.get(found[pick]["id"], "")
        job_url = found[pick]["url"]
        st.caption(job_url)
    elif "found" in st.session_state:
        st.info("No matching jobs right now. Try another keyword.")

if st.button("Prepare application", type="primary"):
    if not job_text.strip():
        st.warning("Add a job first.")
    else:
        with st.spinner("Working, about 30 to 60 seconds..."):
            st.session_state["result"] = prepare_application(job_text, min_score)
            st.session_state["url"] = job_url

res = st.session_state.get("result")

if res:
    for err in res["errors"]:
        st.error(err)

    match = res["match"]
    if "error" not in match:
        c1, c2 = st.columns([1, 3])
        c1.metric("Match score", f'{match["score"]} / 100')
        c2.write(match.get("reason", ""))
        st.write("Matched: " + ", ".join(match["matched_skills"]))
        st.write("Missing: " + ", ".join(match["missing_skills"]))

        if res.get("skipped"):
            st.info("Score is below your cutoff, so tailoring was skipped. Lower the cutoff in the sidebar to prepare it anyway.")
        else:
            t1, t2, t3 = st.tabs(["Tailored CV", "Cover letter", "Fact check"])

            with t1:
                tailored = res.get("tailored")
                if tailored:
                    st.subheader("Summary")
                    st.write(tailored["summary"])
                    st.subheader("Skills")
                    st.write(", ".join(tailored["skills"]))
                    st.subheader("Top projects")
                    st.write(", ".join(tailored["top_projects"]))
                if res.get("bullets"):
                    st.subheader("Bullets")
                    _, new_bullets = res["bullets"]
                    for key, lines in new_bullets.items():
                        st.markdown(f"**{key}**")
                        for line in lines:
                            st.write("- " + line)

            with t2:
                letter = res.get("letter")
                if letter:
                    text = st.text_area("Edit before sending", letter["letter"], height=350)
                    st.download_button("Download letter", text, file_name="cover_letter.txt")

            with t3:
                letter = res.get("letter")
                if letter:
                    report = letter["report"]
                    if report["passed"]:
                        st.success(f'Passed. Fix rounds used: {letter["rounds"]}')
                    else:
                        st.warning("Some claims could not be verified. Check them before sending.")
                        st.write("Unsupported claims:", report["llm_flags"])
                        st.write("Tools not in your profile:", report["keyword_flags"])
                        st.write("Numbers not in your profile:", report["number_flags"])

        if st.session_state.get("url"):
            st.link_button("Open job page to apply", st.session_state["url"])