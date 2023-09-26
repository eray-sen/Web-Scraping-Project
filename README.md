## Introduction
The remote job offers from the [website](https://remote.co/) are fetched, processed, and inserted into the database. The job offers in the database are then checked, updated, deleted or new ones are inserted.


## Technologies Used

* Python 3.11 
* PostgreSQL


## Modules Used

* requests -> In order to make requests from the website
* BeautifulSoup -> In order to parse the data obtained
* argparse -> To use the CLI on selecting.py in order to guide the user

## DML Statemens

* ### inserting.py
          In this program, a user can fetch all the job offers and insert them into the empty database.

    #### Important Points:
          All identities such as Company ID and Job ID are generated using UUID standards.
* ### selecting.py
          In this program, a user can select data in the database based on a table name using the CLI.

* ### updating_jobs.py
          In this program, a user can check for new job offers that are available on the website but not in the database and insert them into to the database.

    #### Important Points:
          While inserting the data of new job offers, it is checked whether the companies of the new jobs exist in the database by having other job adverts in order not to create another ID for the same company.
      
* ### updating_content.py
          In this program, a user can check if there are any data updates to existing job offers in the database.

* ### deleting.py
          In this program, a user can check for expired job offers that are available in the database but not on the website anymore and delete them from the databaes.
     #### Important Points:
          During the deleting process, the companies are checked and deleted in the case that they do not have any job offers anymore.
          
