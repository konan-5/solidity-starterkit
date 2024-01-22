import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from dateutil import parser
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from tendr_backend.scrape.models import Tender


def parse_date(date_string):
    dt = parser.parse(date_string)

    # If the datetime object is naive (no timezone info), assume UTC
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        dt = dt.replace(tzinfo=timezone.utc)

    # Getting Unix time
    unix_time = int(dt.timestamp())

    return unix_time


class Scrape(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        now = time.time()
        twenty_four_hours_ago = timezone.now() - timezone.timedelta(hours=24)
        new_tenders = Tender.objects.filter(date_published__gt=twenty_four_hours_ago).count()
        tickers = [
            {
                "category": "s",
                "workItems": [
                    {
                        "title": "",
                        "deadline": "",
                        "client": "",
                        "value": "",
                    }
                ],
            }
        ]
        response = {
            "widgets": [
                {
                    "is_private": False,
                    "newTenders": new_tenders,
                    "totalTenders": Tender.objects.count(),
                },
            ],
            "tickers": tickers,
        }
        print(time.time() - now, "aaaaaaaaa")
        return Response(response)


class Search(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        # keyword = request.data.get('keyword')
        max_value = request.data.get("max_value")
        cpv = request.data.get("cpv")
        print(max_value)
        # cpv = fetch_entenders_cpv(keyword)
        epp = {
            "max": max_value,
            "cpv": cpv,
        }
        # epps = fetch_entenders_epp(epp)
        epps = [
            {
                "client": "1",
                "title": "3",
                "stage": "e",
                "value": "w",
                "tenders_deadline": "f",
                "download_link": "e",
                "preview_link": "d",
            }
        ]
        return Response(epps)


class ViewMore(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        request_url = request.data.get("link")
        resp = requests.get(request_url)
        soup = BeautifulSoup(resp.content, features="html.parser")
        epps = []

        table = soup.find("table", attrs={"id": "T01"})
        if table is not None:
            for row in table.find("tbody").find_all("tr"):
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
                    result = {
                        "client": client,
                        "title": title,
                        "stage": stage,
                        "value": estimated_value,
                        "tenders_deadline": datetime.strptime(tenders_deadline, "%a %b %d %H:%M:%S GMT %Y").strftime(
                            "%d/%m/%Y"
                        )
                        if tenders_deadline
                        else "",
                        "download_link": download_link,
                        "preview_link": preview_link,
                        # "category":category
                    }
                    epps.append(result)
                    if no == "50":
                        break
        return Response(epps)
