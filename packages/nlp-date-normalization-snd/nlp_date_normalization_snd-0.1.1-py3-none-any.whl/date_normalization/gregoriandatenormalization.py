import re
from .datestandard import CNLPDateManager


class GregorianDateNormalization:
    # Patterns to find gregorian dates in which the names of the months are used
    _gregorian_words_dates_regs = [
        r'\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?(?:,)?)\s+(\d{1,2}(?:st|nd|rd|th)?\s(?:of)?),?\s+(\d{4})\b',
        r'\b(\d{1,2})\s(january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|nov|december|dec)\s(\d{4})\b',
        r'\b(\d{4})-(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?(?:,)?)-(\d{1,2})\b',
        r'\b(\d{4})-(\d{1,2})-(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?(?:,)?)\b',
        r'\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?(?:,)?)-(\d{1,2})-(\d{4})\b',
        r'\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?(?:,)?)-(\d{4})-(\d{1,2})\b',
        r'\b(\d{1,2})-(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?(?:,)?)-(\d{4})\b',
        r'\b(\d{1,2})-(\d{4})-(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?(?:,)?)\b',
        r'\b(january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|nov|december|dec) \d{1,2}, \d{4}\b',
        r'\b(january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|nov|december|dec) \d{1,2}(st|nd|rd|th)?, \d{4}\b',
        r'\b(\d{1,2}(?:st|nd|rd|th)?\s+(?:of)?)\s+(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?(?:,)?),?\s+(\d{4})\b',
        r'\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s(\d{1,2}(?:st|nd|rd|th)?\s(?:of)?)\b',
        r'\b(\d{1,2}(?:st|nd|rd|th)?\s(?:of)?)\s(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b',
        r'\b(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(tember)?|oct(ober)?|nov(ember)?|dec(ember)?)\s(\d{3,4})\b',
        r'\b(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(tember)?|oct(ober)?|nov(ember)?|dec(ember)?)\s(\d{1,2})\b',
        r'\b(\d{3,4})\s(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(tember)?|oct(ober)?|nov(ember)?|dec(ember)?)\b',
        r'\b(\d{1,2})\s(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(tember)?|oct(ober)?|nov(ember)?|dec(ember)?)\b',
        r'\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b',
    ]

    # Patterns to find gregorian dates that refer to a date numerically inside them
    _gregorian_numeric_dates_regs = [
        r'\b(\d{4})[-/](1[0-2])[-/](3[0-1])\b',
        r'\b(\d{4})[-/](1[0-2])[-/]([1-2][0-9])\b',
        r'\b(\d{4})[-/](1[0-2])[-/](0[1-9])\b',
        r'\b(\d{4})[-/](1[0-2])[-/]([1-9])\b',
        r'\b(\d{4})[-/](0[1-9])[-/](3[0-1])\b',
        r'\b(\d{4})[-/](0[1-9])[-/]([1-2][0-9])\b',
        r'\b(\d{4})[-/](0[1-9])[-/](0[1-9])\b',
        r'\b(\d{4})[-/](0[1-9])[-/]([1-9])\b',
        r'\b(\d{4})[-/]([1-9])[-/](3[0-1])\b',
        r'\b(\d{4})[-/]([1-9])[-/](0[1-9])\b',
        r'\b(\d{4})[-/]([1-9])[-/]([1-2][0-9])\b',
        r'\b(\d{4})[-/]([1-9])[-/]([1-9])\b',
        r'\b(\d{4})[-/]([1-9])[-/](1[0-2])\b',
        r'\b(\d{4})[-/](0[1-9])[-/](1[0-9])\b',
        r'\b(\d{4})[-/]([12][0-9])[-/]([1-9])\b',
        r'\b(\d{4})[-/]([12][0-9])[-/](0[1-9])\b',
        r'\b(\d{4})[-/]([12][0-9])[-/](1[0-2])\b',
        r'\b(\d{4})[-/](3[0-9])[-/]([1-9])\b',
        r'\b(\d{4})[-/](3[0-9])[-/](0[1-9])\b',
        r'\b(\d{4})[-/](3[0-9])[-/](1[0-2])\b',
        r'\b(1[0-2])[-/](3[0-1])[-/](\d{4})\b',
        r'\b(1[0-2])[-/]([1-2][0-9])[-/](\d{4})\b',
        r'\b(1[0-2])[-/](0[1-9])[-/](\d{4})\b',
        r'\b(1[0-2])[-/]([1-9])[-/](\d{4})\b',
        r'\b(0[1-9])[-/](3[0-1])[-/](\d{4})\b',
        r'\b(0[1-9])[-/]([1-2][0-9])[-/](\d{4})\b',
        r'\b(0[1-9])[-/](0[1-9])[-/](\d{4})\b',
        r'\b(0[1-9])[-/]([1-9])[-/](\d{4})\b',
        r'\b([1-9])[-/](3[0-1])[-/](\d{4})\b',
        r'\b([1-9])[-/]([1-2][0-9])[-/](\d{4})\b',
        r'\b([1-9])[-/](0[1-9])[-/](\d{4})\b',
        r'\b([1-9])[-/]([1-9])[-/](\d{4})\b',
        r'\b([1-9])[-/](1[0-2])[-/](\d{4})\b',
        r'\b(0[1-9])[-/](1[0-9])[-/](\d{4})\b',
        r'\b([12][0-9])[-/]([1-9])[-/](\d{4})\b',
        r'\b([12][0-9])[-/](0[1-9])[-/](\d{4})\b',
        r'\b([12][0-9])[-/](1[0-2])[-/](\d{4})\b',
        r'\b(3[0-9])[-/]([1-9])[-/](\d{4})\b',
        r'\b(3[0-9])[-/](0[1-9])[-/](\d{4})\b',
        r'\b(3[0-9])[-/](1[0-2])[-/](\d{4})\b',
        r'\b(3[0-1])[-/](\d{4})[-/](1[0-2])\b',
        r'\b([1-9])[-/](\d{4})[-/]([1-9])\b',
        r'\b(0[1-9])[-/](\d{4})[-/]([1-9])\b',
        r'\b(1[0-2])[-/](\d{4})[-/]([1-9])\b',
        r'\b([1-9])[-/](\d{4})[-/](0[1-9])\b',
        r'\b(0[1-9])[-/](\d{4})[-/](0[1-9])\b',
        r'\b(1[0-2])[-/](\d{4})[-/](0[1-9])\b',
        r'\b([1-9])[-/](\d{4})[-/]([12][0-9])\b',
        r'\b(0[1-9])[-/](\d{4})[-/]([12][0-9])\b',
        r'\b(1[0-2])[-/](\d{4})[-/]([12][0-9])\b',
        r'\b([1-9])[-/](\d{4})[-/](3[0-1])\b',
        r'\b(0[1-9])[-/](\d{4})[-/](3[0-1])\b',
        r'\b(1[0-2])[-/](\d{4})[-/](3[0-1])\b',
        r'\b([1-9])[-/](\d{4})[-/]([1-9])\b',
        r'\b([1-9])[-/](\d{4})[-/](0[1-9])\b',
        r'\b([1-9])[-/](\d{4})[-/](1[0-2])\b',
        r'\b(0[1-9])[-/](\d{4})[-/]([1-9])\b',
        r'\b(0[1-9])[-/](\d{4})[-/](0[1-9])\b',
        r'\b(0[1-9])[-/](\d{4})[-/](1[0-2])\b',
        r'\b([12][0-9])[-/](\d{4})[-/]([1-9])\b',
        r'\b([12][0-9])[-/](\d{4})[-/](0[1-9])\b',
        r'\b([12][0-9])[-/](\d{4})[-/](1[0-2])\b',
        r'\b(3[0-1])[-/](\d{4})[-/]([1-9])\b',
        r'\b(3[0-1])[-/](\d{4})[-/](0[1-9])\b',
        r'\b\s([1-9])[-/]([1-9])\s\b',
        r'\b\s([1-9])[-/](0[1-9])\s\b',
        r'\b\s([1-9])[-/]([1-2][0-9])\s\b',
        r'\b\s([1-9])[-/](3[0-1])\s\b',
        r'\b\s(0[1-9])[-/]([1-9])\s\b',
        r'\b\s(0[1-9])[-/](0[1-9])\s\b',
        r'\b\s(0[1-9])[-/]([1-2][0-9])\s\b',
        r'\b\s(0[1-9])[-/](3[0-1])\s\b',
        r'\b\s(1[0-2])[-/]([1-9])\s\b',
        r'\b\s(1[0-2])[-/](0[1-9])\s\b',
        r'\b\s(1[0-2])[-/]([1-2][0-9])\s\b',
        r'\b\s(1[0-2])[-/](3[0-1])\s\b',
        r'\b\s([1-9])[-/]([1-9])\s\b',
        r'\b\s([1-9])[-/](0[1-9])\s\b',
        r'\b\s([1-9])[-/](1[0-2])\s\b',
        r'\b\s(0[1-9])[-/]([1-9])\s\b',
        r'\b\s(0[1-9])[-/](0[1-9])\s\b',
        r'\b\s(0[1-9])[-/](1[0-2])\s\b',
        r'\b\s([1-2][0-9])[-/]([1-9])\s\b',
        r'\b\s([1-2][0-9])[-/](0[1-9])\s\b',
        r'\b\s([1-2][0-9])[-/](1[0-2])\s\b',
        r'\b\s(3[0-1])[-/]([1-9])\s\b',
        r'\b\s(3[0-1])[-/](0[1-9])\s\b',
        r'\b\s(3[0-1])[-/](1[0-2])\s\b',
    ]

    # In this method, we search for gregorian dates by using the patterns of finding dates in which the name of the
    # month is mentioned, and after finding them, we convert them into standard Gregorian dates.
    def g_normalization_dates(self, text: str) -> str:
        date_manager = CNLPDateManager()
        text = date_manager.fixing_text_gregorian_months(text)
        for reg in self._gregorian_words_dates_regs:
            found_items = list(re.finditer(reg, text))
            for found_item in found_items:
                original = found_item.group(0)
                text = text.replace(original, date_manager.str_to_gregorian_standard_date(original))

        return text

    # In this method, we search for gregorian dates by using the patterns of finding dates that are only indicated by
    # numbers, and after finding them, we convert them into standard Gregorian dates.
    def _g_normalization_numeric_dates(self, text: str) -> str:
        for reg in self._gregorian_numeric_dates_regs:
            found_items = list(re.finditer(reg, text))
            for found_item in found_items:
                original = found_item.group(0)
                text = text.replace(original, original.replace('/', '-'))

        return text
