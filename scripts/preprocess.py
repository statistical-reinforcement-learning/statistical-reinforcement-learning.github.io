import mistune

class LaTeXMarkdownRenderer(mistune.HTMLRenderer):
    def block_math(self, text):
        return f"$$ {text} $$"
    
    def inline_math(self, text):
        return f"\\({text}\\)"

markdown = mistune.create_markdown(renderer=LaTeXMarkdownRenderer(), plugins=['math'])
