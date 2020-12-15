#Importing dependencies
from celebrity_bucks_game_player_advantage import __version__
from celebrity_bucks_game_player_advantage import create_celebrity_data_set
import pytest
import bs4
import json
import os
import pandas as pd
import requests
import sys
from datetime import datetime
from datetime import date


#Initializing parameter values for unit tests
celebrity = 'Barack Obama'
api_object = create_celebrity_data_set.get_celebritybucks_api_object()
soup_cb = create_celebrity_data_set.get_celebritybucks_soup_object(api_object, celebrity)
soup_as = create_celebrity_data_set.get_astroseek_soup_object(celebrity)


#Unit tests
def test_version():
	assert __version__ == '0.1.0'

def test_get_celebritybucks_api_object_type_dict():
	api_object = create_celebrity_data_set.get_celebritybucks_api_object()
	assert type(api_object) == dict

def test_get_celebrity_list_type_list():
	celebrities = create_celebrity_data_set.get_celebrity_list(api_object)
	assert type(celebrities) == list 

def test_get_celebritybucks_soup_object_type_bs4():
	soup_cb = create_celebrity_data_set.get_celebritybucks_soup_object(api_object, celebrity)
	assert type(soup_cb) == bs4.BeautifulSoup

def test_get_celebritybucks_soup_object_string_hyphenation():
	celeb_name_split = celebrity.split()
	celeb_name = '-'.join(celeb_name_split)
	assert celeb_name == 'Barack-Obama'

def test_get_astroseek_soup_object_type_bs4():
	soup_as = create_celebrity_data_set.get_astroseek_soup_object(celebrity)
	assert type(soup_as) == bs4.BeautifulSoup

def test_get_astroseek_soup_object_string_conversion_apostrophe():
	celebrity = "Conan O'Brien"
	celeb_name_split = celebrity.replace(".","").replace("'","-").split()
	celeb_name = '-'.join(celeb_name_split)
	assert celeb_name == "Conan-O-Brien"

def test_get_astroseek_soup_object_string_conversion_period():
	celebrity = "Samuel L. Jackson"
	celeb_name_split = celebrity.replace(".","").replace("'","-").split()
	celeb_name = '-'.join(celeb_name_split)
	assert celeb_name == "Samuel-L-Jackson"

def test_create_celeb_df_type_pandas():
	df = create_celebrity_data_set.create_celeb_df()
	assert type(df) == pd.core.frame.DataFrame

def test_create_celeb_df_number_of_columns():
	df = create_celebrity_data_set.create_celeb_df()
	assert len(df.columns) == 15

def test_get_celebritybucks_ranking_wrong_input_type_int():
	with pytest.raises(AssertionError):
		create_celebrity_data_set.get_celebritybucks_ranking(api_object, celebrity=24)

def test_get_celebritybucks_price_no_celeb_found():
	actual = create_celebrity_data_set.get_celebritybucks_price(api_object, celebrity='Not a celebrity')
	expected = 'Not a celebrity not found within CelebrityBucks data set.'
	assert actual == expected

def test_get_celebritybucks_ID_wrong_input_type_list():
	with pytest.raises(AssertionError):
		create_celebrity_data_set.get_celebritybucks_ID(api_object, celebrity=['Taylor Swift','Donald Trump'])

def test_get_gender():
	assert create_celebrity_data_set.get_gender(soup_as) == 'Male'

def test_get_age_type_int():
	assert type(create_celebrity_data_set.get_age(soup_as)) == int 

def test_get_year_minimum_value():
	assert create_celebrity_data_set.get_year() >= 2020

def test_upcoming_birthday():
	current_date = date.today()
	if current_date.day <=27:
		tomorrow = date(current_date.year, current_date.month, current_date.day+1)
		delta = tomorrow - current_date
		assert delta.days == 1
	elif current_date.day >=28 and current_date.month <= 11:
		future_date = date(current_date.year, current_date.month+1, current_date.day)
		delta = future_date - current_date
		assert delta.days > 7
	else:
		future_date = date(current_date.year+1, current_date.month-11, current_date.day)
		delta = future_date - current_date
		assert delta.days > 7

def test_upcoming_birthday_today():
	current_date = date.today()
	other_date = date.today()
	delta = other_date - current_date
	assert delta.days == 0

def test_us_nationality():
	assert create_celebrity_data_set.us_nationality(soup_as) == 'U.S. national'

def test_living_status():
	assert create_celebrity_data_set.living_status(soup_as) == 'Alive'

def test_get_avg_21_day_price_type_int():
	assert type(create_celebrity_data_set.get_avg_21_day_price(soup_cb)) == int

def test_get_all_time_high_price_type_int():
	assert type(create_celebrity_data_set.get_all_time_high_price(soup_cb)) == int

def test_get_days_since_ath_non_negative():
	assert create_celebrity_data_set.get_days_since_ath(soup_cb) >= 0

def test_get_cb_rec_result():
	assert create_celebrity_data_set.get_cb_rec(soup_cb) in ['Hold','Buy','Sell']

def test_get_celeb_data_df_shape():
	df = create_celebrity_data_set.get_celeb_data(api_object, soup_cb, soup_as, celebrity)
	actual = df.shape
	expected = (1,15)
	assert actual == expected