from datetime import datetime
import requests
from bs4 import BeautifulSoup

def fetch_entenders_cpv(request):
    results = []
    # Make a GET request to the URL to retrieve the cookies
    response = requests.get(
        "https://www.etenders.gov.ie/epps/cpv/displayCpvAction.do", 
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    )

    # Get the cookies from the response headers
    cookies = response.headers.get('Set-Cookie')

    resp = requests.get(f"https://www.etenders.gov.ie/epps/cpv/displayCpvAction.do?CPVCodes=&lang=EN&cpv=cache&searchText={request}&searchby=keyword",
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "Cookie": cookies}
    )
    soup = BeautifulSoup(resp.content, features="html.parser")
    select = soup.find("select", attrs={"id":"searchResults"})
    options = select.find_all('option')
    
    for option in options:
        result = option.text.strip()
        results.append(result)

    return results

def fetch_entenders_epp(request):

    request_url = f"https://www.etenders.gov.ie/epps/viewCFTSFromFTSAction.do?estimatedValueMax={request['max']}0&contractType=&procedure=&contractAuthority=&mode=search&cpcCategory=0&estimatedValueMin=0&status=cft.status.tender.submission&status=cft.status.tender.submission&T01_ps=100&cpvArray=${request['cpv']}"
    print(request_url)
    resp = requests.get(request_url)
    soup = BeautifulSoup(resp.content, features="html.parser")
    results =[]

    table = soup.find('table', attrs = {'id':'T01'})
    if table is not None:
        for row in table.find('tbody').find_all("tr"):
            columns = row.find_all("td")
            if len(columns) == 13:
                no = columns[0].text.strip()
                title = columns[1].find("a").text.strip()
                category_link = columns[1].find("a")['href']
                category_req_url = f"https://www.etenders.gov.ie{category_link}"
                category_resp = requests.get(category_req_url)
                soup = BeautifulSoup(category_resp.content, features="html.parser")
                dt_element = soup.find('dt', string="CPV Codes:")
                dd_element = dt_element.find_next_sibling('dd')
                dd_text = dd_element.text.strip().split('\n')
                category = dd_text[0]
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
                    "tenders_deadline":datetime.strptime(tenders_deadline, "%a %b %d %H:%M:%S GMT %Y").strftime("%d/%m/%Y"),
                    "download_link":download_link,
                    "preview_link": preview_link,
                    "category":category
                }
                results.append(result)
                if no == '6':
                    break
    return results


def fetch_public_tenders(request):
    resp = requests.get(request)
    soup = BeautifulSoup(resp.content, features="html.parser")
    new_tenders_result = soup.find('div', attrs={"class":"SearchResults"})
    strongs = new_tenders_result.find_all('strong')
    return strongs[-1].text.strip()