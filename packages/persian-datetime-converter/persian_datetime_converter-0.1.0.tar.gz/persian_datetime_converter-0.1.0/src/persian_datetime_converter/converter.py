# src/persian_datetime_converter/converter.py

"""
Persian Date Converter
-----------------------
This module provides a Python class to convert Python datetime objects
to Persian (Jalali) calendar dates without using any external libraries.

Author: Mohammad Reza Bahmani (bahmanymb@gmail.com)
"""

import datetime


class PersianDateConverter:
    GREGORIAN_EPOCH = 1721425.5
    PERSIAN_EPOCH = 1948320.5

    @staticmethod
    def gregorian_to_jdn(year, month, day):
        # Convert Gregorian date to Julian Day Number (JDN)
        return (PersianDateConverter.GREGORIAN_EPOCH - 1) + 365 * (year - 1) + (year - 1) // 4 - (year - 1) // 100 + (year - 1) // 400 + (367 * month - 362) // 12 + (
            0 if month <= 2 else -1 if PersianDateConverter.is_leap_gregorian(year) else -2) + day

    @staticmethod
    def jdn_to_persian(jdn):
        # Convert Julian Day Number (JDN) to Persian date
        depoch = jdn - PersianDateConverter.persian_to_jdn(475, 1, 1)
        cycle = depoch // 1029983
        cyear = depoch % 1029983

        if cyear == 1029982:
            ycycle = 2820
        else:
            aux1 = cyear // 366
            aux2 = cyear % 366
            ycycle = ((2134 * aux1 + 2816 * aux2 + 2815) // 1028522) + aux1 + 1

        year = ycycle + 2820 * cycle + 474
        if year <= 0:
            year -= 1

        yday = jdn - PersianDateConverter.persian_to_jdn(year, 1, 1) + 1
        month = (yday <= 186) and (yday - 1) // 31 + 1 or (yday - 187) // 30 + 7
        day = (jdn - PersianDateConverter.persian_to_jdn(year, month, 1)) + 1

        return year, month, day

    @staticmethod
    def persian_to_jdn(year, month, day):
        # Convert Persian date to Julian Day Number (JDN)
        epbase = year - 474 if year >= 0 else year - 473
        epyear = 474 + epbase % 2820
        return day + ((month <= 7) and (month - 1) * 31 or (month - 1) * 30 + 6) + (epyear * 682 - 110) // 2816 + (epyear - 1) * 365 + epbase // 2820 * 1029983 + (PersianDateConverter.PERSIAN_EPOCH - 1)

    @staticmethod
    def is_leap_gregorian(year):
        # Check if the Gregorian year is a leap year
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    @staticmethod
    def convert(datetime_obj):
        # Convert Python datetime to Persian date
        jdn = PersianDateConverter.gregorian_to_jdn(datetime_obj.year, datetime_obj.month, datetime_obj.day)
        persian_date = PersianDateConverter.jdn_to_persian(jdn)
        return persian_date
