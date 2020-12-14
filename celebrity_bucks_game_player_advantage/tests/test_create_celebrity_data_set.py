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


celebrity = 'Barack Obama'

api_object = create_celebrity_data_set.get_celebritybucks_api_object()

def test_version():
	assert __version__ == '0.1.0'

def test_get_celebritybucks_api_object_type_dict():
	api_object = create_celebrity_data_set.get_celebritybucks_api_object()
	assert type(api_object) == dict

def test_get_celebrity_list_type_list():
	celebrities = create_celebrity_data_set.get_celebrity_list(api_object)
	assert type(celebrities) == list 

#def test_get_celebritybucks_soup_object_type_bs4():
#	soup_cb = create_celebrity_data_set.get_celebritybucks_soup_object(celebrity)
#	assert type(soup_cb) == bs4.BeautifulSoup

def test_get_celebritybucks_soup_object_string_hyphenation():
	celeb_name_split = celebrity.split()
	celeb_name = '-'.join(celeb_name_split)
	assert celeb_name == 'Barack-Obama'

def test_get_astroseek_soup_object_type_bs4():
	soup_as = create_celebrity_data_set.get_astroseek_soup_object(celebrity)
	assert type(soup_as) == bs4.BeautifulSoup

def test_get_astroseek_soup_object_string_conversion():
	celebrity = "Conan O'Brien"
	celeb_name_split = celebrity.replace(".","").replace("'","-").split()
	celeb_name = '-'.join(celeb_name_split)
	assert celeb_name == "Conan-O-Brien"

def test_create_celeb_df_type_pandas():
	df = create_celebrity_data_set.create_celeb_df()
	assert type(df) == pd.core.frame.DataFrame

def test_create_celeb_df_number_of_columns():
	df = create_celebrity_data_set.create_celeb_df()
	assert len(df.columns) == 15

def test_get_celebritybucks_ranking_wrong_input_type():
	with pytest.raises(AssertionError):
		result = create_celebrity_data_set.get_celebritybucks_ranking(api_object, celebrity=24)

def test_get_celebritybucks_price_no_celeb_found():
	actual = create_celebrity_data_set.get_celebritybucks_price(api_object, celebrity='Not a celebrity')
	expected = 'Not a celebrity not found within CelebrityBucks data set.'
	assert actual == expected

