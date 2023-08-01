from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import logging
import pymongo
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)
import os

app = Flask(__name__)
@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
                try:
                        # query to search for images
                        query = request.form['content'].replace(" ","")

                        # directory to store downloaded images
                        save_directory = "images/"

                        
                        # fetch the search results page
                        response = requests.get(f"https://www.flipkart.com/{query}/product-reviews/itm38acf149a4551?pid=MOBFU5WYVAAGDCGW&lid=LSTMOBFU5WYVAAGDCGWKJD8SS&marketplace=FLIPKART")

                        # parse the HTML using BeautifulSoup
                        soup = BeautifulSoup(response.content, "html.parser")

                        #Searching for col item relevant
                        col_itm = soup.find_all('div', class_='col')
                        delimeter = "|"
                        del col_itm[0]
                        final_set = set()
                        for div in col_itm:
                                #Searching and traversing all row element in html tags
                                row_tag = div.find_all('div', class_="row")
                                div_text = ""
                                p_text = ""
                                for j in row_tag:
                                        #Searching for all div tag
                                        div_tag = j.find_all('div')
                                        for divdtl in div_tag:
                                                if divdtl.text.strip() not in div_text:
                                                        div_text = div_text + delimeter +divdtl.text.strip()
                                        #Searching for all p tags
                                        p_tag = j.find_all('p')
                                        for pdtl in p_tag:
                                                if pdtl.text.strip() not in p_text:
                                                        p_text = p_text + delimeter +pdtl.text.strip()
                                #Removing reduntant data from the string
                                div_text = div_text.replace('READ MORE', "")
                                div_text = div_text.replace('PermalinkReport Abuse', "")
                                div_text = div_text.replace('Certified Buyer', "")
                                parts = div_text.rsplit(delimeter, 2)
                                div_text = parts[0]
                                #Removing reduntant data from the string
                                p_text = p_text.replace('Certified Buyer,', "")
                                p_text = p_text.replace(',', "")
                                #Joining to the single string
                                final_set.add(div_text[1:]+p_text)
                        # Split the strings and store in a list of lists
                        data_list = [item.split('|') for item in final_set]
                        print(data_list)
                    
                        return render_template('base.html', set_data=data_list)
                except Exception as e:
                    print(e)
                    logging.info(e)
                    return 'something is wrong'
            
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run()