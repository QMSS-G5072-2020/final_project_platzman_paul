#Importing dependencies
import bs4
import json
import os
import pandas as pd
import requests
import sys
from datetime import datetime
from datetime import date


#Functions for acquiring celebrity data objects
def get_celebritybucks_api_object():
	"""
	Returns a dictionary containing celebrity rankings and price values from the Celebrity Bucks API. Source: https://celebritybucks.com/developers/.

	Parameters
	----------
	 	  
	Returns
	-------
	dict
	    A JSON object containing celebrity rankings and price values from the Celebrity Bucks API.

	Examples
	--------
	>>> api_object = get_celebritybucks_api_object()
	>>> type(api_object)
	dict
	"""
	r = requests.get(f'https://celebritybucks.com/developers/export/JSON')
	if r.status_code!=200:
		print('API request is NOT successful. Check https://celebritybucks.com/developers and your API query before retrying.')
		sys.exit()
	elif r.status_code==200:
		print('API request is successful.')

	api_object = r.json()
	return(api_object)


def get_celebrity_list(api_object):
	"""
	Returns a ranked list of celebrities generated from a Celebrity Bucks API call. Source: https://celebritybucks.com/developers/.

	Parameters
	----------
	  api_object : dict
	    A JSON object containing celebrity rankings and price values from the Celebrity Bucks API.
	 	  
	Returns
	-------
	list
	    A list of celebrities ranked by their current price values in the Celebrity Bucks API call.

	Examples
	--------
	>>> celebrities = get_celebrity_list()
	>>> len(celebrities)
	717	
	>>> celebrities[0:3]
	['Taylor Swift','Donald Trump','Kim Kardashian']
	"""
	celebrities = []

	for index in range(len(api_object['CelebrityValues'])):
		celebrities.append(api_object['CelebrityValues'][index]['name'])

	return(celebrities)


def get_celebritybucks_soup_object(api_object, celebrity=""):
	"""
	Returns a bs4.BeautifulSoup object containing HTML from the Celebrity Bucks webpage corresponding to a given celebrity. Source: https://celebritybucks.com/celebrities/.

	Parameters
	----------
	  celebrity : str
	    A celebrity's first and last name encapsulated in single or double quotes. Not case sensitive.
	  
	Returns
	-------
	bs4.BeautifulSoup
	    A BeautifulSoup object containing HTML from the Celebrity Bucks webpage corresponding to a given celebrity.

	Examples
	--------
	>>> soup_cb = get_celebritybucks_soup_object("Jamie Foxx")
	>>> type(soup_cb)
	bs4.BeautifulSoup
	"""
	assert type(celebrity) == str, "Input value must be of type string."

	celeb_name_split = celebrity.split()
	celeb_name = '-'.join(celeb_name_split)

	celebID = get_celebritybucks_ID(api_object, celebrity)

	celebrity_bucks_url = f'https://celebritybucks.com/celebrity/{celebID}/{celeb_name}'

	celebrity_bucks_html = requests.get(celebrity_bucks_url)
	soup_cb_object = bs4.BeautifulSoup(celebrity_bucks_html.content, 'html.parser')
	return(soup_cb_object)


def get_astroseek_soup_object(celebrity=""):
	"""
	Returns a bs4.BeautifulSoup object containing HTML from the Astro Seek webpage corresponding to a given celebrity. Source: https://www.astro-seek.com/.

	Parameters
	----------
	  celebrity : str
	    A celebrity's first and last name encapsulated in single or double quotes. Not case sensitive.
	  
	Returns
	-------
	bs4.BeautifulSoup
	    A BeautifulSoup object containing HTML from the Astro Seek birth chart webpage corresponding to a given celebrity.

	Examples
	--------
	>>> soup_as = get_astroseek_soup_object("Gwen Stefani")
	>>> type(soup_as)
	bs4.BeautifulSoup	
	"""
	assert type(celebrity) == str, "Input value must be of type string."

	celeb_name_split = celebrity.replace(".","").replace("'","-").split()
	celeb_name = '-'.join(celeb_name_split)

	astro_seek_url = f'https://www.astro-seek.com/birth-chart/{celeb_name}-horoscope'

	astro_seek_html = requests.get(astro_seek_url)
	soup_as_object = bs4.BeautifulSoup(astro_seek_html.content, 'html.parser')
	return(soup_as_object)


