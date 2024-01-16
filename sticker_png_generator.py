from PIL import Image, ImageFont, ImageDraw
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import sys
from jdatetime import date, timedelta
import os

def persian_format(text):
    # Reformats the persian text to be shown correctly
    reshaped_text = reshape(text)
    return get_display(reshaped_text)

template_paths = {
                    "1" : "templates/bahaar.png",
                    "2": "templates/tabestoon.png", 
                    "3": "templates/paeiz.png", 
                    "4": 'templates/zemestoon.png'
                 }

        
import jdatetime

def entofa_num(number_str):
    number_str = str(number_str)
    english_to_persian_digits = {
        '0': '۰',
        '1': '۱',
        '2': '۲',
        '3': '۳',
        '4': '۴',
        '5': '۵',
        '6': '۶',
        '7': '۷',
        '8': '۸',
        '9': '۹',
    }

    persian_number = ''.join(english_to_persian_digits[digit] for digit in number_str if digit in english_to_persian_digits)
    if int(persian_number) < 10:
        persian_number = "۰" + persian_number
    return persian_number


def entofa_month(month_str):
    translator = {
        'Farvardin': 'فروردین',
        'Ordibehesht': 'اردیبهشت',
        'Khordad': 'خرداد',
        'Tir': 'تیر',
        'Mordad': 'مرداد',
        'Shahrivar': 'شهریور',
        'Mehr': 'مهر',
        'Aban': 'آبان',
        'Azar': 'آذر',
        'Dey': 'دی',
        'Bahman': 'بهمن',
        'Esfand': 'اسفند',
    }

    farsi_month = translator[month_str]
    return farsi_month

def entofa_weekday(weekday):
    translator = {
        'Monday': 'دوشنبه',
        'Tuesday': 'سه‌شنبه',
        'Wednesday': 'چهارشنبه',
        'Thursday': 'پنج‌شنبه',
        'Friday': 'جمعه',
        'Saturday': 'شنبه',
        'Sunday': 'یک‌شنبه',
    }

    farsi_weekday = translator[weekday]
    return farsi_weekday

def generate_jalali_year_info():
    jalali_year = jdatetime.datetime.now().year
    jalali_first_day = jdatetime.date(jalali_year, 1, 1)
    jalali_last_day = jdatetime.date(jalali_year + 1, 1, 1) - jdatetime.timedelta(days=1)

    jalali_year_info = []

    current_day = jalali_first_day
    while current_day <= jalali_last_day:
        day_info = {
            "month_name_english": current_day.strftime('%B'),
            "season_number" : str(((current_day.month-1)//3)+1),
            'weekday': entofa_weekday(current_day.strftime('%A')),
            'month_name': entofa_month(current_day.strftime('%B')),
            'day_in_month': entofa_num(current_day.day),
            'year_number': entofa_num(current_day.year)
        }
        jalali_year_info.append(day_info)

        # Move to the next day
        current_day += jdatetime.timedelta(days=1)

    return jalali_year_info

def create_relative_folder(folder_name, relative_path = "out"):
    # Get the absolute path based on the current working directory
    try:
        os.mkdir(relative_path)
    except FileExistsError:
        print("** out folder already exists, creating sub-folders...")
    current_directory = os.getcwd()
    absolute_path = os.path.abspath(os.path.join(current_directory, relative_path))
    
    # Create the folder
    folder_path = os.path.join(absolute_path, folder_name)

    try:
        os.mkdir(folder_path)
        print(f"Folder '{folder_name}' created successfully at '{absolute_path}'.")
    except FileExistsError:
        print(f"Folder '{folder_name}' already exists at '{absolute_path}'.")

def generate_pictures():
    # At least one dimenstion of our picture must be 512 px.
    # In this case, the resized version should be (507, 512)
    # Change for other pictures

    standard_size = (507, 512)
    for month in ['Farvardin', 'Ordibehesht', 'Khordad', 'Tir', 'Mordad', 'Shahrivar', 'Mehr', 'Aban', 'Azar','Dey', 'Bahman', 'Esfand']:
        create_relative_folder(f"{month}")

    dates = generate_jalali_year_info()

    for date_info in dates:
        template = Image.open(f"{template_paths[date_info['season_number']]}")
        img = template.copy()
        path = f"out\{date_info['month_name_english']}\{date_info['day_in_month']}.png"
        #print(path)
        draw = ImageDraw.Draw(img)

        font_small = ImageFont.truetype('vazir.ttf', 30)
        font_medium = ImageFont.truetype('vazir.ttf', 60)
        font_big = ImageFont.truetype('vazir.ttf', 70)
        font_extra = ImageFont.truetype('vazir.ttf', 120)

        draw = ImageDraw.Draw(img)

        draw.text((50, 50), persian_format(date_info["weekday"]), (255, 255, 255), font=font_big)
        draw.text((450, 420), persian_format(date_info["month_name"]), (255, 255, 255), font=font_medium, anchor='rs', stroke_width=2, stroke_fill=(0,0,0) )
        draw.text((180, 190), persian_format(date_info["day_in_month"]), (255, 255, 255), font=font_extra, stroke_width=4, stroke_fill=(0, 0, 0))
        draw.text((356, 162), persian_format(date_info["year_number"]), (255, 255, 255), font=font_small)
        img = img.resize(standard_size)
        img.save(path)

    print("DONE")

if __name__ == '__main__':
    if not (os.path.exists("out") and os.path.isdir("out")):
        generate_pictures()
    
