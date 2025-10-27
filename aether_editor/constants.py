from PySide6.QtGui import QColor, QFont

#tamanhos de fonte
H1=QFont()
H1.setPointSize(30)

H2=QFont()
H2.setPointSize(25)

H3=QFont()
H3.setPointSize(20)

H4=QFont()
H4.setPointSize(15)

# --- Cores e Constantes do Editor de Código ---
LINE_NUMBER_BG_COLOR = QColor(30, 33, 38)
LINE_NUMBER_TEXT_COLOR = QColor(100, 105, 115)
HIGHLIGHT_LINE_COLOR = QColor(68, 71, 79, 150)

# QSS para o PySide6 (Tema Global Escuro) ---
GLOBAL_DARK_THEME_CSS = """
    QMainWindow, QWidget {
        background-color: #282c34; 
        color: #abb2bf; 
    }
    QPlainTextEdit, QTextEdit {
        background-color: #21252b; 
        border: 1px solid #3e4451;
        padding: 5px; 
        color: #abb2bf; 
    }
    QPushButton {
        padding: 10px 15px;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        margin-right: 5px;
    }
    QPushButton:hover {
        opacity: 0.4;
    }
"""

# --- HTML/CSS para o Preview ---
MARKDOWN_PREVIEW_STYLE = """
    img{max-width: 400px; height: auto;}
    body { 
        background-color: #21252b; 
        color: #abb2bf; 
        
        margin: 20px;
    }
    h1, h2, h3 { 
        color: #f93c9b; 
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 15px 0;
        color: #abb2bf;
    }
    th, td {
        border: 1px solid #3e4451;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #282c34;
    }  

    hr{ background: #3e4451; border: none; height: 1px; }

    pre, code {
        background-color: #272822; 
        color: #f8f8f2; 
        padding: 10px;
        border-radius: 5px;
        overflow-x: auto;
        display: block; 
    }

    blockquote {
        background-color: #2c313a; 
        margin-left: 10px;
        margin-right: 10px;
        margin-top: 15px;
        margin-bottom: 15px;
        padding: 10px 15px;
        border-left: 4px solid #5694f9; 
        font-style: italic;
        color: #b3c0d8; 
        border-radius: 4px; 
    }
    
    /* regras de estilo do pygments */
    .codehilite .hll { background-color: #444444 }
    .codehilite .c { color: #75715e; font-style: italic }
    .codehilite .k { color: #66d9ef; font-weight: bold } 
    .codehilite .kc { color: #66d9ef; font-weight: bold } 
    .codehilite .kd { color: #66d9ef; font-weight: bold }
    .codehilite .kn { color: #f92672; font-weight: bold }
    .codehilite .kp { color: #960050 }
    .codehilite .kr { color: #66d9ef; font-weight: bold }
    .codehilite .kt { color: #a6e22e; font-weight: bold }
    .codehilite .m { color: #ae81ff } 
    .codehilite .s { color: #e6db74 } 
    
    .codehilite .na { color: #a6e22e }
    .codehilite .nb { color: #f8f8f2 }
    .codehilite .nc { color: #a6e22e; font-weight: bold }
    .codehilite .nf { color: #a6e22e; font-weight: bold }
    .codehilite .nt { color: #f92672 }
    .codehilite .nv { color: #f8f8f2 }
    .codehilite .ow { color: #f92672; font-weight: bold }
    .codehilite .o { color: #f92672 }
    .codehilite .mi { color: #ae81ff }
    .codehilite .bp { color: #66d9ef } 
    .codehilite .dl { color: #e6db74 }
    .codehilite .sd { color: #e6db74; font-style: italic } 
    .codehilite .se { color: #e6db74 }
    .codehilite .sh { color: #e6db74 }
    .codehilite .si { color: #e6db74 }
    .codehilite .sx { color: #e6db74 }
    .codehilite .sr { color: #e6db74 }
    .codehilite .s1 { color: #e6db74 }
    .codehilite .ss { color: #e6db74 }
    .codehilite .err { color: #f92672; background-color: #5d0030 }
    .codehilite .dl { color: #e6db74 } /* Adiciona o delimiter, já estava em parte na sua lista */
    .codehilite .s2 { color: #e6db74 } /* String - Delimitador de aspas duplas */
    .codehilite .sa { color: #e6db74 } /* String - Atributo */
    .codehilite .sb { color: #e6db74 } /* String - Binária */
    .codehilite .sc { color: #e6db74 } /* String - Caractere */
    .codehilite .dl { color: #e6db74 } /* String - Delimitador */
    .codehilite .s { color: #e6db74 }  /* String genérica, já estava na sua lista */

    /* Adicionado: Nomes */
    .codehilite .nd { color: #a6e22e } 
    .codehilite .ni { color: #f8f8f2 } 
    .codehilite .ne { color: #a6e22e; font-weight: bold } 
    .codehilite .no { color: #f92672 } 
    .codehilite .bp { color: #66d9ef } 
    .codehilite .vg { color: #f8f8f2 } 
    .codehilite .vi { color: #f8f8f2 } 
    .codehilite .vc { color: #f8f8f2 } 
    .codehilite .cp { color: #75715e; font-style: italic } 
    .codehilite .cs { color: #75715e; font-style: italic } 
    .codehilite .ge { font-style: italic } 
    .codehilite .gh { color: #f92672 } 
    .codehilite .gp { color: #f8f8f2 } 
    .codehilite .gu { color: #75715e; font-style: italic } 
    .codehilite .w { color: #f8f8f2 } 
    .codehilite .dl { color: #f8f8f2 } 
    .codehilite .il { color: #ae81ff }

    .codehilite .c { color: #78a9c0; font-style: italic } 
    .codehilite .cm { color: #78a9c0; font-style: italic }
    .codehilite .cp { color: #78a9c0; font-style: italic }
    .codehilite .c1 { color: #78a9c0; font-style: italic }
    .codehilite .cs { color: #78a9c0; font-style: italic }
    .codehilite .ch { color: #78a9c0; font-style: italic }
"""