import requests
from bs4 import BeautifulSoup
from django.conf import settings


def download_file(url, destination):
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"{settings.MEDIA_ROOT}/{destination}", "wb") as file:
            file.write(response.content)
        print(f"File downloaded successfully to {destination}")
        return destination
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
        return None


def main(page: int):
    request_url = f"https://www.etenders.gov.ie/epps/viewCFTSFromFTSAction.do?estimatedValueMax=&contractType=&publicationUntilDate=&cpvLabels=&description=&procedure=&title=&tenderOpeningUntilDate=&cftId=&contractAuthority=&mode=search&cpcCategory=&submissionUntilDate=&estimatedValueMin=&publicationFromDate=&submissionFromDate=&d-3680175-p={page}&tenderOpeningFromDate=&T01_ps=100&uniqueId=&status="  # noqa

    resp = requests.get(request_url)

    soup = BeautifulSoup(resp.content, features="html.parser")

    table = soup.find("table", attrs={"id": "T01"})

    # with open('../output.html' ,'w') as f:
    #     f.write(str(table))
    work_items = []
    if table is not None:
        for row in table.find("tbody").find_all("tr"):
            columns = row.find_all("td")
            if columns:
                title = columns[1].find("a").text.strip()
                resource_id = columns[2].text.strip()
                ca = columns[3].text.strip()
                info = columns[4].find("img")["title"].strip()
                date_published = columns[5].text.strip()
                tenders_submission_deadline = columns[6].text.strip()
                procedure = columns[7].text.strip()
                status = columns[8].text.strip()
                notice_pdf_link = columns[9].find("a")["href"] if columns[9].find("a") else None
                if notice_pdf_link:
                    notice_pdf = download_file(
                        f"https://www.etenders.gov.ie{notice_pdf_link}", f"notice_pdf/{resource_id}.pdf"
                    )
                else:
                    notice_pdf = None
                print(notice_pdf)
                award_date = columns[10].text.strip()
                estimated_value = columns[11].text.strip()
                cycle = columns[12].text.strip()
                work_item = {
                    "title": title,
                    "resource_id": resource_id,
                    "ca": ca,
                    "info": info,
                    "date_published": date_published,
                    "tenders_submission_deadline": tenders_submission_deadline,
                    "procedure": procedure,
                    "status": status,
                    "notice_pdf": notice_pdf,
                    "award_date": award_date,
                    "estimated_value": estimated_value,
                    "cycle": cycle,
                }
                work_items.append(work_item)
    with open("../out.json", "w") as f:
        f.write(str(work_items))
    return work_items
