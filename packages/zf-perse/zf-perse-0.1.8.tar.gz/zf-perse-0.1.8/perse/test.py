from bs4 import BeautifulSoup

from .get import simplify_structure

test_html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Test</title>
    </head>
    <body>
        <div id="parent" class="container">
            <div id="child" class="row">
                <p>Some text1</p>
                <p>Some text2</p>
            </div>
        </div>
    </body>
</html>
"""

soup = BeautifulSoup(test_html, "html.parser")
simplify_structure(soup.body)

print(soup.prettify())
