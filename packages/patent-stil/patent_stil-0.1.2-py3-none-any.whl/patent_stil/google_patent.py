import json
import os
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from . import createDirs, downloadFile
from .utils import log


class GooglePatentInfo:
    def __init__(self, title='', abstract='', inventors='', application_number='', publication_number='',
                 publication_date='', pdf_url='', assignee_current='', claims_texts='', events=None,
                 classifications=None, descriptions='', patent_citations=None, non_patent_citations=None, city_bys=None,
                 similar_documents=None, legal_events=None, concepts=None):
        self.title = title
        self.abstract = abstract
        self.inventors = inventors
        self.application_number = application_number
        self.publication_number = publication_number
        self.publication_date = publication_date
        self.pdf_url = pdf_url
        self.assignee_current = assignee_current
        self.claims_texts = claims_texts
        self.events = events if events is not None else []
        self.classifications = classifications if classifications is not None else []
        self.descriptions = descriptions
        self.patent_citations = patent_citations if patent_citations is not None else []
        self.non_patent_citations = non_patent_citations if non_patent_citations is not None else []
        self.city_bys = city_bys if city_bys is not None else []
        self.similar_documents = similar_documents if similar_documents is not None else []
        self.legal_events = legal_events if legal_events is not None else []
        self.concepts = concepts if concepts is not None else []
    def toDataFrame(self):
        x={
            'title': [self.title],
            'abstract': [self.abstract],
            'inventors': [self.inventors],
            'application_number': [self.application_number],
            'publication_number': [self.publication_number],
            'publication_date': [self.publication_date],
            'pdf_url': [self.pdf_url],
            'assignee_current': [self.assignee_current],
            'claims_texts': [str(self.claims_texts)],
            'events': [str(self.events)],
            'classifications': [str(self.classifications)],
            'patent_citations': [str(self.patent_citations)],
            'non_patent_citations': [str(self.non_patent_citations)],
            'city_bys': [str(self.city_bys)],
            'similar_documents': [str(self.similar_documents)],
            'legal_events': [str(self.legal_events)],
            'concepts': [str(self.concepts)]
        }
        x1={
        }
        for k,v in self.descriptions.items():
            x1[k]=[v]
        return pd.DataFrame(x),pd.DataFrame(x1)


