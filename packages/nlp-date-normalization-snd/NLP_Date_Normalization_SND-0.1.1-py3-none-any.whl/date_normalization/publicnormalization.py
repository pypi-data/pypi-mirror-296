import re


class PublicNormalization:
    # Persian words that refer to numbers
    _number_words_map = {
        "اول": 1,
        "یکم": 1,
        "دوم": 2,
        "سوم": 3,
        "چهارم": 4,
        "پنجم": 5,
        "ششم": 6,
        "هفتم": 7,
        "هشتم": 8,
        "نهم": 9,
        "دهم": 10,
        "یازدهم": 11,
        "دوازدهم": 12,
        "سیزدهم": 13,
        "چهاردهم": 14,
        "پانزدهم": 15,
        "شانزدهم": 16,
        "هفدهم": 17,
        "هجدهم": 18,
        "نوزدهم": 19,
        "بیستم": 20,
        "بیست و یکم": 21,
        "بیست و دوم": 22,
        "بیست و سوم": 23,
        "بیست و چهارم": 24,
        "بیست و پنجم": 25,
        "بیست و ششم": 26,
        "بیست و هفتم": 27,
        "بیست و هشتم": 28,
        "بیست و نهم": 29,
        "سی‌ام": 30,
        "سی و یکم": 31
    }

    # Extra symbols that should be changed in the text
    _translation_extra_symbols = str.maketrans(
        'يكيإأؤئة؛،!ئء',
        'یکیاااوه.,.ی '
    )

    # First step, At this stage, we need to normalize the texts that refer to numbers and change Persian and Arabic
    # numbers to English.
    def normalization_numbers(self, text: str) -> str:
        for word, number in self._number_words_map.items():
            text = re.sub(rf'\b{word}\s\b', str(number) + " ", text)

        translation_table = str.maketrans(
            '۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩',
            '01234567890123456789'
        )
        return text.translate(translation_table)

    # Second step, in this step we remove the extra symbols and change the non-standard characters to standard
    # characters.
    def _repair_text_to_standard_persian_text(self, text: str) -> str:
        text = text.translate(self._translation_extra_symbols)
        text = re.sub(r'[،]{2,}', '،', text)
        text = re.sub(r'[.]{2,}', '.', text)
        text = re.sub(r'[؟]{2,}', '؟', text)
        text = re.sub(r'[!]{2,}', '!', text)
        text = re.sub(r'[ء]{2,}', '', text)
        text = re.sub(r'([.,؟])\1+', r'\1', text)

        return re.sub(r'([.,؟]){2,}', lambda m: m.group(0)[-1], text.translate(self._translation_extra_symbols))

    # third step, in this step, we remove the non-standard signs from the text and optimize the spaces in the text.
    def _clean_text_with_keep_punctuation(self, text: str) -> str:
        text = re.sub(r'[^\w\s.,؟\-/()]', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()

        return self._repair_text_to_standard_persian_text(text).lower()

    # input method to normalize the text in general
    def normalizing(self, text: str) -> str:
        text = self.normalization_numbers(text=text)
        text = self._repair_text_to_standard_persian_text(text=text)
        text = self._clean_text_with_keep_punctuation(text=text)

        return text
