#Importing Dependencies
import bs4
import json
import os
import pandas as pd
import requests
import sys
from datetime import datetime
from datetime import date


#Functions for acquiring celebrity attributes
def get_celebritybucks_ranking(celebrity=""):
    assert type(celebrity) == str, "Input value must be of type string."
   
    for index in range(len(celebs['CelebrityValues'])):
        if celebs['CelebrityValues'][index]['name'] == celebrity:
            return(index+1)
        else:
            next
    return(f'{celebrity} not found within CelebrityBucks data set.')


def get_celebritybucks_price(celebrity=""):
    assert type(celebrity) == str, "Input value must be of type string."
   
    for index in range(len(celebs['CelebrityValues'])):
        if celebs['CelebrityValues'][index]['name'] == celebrity:
            return(celebs['CelebrityValues'][index]['price'])
        else:
            next
    return(f'{celebrity} not found within CelebrityBucks data set.')


def get_celebritybucks_ID(celebrity=""):
    assert type(celebrity) == str, "Input value must be of type string."
   
    for index in range(len(celebs['CelebrityValues'])):
        if celebs['CelebrityValues'][index]['name'] == celebrity:
            return(celebs['CelebrityValues'][index]['celebId'])
        else:
            next
    return(f'{celebrity} not found within CelebrityBucks data set.')


def get_gender(soup_object):
    try:
        return(soup_object.find_all(class_='fl')[1].get_text().strip())
    except:
        return('NaN')


def get_age(soup_object):
    try:
        return(int(soup_object.find_all(class_='fl')[-5].get_text().strip()[2:5]))
    except:
        try:
            return(int(soup_object.find_all(class_='fl')[-3].get_text().strip()[0:3]))
        except:
            return('NaN')


def get_year():
    today = datetime.today()
    if today.month==1 and today.day<=7:
        return(today.year+1)
    else:
        return(today.year)


def upcoming_birthday(soup_object):
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
    try:
        if soup_object.find_all(class_='fl')[7].get_text().strip()[0:2]=='US':
            return("U.S. national")
        elif soup_object.find_all(class_='fl')[7].get_text().strip()[0:2]!='US':
            return("Foreign to U.S.")
    except:
        return('NaN')


def living_status(soup_object):
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
    try:
        twenty_one_day_price = int(soup_object.find_all(class_='panel-body center')[0].get_text().strip()[1:].replace(',', ''))
        return(twenty_one_day_price)
    except:
        return('NaN')


def get_all_time_high_price(soup_object):
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
    return(soup_object.find_all(role='alert')[1].get_text().strip().split()[-1])


def append_to_df(celebrity):
    global df
    
    #Scraping Celebrity Bucks individual celebrity site
    celeb_name_split = celebrity.split()
    celeb_name = '-'.join(celeb_name_split)

    celebID = get_celebritybucks_ID(celebrity)

    celebrity_bucks_url = f'https://celebritybucks.com/celebrity/{celebID}/{celeb_name}'

    celebrity_bucks_html = requests.get(celebrity_bucks_url)
    soup_cb = bs4.BeautifulSoup(celebrity_bucks_html.content, 'html.parser')
            
    #Scraping Astro Seek individual celebrity site
    celeb_name_split = celebrity.replace(".","").replace("'","-").split()
    celeb_name = '-'.join(celeb_name_split)

    astro_seek_url = f'https://www.astro-seek.com/birth-chart/{celeb_name}-horoscope'

    astro_seek_html = requests.get(astro_seek_url)
    soup_as = bs4.BeautifulSoup(astro_seek_html.content, 'html.parser')
    
    try:
        #Current Ranking
        current_ranking = get_celebritybucks_ranking(celebrity)

        #Current Price
        current_price = get_celebritybucks_price(celebrity)

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


if __name__ == "__main__":

	#Celebrity Bucks API call
	r = requests.get(f'https://celebritybucks.com/developers/export/JSON')

	if r.status_code!=200:
		print('API request is NOT successful. Check https://celebritybucks.com/developers and your API query before retrying.')
		sys.exit()
	elif r.status_code==200:
		print('API request is successful.')

	celebs = r.json()


	#Creating a list of celebrities based on the results of the API call
	celebrities = []
	for index in range(len(celebs['CelebrityValues'])):
	    celebrities.append(celebs['CelebrityValues'][index]['name'])

	print(f'There are {len(celebrities)} celebrities who have Celebrity Bucks values!')


	#Creating the celebrity attribute data frame
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

	for num in range(len(celebrities)):
	    celebrity = celebrities[num]
	    append_to_df(celebrity)
	    
	    #Progress tracker
	    if num%10==0:
	        print(f'{num} celebrities out of {len(celebrities)} collected!')
	    if num+1==len(celebrities):
	        print('Done!')

	#Saving the data frame to disk
	current_time = datetime.now()
	df.to_csv(f'../data/celebrity_data_attributes_{current_time.year}-{current_time.month}-{current_time.day}_{current_time.hour}_{current_time.minute}_{current_time.second}.csv',index=False)