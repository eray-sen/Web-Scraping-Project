import requests
from bs4 import BeautifulSoup
import time
from RemoteJobs.Parameters.arrays import array
from RemoteJobs.Parameters.db_connection import connect
from RemoteJobs.Parameters.identification import parameters
import uuid


class ScraperJob(parameters, connect, array):
    """"Contains the "new_jobs_check", "new_jobs", "extract_new_jobs", and "insert_new_jobs" functions"""
    def new_jobs_check(self):
        """Checks the new job adverts by making comparisons on the database and website"""
        db_links = []
        query_select_job = "SELECT link_url FROM links WHERE link_category = 'J'"
        self.cursor.execute(query_select_job)
        links = self.cursor.fetchall() # the links on the db are fetched
        for link in links:
            db_links.append(link[0])  # they are appended to the array in order to convert them into list from tuple

        for field in self.fields:
            r = requests.get(self.url + field)
            sp = BeautifulSoup(r.content, "html.parser")
            content = sp.find_all("a", class_="card m-0 border-left-0 border-right-0 border-top-0 border-bottom")

            for job_adverts in content:
                if job_adverts.has_attr("href"):
                    current_link = self.base_url + job_adverts["href"]
                    if current_link not in db_links:
                        self.urls.append(current_link)

        for x in self.urls:
            print(x)
        print(len(self.urls))

    def new_jobs(self):
        """Gets some data of the new jobs"""
        db_links = []
        query_select_job = "SELECT link_url FROM links WHERE link_category = 'J'"
        self.cursor.execute(query_select_job)
        links = self.cursor.fetchall()  # the current links on the database
        for link in links:
            db_links.append(link[0])  # from tuple to list

        for field in self.fields:
            amount = 1
            r = requests.get(self.url + field)
            sp = BeautifulSoup(r.content, "html.parser")
            content = sp.find_all("a", class_="card m-0 border-left-0 border-right-0 border-top-0 border-bottom")

            if field.isalpha() is False:
                field = field.split("-")
                if len(field) == 2:
                    if "Online" in field:
                        field = field[1]
                    else:
                        field = field[0] + " " + field[1]
                elif len(field) == 3:
                    field = field[1] + " " + field[2]

            for job_adverts in content:
                amount += 1
                if job_adverts.has_attr("href"):
                    current_link = self.base_url + job_adverts["href"]
                    if current_link not in db_links:
                        self.urls.append(current_link)
                        self.rec_fields.append(field)
            self.fields_amount.append([field, amount])

        print(len(self.urls))

    def extract_new_jobs(self):
        """Extracts the all data of the new jobs"""
        for i in range(len(self.urls)):
            current_link = self.urls[i]
            current_field = self.rec_fields[i]
            r = requests.get(current_link)
            sp = BeautifulSoup(r.content, "html.parser")
            name = sp.find("div", class_="job_description").find_all("p")[0].text
            brand = sp.find("div", class_="co_name").text
            post_date = sp.find("time").text.split(":")[1]
            shift = sp.find_all("a", class_="job_flag")
            length = len(shift)

            if length == 3:
                shift = (shift[0].text, shift[1].text, shift[2].text)
            elif length == 2:
                shift = (shift[0].text, shift[1].text)
            elif length == 1:
                shift = shift[0].text
            else:
                shift = "None"

            self.main_rec.append(
                [brand.strip(), name.strip(), post_date.strip(), shift, current_field.strip(),
                 current_link.strip()])

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
                    if value.__contains__(current_link):
                        self.main_rec.pop(counter)

    def insert_new_jobs(self):
        """Inserts the data of the new jobs to the database"""
        query_link = "INSERT INTO links VALUES (%s,%s,%s)"
        query_link_co = "INSERT INTO links_companies VALUES (%s,%s)"
        query_job = "INSERT INTO jobs VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        query_co = "INSERT INTO companies VALUES (%s,%s)"
        query_co_select = "SELECT company_id FROM companies WHERE company_name = (%s)"
        query_field_select = "SELECT field_id FROM fields WHERE field_name = (%s)"
        query_link_select = "SELECT link_id FROM links WHERE link_url = (%s)"
        query_link_ctr = "SELECT link_id FROM links WHERE link_url = (%s)"
        query_field_id = "SELECT field_id FROM fields WHERE field_name = (%s)"
        query_field_update = "UPDATE fields SET field_job_amount = (%s) WHERE field_id = (%s)"

        for field in self.fields_amount:
            name = field[0]
            amount = field[1]
            self.cursor.execute(query_field_id, (name,))
            field_id = self.cursor.fetchone()
            self.cursor.execute(query_field_update, (amount, field_id))
        for url in self.urls:  # LINKS
            ID = uuid.uuid4()
            self.cursor.execute(query_link, (str(ID), url, "J",))  # JOBS

        for i in range(len(self.urls_co)):
            url = self.urls_co[i]
            co_name = self.main_rec[i][0]
            self.cursor.execute(query_link_ctr, (url,))  # if the company already exists in table links
            data_link = self.cursor.fetchone()
            link_ID = uuid.uuid4()
            co_ID = uuid.uuid4()

            if data_link is None:
                self.cursor.execute(query_link, (str(link_ID), url, "C")) 
                self.cursor.execute(query_co, (str(co_ID), co_name))
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


def main():
    ans = True
    while ans:
        print(""""
        1.Check New Offers
        2.Insert New Offers to the DB
        3.Exit/Quit
        """"")
        ans = input("Choice: ")
        start_time = time.time()
        s = ScraperJob()

        if ans == "1":
            s.new_jobs_check()
        elif ans == "2":
            s.new_jobs()
            s.extract_new_jobs()
            s.insert_new_jobs()
        elif ans == "3":
            exit()
        elif ans != "":
            print("\n Try again")

        duration = time.time() - start_time
        print(duration)


if __name__ == "__main__":
    main()
