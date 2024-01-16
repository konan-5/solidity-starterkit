import json
from datetime import datetime, timedelta
import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from bs4 import BeautifulSoup
from .utils.scrape import fetch_entenders_epp, fetch_public_tenders

class Scrape(APIView):

    permission_classes = (AllowAny,)
    def post(self, request):
        request_url = [
            {
                "category":"Construction Works",
                "url":"https://www.etenders.gov.ie/epps/viewCFTSFromFTSAction.do?cpvArray=45000000-Construction+work&estimatedValueMax=5500000&contractType=&contractType=&publicationUntilDate=&cpvLabels=45000000&description=&description=&procedure=cft.procedure.type.open&procedure=cft.procedure.type.open&title=&tenderOpeningUntilDate=&cftId=&contractAuthority=&mode=search&cpcCategory=&cpcCategory=0&submissionUntilDate=&estimatedValueMin=0&publicationFromDate=&submissionFromDate=&d-3680175-p=&tenderOpeningFromDate=&T01_ps=100&uniqueId=&status=cft.status.tender.submission&status=cft.status.tender.submission"
            },
            {
                "category":"IT Services",
                "url":"https://www.etenders.gov.ie/epps/viewCFTSFromFTSAction.do?cpvArray=72000000-IT+services%3A+consulting%2C+software+development%2C+Internet+and+support&estimatedValueMax=5500000&contractType=&contractType=&publicationUntilDate=&cpvLabels=72000000&description=&description=&procedure=cft.procedure.type.open&procedure=cft.procedure.type.open&title=&tenderOpeningUntilDate=&cftId=&contractAuthority=&mode=search&cpcCategory=&cpcCategory=0&submissionUntilDate=&estimatedValueMin=0&publicationFromDate=&submissionFromDate=&tenderOpeningFromDate=&d-3680175-p=&uniqueId=&status=cft.status.tender.submission&status=cft.status.tender.submission&T01_ps=100"
            },
        ]
        total_url = "https://www.etenders.gov.ie/epps/viewCFTSFromFTSAction.do?estimatedValueMax=&contractType=&contractType=&publicationUntilDate=&cpvLabels=&description=&description=&procedure=&procedure=&title=&tenderOpeningUntilDate=&cftId=&contractAuthority=&mode=search&cpcCategory=&cpcCategory=0&submissionUntilDate=&estimatedValueMin=&publicationFromDate=&submissionFromDate=&tenderOpeningFromDate=&d-3680175-p=&uniqueId=&status=&status=&T01_ps=100"
        total_tenders = fetch_public_tenders(total_url)
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        new_url = f"https://www.etenders.gov.ie/epps/viewCFTSFromFTSAction.do?estimatedValueMax=&contractType=&contractType=&publicationUntilDate=&cpvLabels=&description=&description=&procedure=&procedure=&title=&tenderOpeningUntilDate=&cftId=&contractAuthority=&mode=search&cpcCategory=&cpcCategory=0&submissionUntilDate=&estimatedValueMin=&publicationFromDate={yesterday.strftime('%d/%m/%Y')}&submissionFromDate=&tenderOpeningFromDate=&d-3680175-p=&uniqueId=&status=&status=&T01_ps=100"
        new_tenders = fetch_public_tenders(new_url)

        tickers =[]
        for req in request_url:
            resp = requests.get(req["url"])
            soup = BeautifulSoup(resp.content, features="html.parser")
            table = soup.find("table", attrs={"id": "T01"})
            work_items =[]
            if table is not None:
                for row in table.find("tbody").find_all("tr"):
                    columns = row.find_all("td")
                    if len(columns) == 13:
                        title = columns[1].find("a").text.strip()
                        client = columns[3].text.strip()
                        tenders_deadline = columns[6].text.strip()
                        estimated_value = columns[11].text.strip()
                        work_item ={
                            "title":title,
                            "deadline":datetime.strptime(tenders_deadline, "%a %b %d %H:%M:%S GMT %Y").strftime("%d/%m/%Y") if tenders_deadline else "",
                            "client": client,
                            "value":estimated_value,
                        }
                        work_items.append(work_item)
            ticker = {
                "category":req["category"],
                "workItems":work_items,
            }
            tickers.append(ticker)
        
        response = {
            "tenders":[
                {
                    'is_private':False,
                    'newTenders':new_tenders,
                    'totalTenders':total_tenders,
                    'view_link':total_url
                },
                {
                    'is_private':True,
                    'newTenders':47,
                    'totalTenders':1795,
                },
            ],
            "tickers":tickers
        }
        return Response(response)

class Search(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        # keyword = request.data.get('keyword')
        max_value =request.data.get('maxValue')
        cpv =request.data.get('cpv')
        print(request.data.get('maxValue'))
        # cpv = fetch_entenders_cpv(keyword)
        epp ={
            'max': max_value,
            'cpv':cpv,
        }
        epps = fetch_entenders_epp(epp)
        
        return Response(epps)

class ViewMore(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        request_url = request.data.get('link')
        resp = requests.get(request_url)
        soup = BeautifulSoup(resp.content, features="html.parser")
        epps =[]

        table = soup.find('table', attrs = {'id':'T01'})
        if table is not None:
            for row in table.find('tbody').find_all("tr"):
                columns = row.find_all("td")
                if len(columns) == 13:
                    no = columns[0].text.strip()
                    title = columns[1].find("a").text.strip()
                    # category_link = columns[1].find("a")['href']
                    # category_req_url = f"https://www.etenders.gov.ie{category_link}"
                    # category_resp = requests.get(category_req_url)
                    # soup = BeautifulSoup(category_resp.content, features="html.parser")
                    # dt_element = soup.find('dt', string="CPV Codes:")
                    # dd_element = dt_element.find_next_sibling('dd')
                    # dd_text = dd_element.text.strip().split('\n')
                    # category = dd_text[0]
                    preview_link_element = columns[1].find("a")
                    preview_link = preview_link_element["href"] if preview_link_element else ""
                    client = columns[3].text.strip()
                    tenders_deadline = columns[6].text.strip()
                    stage = columns[8].text.strip()
                    download_link_element = columns[9].find("a")
                    download_link = download_link_element["href"] if download_link_element else ""
                    estimated_value = columns[11].text.strip()
                    result ={
                        "client":client,
                        "title":title,
                        "stage":stage,
                        "value":estimated_value,
                        "tenders_deadline":datetime.strptime(tenders_deadline, "%a %b %d %H:%M:%S GMT %Y").strftime("%d/%m/%Y") if tenders_deadline else "",
                        "download_link":download_link,
                        "preview_link": preview_link,
                        # "category":category
                    }
                    epps.append(result)
                    if no == '50':
                        break
        return Response(epps)
