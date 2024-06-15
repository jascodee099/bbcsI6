import streamlit as st
import pandas as pd
import numpy as np

code = """
def hello():
   print("Hello there!")
"""
st.code(code, language="python", line_numbers=True)
