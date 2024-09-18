import json

import pytest

from parse_document_model import Document, Page
from parse_document_model.attributes import PageAttributes, TextAttributes
from parse_document_model.marks import Mark, TextStyleMark, UrlMark


def test_read_from_json():
    filepaths = ["test/data/extract-text-1.json",
                 "test/data/extract-text-2.json",
                 "test/data/extract-text-empty.json"]
    for filepath in filepaths:
        doc_json = json.load(open(filepath, "r"))
        doc = Document(**doc_json)

        # Check the Document
        assert doc.category == "doc"
        assert isinstance(doc.content, list)

        # Check the Page
        for page in doc.content:
            assert isinstance(page, Page)
            assert page.category == "page"
            assert isinstance(page.attributes, PageAttributes)
            assert isinstance(page.content, list)

            # Check Text
            for text in page.content:
                assert text.category in ["page-header", "title", "heading", "body", "footer"]
                assert isinstance(text.content, str)
                assert isinstance(text.attributes, TextAttributes)
                assert isinstance(text.marks, list)

                # Check Marks
                for mark in text.marks:
                    assert isinstance(mark, Mark)


def test_style_marks():
    text_style_mark_json = [{"category": "textStyle", "font": {"id": "1", "name": "test-font", "size": 1}},
                            {"category": "textStyle", "color": {"id": "1", "r": 0, "g": 0, "b": 0}},
                            {"category": "textStyle", "font": {"id": "1", "name": "test-font", "size": 1},
                             "color": {"id": "1", "r": 0, "g": 0, "b": 0}},
                            {"category": "textStyle"},
                            {"category": "textStyle", "url": "test-url"}]
    for mark_json in text_style_mark_json:
        if "font" in mark_json or "color" in mark_json:
            mark = TextStyleMark(**mark_json)
            assert isinstance(mark, TextStyleMark)
        else:
            with pytest.raises(ValueError):
                TextStyleMark(**mark_json)


def test_url_marks():
    url_mark_json = [{"category": "link", "url": "test-url"},
                     {"category": "link"},
                     {"category": "link", "font": {"id": "1", "name": "test-font", "size": 1}},
                     {"category": "link", "color": {"id": "1", "r": 0, "g": 0, "b": 0}}]
    for mark_json in url_mark_json:
        if "url" in mark_json:
            mark = UrlMark(**mark_json)
            assert isinstance(mark, UrlMark)
        else:
            with pytest.raises(ValueError):
                UrlMark(**mark_json)
