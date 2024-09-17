from bs4 import BeautifulSoup, Tag
from loguru import logger


def merge_parent_with_only_child(parent: Tag, child: Tag) -> Tag:
    child.attrs["id"] = child.get("id") if not parent.get("id") and child.get("id") else parent.get("id")
    child.attrs["class"] = parent.get("class", []) + child.get("class", [])
    parent.replace_with(child)
    return child


def simplify_structure(tag: Tag) -> None:
    if tag is None:
        return

    if tag.name in ["script", "style", "svg", "iframe"]:
        logger.info(f"Removing tag <{tag.name}> and its contents")
        tag.decompose()
        return

    while True:
        children = [child for child in tag.contents if isinstance(child, Tag)]
        # logger.debug(f"Processing <{tag.name}> with {len(children)} children")
        if len(children) != 1 or not isinstance(children[0], Tag) or children[0].name != "div":
            break

        only_child = children[0]
        logger.debug(f"Merging <{tag.name}> with its only child <{only_child.name}>")
        tag = merge_parent_with_only_child(tag, only_child)

    for child in list(tag.children):
        if isinstance(child, Tag):
            simplify_structure(child)


def collapse(content: str = None) -> str:
    if not content:
        raise ValueError("HTML data is empty")

    soup = BeautifulSoup(content, "html.parser")
    if soup.body:
        simplify_structure(soup)
    return soup.prettify()


if __name__ == "__main__":
    content = open("./tests/input.html", "r", encoding="utf-8").read()
    collapsed = collapse(content)

    with open("./tests/got.html", "w", encoding="utf-8") as f:
        f.write(collapsed)