def getGooglePatentInfoByUrl(url,proxies=None,headers=None):
    parsed_url = urlparse(url)
    base_url=f"{parsed_url.scheme}://{parsed_url.netloc}"
    field_dict = {
        'title': '',
        'abstract': '',
        'inventors': '',
        'application_number': '',
        'publication_number':'',
        'publication_date': '',
        'pdf_url':'',
        'assignee_current':'',
        'claims_texts':'',
        'events':[],
        'classifications':[],
        'descriptions':'',
        'patent_citations':[],
        'non_patent_citations':[],
        'city_bys':[],
        'similar_documents':[],
        'legal_events':[],
        'concepts':[]
    }
    if proxies:
        if proxies=="clash":
            proxies = {
                'http': 'http://127.0.0.1:7890',
                'https': 'http://127.0.0.1:7890',
            }
    res=requests.get(url,proxies=proxies,headers=headers)
    soup=BeautifulSoup(res.content,"html.parser")
    field_dict["title"] = soup.find("span",{"itemprop":"title"}).text.strip()
    field_dict["pdf_url"] = soup.find('a', {'itemprop': 'pdfLink'})['href']
    field_dict["abstract"] = soup.find(class_="abstract").text.strip()
    field_dict["inventors"] = ', '.join([i.text.strip() for i in soup.findAll(itemprop="inventor")])
    field_dict["assignee_current"]=', '.join([i.text.strip() for i in soup.findAll(itemprop="assigneeCurrent")])
    field_dict["publication_number"] = soup.find(itemprop="publicationNumber").text.strip()
    field_dict["publication_date"]=soup.find(itemprop="publicationDate").text.strip()
    field_dict["application_number"]=soup.find(itemprop="applicationNumber").text.strip()
    events=soup.find_all(itemprop="events")
    if events:
        for event in events:
            event_document_id=event.find(itemprop="documentId")
            if event_document_id:
                event_document_id=event_document_id.text.strip()
            else:
                event_document_id=""
            event_dict={
                "date" : event.find(itemprop="date").text.strip(),
                "title" : event.find(itemprop="title").text.strip(),
                "type" : event.find(itemprop="type").text.strip(),
                "document_id" : event_document_id,
                # "description": ', '.join([i.text.strip() for i in soup.findAll(itemprop="description")])
            }
            field_dict["events"].append(event_dict)
    classifications_list=soup.find_all("li",itemprop='classifications')
    if classifications_list:
        for classifications in classifications_list:
            classifications_dict={
                "code" : classifications.find(itemprop='Code').text.strip(),
                "description" : classifications.find(itemprop='Description').text.strip()
            }
            field_dict["classifications"].append(classifications_dict)
    field_dict["claims_texts"]= soup.find('div',class_="claims").text.strip()
    description_div=soup.find(class_="description")
    if description_div is None:
        log(url+":\n"+str(soup),f"log/{time.time()}.log")
        raise Exception("无法解析正文:",url)
    content_dict = {}
    headings = description_div.find_all("heading")
    if headings is None or len(headings)==0:
        split_tag_list=["background-art","disclosure","description-of-drawings","mode-for-invention"]
        invention_title = soup.find('invention-title')
        background_art=description_div.find("background-art")
        tmp_list=[]
        sibling = invention_title.find_next_sibling()
        while sibling and sibling != background_art:
            tmp_list.append(sibling.text.strip())
            sibling = sibling.find_next_sibling()
        content_dict["交叉引用"]="\n".join(tmp_list[1:])
        for tag in split_tag_list:
            tag_obj=description_div.find(tag)
            if tag_obj or len(tag_obj)>1:
                div_list=tag_obj.find_all(class_="description-paragraph")
                content_dict[div_list[0].text.strip()]='\n'.join([i.text.strip() for i in div_list[1:]])
    else:
        for heading in headings:
            content_list = []
            next_element = heading.find_next_sibling()
            while next_element and next_element.name != 'heading':
                if next_element.name is not None:
                    content_list.append(next_element.get_text().strip())
                next_element = next_element.find_next_sibling()
            content_dict[heading.get_text().strip()] = "\n".join(content_list)
    field_dict["descriptions"] = content_dict
    #提取
    patent_citations = soup.find_all("tr", {"itemprop": "backwardReferencesOrig"})
    if patent_citations is None or len(patent_citations)==0:
        patent_citations = soup.find_all("tr", {"itemprop": "backwardReferencesFamily"})
    for patent_citation in patent_citations:
        assignee_original_obj=patent_citation.find("span",{"itemprop":"assigneeOriginal"})
        patent_citation_dict={
            "publication_number":patent_citation.find("span",{"itemprop":"publicationNumber"}).text.strip(),
            "primary_language":patent_citation.find("span",{"itemprop":"primaryLanguage"}).text.strip(),
            "url":base_url+patent_citation.find("a")['href'],
            "priority_date":patent_citation.find("td",{"itemprop":"priorityDate"}).text.strip(),
            "publication_date":patent_citation.find("td",{"itemprop":"publicationDate"}).text.strip(),
            "assignee_original":"" if assignee_original_obj is None else assignee_original_obj.text.strip(),
            "title":patent_citation.find("td",{"itemprop":"title"}).text.strip(),
        }
        field_dict["patent_citations"].append(patent_citation_dict)
    non_patent_citations = soup.find_all("tr", {"itemprop": "detailedNonPatentLiterature"})
    if non_patent_citations:
        for non_patent_citation in non_patent_citations:
            # non_patent_citation.find("a")['href'],
            non_patent_citation_dict = {
                # "url": non_patent_citation.find("a")['href'],
                "title": non_patent_citation.find("span", {"itemprop": "title"}).text.strip(),
            }
            field_dict["non_patent_citations"].append(non_patent_citation_dict)
    city_bys = soup.find_all("tr", {"itemprop": "forwardReferencesFamily"})
    if city_bys is None or len(city_bys)==0:
        city_bys = soup.find_all("tr", {"itemprop": "forwardReferencesOrig"})
    for city_by in city_bys:
        city_by_original_obj=city_by.find("span", {"itemprop": "assigneeOriginal"})
        city_by_dict = {
            "publication_number": city_by.find("span", {"itemprop": "publicationNumber"}).text.strip(),
            "primary_language": city_by.find("span", {"itemprop": "primaryLanguage"}).text.strip(),
            "url": base_url + city_by.find("a")['href'],
            "priority_date": city_by.find("td", {"itemprop": "priorityDate"}).text.strip(),
            "publication_date": city_by.find("td", {"itemprop": "publicationDate"}).text.strip(),
            "assignee_original": ""if city_by_original_obj is None else city_by_original_obj.text.strip(),
            "title": city_by.find("td", {"itemprop": "title"}).text.strip(),
        }
        field_dict["city_bys"].append(city_by_dict)
    similar_documents = soup.find_all("tr", {"itemprop": "similarDocuments"})
    if similar_documents:
        for similar_document in similar_documents:
            publication_number=''
            scholar_id=''
            primary_language=''
            if similar_document.find("meta", {"itemprop": "isScholar"}):
                type="scholar"
                scholar_id=similar_document.find("meta", {"itemprop": "scholarID"})["content"]
            else:
                type="patent"
                primary_language=similar_document.find("span", {"itemprop": "primaryLanguage"}).text.strip()
                publication_number=similar_document.find("span",{"itemprop":"publicationNumber"}).text.strip()
            similar_document_dict = {
                "type":type,
                "scholar_id":scholar_id,
                "publication_number": publication_number,
                "primary_language": primary_language,
                "url": base_url + similar_document.find("a")['href'],
                "publication_date": similar_document.find("time", {"itemprop": "publicationDate"}).text.strip(),
                "title": similar_document.find("td", {"itemprop": "title"}).text.strip(),
            }
            field_dict["similar_documents"].append(similar_document_dict)
    legal_events = soup.find_all("tr", {"itemprop": "legalEvents"})
    if legal_events:
        for legal_event in legal_events:
            legal_event_dict = {
                "date": legal_event.find("time", {"itemprop": "date"}).text.strip(),
                "code": legal_event.find("td", {"itemprop": "code"}).text.strip(),
                "title": legal_event.find("td", {"itemprop": "title"}).text.strip(),
                "attributes": '\n'.join([i.text.strip().replace("\n","") for i in legal_event.findAll("p",itemprop="attributes")]),
            }
            field_dict["legal_events"].append(legal_event_dict)
    concepts_ul = soup.find("ul", {"itemprop": "concept"})
    if concepts_ul:
        for concept in concepts_ul.find_all("li", {"itemprop": "match"}):
            concept_dict = {
                "id": concept.find("span", {"itemprop": "id"}).text.strip(),
                "name":concept.find("span", {"itemprop": "name"}).text.strip(),
                "sections":', '.join([i.text.strip() for i in concept.find_all("span",itemprop="sections")]),
                "similarity":concept.find("span", {"itemprop": "similarity"}).text.strip(),
                "count":concept.find("span", {"itemprop": "count"}).text.strip(),
            }
            field_dict["concepts"].append(concept_dict)
    return field_dict