def create_celeb_df():
	"""
	Creates an empty Pandas data frame in which to store celebrity attributes collected in other functions.

	Parameters
	----------
	
	Returns
	-------
	pandas.core.frame.DataFrame
	    A Pandas data frame with column names that correspond to celebrity attributes collected in other functions.

	Examples
	--------
	>>> df = create_celeb_df()
	>>> df.to_dict()
	{'Celebrity': {},
	 'Current Ranking': {},
	 'Current Price': {},
	 'Avg. 21-Day Price': {},
	 'Avg. 21-Day Price/Current Price': {},
	 'All-Time High Price': {},
	 'All-Time High Price/Current Price': {},
	 'Days Since All-Time High Price': {},
	 'Gender': {},
	 'Age': {},
	 'Upcoming Birthday': {},
	 'U.S. Nationality': {},
	 'Living Status': {},
	 'Celebrity Bucks Recommendation': {},
	 'Last Update': {}}	
	"""
	df = pd.DataFrame(columns = ['Celebrity',
								 'Current Ranking',
								 'Current Price',
								 'Avg. 21-Day Price',
								 'Avg. 21-Day Price/Current Price',
								 'All-Time High Price',
								 'All-Time High Price/Current Price',
								 'Days Since All-Time High Price',
								 'Gender',
								 'Age',
								 'Upcoming Birthday',
								 'U.S. Nationality',
								 'Living Status',
								 'Celebrity Bucks Recommendation',
								 'Last Update'])
	return(df)


#Functions for acquiring celebrity attributes
def get_celebritybucks_ranking(api_object, celebrity=""):
	"""
	Returns the Celebrity Bucks ranking for a given celebrity from the Celebrity Bucks API.

	Parameters
	----------
	  api_object : dict
	    A JSON object containing celebrity rankings and price values from the Celebrity Bucks API.
	  celebrity : str
	    A celebrity's first and last name encapsulated in single or double quotes. Not case sensitive.
	  
	Returns
	-------
	int
	  The current Celebrity Bucks ranking of the celebrity

	Examples
	--------
	>>> get_celebritybucks_ranking('LeBron James')
	75
	>>> get_celebritybucks_ranking("Eminem")
	209
	"""
	assert type(celebrity) == str, "Input value must be of type string."

	for index in range(len(api_object['CelebrityValues'])):
		if api_object['CelebrityValues'][index]['name'] == celebrity:
			return(index+1)
		else:
			next
	return(f'{celebrity} not found within CelebrityBucks data set.')


def get_celebritybucks_price(api_object, celebrity=""):
	"""
	Returns the Celebrity Bucks price for a given celebrity from the Celebrity Bucks API.

	Parameters
	----------
	  api_object : dict
	    A JSON object containing celebrity rankings and price values from the Celebrity Bucks API.
	  celebrity : str
	    A celebrity's first and last name encapsulated in single or double quotes. Not case sensitive.
	  
	Returns
	-------
	int
	  The current Celebrity Bucks dollar value associated with the celebrity

	Examples
	--------
	>>> get_celebritybucks_price('Donald Trump')
	334000
	"""
	assert type(celebrity) == str, "Input value must be of type string."

	for index in range(len(api_object['CelebrityValues'])):
		if api_object['CelebrityValues'][index]['name'] == celebrity:
			return(api_object['CelebrityValues'][index]['price'])
		else:
			next
	return(f'{celebrity} not found within CelebrityBucks data set.')


