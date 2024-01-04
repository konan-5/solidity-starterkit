import codecs

import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from bs4 import BeautifulSoup

class Scrape(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        resp = requests.get("https://www.etenders.gov.ie/epps/viewCFTSFromFTSAction.do?cpvArray=45000000-Construction+work&cpvArray=72000000-IT+services%3A+consulting%2C+software+development%2C+Internet+and+support&cpvArray=85000000-Health+and+social+work+services&estimatedValueMax=5500000&contractType=&contractType=&publicationUntilDate=&cpvLabels=45000000%2C72000000%2C85000000&description=&description=&procedure=cft.procedure.type.open&procedure=cft.procedure.type.open&title=&tenderOpeningUntilDate=&cftId=&contractAuthority=&mode=search&cpcCategory=&cpcCategory=0&submissionUntilDate=&estimatedValueMin=0&publicationFromDate=&submissionFromDate=&tenderOpeningFromDate=&d-3680175-p=&uniqueId=&status=cft.status.tender.submission&status=cft.status.tender.submission&T01_ps=20")
        soup = BeautifulSoup(resp.content, features="html.parser")
        f = codecs.open("a.html", mode="w", encoding="utf-8")
        f.write(str(soup))
        f.close()

        # print(str(soup))
        return Response(str(soup))
