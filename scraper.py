from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

import pandas as pd
import datetime
import os

def launch_soup(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup

def url_req(link):
    """return the page html"""
    x = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    x = urlopen(x)
    html = x.read().decode()
    return html

def remove_blanks(article):
    while True:
        try:
            article.remove("")
        except:
            break
    return article

def check_repeat_articles(candidate, article_title):
    txtfile = os.getcwd() + "\\data\\" + candidate + "_articles.txt"
            # print(txtfile)
            # creates a txt file of all article titles that have been counted
    with open(txtfile, "a+") as file:
        file.seek(0)
        # checks if article has been already counted before
        # if article is not in the txt file, it is counted and its title written 
        #file_content = file.readlines()
        #print(f"File content: {file_content}")
        if article_title.lower() not in file.read():
            file.write(article_title.lower())
            return True
        else:
            return False





def article_count_nat(candidate, link):
    """This function counts the number of articles featuring each candidate"""
    count = 0

    html = url_req(link)
    soup = launch_soup(html)
    soup = soup.find("ol", class_="article-collection")
    articles = soup.find_all("li")

    for article in articles:
        article = article.text
        article = article.strip().split("\n")

        # while True:
        #     try:
        #         article.remove("")
        #     except:
        #         break

        article = remove_blanks(article)
        
        # new line is added to the article title to improve readability when written to a text file later
        article_title = article[0] + "\n"
        article_date = article[-1]

        #print(f"{article_title} {article_date}")

        # considers articles published after July 14th
        if article_date == "Jul 20":
            #print("Past due date")
            break
        elif check_repeat_articles(candidate, article_title):
            count += 1


    return count

def nat_articles(news_links):
    """This functions returns a dictionary with candidates as the key and their articles count as the value for standard nation africa"""
    new_row = {}

    # The first column is date of the day the count is done
    new_row["date"] = [datetime.date.today()]

    for candidate, link in news_links.items():    
        #print(f"Counting {candidate}............")
        new_row[candidate] = [article_count_nat(candidate, link)]
    
    return new_row





def article_count_std(candidate, link):
    """Counts articles in standard media and returns the total count for each candidate link"""
    
    #html = url_req("https://www.standardmedia.co.ke/topic/raila-odinga")
    #html = url_req("https://www.standardmedia.co.ke/topic/william-ruto")
    html = url_req(link)
    soup = launch_soup(html)

    std_articles = {}

    def get_days():
        today = str(datetime.date.today())
        
        # Counts article published after July 14th
        initial_date = "2022-07-21"
        today = datetime.datetime.strptime(today, "%Y-%m-%d")
        initial_date = datetime.datetime.strptime(initial_date, "%Y-%m-%d")
        days = today - initial_date
        return days.days

    def check_date(article_date):
        article_date = article_date.split()
        
        if "month" in article_date or "months" in article_date:
            return False
        elif "day" in article_date or "days" in article_date:
            if int(article_date[0]) <= get_days():
                return True
        else:
            return True

    def first_container():
        articles = soup.find("div", class_="row boda-bottom")
        #print(articles)
        articles = articles.text.split("ago")

        for index, article in enumerate(articles):

            article = article.strip().split("\n")
            #print(article)

            try:
                try:
                    article.remove(".")
                    # Removes the "Premium" label for premium articles
                    article.remove("Premium")
                except:
                    article.remove("Premium")
            except:
                pass

            article = remove_blanks(article)

            if article == []:
                continue
            
            # The first article on the page has the name of the candidate
            if index == 0:
                # new line is added to the article title to improve readability when written to a text file later
                # Ignore the first element because it is the name of the candidate and not the article's title
                article_title = article[1] + "\n"
            else:
                article_title = article[0] + "\n"
            
            # last element is date article was published
            article_date = article[-1]

            if check_date(article_date) and check_repeat_articles(candidate, article_title):
                # print(article_title)
                std_articles[article_title] = article_date
    
        return std_articles

    def other_containers(std_articles):
        articles = soup.find_all("div", class_="card border-0 mb-3")

        for article in articles:
            article = article.text.strip().split("\n")

            try:
                try:
                    article.remove(".")
                    # Removes the "Premium" label for premium articles
                    article.remove("Premium")
                except:
                    article.remove("Premium")
            except:
                pass

            article = remove_blanks(article)

            article_title = article[0] + "\n"
            
            article_date = article[-1]

            if check_date(article_date) and check_repeat_articles(candidate, article_title):
                std_articles[article_title] = article_date

        return std_articles

    result = other_containers(first_container())
    count = len(result)
    return count

def std_articles(news_links):
    """This functions returns a dictionary with candidates as the key and their articles count as the value for standard media"""
    new_row = {}

    # The first column is date of the day the count is done
    new_row["date"] = [datetime.date.today()]

    for candidate, link in news_links.items():    
        #print(f"Counting {candidate}............")
        new_row[candidate] = [article_count_std(candidate, link)]
    
    return new_row



def check_write_csv(csv_sheet, article_count):
    """ Checks if csv exists """
    """ If csv does not exist, it creates a new one and writes to it with a header
        If csv exists, it writes to csv without header """
    
    destination = "data/" + csv_sheet

    def write_to_csv(df):
        df2 = pd.DataFrame(article_count)
        df = df.append(df2, ignore_index=True)
        df.to_csv(destination, index=False)

    if os.path.exists(os.getcwd() + "/data/" + csv_sheet):
        # If csv already exists, append new dataframe and write to csv without header
        df = pd.read_csv(destination)
        write_to_csv(df)
    else:
        df = pd.DataFrame()
        write_to_csv(df)

def nation_africa():
    """ This function counts the articles on each link(candidate), records the counts to a csv file, and 
        returns a dictionary of candidate and their counts"""
    
    news_links ={
    "raila": "https://nation.africa/kenya/people/raila-amolo-odinga-3809512",
    "ruto": "https://nation.africa/kenya/people/william-samoei-ruto-3809570",
    "karua": "https://nation.africa/kenya/people/martha-karua-3813480",
    "rigathi": "https://nation.africa/kenya/people/rigathi-gachagua-3815200"
    }
    
    nat_article_count = nat_articles(news_links)
    print(nat_article_count)
    print()
    csv_sheet = "nat_data.csv"
    
    check_write_csv(csv_sheet, nat_article_count)

    # if os.path.exists(os.getcwd() + "/data.csv"):
    #     #print("exists")
    #     df = pd.read_csv("data.csv")
    #     data_frame(nat_article_count, False, csv_sheet)
    # else:
    #     df = pd.DataFrame()
    #     data_frame(nat_article_count, True, csv_sheet)

    # df2 = pd.DataFrame(nat_article_count)
    # df = df.append(df2, ignore_index=True)

    # df.to_csv("data.csv", index=False)

    return nat_article_count

def std_media():
    """ This function counts the articles on each link(candidate), records the counts to a csv file, and 
        returns a dictionary of candidate and their counts"""

    news_links ={
    "raila": "https://www.standardmedia.co.ke/topic/raila-odinga",
    "ruto": "https://www.standardmedia.co.ke/topic/william-ruto",
    "karua": "https://www.standardmedia.co.ke/topic/martha-karua",
    "rigathi": "https://www.standardmedia.co.ke/topic/rigathi-gachagua"
    }

    std_article_count = std_articles(news_links)
    csv_sheet = "std_data.csv"
    print(std_article_count)
    print()
    
    check_write_csv(csv_sheet, std_article_count)

    # if os.path.exists(os.getcwd() + "/std_data.csv"):
    #     #print("exists")
    #     df = pd.read_csv("std_data.csv")
    # else:
    #     df = pd.DataFrame()
    
    # #df = pd.DataFrame()
    # std_article_count = std_articles(news_links)
    # df2 = pd.DataFrame(std_article_count)
    # df = df.append(df2, ignore_index=True)

    # df.to_csv("std_data.csv", index=False)

    return std_article_count

def total_data():
    nation = nation_africa()
    std = std_media()
    
    all_article_count = {}
    for key in std:
        if key in nation:
            if key == "date":
                all_article_count[key] = std[key]
            else:
                all_article_count[key] = [std[key][0] + nation[key][0]]

    print(all_article_count)
    csv_sheet = "totals_data.csv"
    
    check_write_csv(csv_sheet, all_article_count)