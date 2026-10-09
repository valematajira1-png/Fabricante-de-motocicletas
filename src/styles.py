import streamlit as st

CSS = """
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    .main-title { font-size: 2.1rem; font-weight: 800; line-height: 1.1; margin-bottom: .2rem; }
    .subtitle { color: #667085; font-size: 1rem; margin-bottom: 1.2rem; }
    .section-title { font-size: 1.25rem; font-weight: 750; margin-top: .5rem; margin-bottom: .35rem; }
    .section-note { color: #667085; font-size: .9rem; margin-bottom: .8rem; }
    .insight-card { padding: 1rem 1.1rem; border: 1px solid #e4e7ec; border-radius: 12px;
                    background: #ffffff; min-height: 135px; }
    .insight-card h4 { margin: 0 0 .45rem 0; font-size: 1rem; }
    .insight-card p { margin: 0; color: #475467; font-size: .92rem; line-height: 1.45; }
    div[data-testid="stMetric"] { border: 1px solid #e4e7ec; border-radius: 12px;
                                  padding: 12px 14px; background: #ffffff; }
    [data-testid="stSidebar"] { border-right: 1px solid #eaecf0; }
</style>
"""


def apply():
    st.markdown(CSS, unsafe_allow_html=True)


def section(title: str, note: str):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-note">{note}</div>', unsafe_allow_html=True)
