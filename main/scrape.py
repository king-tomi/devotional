import re
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Union

def get_content(url: str) -> Union[BeautifulSoup,None]:
    """gets content from the website and returns a Beautiful soup object"""
    
    try:
        req = requests.get(url=url, stream=True)
        if req.status_code == 200:
            print("connection successful")
            print()
            soup = BeautifulSoup(req.content, 'html.parser')
            return soup
        else:
            print("Site not found")
            return
    except requests.RequestException:
        print("Error establishing request")
        return

def get_all_posts(url: str, category: str, church: str, date: str):
    content = get_content(url + "/" + category)
    results = {}
    if content:
        div = content.find_all("h2", class_ = "post-title entry-title")
        for d in div:
            a = d.find("a")
            title = a.text
            if church not in title:
                continue
            elif date not in title:
                continue
            elif "..." in title:
                continue
            else:
                link = str(a["href"])
                results[title] = link
        return results
    else:
        return None



def get_data_trem(post: str, church: str) -> Dict[str, List]:
    result = {}

    soup = get_content(post)
    if soup:
        article = soup.find("article")
        title = article.find("h2", class_ = "has-text-align-center").text
        result["title"] = title
        topic = article.find("div", class_="et_pb_text_inner").find_all("p")
        tp = [p.text for p in topic[1:]]
        result["topic"] = tp[0]
        result["bible_verse"] = tp[1]
        furth = ""
        daily = ""
        mes = []
        for m in tp[3:]:
            if church not in m and "Further Reading" not in m and "Also Read" not in m and "Devotional" not in m and "Daily Bible Reading" not in m and "Flatimes" not in m and "Phone" not in m:
                mes.append(m)
            elif "Further Reading" in m:
                furth += m
            elif "Daily Bible" in m:
                daily += m
            else:
                continue

        message = "\n\n".join(mes)
        result["message"] = message
        result["further_reading"] = furth
        result["daily_verse"] = daily
        return result
    else:
        return None

def get_data_anglican(post: str, church: str):
    soup = get_content(post)
    if soup:
        result = {}
        article = soup.find("article")
        div = article.find("div", class_ = "et_pb_text_inner")
        topic = div.find_all("p")
        tp = [p.text for p in topic]
        result["topic"] = tp[1]
        result["text"] = tp[2]
        verse = "\n\n".join([li.text for li in div.find_all("li")])
        result["verse"] = verse
        mes = []
        pray = ""
        for m in tp[3:]:
            if "THE MESSAGE" not in m and "PRAYER" not in m and church not in m:
                mes.append(m)
            elif "PRAYER" in m:
                pray += m
            else:
                continue

        message = "\n\n".join(mes)
        result["message"] = message
        result["prayer"] = pray
        return result
    else:
        return None



def get_data_open_teens(post: str, church: str):
    soup = get_content(post)
    if soup:
        result = {}
        article = soup.find("article")
        div = article.find("div", class_ = "et_pb_text_inner")
        topic = div.find_all("p")
        tp = [p.text for p in topic]
        result["topic"] = tp[1]
        result["memorise"] = tp[2]
        result["read"] = tp[4]
        verse = "\n\n".join([li.text for li in div.find_all("li")])
        result["verse"] = verse
        bible = ""
        mes = []
        h_t = ""
        for m in tp[5:]:
            if "ALSO READ" not in m and "BIBLE IN ONE YEAR" not in m and "KEY POINT" not in m and "HYMN" not in m and "CHORUS" not in m and "Daily Devotional" not in m and "Flatimes" not in m and church not in m:
                mes.append(m)
            elif "BIBLE IN ONE YEAR" in m:
                bible += m
            elif "HYMN" in m:
                h_t += m
            else:
                continue

        message = "\n".join(mes[:-1])
        result["message"] = message
        result["bible"] = bible
        result["key_point"] = mes[-1]
        result["hymn_title"] = h_t
        return result
    else:
        return None

