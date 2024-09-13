import requests
from pydantic import BaseModel, Field

from plurally.models.misc import Table
from plurally.models.node import Node


class ScrapePageBase(Node):
    class OutputSchema(BaseModel):
        content: str = Field(
            title="Content",
            description="The content of the page",
        )

    def _get_html_content(self, url):
        req = requests.get(url)
        req.raise_for_status()

        return req.text

    def scrape(self, url, selector):
        from bs4 import BeautifulSoup

        req = requests.get(url)
        req.raise_for_status()

        html_content = self._get_html_content(url)

        soup = BeautifulSoup(html_content, "html.parser")
        selected = soup.select_one(selector)
        if selected is None:
            self.outputs = {"content": ""}
        else:
            content = selected.get_text()
            self.outputs = {"content": content}


class ScrapePageDynamic(ScrapePageBase):

    class InitSchema(Node.InitSchema):
        """Scrape the content of a webpage, with dynamic inputs"""

    class InputSchema(Node.InputSchema):
        url: str = Field(
            title="URL",
            description="The URL of the page to scrape",
            examples=["https://example.com"],
        )
        selector: str = Field(
            title="Selector",
            description="The selector to use to scrape the content",
            examples=["h1"],
        )

    DESC = InitSchema.__doc__

    def forward(self, node_inputs):
        return self.scrape(node_inputs.url, node_inputs.selector)


class ScrapePagesDynamic(ScrapePageBase):

    class InitSchema(Node.InitSchema):
        """Scrape the content of multiple webpages. Each row in the input table should contain a URL and a selector. Columns should be named 'url' and 'selector'."""

    class InputSchema(Node.InputSchema):
        urls_and_selectors: Table = Field(
            title="URLs and Selectors",
            description="The URLs and selectors to use to scrape the content",
        )

    class OutputSchema(BaseModel):
        contents: Table = Field(
            title="Contents",
            description="The contents of the pages",
        )

    DESC = InitSchema.__doc__

    def forward(self, node_inputs):
        urls_and_selectors = node_inputs.urls_and_selectors
        contents = []
        for row in urls_and_selectors.data:
            url = row["url"]
            selector = row["selector"]
            self.scrape(url, selector)
            contents.append({"content": self.outputs["content"]})
        self.outputs = {"contents": Table(data=contents)}


class ScrapePageStatic(ScrapePageBase):

    class InitSchema(Node.InitSchema):
        """Scrape the content of a webpage, with static inputs"""

        url: str = Field(
            title="URL",
            description="The URL of the page to scrape",
            examples=["https://example.com"],
        )
        selector: str = Field(
            title="Selector",
            description="The selector to use to scrape the content",
            examples=["h1"],
        )

    class InputSchema(Node.InputSchema): ...

    DESC = InitSchema.__doc__

    def __init__(self, init_inputs: InitSchema, outputs=None):
        self.url = init_inputs.url
        self.selector = init_inputs.selector
        super().__init__(init_inputs, outputs)

    def forward(self, _: Node.InputSchema):
        return self.scrape(self.url, self.selector)

    def serialize(self):
        return super().serialize() | {
            "url": self.url,
            "selector": self.selector,
        }


__all__ = ["ScrapePageDynamic", "ScrapePageStatic", "ScrapePagesDynamic"]
