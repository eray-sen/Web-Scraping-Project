import requests
from bs4 import BeautifulSoup
import time
from RemoteJobs.Parameters.arrays import array
from RemoteJobs.Parameters.db_connection import connect
from RemoteJobs.Parameters.identification import parameters
import uuid


class ScraperJob(parameters, connect, array):
    """Contains the "extract", "extract details", and "insert" functions"""
    def extract(self, sector):
        """Extracts the main information of the job offers"""
        r = requests.get(self.url + sector)
        sp = BeautifulSoup(r.content, "html.parser")
        content = sp.find_all("a", class_="card m-0 border-left-0 border-right-0 border-top-0 border-bottom")

        sector = sector.title()
        if sector.isalpha() is False:  # sector is it to request, but it's accepted as IT in the database
            sector = sector.split("-")  # Customer-Service -> Customer Service
            if len(sector) == 2:  # list
                if "Online" in sector:
                    sector = sector[1]  # Online Teaching -> Teaching
                else:
                    sector = sector[0] + " " + sector[1]
            elif len(sector) == 3:
                sector = sector[1] + " " + sector[2]
        elif len(sector) == 2:  # it -> IT
            sector = sector.upper()

        for job_adverts in content:
            brand = job_adverts.find("img")["alt"]
            name = job_adverts.find("span", class_="font-weight-bold").text
            post_date = job_adverts.find("date").text
            if job_adverts.has_attr("href"):
                link = self.base_url + job_adverts["href"]

            shift = job_adverts.find_all("span", class_="badge badge-success")
            length = len(shift) # (always between 0-3)

            if length == 3:
                shift = (shift[0].text, shift[1].text, shift[2].text)
            elif length == 2:
                shift = (shift[0].text, shift[1].text)
            elif length == 1:
                shift = shift[0].text
            else:
                shift = "None"

            self.main_rec.append([brand.strip(), name.strip(), post_date.strip(), shift, sector.strip(), link.strip()])
            self.urls.append(link.strip())

    def extract_details(self):
        """Extracts the detailed information of the job offers"""
        for i in range(len(self.urls)):
            r = requests.get(self.urls[i])
            sp = BeautifulSoup(r.content, "html.parser")
            content_details = sp.find_all("div", class_="job_info_container_sm")
            if content_details:  # some job offers might be expired.
                company_details = sp.find("div", class_="links_sm")("a")
                for details in content_details:
                    location = details.find("div", class_="location_sm row").text.split(":")[1]
                    try:
                        salary = details.find("div", class_="salary_sm row").text.split(":")[1]
                    except:
                        salary = str(None)
                    try:
                        benefit = details.find("div", class_="benefits_sm row").text.split(":")[1]
                    except:
                        benefit = str(None)
                    for co_details in company_details:
                        co_link = co_details["href"]
                        self.urls_co.append(co_link.strip())

                    self.det_rec.append([salary.strip(), benefit.strip(), location.strip()])
            else:
                for counter, value in enumerate(self.main_rec):  # value-> list
                    if value.__contains__(str(self.urls[i])):
                        self.main_rec.pop(counter)

    def insert(self):
        """Inserts the data of scraped job offers to the database"""
        query_link = "INSERT INTO links VALUES (%s,%s,%s)"
        query_link_co = "INSERT INTO links_companies VALUES (%s,%s)"
        query_job = "INSERT INTO jobs VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        query_co = "INSERT INTO companies VALUES (%s,%s)"
        query_co_select = "SELECT company_id FROM companies WHERE company_name = (%s)"
        query_field_select = "SELECT field_id FROM fields WHERE field_name = (%s)"
        query_link_select = "SELECT link_id FROM links WHERE link_url = (%s)"
        query_link_ctr = "SELECT link_id FROM links WHERE link_url = (%s)"

        for url in self.urls:  # LINKS
            ID = uuid.uuid4()
            self.cursor.execute(query_link, (str(ID), url, "J",))  # JOBS

        for i in range(len(self.urls_co)):
            url = self.urls_co[i]
            co_name = self.main_rec[i][0]
            self.cursor.execute(query_link_ctr, (url,))  # if the company already exists in table 'links'
            data_link = self.cursor.fetchone()
            link_ID = uuid.uuid4()
            co_ID = uuid.uuid4()

            if data_link is None: # the company will be inserted to the db in the case it does not exist in the table
                self.cursor.execute(query_link, (str(link_ID), url, "C"))  # COMPANIES
                self.cursor.execute(query_co, (str(co_ID), co_name))  # ID-NAME
                self.cursor.execute(query_link_co, (str(link_ID), str(co_ID)))

            else:
                print("This company already exists!")

        for i in range(len(self.main_rec)):
            data = [self.main_rec[i][0], self.main_rec[i][1], self.main_rec[i][2], self.main_rec[i][3],
                    self.det_rec[i][0], self.det_rec[i][1], self.det_rec[i][2], self.urls[i], self.main_rec[i][4]]
            company_name, job_name, post_date, shift, salary, benefit, location, link, field_name = data

            job_ID = uuid.uuid4()
            self.cursor.execute(query_co_select, (company_name,))
            co_ID = self.cursor.fetchone()
            self.cursor.execute(query_field_select, (field_name,))
            field_ID = self.cursor.fetchone()
            self.cursor.execute(query_link_select, (link,))
            link_ID = self.cursor.fetchone()
            self.cursor.execute(query_job, (str(job_ID), job_name, post_date, shift,
                                            salary, benefit, location, field_ID,
                                            co_ID, link_ID))

        duration = time.time() - self.start_time
        print(duration)


def main():
    s = ScraperJob()
    for sector in s.fields:
        s.extract(sector)
        s.extract_details()
        s.insert()


if __name__ == "__main__":
    main()