def get_data_dunamis(post: str, church: str):
    soup = get_content(post)
    if soup:
        result = {}
        article = soup.find("article")
        div = article.find("div", class_ = "et_pb_text_inner")
        topic = div.find_all("p")
        tp = [p.text for p in topic]
        result["topic"] = tp[1]
        result["scripture"] = tp[2]
        result["thoughts"] = tp[3]
        proh = ""
        bible = ""
        quote = ""
        prayer = ""
        fact = ""
        furth = ""
        mes = []
        for m in tp[4:]:
            if church not in m and "Also Read" not in m and "ASSIGNMENTS" not in m and "PRAYER" not in m and "FOR FURTHER UNDERSTANDING" not in m and "QUOTE" not in m and "DAILY BIBLE" not in m and "AMAZING FACT" not in m and "PROPHETIC WORD" not in m and "Flatimes" not in m:
                mes.append(m)
            elif "PROPHETIC WORD/DECLARATION" in m:
                proh += m
            elif "AMAZING FACT" in m:
                fact += m
            elif "DAILY BIBLE READING" in m:
                bible += m
            elif "QUOTE" in m:
                quote += m
            elif "PRAYER" in m:
                prayer += m
            elif "FOR FURTHER UNDERSTANDING, GET THIS MESSAGE" in m:
                furth += m
            else:
                continue
        messsage = "\n".join(mes)
        result["message"] = messsage
        result["bible_daily"] = bible
        result["amazing_fact"] = fact
        result["prayer"] = prayer
        result["further_reading"] = furth
        result["quote"] = quote
        result["prophetic"] = proh
        return result
    else:
        return None


def get_data_dlcm(post: str, church: str):
    soup = get_content(post)
    if soup:
        result = {}
        article = soup.find("article")
        div = article.find("div", class_ = "et_pb_text_inner")
        topic = div.find_all("p")
        tp = [p.text for p in topic]
        result["topic"] = tp[1]
        result["text"] = tp[2]
        verse = []
        bible = ""
        thought = ""
        mes = []
        key = ""
        for m in tp[3:]:
            if church not in m and "KEY VERSE" not in m and "DCLM Daily Manna For Today MESSAGE" not in m and "Also Read" not in m and "THOUGHT FOR THE DAY" not in m and "THE BIBLE IN ONE YEAR" not in m and "DCLM Daily Manna" not in m and "Flatimes’ Notice Board" not in m and not re.search(r"^\d\d", m):
                mes.append(m)
            elif "KEY VERSE" in m:
                key += m
            elif "THOUGHT FOR THE DAY" in m:
                thought += m
            elif "THE BIBLE IN ONE YEAR" in m:
                bible += m
            elif re.search(r"^(\d){1,2}", m):
                verse.append(m)

            ver = "\n".join(verse)
            message = "\n".join(mes)
        result["verse"] = ver
        result["message"] = message
        result["key"] = key
        result["thought"] = thought
        result["bible"] = bible
        return result
    else:
        return None

def get_data_kenneth(post: str, church: str):
    soup = get_content(post)
    if soup:
        result = {}
        article = soup.find("article")
        div = article.find("div", class_ = "et_pb_text_inner")
        topic = div.find_all("p")
        tp = [p.text for p in topic]
        result["topic"] = tp[1]
        result["memory"] = tp[2]
        scripture = ""
        mes = []
        for m in tp[3:]:
            if church not in m and "Scripture Reading" not in m and "Flatimes" not in m:
                mes.append(m)
            elif "Scripture Reading" in m:
                scripture += m
            else:
                continue
        message = "\n".join(mes)
        result["message"] = message
        result["scripture"] = scripture
        return result
    else:
        return None


def get_data_andrew(post: str, church: str):
        soup = get_content(post)
        if soup:
            result = {}
            article = soup.find("article")
            div = article.find("div", class_ = "et_pb_text_inner")
            topic = div.find_all("p")
            tp = [p.text for p in topic]
            result["topic"] = tp[1]
            result["memory"] = tp[2]
            result["scripture"] = tp[3]
            mes = []
            for m in tp[4:]:
                if church not in m and "Flatimes Notice Board" not in m:
                    mes.append(m)
            message = "\n".join(mes)
            result["message"] = message
            return result
        else:
            return None