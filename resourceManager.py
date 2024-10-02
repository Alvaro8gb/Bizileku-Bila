import streamlit as st
import base64
from PIL import Image


def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    return html


@st.cache_data
def load_resources():
    with open("static/flag.svg") as f:
        logo_string = f.read()

    logo = render_svg(logo_string)

    return logo


@st.cache_data
def load_image(image_path):
    img = Image.open(image_path)
    return img