def get_celebritybucks_ID(api_object, celebrity=""):
	"""
	Returns the four-digit Celebrity Bucks ID value for a given celebrity from the Celebrity Bucks API.

	Parameters
	----------
	  api_object : dict
	    A JSON object containing celebrity rankings and price values from the Celebrity Bucks API.
	  celebrity : str
	    A celebrity's first and last name encapsulated in single or double quotes. Not case sensitive.
	  
	Returns
	-------
	str
	  The Celebrity Bucks four-digit ID value associated with the celebrity

	Examples
	--------
	>>> get_celebritybucks_ID("Eminem")
	'2488'
	"""
	assert type(celebrity) == str, "Input value must be of type string."

	for index in range(len(api_object['CelebrityValues'])):
		if api_object['CelebrityValues'][index]['name'] == celebrity:
			return(api_object['CelebrityValues'][index]['celebId'])
		else:
			next
	return(f'{celebrity} not found within CelebrityBucks data set.')


def get_gender(soup_object):
	"""
	Returns the gender associated with a given celebrity. Source: https://www.astro-seek.com/.

	Parameters
	----------
	  soup_object: bs4.BeautifulSoup
	    A BeautifulSoup object containing HTML from the Astro Seek birth chart webpage corresponding to a given celebrity. 
	  
	Returns
	-------
	str
	  The gender associated with the celebrity

	Examples
	--------
	>>> get_gender(soup_taylor_swift)
	'Female'
	"""
	try:
		return(soup_object.find_all(class_='fl')[1].get_text().strip())
	except:
		return('NaN')


def get_age(soup_object):
	"""
	Returns the age of a given celebrity. Source: https://www.astro-seek.com/.

	Parameters
	----------
	  soup_object: bs4.BeautifulSoup
	    A BeautifulSoup object containing HTML from the Astro Seek birth chart webpage corresponding to a given celebrity. 
	  
	Returns
	-------
	int
	  The age of the celebrity

	Examples
	--------
	>>> get_age(soup_meryl_streep)
	71
	"""
	try:
		return(int(soup_object.find_all(class_='fl')[-5].get_text().strip()[2:5]))
	except:
		try:
			return(int(soup_object.find_all(class_='fl')[-3].get_text().strip()[0:3]))
		except:
			return('NaN')


def get_year():
	"""
	Returns the current calendar year unless the current date is within the first seven days of its year.

	Parameters
	----------
	 	  
	Returns
	-------
	int
	  The current year or the prior year if the current date is within the first seven days of the year

	Examples
	--------
	>>> get_year()
	2020
	"""
	today = datetime.today()
	if today.month==1 and today.day<=7:
		return(today.year+1)
	else:
		return(today.year)


def upcoming_birthday(soup_object):
	"""
	Identifies whether a given celebrity will have a birthday within the next seven days. Source: https://www.astro-seek.com/.

	Parameters
	----------
	  soup_object: bs4.BeautifulSoup
	    A BeautifulSoup object containing HTML from the Astro Seek birth chart webpage corresponding to a given celebrity. 
	  
	Returns
	-------
	str
	  A binary declaration as to whether the celebrity has or does not have a birthday upcoming in the following week

	Examples
	--------
	>>> upcoming_birthday(soup_harrison_ford)
	'No upcoming birthday'
	>>> upcoming_birthday(soup_billie_eilish)
	'Upcoming birthday'
	"""
	months = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
	try:
		month_str = soup_object.find_all(class_='fl')[3].find(class_='tenky-modry').get_text().strip().split()[1]
		month = months[month_str]
		day = int(soup_object.find_all(class_='fl')[3].find(class_='tenky-modry').get_text().strip().split()[0])
		year = get_year()

		current_date = date.today()

		delta = date(year,month,day) - date.today()

		if delta.days >=0 and delta.days<=7:
			return('Upcoming birthday')
		else:
			return('No upcoming birthday')
	except:
		return('NaN')


