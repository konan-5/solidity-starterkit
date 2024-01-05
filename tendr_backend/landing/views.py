import json
from datetime import datetime
import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from bs4 import BeautifulSoup

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
                        no = columns[0].text.strip()
                        title = columns[1].find("a").text.strip()
                        resource_id = columns[2].text.strip()
                        client = columns[3].text.strip()
                        date_publish = columns[5].text.strip()
                        tenders_deadline = columns[6].text.strip()
                        procedure = columns[7].text.strip()
                        status = columns[8].text.strip()
                        notice_pdf = columns[9].find("a")["href"]
                        estimated_value = columns[11].text.strip()
                        cycle = columns[12].text.strip()
                        values_list = [
                            f"no: {no}",
                            f"title: {title}",
                            f"resource_id: {resource_id}",
                            f"client: {client}",
                            f"date_publish: {date_publish}",
                            f"tenders_deadline: {tenders_deadline}",
                            f"procedure: {procedure}",
                            f"status: {status}",
                            f"notice_pdf: {notice_pdf}",
                            f"estimated_value: {estimated_value}",
                            f"cycle: {cycle}"
                        ]
                        
                        joined_string = "\n".join(values_list)
                        work_item ={
                            "title":title,
                            "deadline":datetime.strptime(tenders_deadline, "%a %b %d %H:%M:%S GMT %Y").strftime("%d/%m/%Y %H:%M:%S"),
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
