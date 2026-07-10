from core.elements import Table


class TableValidator:

    MIN_HTML_LENGTH = 500

    MIN_ROWS = 3

    def is_valid(self, table: Table):

        html = table.html

        if not html:
            return False

        if len(html) < self.MIN_HTML_LENGTH:
            return False

        rows = html.count("<tr")

        if rows < self.MIN_ROWS:
            return False

        return True