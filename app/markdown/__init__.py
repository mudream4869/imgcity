import markdown
from bs4 import BeautifulSoup
from markdown.inlinepatterns import SimpleTagInlineProcessor
from markdown.extensions import Extension


class DelExtension(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            SimpleTagInlineProcessor(r'()~~(.*?)~~', 'del'), 'del', 175)


markdown_extensions = ['tables', 'fenced_code', 'app.markdown:DelExtension']


def markdownToHTML(content: str):
    """
        Transform markdown to HTML
    """
    return markdown.markdown(content, extensions=markdown_extensions)


def abbrMarkdownHTML(content: str, line_count=3):
    """
        Tranform markdown to HTML and retain few lines
    """
    html = markdownToHTML(content)
    soup = BeautifulSoup(html, 'html.parser')

    result = []
    for ele in soup.find_all('p')[:line_count]:
        result.append(ele.text)

    return '<br>\n'.join(result) + '<br>'
