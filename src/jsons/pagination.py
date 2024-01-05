import math


class Pagination:
    def __init__(self, total_rows=0, rows_per_page=10, current_page=1):
        self._total_rows = total_rows
        self._total_pages = math.ceil(total_rows / rows_per_page)
        self._current_page = current_page

        # 是否在第一页之后且不超过最后一页
        self._has_prev_page = current_page > 1 and current_page <= self._total_pages

        # 是否在第一页及之后且在最后一页之前
        self._has_next_page = current_page >= 1 and current_page < self._total_pages

        self._rows_per_page = rows_per_page
        self._paged_data = []  # 泛型对象数组，存储查询到的每页数据

    # Setter methods
    def set_total_rows(self, total_rows):
        self._total_rows = total_rows
        self._update_pagination()

    def set_rows_per_page(self, rows_per_page):
        self._rows_per_page = rows_per_page
        self._update_pagination()

    def set_current_page(self, current_page):
        self._current_page = current_page
        self._update_pagination()

    # Getter methods
    @property
    def total_rows(self):
        return self._total_rows

    @property
    def total_pages(self):
        return self._total_pages

    @property
    def current_page(self):
        return self._current_page

    @property
    def has_prev_page(self):
        return self._has_prev_page

    @property
    def has_next_page(self):
        return self._has_next_page

    @property
    def rows_per_page(self):
        return self._rows_per_page

    @property
    def paged_data(self):
        return self._paged_data

    # Private method to update pagination properties after changing total_rows, rows_per_page, or current_page
    def _update_pagination(self):
        self._total_pages = math.ceil(self._total_rows / self._rows_per_page)

        self._has_prev_page = (
            self._current_page > 1 and self._current_page <= self._total_pages
        )
        self._has_next_page = (
            self._current_page >= 1 and self._current_page < self._total_pages
        )

    # to_string method
    def to_string(self):
        return f"Total Rows: {self.total_rows}, Total Pages: {self.total_pages}, Current Page: {self.current_page}, Rows per Page: {self.rows_per_page}, Has Previous Page: {self.has_prev_page}, Has Next Page: {self.has_next_page}"

    def to_dictionary(self):
        return {
            "total_rows": self._total_rows,
            "total_pages": self._total_pages,
            "current_page": self._current_page,
            "has_prev_page": self._has_prev_page,
            "has_next_page": self._has_next_page,
            "rows_per_page": self._rows_per_page,
            "paged_data": self._paged_data,
        }
