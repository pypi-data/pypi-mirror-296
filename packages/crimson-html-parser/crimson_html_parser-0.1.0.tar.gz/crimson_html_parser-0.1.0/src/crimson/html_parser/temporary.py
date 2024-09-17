from typing import List, Dict, Optional, Any
import json
from bs4 import BeautifulSoup, Tag, NavigableString
from anytree import Node, RenderTree


def wrap_by_json(data: Dict):
    return json.loads(json.dumps(data))


def extract_all_attrs(soup: BeautifulSoup, name: str):
    tags: List[Tag] = soup.find_all(
        name=name,
    )

    json_data: Dict[str, List] = {}

    for tag in tags:
        for attr, item in tag.attrs.items():
            if not isinstance(item, list):
                item = [item]

            if attr in json_data.keys():
                json_data[attr] += item
            else:
                json_data[attr] = item

    for key, value in json_data.items():
        json_data[key] = list(set(value))

    return wrap_by_json(json_data)


class HTMLNode(Node):
    def __init__(self, name, parent=None, children=None, **kwargs):
        super().__init__(name, parent, children, **kwargs)
        self.bs_element: Tag = None


def print_node(node: HTMLNode):
    for pre, _, node in RenderTree(node):
        print(f"{pre}{node.name}")


def soup_to_tree(soup_element, parent: Optional[HTMLNode] = None) -> HTMLNode:
    """
    BeautifulSoup 요소를 anytree HTMLNode로 변환합니다.

    :param soup_element: BeautifulSoup 태그 또는 NavigableString
    :param parent: 부모 HTMLNode (옵션)
    :return: HTMLNode
    """
    if isinstance(soup_element, NavigableString):
        node = HTMLNode(
            f"Text: {soup_element[:20]}{'...' if len(soup_element) > 20 else ''}",
            parent=parent,
        )
        node.bs_element = soup_element
        return node

    # 태그의 이름과 주요 속성들을 포함하여 노드 이름 생성
    attrs = []
    if "class" in soup_element.attrs:
        attrs.append(f"class='{' '.join(soup_element['class'])}'")
    if "id" in soup_element.attrs:
        attrs.append(f"id='{soup_element['id']}'")

    node_name = soup_element.name
    if attrs:
        node_name += f"[{', '.join(attrs)}]"

    node = HTMLNode(node_name, parent=parent)
    node.bs_element = soup_element

    for child in soup_element.children:
        if child.name is not None or not isinstance(child, str) or child.strip():
            soup_to_tree(child, node)

    return node


def get_original_element(node: HTMLNode) -> Any:
    """
    HTMLNode로부터 원본 BeautifulSoup 요소를 반환합니다.

    :param node: HTMLNode
    :return: BeautifulSoup 요소 (Tag 또는 NavigableString)
    """
    return node.bs_element


def extract_unit_info(unit_event: Tag):
    info = {
        "title": unit_event.find("img")["alt"],
        "month": unit_event.find("span", class_="month").text,
        "date": unit_event.find("span", class_="date").text,
        "availability": unit_event.find("div", class_="descriptor").text,
    }

    return info


def extract_infos(event_divs: List[Tag]):
    infos = []

    try:
        for event_div in event_divs:
            infos.append(extract_unit_info(event_div))
    except Exception as e:
        print("Invalid div caused an error: ", e)

    return infos
