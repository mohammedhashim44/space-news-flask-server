import requests
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import config
import sys

def get_last_yesterday_iso():

    today = datetime.now()

    yesterday = today - timedelta(days=1)
    yesterday = yesterday.replace(hour=0,minute=0,second=0,microsecond=0)
    yesterday_iso = yesterday.isoformat()

    return yesterday_iso

def get_results_json(after_date):
    url = f"https://api.spaceflightnewsapi.net/v4/articles/?published_at_gte={after_date}&limit=1000";
    print(url)
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Request error")

    json_raw = response.json()

    # maybe to get all results we need to fetch the next url,
    # check next urls to fetch data until its finished
    if not json_raw["next"] :
        results_json_raw = json_raw["results"]
        return results_json_raw
    
    # fetch next url until its finished
    all_results = json_raw["results"]
    while json_raw["next"] is not None :
        url = json_raw["next"]
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Request error")

        json_raw = response.json()
        results_json_raw = json_raw["results"]
        print(url)
        print(len(results_json_raw))
        print()
        all_results += results_json_raw

    return all_results

def get_articles_df(results_json):

    def get_data_from_article(article_raw_json):
        columns = [
            "id",
            "title",
            "image_url",
            "url",
            "published_at",
        ]
        # check if all columns are in article_raw_json
        for column in columns:
            if column not in article_raw_json:
                raise Exception(f"Column {column} not in article_raw_json")
        
        data =  {
            "id": article_raw_json["id"],
            "title": article_raw_json["title"],
            "image_url": article_raw_json["image_url"],
            "url": article_raw_json["url"],
            "published_at": article_raw_json["published_at"],
        }
        return data

    all_articles = []
    for article_raw_json in results_json:
        article_data = get_data_from_article(article_raw_json)
        all_articles.append(article_data)

    df = pd.DataFrame(all_articles)
    return df


def store_df_to_sqllite(df):
    # if df is empty, exit
    if len(df) == 0:
        return

    # store data to sqllite
    conn = sqlite3.connect(config.SQLITE_FILE)
    df.to_sql(config.TABLE_NAME,conn,if_exists=config.ACTION_IF_DATA_EXIST,index=False,index_label="published_at")
    conn.close()


if __name__ == "__main__":
    # check cmd arguemnts 
    # if no valid date is passed, use yesterday's date 
    after_date = None

    # date format: dd-mm-yyyy
    # example: python3 fetch_data.py --date 09-02-2023
    if len(sys.argv) == 3:
        if sys.argv[1] == "--date":
            after_date = sys.argv[2]
            try:
                after_date = datetime.strptime(after_date, '%d-%m-%Y')
                # convert to iso format
                after_date = after_date.isoformat()
            except ValueError:
                print("Incorrect data format, should be dd-mm-YYYY")
                exit()
    
    # use yesterday's date
    if after_date is None:
        after_date = get_last_yesterday_iso()

    # get json raw data
    results_json = get_results_json(after_date=after_date)

    print(len(results_json))

    # get articles df
    df = get_articles_df(results_json)

    # store data to sqllite
    store_df_to_sqllite(df)  