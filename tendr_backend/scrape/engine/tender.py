import re
import time

import requests
from bs4 import BeautifulSoup
from django.conf import settings

from tendr_backend.scrape.models import CftFile, ClientInfo


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


def get_cft_file(resource_id):
    request_url = (
        f"https://www.etenders.gov.ie/epps/cft/listContractDocuments.do?d-5419-p=&resourceId={resource_id}&T02_ps=100"
    )
    resp = requests.get(request_url)
    soup = BeautifulSoup(resp.content, features="html.parser")
    print(resource_id)
    cft_files = []
    tbody = soup.find("tbody")
    if tbody:
        for row in tbody.find_all("tr"):
            columns = row.find_all("td")
            if columns:
                addendum_id = columns[0].text.strip()
                title = columns[1].text.strip()
                document = columns[2].find("a") if columns[2].find("a") else None
                if document:
                    document_id = re.search(r"\d+", document.get("onclick")).group()
                    document_type = document.text.strip().split(".")[-1]
                    file = download_file(
                        f"https://www.etenders.gov.ie/epps/cft/downloadContractDocument.do?documentId={document_id}",
                        f"cft_file/{document_id}.{document_type}",
                    )
                description = columns[3].text.strip()
                lang = columns[4].text.strip()
                doument_version = f"/epps/cft/viewDocumentVersions.do?resourceId={resource_id}&d-16398-p=&T02_ps=100"
                action = f"/epps/cft/viewContractDocument.do?resourceId={resource_id}&contractDocID={document_id}"
            try:
                cft_file = CftFile.objects.create(
                    addendum_id=addendum_id,
                    title=title,
                    file=file,
                    description=description,
                    lang=lang,
                    doument_version=doument_version,
                    action=action,
                )
                print(cft_file)
                cft_files.append(cft_file)
            except Exception as e:
                print(e)
        time.sleep(1)
    return cft_files


def get_client_info(info_url, resource_id):
    request_url = f"https://www.etenders.gov.ie{info_url}"  # noqa
    resp = requests.get(request_url)
    soup = BeautifulSoup(resp.content, features="html.parser")
    table = soup.find("dl", attrs={"class": "row no-gutters"})
    dt_elements = table.find_all("dt")
    if len(dt_elements) == 12:
        organisation_name = dt_elements[0].find_next("dd").text.strip()
        ca_abbreviation = dt_elements[1].find_next("dd").text.strip()
        ca_type = dt_elements[2].find_next("dd").text.strip()
        annex = dt_elements[3].find_next("dd").text.strip()
        address = dt_elements[4].find_next("dd").text.strip()
        eircode_or_postal_code = dt_elements[5].find_next("dd").text.strip()
        city = dt_elements[6].find_next("dd").text.strip()
        county = dt_elements[7].find_next("dd").text.strip()
        email = dt_elements[8].find_next("dd").text.strip()
        phone_number = dt_elements[9].find_next("dd").text.strip()
        fax = dt_elements[10].find_next("dd").text.strip()
        website = dt_elements[11].find_next("dd").text.strip()
        client_info = ClientInfo(
            resource_id=resource_id,
            organisation_name=organisation_name,
            ca_abbreviation=ca_abbreviation,
            ca_type=ca_type,
            annex=annex,
            address=address,
            eircode_or_postal_code=eircode_or_postal_code,
            city=city,
            county=county,
            email=email,
            phone_number=phone_number,
            fax=fax,
            website=website,
        )
        client_info.save()


def get_tender_detail(detail_url, resource_id):
    request_url = f"https://www.etenders.gov.ie{detail_url}"
    resp = requests.get(request_url)
    soup = BeautifulSoup(resp.content, features="html.parser")
    table = soup.find("dl", attrs={"class": "row no-gutters"})
    if table:
        dt_elements = table.find_all("dt")
        data_dict = {}
        for dt in dt_elements:
            dt_text = re.sub(r"_+$", "", re.sub(r"[^\w]+", "_", dt.text.strip().lower()))
            if dt.find_next("dd").find("a"):
                if dt.find_next("dd").find("a", href=lambda href: href and "https://ted" in href):
                    dd_text = dt.find_next("dd").find("a")["href"]
                else:
                    info_url = dt.find_next("dd").find("a")["href"]
                    get_client_info(info_url, resource_id)
            else:
                dd_text = dt.find_next("dd").text.strip().replace("\r", "").replace("\t", "")
            data_dict[dt_text] = dd_text
        return data_dict


def main(page: int):
    request_url = f"https://www.etenders.gov.ie/epps/viewCFTSFromFTSAction.do?estimatedValueMax=&contractType=&publicationUntilDate=&cpvLabels=&description=&procedure=&title=&tenderOpeningUntilDate=&cftId=&contractAuthority=&mode=search&cpcCategory=&submissionUntilDate=&estimatedValueMin=&publicationFromDate=&submissionFromDate=&d-3680175-p={page}&tenderOpeningFromDate=&T01_ps=100&uniqueId=&status="  # noqa
    resp = requests.get(request_url)
    soup = BeautifulSoup(resp.content, features="html.parser")
    table = soup.find("table", attrs={"id": "T01"})
    tenders = []
    if table is not None:
        for row in table.find("tbody").find_all("tr"):
            columns = row.find_all("td")
            if columns:
                title = columns[1].find("a").text.strip()
                detail_url = columns[1].find("a")["href"]
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
                tender_detail = get_tender_detail(detail_url, resource_id)
                cft_files = get_cft_file(resource_id)
                tender = {
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
                    "tender_detail": tender_detail,
                    "cft_files": cft_files,
                }
                tenders.append(tender)

    return tenders
