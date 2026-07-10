from validator.table_validator import TableValidator
from core.elements import Table


class DocumentValidator:

    def __init__(self):

        self.validator = TableValidator()

    def validate(self, document):

        broken = []

        for page in document.pages:

            for element in page.elements:

                if isinstance(element, Table):

                    if not self.validator.is_valid(element):

                        broken.append((page, element))

        return broken