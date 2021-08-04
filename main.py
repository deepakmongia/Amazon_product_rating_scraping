from flask import Flask, render_template, request, jsonify
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
import logging as lg
from amazon_scrape import get_url, extract_record

app = Flask(__name__)

lg.basicConfig(filename = "logfile.log", level = lg.INFO, format = '%(asctime)s %(name)s %(message)s')

@app.route('/amazon_product_search_comparison', methods=['POST']) # for calling the API from Postman/SOAPUI
def amazon_product_search_scrape():
    try:
        #print("C")
        if (request.method=='POST'):
            #print("D")
            search_term = request.json['search_term']

            """ Run the main routine """

            # start up the webdriver
            driver = webdriver.Chrome('/Users/deepakmongia/Documents/Data Science/iNeuron/Selenium/chromedriver')

            records = []
            url = get_url(search_term)

            #    for page in range(1,21):
            for page in range(1, 5):
                url_page = url.format(page, page)
                print(url_page)
                driver.get(url_page)
                soup = BeautifulSoup(driver.page_source, 'html')
                results = soup.find_all('div', {'data-component-type': 's-search-result'})

                for item in results:
                    record = extract_record(item)

                    if record:
                        records.append(record)

            driver.close()

            # save data to csv file
            file_name = search_term.replace(" ", "_") + ".csv"

            with open(file_name, "w") as f:
                writer = csv.writer(f)
                writer.writerow(['description', 'price', 'rating', 'review_count', 'url'])
                writer.writerows(records)

            return jsonify("file " + file_name + " created successfully")

    except Exception as e:
        print("Check logs for error")
        lg.error("Error occured here")
        lg.exception(e)

        return jsonify("an error occured")





# def get_url(search_term):
#     """Generate a url from search term"""
#     template = "https://www.amazon.com/s?k={}&crid=1AU02VKAA00X0&sprefix=ultra%2Caps%2C198&ref=nb_sb_ss_ts-doa-p_1_7"
#     search_term = search_term.replace(" ", "+")
#
#     # add term query
#     url = template.format(search_term)
#
#     # add pagequery placeholder
#     # url += '&page{}'
#     url += '&page={}&ref=sr_pg_{}'
#
#     return url
#
#
# def extract_record(item):
#     """ Extract and return record from a single record"""
#
#     # description and url
#     atag = item.h2.a
#     description = atag.text.strip()
#     url = 'https://www.amazon.com' + atag.get('href')
#
#     # print(description)
#     # price
#     try:
#         price_parent = item.find('span', 'a-price')
#         price = price_parent.find('span', 'a-offscreen').text
#     except AttributeError:
#         return
#
#     try:
#
#         # rating
#         rating = item.i.text
#
#         # review count
#         review_count = item.find('span', 'a-size-base').text.replace(",", "")
#     except AttributeError:
#         rating = ' '
#         review_count = ' '
#
#     result = (description, price, rating, review_count, url)
#
#     return result
#
#
# def main(search_term):
#     """ Run the main routine """
#
#     # start up the webdriver
#     driver = webdriver.Chrome('/Users/deepakmongia/Documents/Data Science/iNeuron/Selenium/chromedriver')
#
#     records = []
#     url = get_url(search_term)
#
#     #    for page in range(1,21):
#     for page in range(1, 5):
#         url_page = url.format(page, page)
#         print(url_page)
#         driver.get(url_page)
#         soup = BeautifulSoup(driver.page_source, 'html')
#         results = soup.find_all('div', {'data-component-type': 's-search-result'})
#
#         for item in results:
#             record = extract_record(item)
#
#             if record:
#                 records.append(record)
#
#     driver.close()
#
#     # save data to csv file
#     with open(search_term.replace(" ", "_") + ".csv", "w") as f:
#         writer = csv.writer(f)
#         writer.writerow(['description', 'price', 'rating', 'review_count', 'url'])
#         writer.writerows(records)
#
#
#
# main("ultrawide monitor")



if __name__ == '__main__':
    app.run()
