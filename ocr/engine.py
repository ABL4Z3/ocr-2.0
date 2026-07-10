from paddleocr import PPStructureV3


class OCREngine:

    _instance = None

    @classmethod
    def get(cls):

        if cls._instance is None:

            cls._instance = PPStructureV3(

                lang="hi",

                text_recognition_model_name="devanagari_PP-OCRv5_mobile_rec"

            )

        return cls._instance