def us_nationality(soup_object):
	"""
	Identifies whether a given celebrity is a U.S. national. Source: https://www.astro-seek.com/.

	Parameters
	----------
	  soup_object: bs4.BeautifulSoup
	    A BeautifulSoup object containing HTML from the Astro Seek birth chart webpage corresponding to a given celebrity. 
	  
	Returns
	-------
	str
	  A binary declaration as to whether the celebrity is or is not a U.S. national

	Examples
	--------
	>>> us_nationality(soup_kylie_jenner)
	'U.S. national'
	>>> us_nationality(soup_hayden_christensen)
	'Foreign to U.S.'
	"""
	try:
		if soup_object.find_all(class_='fl')[7].get_text().strip()[0:2]=='US':
			return("U.S. national")
		elif soup_object.find_all(class_='fl')[7].get_text().strip()[0:2]!='US':
			return("Foreign to U.S.")
	except:
		return('NaN')


def living_status(soup_object):
	"""
	Identifies whether a given celebrity is alive or dead. Source: https://www.astro-seek.com/.

	Parameters
	----------
	  soup_object: bs4.BeautifulSoup
	    A BeautifulSoup object containing HTML from the Astro Seek birth chart webpage corresponding to a given celebrity. 
	  
	Returns
	-------
	str
	  A binary declaration as to whether the celebrity is alive or dead

	Examples
	--------
	>>> living_status(soup_bill_clinton)
	'Alive'
	>>> living_status(soup_muhammad_ali)
	'Dead'
	"""
	try:
		if 'Seek celebrities by planet positions' in soup_object.find_all(class_='fl')[0].get_text().strip():
			return('NaN')

		for row in range(len(soup_object.find_all(class_='fl'))):
			if soup_object.find_all(class_='fl')[row].get_text().strip() == 'Death:':
				return('Dead')
			else:
				next
		return('Alive')
	except:
		return('NaN')


def get_avg_21_day_price(soup_object):
	"""
	Returns the average 21-day Celebrity Bucks price for a given celebrity. Source: https://celebritybucks.com/celebrities/.

	Parameters
	----------
	  soup_object: bs4.BeautifulSoup
	    A BeautifulSoup object containing HTML from the Celebrity Bucks webpage corresponding to a given celebrity. 
	  
	Returns
	-------
	int
	  The average 21-day Celebrity Bucks dollar value associated with the celebrity

	Examples
	--------
	>>> get_avg_21_day_price(soup_kelly_clarkson)
	36000
	"""
	try:
		twenty_one_day_price = int(soup_object.find_all(class_='panel-body center')[0].get_text().strip()[1:].replace(',', ''))
		return(twenty_one_day_price)
	except:
		return('NaN')


def get_all_time_high_price(soup_object):
	"""
	Returns the all-time high Celebrity Bucks price for a given celebrity. Source: https://celebritybucks.com/celebrities/.

	Parameters
	----------
	  soup_object: bs4.BeautifulSoup
	    A BeautifulSoup object containing HTML from the Celebrity Bucks webpage corresponding to a given celebrity. 
	  
	Returns
	-------
	int
	  The all-time high Celebrity Bucks dollar value associated with the celebrity

	Examples
	--------
	>>> get_all_time_high_price(soup_george_clooney)
	1721000
	"""
	try:
		return(int(soup_object.find_all(class_='panel-body center')[2].get_text().strip()[1:].replace(',', '')))
	except:
		try:
			return(int(soup_object.find_all(class_='panel-body center')[1].get_text().strip()[1:].replace(',', '')))
		except:
			try:
				return(int(soup_object.find_all(class_='panel-body center')[-2].get_text().strip()[1:].replace(',', '')))
			except:
				return('NaN')


