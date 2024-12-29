import json
import streamlit as st
import pandas as pd

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

class StreamlitApp:
    def __init__(self, data_file):
        self.data_file = data_file

    def load_data(self):
        with open(self.data_file, "r") as file:
            data = json.load(file)
        return data

    def run(self):
        local_css("style.css")
        st.title("Processed Questions")
        data = self.load_data()
        df = pd.DataFrame(data)

        page = st.sidebar.selectbox("Select Page", ["Markdown View", "Table View", "Dataframe View"])

        if page == "Markdown View":
            for item in data:
                st.subheader(f"Question: {item['question']}")
                st.markdown(f"**Expected Answer:** {item['expected_answer']}")
                st.markdown(f"**LLM Answer:** {item['llm_answer']}")
                st.markdown(f"**Grading Result:** {item['grading_result']}")
                st.markdown("---")
        elif page == "Table View":
            st.table(df)
        elif page == "Dataframe View":
            st.dataframe(df)

if __name__ == "__main__":
    data_file = "processed_questions2.json"
    app = StreamlitApp(data_file)
    app.run()