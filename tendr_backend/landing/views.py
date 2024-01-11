import json
from datetime import datetime
import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from bs4 import BeautifulSoup
from .utils.scrape import fetch_entenders_cpv, fetch_entenders_epp
class Scrape(APIView):

    permission_classes = (AllowAny,)
    def post(self, request):
        results =[]
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
                            "deadline":datetime.strptime(tenders_deadline, "%a %b %d %H:%M:%S GMT %Y").strftime("%d/%m/%Y"),
                            "client": client,
                            "value":estimated_value,
                        }
                        work_items.append(work_item)
            result = {
                "category":req["category"],
                "workItems":work_items,
            }
            results.append(result)

        return Response(json.dumps(results))



class Search(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        keyword = request.data.get('keyword')
        max_value =request.data.get('maxValue')
        cpv = fetch_entenders_cpv(keyword)
        epp ={
            'max': max_value,
            'type':'services',
            'cpv':cpv
        }
        epps = fetch_entenders_epp(epp)
        
        return Response(epps)