def get_days_since_ath(soup_object):
	"""
	Returns the number of days since a given celebrity acheived their all-time high Celebrity Bucks price. Source: https://celebritybucks.com/celebrities/.

	Parameters
	----------
	  soup_object: bs4.BeautifulSoup
	    A BeautifulSoup object containing HTML from the Celebrity Bucks webpage corresponding to a given celebrity. 
	  
	Returns
	-------
	int
	  The number of days since the celebrity acheived their all-time high Celebrity Bucks price

	Examples
	--------
	>>> get_days_since_ath(soup_kate_middleton)
	2049
	"""
	months_shortened = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
	try:
		month_str_sh = soup_object.find_all(class_='panel-body center')[-1].get_text().strip().replace(",","").split()[0]
		day = int(soup_object.find_all(class_='panel-body center')[-1].get_text().strip().replace(",","").split()[1])
		year = int(soup_object.find_all(class_='panel-body center')[-1].get_text().strip().replace(",","").split()[2])
	except:
		return('NaN')
			
	month = months_shortened[month_str_sh]
	
	duration = date.today() - date(year,month,day)
	return(duration.days)


def get_cb_rec(soup_object):
	"""
	Returns the current Celebrity Bucks recommendation as to whether game players should buy, hold, or sell a given celebrity. Source: https://celebritybucks.com/celebrities/.

	Parameters
	----------
	  soup_object: bs4.BeautifulSoup
	    A BeautifulSoup object containing HTML from the Celebrity Bucks webpage corresponding to a given celebrity.
	  
	Returns
	-------
	str
	   The current Celebrity Bucks recommended action with regard to the celebrity

	Examples
	--------
	>>> get_cb_rec(soup_tom_hanks)
	'Buy'
	>>> get_cb_rec(soup_gwyneth_paltrow)
	'Hold'
	>>> get_cb_rec(soup_miley_cyrus)
	'Sell'
	"""
	return(soup_object.find_all(role='alert')[1].get_text().strip().split()[-1])


def append_to_df(df, celebrity):
	"""
	Collects data for a given celebrity from three sources and appends data to a `celebrity_data_attributes` Pandas data frame. Intended for script execution. Sources: Celebrity Bucks API, https://www.astro-seek.com/, and https://celebritybucks.com/celebrities/. 

	Parameters
	----------
	  df : pandas.core.frame.DataFrame
	    A Pandas data frame with column names that correspond to celebrity attributes collected in other functions.

	  celebrity : str
	    A celebrity's first and last name encapsulated in single or double quotes. Not case sensitive.
	
	Returns
	-------
	pandas.core.frame.DataFrame
	   A Pandas data frame containing celebrity attributes

	Examples
	--------
	>>> len(df)
	64
	>>> df = append_to_df(df, 'Rachel McAdams')
	>>> len(df)
	65
	>>> df[df['Celebrity'] == 'Rachel McAdams'].to_dict()
	{'Celebrity': {64: 'Rachel McAdams'},
	 'Current Ranking': {64: 65},
	 'Current Price': {64: 51000},
	 'Avg. 21-Day Price': {64: 3000},
	 'Avg. 21-Day Price/Current Price': {64: 0.059000000000000004},
	 'All-Time High Price': {64: 377000},
	 'All-Time High Price/Current Price': {64: 7.392},
	 'Days Since All-Time High Price': {64: 2333},
	 'Gender': {64: 'Female'},
	 'Age': {64: 42.0},
	 'Upcoming Birthday': {64: 'No upcoming birthday'},
	 'U.S. Nationality': {64: 'Foreign to U.S.'},
	 'Living Status': {64: 'Alive'},
	 'Celebrity Bucks Recommendation': {64: 'Buy'},
	 'Last Update': {64: '31:02.3'}}
	"""
	#Scraping Celebrity Bucks individual celebrity site
	soup_cb = get_celebritybucks_soup_object(api_object, celebrity)

	#Scraping Astro Seek individual celebrity site
	soup_as = get_astroseek_soup_object(celebrity)

	try:
		#Current Ranking
		current_ranking = get_celebritybucks_ranking(api_object, celebrity)

		#Current Price
		current_price = get_celebritybucks_price(api_object, celebrity)

		#Avg. 21-Day Price
		twenty_one_day_price = get_avg_21_day_price(soup_cb)

		#Avg. 21-Day Price/Current Price
		ratio_21d = round(twenty_one_day_price/current_price,3)

		#All-Time High Price
		all_time_high_price = get_all_time_high_price(soup_cb)

		#All-Time High Price/Current Price
		ratio_ath = round(all_time_high_price/current_price,3)

		#Days Since All-Time High Price
		duration_since_ath = get_days_since_ath(soup_cb)

		#Gender
		gender = get_gender(soup_as)

		#Age
		age = get_age(soup_as)

		#Upcoming Birthday
		birthday_next_7_days = upcoming_birthday(soup_as)

		#U.S. Nationality
		nationality = us_nationality(soup_as)

		#Living Status
		living = living_status(soup_as)

		#Celebrity Bucks Recommendation
		cb_rec = get_cb_rec(soup_cb)

		#Last Update
		current_time = datetime.now()

		#Appending row to dataframe
		df = df.append({'Celebrity':celebrity, 
						'Current Ranking':current_ranking,
						'Current Price':current_price,
						'Avg. 21-Day Price':twenty_one_day_price,
						'Avg. 21-Day Price/Current Price':ratio_21d,
						'All-Time High Price':all_time_high_price,
						'All-Time High Price/Current Price':ratio_ath,
						'Days Since All-Time High Price':duration_since_ath,
						'Gender':gender,
						'Age':age,
						'Upcoming Birthday':birthday_next_7_days,
						'U.S. Nationality':nationality,
						'Living Status':living,
						'Celebrity Bucks Recommendation':cb_rec,
						'Last Update':current_time},  
						ignore_index = True) 
	except:
		print(f'Unable to add record for {celebrity} to data frame.')

	return(df)


