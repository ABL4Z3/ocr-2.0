from core.page_batch import PageBatch


class BatchPlanner:

    def create_batches(self, pages):

        if not pages:
            return []

        batches = []

        current = [pages[0]]

        current_extractor = pages[0].extractor

        for page in pages[1:]:

            if page.extractor == current_extractor:

                current.append(page)

            else:

                batches.append(
                    PageBatch(
                        extractor=current_extractor,
                        pages=current
                    )
                )

                current = [page]

                current_extractor = page.extractor

        batches.append(
            PageBatch(
                extractor=current_extractor,
                pages=current
            )
        )

        return batches