from RemoteJobs.Parameters.db_connection import connect
import argparse


class arguments:
    parser = argparse.ArgumentParser(description="Searching for a specific table's data")
    parser.add_argument("-n", "--name", metavar="Topic", type=str, nargs="?",
                        help="The tables that you are looking for",
                        choices=["jobs", "companies", "fields", "links", "links_jobs", "links_companies"])
    args = parser.parse_args()


class Select(connect, arguments):
    """Select the data from the database by arguments on the CLI """

    def extract(self):
        try:
            query = "SELECT * FROM (%s)"
            param = self.args.name

            if param == "jobs":
                query = "SELECT * FROM jobs order by job_id"
            elif param == "companies":
                query = "SELECT * FROM companies order by company_id"
            elif param == "fields":
                query = "SELECT * FROM fields order by field_id"
            elif param == "links":
                query = "SELECT * FROM links order by link_id"
            elif param == "links_jobs":
                query = "SELECT * FROM links_jobs order by link_id"
            elif param == "links_companies":
                query = "SELECT * FROM links_companies order by link_id"

            self.cursor.execute(query, (param,))
            records = self.cursor.fetchall()

            i = 1
            for data in records:
                print(f"Record {i}: {data}")
                print("")
                i += 1

        except Exception as error:
            print("An error occurred while connecting to the database!", error)


def main():
    s1 = Select()
    s1.extract()


if __name__ == "__main__":
    main()