def get_celeb_data(api_object, soup_cb, soup_as, celebrity):
	"""
	Collects data for a given celebrity from three sources and returns data as a single row in a Pandas data frame. Intended for interactive usage. Sources: Celebrity Bucks API, https://www.astro-seek.com/, and https://celebritybucks.com/celebrities/. 

	Parameters
	----------
	  api_object : dict
	    A JSON object containing celebrity rankings and price values from the Celebrity Bucks API.

	  soup_object: bs4.BeautifulSoup
	    A BeautifulSoup object containing HTML from the Celebrity Bucks webpage corresponding to a given celebrity.

	  soup_object: bs4.BeautifulSoup
	    A BeautifulSoup object containing HTML from the Astro Seek birth chart webpage corresponding to a given celebrity. 

	  celebrity : str
	    A celebrity's first and last name encapsulated in single or double quotes. Not case sensitive.
	
	Returns
	-------
	pandas.core.frame.DataFrame
	   A Pandas data frame containing attributes for a given celebrity

	Examples
	--------
	>>> get_celeb_data(api_object, soup_cb, soup_as, celebrity='Rachel McAdams')
	>>> df[df['Celebrity'] == 'Rachel McAdams'].to_dict()
	{'Celebrity': {0: 'Rachel McAdams'},
	 'Current Ranking': {0: 65},
	 'Current Price': {0: 51000},
	 'Avg. 21-Day Price': {0: 3000},
	 'Avg. 21-Day Price/Current Price': {0: 0.059000000000000004},
	 'All-Time High Price': {0: 377000},
	 'All-Time High Price/Current Price': {0: 7.392},
	 'Days Since All-Time High Price': {0: 2333},
	 'Gender': {0: 'Female'},
	 'Age': {0: 42.0},
	 'Upcoming Birthday': {0: 'No upcoming birthday'},
	 'U.S. Nationality': {0: 'Foreign to U.S.'},
	 'Living Status': {0: 'Alive'},
	 'Celebrity Bucks Recommendation': {0: 'Buy'},
	 'Last Update': {0: '31:02.3'}}
	"""
	df = create_celeb_df()

	#Current Ranking
	try:
		current_ranking = get_celebritybucks_ranking(api_object, celebrity)
	except:
		current_ranking = 'NaN'

	#Current Price
	try:
		current_price = get_celebritybucks_price(api_object, celebrity)
	except:
		current_price = 'NaN'

	#Avg. 21-Day Price
	try:
		twenty_one_day_price = get_avg_21_day_price(soup_cb)
	except:
		twenty_one_day_price = 'NaN'

	#Avg. 21-Day Price/Current Price
	try:
		ratio_21d = round(twenty_one_day_price/current_price,3)
	except:
		ratio_21d = 'NaN'

	#All-Time High Price
	try:
		all_time_high_price = get_all_time_high_price(soup_cb)
	except:
		all_time_high_price = 'NaN'

	#All-Time High Price/Current Price
	try:
		ratio_ath = round(all_time_high_price/current_price,3)
	except:
		ratio_ath = 'NaN'

	#Days Since All-Time High Price
	try:
		duration_since_ath = get_days_since_ath(soup_cb)
	except:
		duration_since_ath = 'NaN'

	#Gender
	try:
		gender = get_gender(soup_as)
	except:
		gender = 'NaN'

	#Age
	try:
		age = get_age(soup_as)
	except:
		age = 'NaN'

	#Upcoming Birthday
	try:
		birthday_next_7_days = upcoming_birthday(soup_as)
	except:
		birthday_next_7_days = 'NaN'

	#U.S. Nationality
	try:
		nationality = us_nationality(soup_as)
	except:
		nationality = 'NaN'

	#Living Status
	try:
		living = living_status(soup_as)
	except:
		living = 'NaN'

	#Celebrity Bucks Recommendation
	try:
		cb_rec = get_cb_rec(soup_cb)
	except:
		cb_rec = 'NaN'

	#Last Update
	try:
		current_time = datetime.now()
	except:
		current_time = 'NaN'

	#Appending row to dataframe
	df = df.append({'Celebrity':celebrity, 
					'Current Ranking':current_ranking,
					'Current Price':current_price,
					'Avg. 21-Day Price':twenty_one_day_price,
					'Avg. 21-Day Price/Current Price':ratio_21d,
					'All-Time High Price':all_time_high_price,
					'All-Time High Price/Current Price':ratio_ath,
					'Days Since All-Time High Price':duration_since_ath,
					'Gender':gender,
					'Age':age,
					'Upcoming Birthday':birthday_next_7_days,
					'U.S. Nationality':nationality,
					'Living Status':living,
					'Celebrity Bucks Recommendation':cb_rec,
					'Last Update':current_time},  
					ignore_index = True) 

	return(df)



if __name__ == "__main__":

	#Celebrity Bucks API call
	api_object = get_celebritybucks_api_object()

	#Creating a list of celebrities based on the results of the API call
	celebrities = get_celebrity_list(api_object)

	print(f'There are {len(celebrities)} celebrities who have Celebrity Bucks values!')

	#Creating the celebrity attribute data frame
	df_celeb = create_celeb_df()

	#Filling the data frame
	for num in range(len(celebrities)):
	    celebrity = celebrities[num]
	    df_celeb = append_to_df(df_celeb, celebrity)
	    
	    #Progress tracker
	    if num%10==0:
	        print(f'{num} celebrities out of {len(celebrities)} collected!')
	    if num+1==len(celebrities):
	        print('Done!')

	#Saving the data frame
	current_time = datetime.now()
	df_celeb.to_csv(f'../data/celebrity_data_attributes_{current_time.year}-{current_time.month}-{current_time.day}_{current_time.hour}_{current_time.minute}_{current_time.second}.csv',index=False)