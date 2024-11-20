import os
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import json

from functions.create_folder import create_films_folder
from functions.read_csv import read_movies_from_csv
from functions.read_json import read_cookies_from_json
from functions.create_headers import create_headers
from functions.crawl_movies import crawl_movies_and_save_to_csv
from functions.download_excels import download_movie_excels


def main():
    folder_name = 'films'
    csv_file = 'vietnam_movies.csv'
    json_file = 'cookies.json'
    cookies = read_cookies_from_json(json_file)
    headers = create_headers(cookies)

    crawl_movies_and_save_to_csv(csv_file, headers)
    movies = read_movies_from_csv(csv_file)
    download_movie_excels(movies, headers, folder_name)

if __name__ == "__main__":
    main()
