import csv
import requests
from bs4 import BeautifulSoup
from time import sleep

BASE_URL        = "https://www.imdb.com/"
TV_SHOW_URL     = "https://www.imdb.com/chart/tvmeter/?ref_=nv_tvv_mptv"
tv_shows_data    = []

def get_tvshow_basicdata():
    page            = requests.get(TV_SHOW_URL).content
    souppage        = BeautifulSoup(page, 'html.parser')
    tv_shows_table  = souppage.find(class_="lister-list")
    tv_shows        = tv_shows_table.findAll("tr")

    #Read basic tv show data
    print(type(tv_shows))
    for tv_show in tv_shows:
        tv_show_data         = []
        tv_show_title       = tv_show.find(class_="titleColumn").find("a").text.strip()
        tv_show_year        = tv_show.find(class_="titleColumn").find(class_="secondaryInfo").text.strip("()")
        tv_show_rating      = tv_show.find(class_="imdbRating").find("strong").text.strip()

        #Fetching TV show details
        tv_show_detailURL   = tv_show.find(class_="titleColumn").find("a")["href"]
        tv_show_summary, tv_show_geners = get_tvshow_detaildata(tv_show_detailURL)
        tv_show_data = [tv_show_title, tv_show_year, tv_show_rating, tv_show_geners, tv_show_summary]
        tv_shows_data.append(tv_show_data)
        sleep(5)



def get_tvshow_detaildata(tv_show_detailURL):
    TV_SHOW_DETAIL_URL      = BASE_URL + tv_show_detailURL
    page = requests.get(TV_SHOW_DETAIL_URL).content
    souppage = BeautifulSoup(page, 'html.parser')
    gener_anchor_tags = souppage.find(class_="subtext").findAll("a")
    show_summary = souppage.find(class_="summary_text").text.strip()
    geners = [gener_anchor_tag.text for gener_anchor_tag in gener_anchor_tags[:-1]]
    geners_list_tostring = '/'.join(geners)
    return show_summary, geners_list_tostring

def write_tvshow_csv():
    tv_show_header = ['Title', 'Year', 'Rating', 'Genre', 'Summary']

    # data rows of csv file
    tv_shows_all_data = tv_shows_data

    # name of csv file
    filename = "tv_show.csv"

    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the header
        csvwriter.writerow(tv_show_header)

        # writing the data rows
        csvwriter.writerows(tv_shows_all_data)


if __name__ == "__main__":
    get_tvshow_basicdata()
    write_tvshow_csv()




