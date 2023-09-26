import requests
from bs4 import BeautifulSoup
import time
from RemoteJobs.Parameters.arrays import array
from RemoteJobs.Parameters.db_connection import connect
from RemoteJobs.Parameters.identification import parameters


class ScraperExpiredJobs(array, parameters, connect):
    """Contains the "job_existence_ctr", and "delete_expired_jobs" functions"""
    def job_existence_ctr(self):
        """Checks the existence of the jobs by making comparisons on the database and website"""
        db_links = []
        current_links = []

        query_select_job = "SELECT link_url FROM links WHERE link_category = 'J'"
        self.cursor.execute(query_select_job)
        links = self.cursor.fetchall()  # the current links on the database

        for link in links:
            db_links.append(link[0])  # they are appended to the array in order to convert them into list from tuple

        for field in self.fields:
            r = requests.get(self.url + field)
            sp = BeautifulSoup(r.content, "html.parser")
            content = sp.find_all("a", class_="card m-0 border-left-0 border-right-0 border-top-0 border-bottom")

            for job_adverts in content:
                if job_adverts.has_attr("href"):
                    current_link = self.base_url + job_adverts["href"]
                    current_links.append(current_link)

        for i in range(len(db_links)):
            if db_links[i] not in current_links:
                self.expired_links.append(db_links[i])

        for x in self.expired_links:
            print(x)
        print(len(self.expired_links))

    def delete_expired_jobs(self):
        """Deletes the expired jobs from the database"""
        for i in range(len(self.expired_links)):
            link_url = self.expired_links[i]
            q_sel_link_id = "SELECT link_id FROM links WHERE link_url = (%s)"
            q_sel_co_id = "SELECT company_id FROM jobs WHERE link_id = (%s)"
            q_del_job = "DELETE FROM jobs WHERE link_id = (%s)"
            q_ctr_co = "SELECT * FROM jobs WHERE company_id = (%s)"
            q_del_co = "DELETE FROM links_companies WHERE company_id = (%s)"

            self.cursor.execute(q_sel_link_id, (link_url,))
            link_ID = self.cursor.fetchone()

            self.cursor.execute(q_sel_co_id, (link_ID,))  # co_id is to delete it from the tables regarding companies
            co_ID = self.cursor.fetchone()

            self.cursor.execute(q_del_job, (link_ID,))  # the job offer is deleted.
            self.cursor.execute(q_ctr_co, (co_ID,))  # the company is being checked if it has other offers.
            data_ctr = self.cursor.fetchall()

            if data_ctr is None:  # the company will be deleted from the database in the case it has no other offers
                self.cursor.execute(q_del_co, (co_ID,))
                print("This company has been deleted!")
            else:
                print("This company has other offers!")


def main():
    ans = True
    while ans:
        print(""""
        1.Check Expired Offers
        2.Delete Expired Offers From DB
        3.Exit/Quit
        """"")
        ans = input("Choice: ")
        start_time = time.time()
        s = ScraperExpiredJobs()

        if ans == "1":
            s.job_existence_ctr()
        elif ans == "2":
            s.job_existence_ctr()
            s.delete_expired_jobs()
        elif ans == "3":
            exit()
        elif ans != "":
            print("\n Try again!")

        duration = time.time() - start_time
        print(duration)


if __name__ == "__main__":
    main()
