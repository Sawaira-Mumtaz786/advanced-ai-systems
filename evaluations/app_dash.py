import streamlit as st
import pandas as pd
import plotly.express as px
from eval_engine import run_evaluation

st.set_page_config(page_title="LLM Evaluation Dashboard", layout="wide")

st.title("🧪 LLM Evaluation Dashboard")
st.markdown("Automated evaluation of LLM outputs using LLM-as-judge methodology.")

if st.button("▶️ Run Evaluation", type="primary"):
    with st.spinner("Evaluating responses..."):
        results = run_evaluation()
        df = pd.DataFrame(results)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Faithfulness", f"{df['faithfulness'].mean():.2%}")
        col2.metric("Avg Relevance", f"{df['answer_relevance'].mean():.2%}")
        col3.metric("Total Samples", len(df))
        
        st.subheader("📊 Per-Question Scores")
        fig = px.bar(
            df.melt(id_vars=["question"], value_vars=["faithfulness", "answer_relevance"]),
            x="question", y="value", color="variable",
            barmode="group", title="Faithfulness vs Relevance"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("📋 Detailed Results")
        st.dataframe(df, use_container_width=True)