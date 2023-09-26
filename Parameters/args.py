import argparse


class arguments:
    """Contains arguments for any programme running on the CLI"""
    parser = argparse.ArgumentParser(description="Searching for a specific job offer")
    parser.add_argument("-n", "--name", metavar="Topic", type=str, nargs="?",
                        help="Topic of the job offer that you are looking for",
                        choices=["accounting", "customer-service", "online-data-entry", "design", "developer",
                                 "online-editing", "healthcare", "recruiter", "it", "legal", "marketing", "other",
                                 "project-manager", "qa", "sales", "online-teaching", "virtual-assistant", "writing"])
    args = parser.parse_args()


