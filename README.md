## Introduction
The remote job offers from the [website](https://remote.co/) are fetched, processed, and inserted into a database. The job offers in a database are then checked, updated, deleted or new ones are inserted.


## Technologies Used

* Python 3.11 
* PostgreSQL


## Modules Used

* [requests](https://realpython.com/python-requests/) -> In order to make requests from the website
* [BeautifulSoup](https://realpython.com/beautiful-soup-web-scraper-python/) -> In order to parse the data obtained
* [argparse](https://realpython.com/command-line-interfaces-python-argparse/) -> To use the CLI on the selecting.py file in order to guide the user

## DML Statemens

* ### inserting.py
          In this program, a user can fetch all the job offers and insert them into an empty database.

    #### Important Points:
          All identities such as Company ID and Job ID are generated using UUID standards.
* ### selecting.py
          In this program, a user can select data in the database based on a table name using the CLI.

* ### updating_jobs.py
          In this program, a user can check for new job offers that are available on the website but not in the database and insert them into to a database.

    #### Important Points:
          While inserting the data of new job offers, it is checked whether the companies of the new jobs exist in the database by having other job adverts in order not to create another ID for the same company.
      
* ### updating_content.py
          In this program, a user can check if there are any data updates to existing job offers in the database.

* ### deleting.py
          In this program, a user can check for expired job offers that are available in the database but not on the website anymore and delete them from the databaes.
     #### Important Points:
          During the deleting process, the companies are checked and deleted in the case that they do not have any job offers anymore.
## Database Schema

 ### Fields
All fields have their own IDs and it is calculated how many job offers each one has.

### Links
The 'links' table contains the URLs of the links and their own IDs. Furthermore, the categories of the Links (job/company) are represented by an entity.
The 'links' table is connected to the 'links_jobs' and 'links_companies table by disjoint. 
### Jobs
The 'jobs' table contains all information about jobs. Also, the 'Foreign Keys' in the 'companies', 'fields', and 'links' tables refer to the 'Primary Key' of the 'jobs' table to prevent actions that would destroy links between the tables.