def dictToGooglePatentInfo(d):
    return GooglePatentInfo(**d)
def getGooglePatentInfo(query_txt,base_url="https://patents.google.com",proxies=None,headers=None,language="auto"):
    if language == "auto":
        if query_txt.find("CN")!=-1:
            language = "zh"
        else:
            language = "en"
    url=f"{base_url}/patent/{query_txt}/{language}?oq={query_txt}"
    d=getGooglePatentInfoByUrl(url,proxies=proxies,headers=headers)
    if d is None:
        return None
    return dictToGooglePatentInfo(d)
def downloadGooglePdf(pdf_url,save_path):
    return downloadFile(pdf_url,save_path)
def autoGoogleSpider(query_txt,save_dir="data",save_pdf=True,base_url="https://patents.google.com",proxies=None,headers=None):
    google_patent_info=getGooglePatentInfo(query_txt,base_url=base_url,proxies=proxies,headers=headers)
    if google_patent_info is None:return False
    createDirs(save_dir)
    base_patent_dir = os.path.join(save_dir, google_patent_info.publication_number)
    createDirs(base_patent_dir)
    patent_info_dataframe,patent_content_dataframe=google_patent_info.toDataFrame()

    patent_info_file = os.path.join(base_patent_dir, f"info.xlsx")
    patent_info_dataframe.to_excel(patent_info_file,index=False)

    patent_content_file = os.path.join(base_patent_dir, f"content.xlsx")
    patent_content_dataframe.to_excel(patent_content_file,index=False)
    with open(os.path.join(base_patent_dir, f"origin_data.json"), "w", encoding="utf-8") as f:
        json.dump(google_patent_info.__dict__, f, ensure_ascii=False)
    if save_pdf:
        patent_pdf_file = os.path.join(base_patent_dir, f"patent.pdf")
        downloadGooglePdf(google_patent_info.pdf_url, patent_pdf_file)
    return True
