"""This module provides functions to load and inject CSS styles into a Streamlit application."""

import os
import streamlit as st


def load_css(file_path: str):
    """Load CSS from external file and inject into Streamlit"""
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            st.error(f"CSS file {file_path} not found")
            return

        # Read CSS content
        with open(file_path, "r", encoding="utf-8") as f:
            css_content = f.read()

        # Inject CSS into Streamlit
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

    except (FileNotFoundError, IOError, UnicodeDecodeError) as e:
        st.error(f"Error loading CSS file {file_path}: {e}")


def load_multiple_css(file_paths: list):
    """Load multiple CSS files"""
    for file_path in file_paths:
        load_css(file_path)
