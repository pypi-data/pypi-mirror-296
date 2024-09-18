from typing import TypedDict


class CurrentPagePagination(TypedDict, total=True):
    current_page: int
    pages: int
    per_page: int
    total: int


class PagePagination(TypedDict, total=True):
    page: int
    pages: int
    per_page: int
    total: int


class RowsPagination(TypedDict, total=True):
    page: int
    size: int
    total_page: int
    total_rows: int
