from lxml import html
from mkdocs.config import config_options
from .elements import (
    create_style_element,
    create_bpmn_lib_element,
    create_render_script_element,
)
from mkdocs.plugins import BasePlugin

DEFAULT_BPMN_LIB_URL = (
    "https://unpkg.com/bpmn-js@17.11.1/dist/bpmn-navigated-viewer.production.min.js"
)


class BpmnPlugin(BasePlugin):
    config_scheme = (
        ("bpmn_lib_url", config_options.Type(str, default=DEFAULT_BPMN_LIB_URL)),
    )

    style_element = None
    lib_element = None
    render_element = None

    def on_config(self, config):
        self.style_element = create_style_element()
        self.lib_element = create_bpmn_lib_element(self.config["bpmn_lib_url"])
        self.render_element = create_render_script_element()

    def on_post_page(self, output_content, config, page, **kwargs):
        if ".bpmn" not in output_content:
            return output_content

        tree = html.fromstring(output_content)
        imgs = [
            img for img in tree.xpath("//img") if img.attrib["src"].endswith(".bpmn")
        ]

        if not imgs:
            return output_content

        for i, img in enumerate(imgs):
            img.tag = "span"
            img.attrib["id"] = f"mk-bpmn-container-{i}"
            img.attrib["class"] = "mk-bpmn-container"

        tree.body.append(self.style_element)
        tree.body.append(self.lib_element)
        tree.body.append(self.render_element)

        return html.tostring(tree, pretty_print=True).decode("utf-8")
