"""
Module defining application-wide constants, including predefined font sizes, 
base directory paths, and utility functions for managing application themes 
and Markdown preview styles.
"""

import os

from PySide6.QtGui import QFont

# fonts size
H1=QFont()
H1.setPointSize(30)

H2=QFont()
H2.setPointSize(25)

H3=QFont()
H3.setPointSize(20)

H4=QFont()
H4.setPointSize(15)

BASE_PATH=os.path.dirname(__file__)

css_path=os.path.join(BASE_PATH,"documents_styles", "main_style.css")
with open(css_path,"r", encoding="utf-8") as file:
    markdown_preview_style = file.read() 

def get_css_style() -> str:
    """
    the getter of css style

    Returns: 
        str: content of css file
    """
    return markdown_preview_style

def set_css_style(css_file_name: str) -> None:
    """
    set new css file for document
    
    Args:
        css_file_name (str): name of css file 
    """
    global css_path, markdown_preview_style 
    css_path=os.path.join(BASE_PATH,"documents_styles",css_file_name)

    with open(css_path,"r", encoding="utf-8") as file:
        markdown_preview_style = file.read()

QSS_PATH=os.path.join(BASE_PATH,"app_styles","dark_theme.qss")
with open(QSS_PATH,"r", encoding="utf-8") as file:
    qss_style_sheet = file.read()
    

