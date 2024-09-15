import re
import datetime
import jdatetime


class CNLPDateManager:
    # Jalalian months name map
    _jalalian_months_map = {
        'فروردین': 1,
        'اردیبهشت': 2,
        'خرداد': 3,
        'تیر': 4,
        'مرداد': 5,
        'شهریور': 6,
        'مهر': 7,
        'آبان': 8,
        'آذر': 9,
        'دی': 10,
        'بهمن': 11,
        'اسفند': 12,
    }

    # gregorian months name map
    _gregorian_months_map = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }

    # The names of the months of the year in persian and English
    _gregorian_months_translator_map = {
        'ژانویه': 'january',
        'فوریه': 'february',
        'مارس': 'march',
        'آوریل': 'april',
        ' مه ': ' may ',
        'ژوئن': 'june',
        'ژوئیه': 'july',
        'جولای': 'july',
        ' اوت ': ' august ',
        'آگوست': 'august',
        'سپتامبر': 'september',
        'اکتبر': 'october',
        'نوامبر': 'november',
        'دسامبر': 'december'
    }

    # jalalian date methods
    # in this method, we will convert the jalalian dates that use the names of the months into standard Gregorian dates
    def convert_str_jalali_to_standard_date(self, text_date: str) -> str:
        if len(text_date):
            text_date = (text_date.replace("ماه سال", "").replace("ماه", "")
                         .replace("سال", '').replace(",", "").replace('-', ' '))
            text_date = re.sub(r'\s+', ' ', text_date).strip()
            parts = text_date.lower().split()
            parts, day = self._find_day(parts)
            year, month = self._find_jalalian_month_by_name(parts)

            return jdatetime.date(int(year), int(month), int(day)).togregorian().isoformat()

        return text_date

    # During this period, we convert the jalalian dates, which are full of numbers, into standard Gregorian dates
    def convert_fmt_jalali_to_standard_date(self, text_date: str) -> str:
        if len(text_date):
            text_date = (text_date.replace("/", '-'))
            text_date = re.sub(r'\s+', ' ', text_date).strip()
            parts = text_date.lower().split("-")
            parts, day = self._find_day(parts)
            year, month, day = self._find_jalalian_month(parts, day)
            jalali_year = jdatetime.date.today().year + 100

            if int(year) <= jalali_year:
                return jdatetime.date(int(year), int(month), int(day)).togregorian().isoformat()

        return text_date

    # In this method, we return its position using the name of the month.
    def _find_jalalian_month_by_name(self, parts: list) -> tuple:
        month = "01"
        year = ""
        for part in parts:
            position = self._found_jalalian_month_position(part)
            if position != '':
                month = position
            else:
                year = part

        if year == '':
            year = jdatetime.date.today().year
        return year, month

    # In this method, we found its position using the name of the month.
    def _found_jalalian_month_position(self, month_jalali_name: str) -> str:
        for list_month, month_position in self._jalalian_months_map.items():
            if list_month.lower() == month_jalali_name:
                _position = str(month_position).lower()
                if len(_position) == 2:
                    return _position
                else:
                    return "0" + _position
        return ""

    # In this method, we look for the jalalian month in the text that is given as a date
    @staticmethod
    def _find_jalalian_month(parts: list, day) -> tuple:
        month = "01"
        month_not_founded = True
        _day = day
        year = ''
        for part in parts:
            if month_not_founded and 1 <= len(part) <= 2:
                try:
                    _part = int(part)
                    if 1 <= _part <= 12:
                        if len(part) == 2:
                            month = part
                        else:
                            month = "0" + part
                        month_not_founded = False
                    elif int(day) < _part and 1 <= int(day) <= 12:
                        month_not_founded = False
                        month = day
                        if len(part) == 2:
                            _day = part
                        else:
                            _day = "0" + part
                except:
                    year = part
            else:
                year = part
        if year == '':
            year = jdatetime.date.today().year
        return year, month, _day

    # gregorian date methods
    # in this method, we will convert the gregorian dates that use the names of the months into standard Gregorian dates
    def str_to_gregorian_standard_date(self, text_date: str) -> str:
        if len(text_date):
            text_date = (text_date.replace("th of", "").replace("th", "")
                         .replace("th", "").replace(",", "").replace('-', ' '))
            text_date = re.sub(r'\s+', ' ', text_date).strip()
            parts = text_date.lower().split()
            parts, day = self._find_day(parts)
            year, month = self._find_gregorian_month_by_name(parts)

            return year + '-' + month + "-" + day

        return text_date

    # During this period, we convert the gregorian dates, which are full of numbers, into standard Gregorian dates
    def fmt_to_gregorian_standard_date(self, text_date: str) -> str:
        if len(text_date):
            text_date = (text_date.replace("/", "-"))
            text_date = re.sub(r'\s+', ' ', text_date).strip()
            parts = text_date.lower().split('-')
            parts, day = self._find_day(parts)
            year, month, day = self._find_gregorian_month(parts, day)
            print(parts)

            return year + '-' + month + "-" + day

        return text_date

    # In this method, we change the months written in Persian to English.
    def fixing_text_gregorian_months(self, text: str) -> str:
        for key, value in self._gregorian_months_translator_map.items():
            text = text.replace(key, value)
        return text.lower()

    # In this method, we use the name of the Gregorian month to return its position numerically.
    def _find_gregorian_month_by_name(self, parts: list) -> tuple:
        month = "01"
        year = ""
        for part in parts:
            if part == 'may':
                month = "05"
            elif part == 'june':
                month = "06"
            elif part == 'july':
                month = "07"
            elif len(part) > 4:
                for list_month, month_position in self._gregorian_months_map.items():
                    if list_month.lower() == part:
                        _position = str(month_position).lower()
                        if len(_position) == 2:
                            month = _position
                        else:
                            month = "0" + _position
                        continue
            else:
                year = part

        if year == '':
            year = str(datetime.datetime.now().year)
        return year, month

    # In this method, we look for the gregorian month in the text that is given as a date
    @staticmethod
    def _find_gregorian_month(parts: list, day) -> tuple:
        month = "01"
        month_not_founded = True
        year = ''
        _day = day
        for part in parts:
            if month_not_founded and 1 <= len(part) <= 2:
                _part = int(part)
                if 1 <= _part <= 12:
                    if len(part) == 2:
                        month = part
                    else:
                        month = "0" + part
                    month_not_founded = False
                elif int(day) < _part and 1 <= int(day) <= 12:
                    month_not_founded = False
                    month = day
                    if len(part) == 2:
                        _day = part
                    else:
                        _day = "0" + part
            else:
                year = str(datetime.datetime.now().year)
        if year == '':
            year = jdatetime.date.today().year
        return year, month, _day

    # public date methods
    # In this method, we look for the day in the text that is passed as date.
    @staticmethod
    def _find_day(parts: list) -> tuple:
        day = "01"
        day_not_founded = True
        new_parts = []
        parts.reverse()
        for part in parts:
            if day_not_founded and 1 <= len(part) <= 2:
                try:
                    _part = int(part)
                    if 1 <= _part <= 31:
                        if len(part) == 2:
                            day = part
                        else:
                            day = "0" + part
                    day_not_founded = False
                except:
                    new_parts.append(part)
            else:
                new_parts.append(part)
        return new_parts, day
