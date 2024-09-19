from bs4 import BeautifulSoup, Comment
import re


def clean_html(html_string: str) -> str:
    # Parse the HTML
    soup = BeautifulSoup(html_string, "html.parser")

    # Remove all script and style elements
    for script in soup(["script", "style"]):
        script.decompose()

    # Remove HTML comments
    for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Remove empty tags
    for tag in soup.find_all():
        if len(tag.get_text(strip=True)) == 0 and len(tag.find_all()) == 0:
            tag.decompose()

    # Get the cleaned HTML as a string
    cleaned_html = str(soup)

    # Remove white spaces between tags
    cleaned_html: str = cleaned_html.replace(">\n<", "><")

    # Remove multiple empty lines
    cleaned_html = re.sub(r"\n\s*\n", "\n", cleaned_html)

    return cleaned_html
