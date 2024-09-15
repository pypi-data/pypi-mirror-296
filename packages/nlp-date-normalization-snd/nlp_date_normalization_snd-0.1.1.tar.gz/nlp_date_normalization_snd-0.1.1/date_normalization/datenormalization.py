from .jalaliandatenormalization import JalalianDateNormalization
from .gregoriandatenormalization import GregorianDateNormalization
from .publicnormalization import PublicNormalization
import re


class DateNormalization(GregorianDateNormalization, JalalianDateNormalization):

    # Remove duplicate dates req
    _remove_duplicate_dates_req = r'\b(\d{4})-(\d{2})-(\d{2})\b'

    # In this method, we thoroughly check the text we received, extract the solar and Gregorian dates from it and
    # convert it to the standard Gregorian date and remove duplicate dates in it.
    def normalization_text(self, text_date: str) -> str:
        pn = PublicNormalization()
        text_date = pn.normalization_numbers(text_date)
        text_date = self.j_normalization_dates(text_date)
        text_date = self.g_normalization_dates(text_date)
        text_date = self._remove_duplicate_dates(text_date)
        return pn.normalizing(text_date)

    # In this method, we are removing duplicate dates
    def _remove_duplicate_dates(self, text_date: str) -> str:
        matches = list(re.finditer(self._remove_duplicate_dates_req, text_date))
        seen_dates = {}
        to_remove = set()

        for match in matches:
            date_str = match.group(0)
            if date_str in seen_dates:
                to_remove.add(match.span())
            else:
                seen_dates[date_str] = match.span()

        for start, end in reversed(sorted(to_remove)):
            text_date = text_date[:start] + text_date[end:]

        return re.sub(r'\s+', ' ', text_date)
