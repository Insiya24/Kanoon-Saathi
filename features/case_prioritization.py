import streamlit as st
import pandas as pd
from datetime import datetime
import os

def case_prioritization_tab():
    # ---------- Setup ----------
    if not os.path.exists("cases.csv"):
        pd.DataFrame([
            {"case_id": 1, "title": "Fix potholes", "description": "Sector 12 road", "upvotes_with": 0, "upvotes_without": 0},
            {"case_id": 2, "title": "Install street lights", "description": "Dark Block A-B", "upvotes_with": 0, "upvotes_without": 0}
        ]).to_csv("cases.csv", index=False)

    if not os.path.exists("upvotes.csv"):
        pd.DataFrame(columns=["user_name", "case_id", "with_testimonial", "timestamp"]).to_csv("upvotes.csv", index=False)

    if not os.path.exists("testimonials.csv"):
        pd.DataFrame(columns=["user_name", "case_id", "text", "file_path", "timestamp"]).to_csv("testimonials.csv", index=False)

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    if "tab" not in st.session_state:
        st.session_state["tab"] = "Home"

    tab = st.session_state["tab"]

    # ---------- HOME ----------
    if tab == "Home":
        st.header("📌 Case Prioritization")
        user_name = st.text_input("Enter your name")
        cases = pd.read_csv("cases.csv")
        upvotes = pd.read_csv("upvotes.csv")

        for i, row in cases.iterrows():
            st.subheader(row["title"])
            st.write(row["description"])
            st.write(f"👍 With Testimonial: {row['upvotes_with']} | Without: {row['upvotes_without']}")
            voted = ((upvotes['user_name'] == user_name) & (upvotes['case_id'] == row['case_id'])).any()
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Upvote without testimonial", key=f"up_{i}", disabled=voted or not user_name):
                    upvotes.loc[len(upvotes)] = [user_name, row['case_id'], False, datetime.now()]
                    upvotes.to_csv("upvotes.csv", index=False)
                    cases.at[i, "upvotes_without"] += 1
                    cases.to_csv("cases.csv", index=False)
                    st.experimental_rerun()
            with col2:
                if st.button("Give testimonial", key=f"test_{i}", disabled=voted or not user_name):
                    st.session_state["case_id"] = row["case_id"]
                    st.session_state["user_name"] = user_name
                    st.session_state["tab"] = "Submit Testimonial"
                    st.experimental_rerun()

        st.markdown("---")
        if st.button("🔐 Go to Authority View"):
            st.session_state["tab"] = "Authority View"
            st.experimental_rerun()

    # ---------- TESTIMONIAL SUBMIT ----------
    elif tab == "Submit Testimonial":
        st.header("📝 Testimonial")
        case_id = st.session_state.get("case_id")
        user_name = st.session_state.get("user_name")

        if not case_id or not user_name:
            st.warning("Please select a case and enter your name in the Home tab.")
            return

        text = st.text_area("Your testimonial")
        file = st.file_uploader("Upload proof (image/pdf)", type=["jpg", "png", "pdf"])

        if st.button("Submit"):
            if text and file:
                filepath = f"uploads/{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.name}"
                with open(filepath, "wb") as f:
                    f.write(file.read())

                # Save testimonial
                t_df = pd.read_csv("testimonials.csv")
                new_row = {
                    "user_name": user_name,
                    "case_id": case_id,
                    "text": text,
                    "file_path": filepath,
                    "timestamp": datetime.now()
                }
                t_df = pd.concat([t_df, pd.DataFrame([new_row])], ignore_index=True)
                t_df.to_csv("testimonials.csv", index=False)
                t_df.to_csv("testimonials.csv", index=False)

                # Save upvote
                u_df = pd.read_csv("upvotes.csv")
                u_df.loc[len(u_df)] = [user_name, case_id, True, datetime.now()]
                u_df.to_csv("upvotes.csv", index=False)

                # Update case upvote count
                c_df = pd.read_csv("cases.csv")
                c_df.loc[c_df["case_id"] == case_id, "upvotes_with"] += 1
                c_df.to_csv("cases.csv", index=False)

                st.success("Submitted ✅")
                del st.session_state["case_id"]
                del st.session_state["user_name"]
                st.session_state["tab"] = "Home"
                st.experimental_rerun()
            else:
                st.error("Please provide both testimonial and proof file.")

        st.markdown("---")
        if st.button("🔐 Go to Authority View"):
            st.session_state["tab"] = "Authority View"
            st.experimental_rerun()

    # ---------- AUTHORITY VIEW ----------
    elif tab == "Authority View":
        st.header("🔐 Authority Access")
        password = st.text_input("Password", type="password")
        if password == "admin123":
            st.success("Access granted")
            try:
                t_df = pd.read_csv("testimonials.csv")
                c_df = pd.read_csv("cases.csv")

                if t_df.empty:
                    st.write("No testimonials submitted yet.")
                else:
                    for idx, row in t_df.iterrows():
                        case_row = c_df[c_df["case_id"] == int(row["case_id"])]
                        case_title = case_row["title"].values[0] if not case_row.empty else f"Unknown (ID {row['case_id']})"

                        st.markdown(f"### 🧾 Case: {case_title}")
                        st.markdown(f"**User:** {row['user_name']}  \n**Text:** {row['text']}  \n**Time:** {row['timestamp']}")

                        if os.path.exists(row["file_path"]):
                            with open(row["file_path"], "rb") as f:
                                st.download_button(
                                    label="Download Proof",
                                    data=f,
                                    file_name=row["file_path"].split("/")[-1],
                                    mime="application/pdf" if row["file_path"].endswith(".pdf") else "image/png"
                                )

                        else:
                            st.warning("⚠️ File not found for download.")
                        st.divider()
            except Exception as e:
                st.error(f"Error loading testimonials: {e}")
        else:
            st.warning("Enter correct password to continue.")
        if st.button("🔙 Back to Home"):
                st.session_state["tab"] = "Home"
                st.session_state["auth_passed"] = False
                st.experimental_rerun()
