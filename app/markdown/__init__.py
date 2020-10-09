import markdown
from bs4 import BeautifulSoup


def markdownToHTML(content: str):
    """
        Transform markdown to HTML
    """
    return markdown.markdown(
        content, extensions=['tables', 'fenced_code'])


def abbrMarkdownHTML(content: str, line_count=3):
    """
        Tranform markdown to HTML and retain few lines
    """
    html = markdownToHTML(content)
    soup = BeautifulSoup(html, 'html.parser')

    result = []
    for ele in soup.find_all('p')[:3]:
        result.append(ele.text)

    return '<br>\n'.join(result) + '<br>'
