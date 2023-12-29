from flask import render_template

import records


def get_pagin_blog_entry_page():
    html_path = "essay/pagin-blog-entry.html"
    return render_template(html_path)
