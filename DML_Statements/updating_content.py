import requests
from bs4 import BeautifulSoup
import time
from RemoteJobs.Parameters.arrays import array
from RemoteJobs.Parameters.db_connection import connect
from RemoteJobs.Parameters.identification import parameters


class ScraperJob(parameters, connect, array):
    """Contains only the "update" function"""

    def update(self):
        """Checks whether there is any data update in the job adverts by making a comparison on the database and
        website and makes updates on the database"""
        db_links = []
        query_select_job = "SELECT link_url FROM links WHERE link_category = 'J'"
        self.cursor.execute(query_select_job)
        links = self.cursor.fetchall()  # the links on the db are fetched
        for link in links:
            db_links.append(link[0])  # they are appended to the array in order to convert them into list from tuple

        for i in range(len(db_links)):
            print(i)
            url = db_links[i]
            r = requests.get(url)
            sp = BeautifulSoup(r.content, "html.parser")
            content_details = sp.find_all("div", class_="job_info_container_sm")

            if content_details:  # some job offers might be expired.
                name = sp.find("div", class_="job_description").find_all("p")[0].text
                post_date = sp.find("time").text.split(":")[1]
                self.main_rec.append(
                    [name.strip(), post_date.strip()])

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

                    self.det_rec.append([salary.strip(), benefit.strip(), location.strip()])

                current_data = [self.main_rec[i][0], self.main_rec[i][1], self.det_rec[i][0],
                                self.det_rec[i][1], self.det_rec[i][2]]
                c_name, c_date, c_salary, c_benefit, c_location = current_data  # current data from the website

                query_link_id = "SELECT link_id FROM links WHERE link_url = (%s)"
                self.cursor.execute(query_link_id, (url,))
                link_id = self.cursor.fetchone()

                query_url = "SELECT job_name, job_post_date, job_salary, job_benefit, job_location FROM jobs WHERE " \
                            "link_id = (%s)"
                self.cursor.execute(query_url, (link_id,))
                data = self.cursor.fetchall()

                existed_data = [data[0][0], data[0][1], data[0][2], data[0][3], data[0][4]]
                e_name, e_date, e_salary, e_benefit, e_location = existed_data  # existed data from the db

                if c_name != e_name:
                    query_update = "UPDATE jobs SET job_name =(%s) WHERE link_id =(%s)"
                    self.cursor.execute(query_update, (c_name, link_id))
                if c_date != e_date:
                    query_update = "UPDATE jobs SET job_post_date =(%s) WHERE link_id =(%s)"
                    self.cursor.execute(query_update, (c_date, link_id))
                if c_salary != e_salary:
                    query_update = "UPDATE jobs SET job_salary =(%s) WHERE link_id =(%s)"
                    self.cursor.execute(query_update, (c_salary, link_id))
                if c_benefit != e_benefit:
                    query_update = "UPDATE jobs SET job_benefit =(%s) WHERE link_id =(%s)"
                    self.cursor.execute(query_update, (c_benefit, link_id))
                if c_location != e_location:
                    query_update = "UPDATE jobs SET job_location =(%s) WHERE link_id =(%s)"
                    self.cursor.execute(query_update, (c_location, link_id))
            else:

                self.main_rec.append([None, None])
                self.det_rec.append([None, None, None])  # in order to not have an 'out of list' error

        duration = time.time() - self.start_time
        print(duration)


def main():
    s = ScraperJob()
    s.update()


if __name__ == "__main__":
    main()
