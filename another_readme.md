# Python utilities for Mongodb

## MongoDB what and how
### Create MongoDB account and database
MongoDB is a scalable, high-performance, open source, document-oriented NoSQL database. It supports a large number of languages and application development platforms.
There are few options to MongoDB, I chose mLab, mainly bacause I liked the documentation.
Create an account here:
https://mlab.com/
Choose free account to start with, and you will get:
* Sandbox
> Our free Sandbox plan provides a single database with 0.5 GB of storage on a shared database server process running on a shared virtual machine (VM). This plan is best for development and prototyping.# Welcome to StackEdit!

Hi! I'm your first Markdown file in **StackEdit**. If you want to learn about StackEdit, you can read me. If you want to play with Markdown, you can edit me. If you have finished with me, you can just create new files by opening the **file explorer** on the left corner of the navigation bar.

In `CLOUD HOSTING LOCATION ` I chose 
Authenticate your email, to get access to creating new deployment. Choose free SandBox plan and create a database.
Create user in mLab web page, and we are set to use connect to our database in MongoDB.
### Connect to MongoDB data base
After your new deployment is created, choose it in the mLab web page, and you will get the connection information. Information has the form of:
* Database: db_name
** To connect using the mongo shell:
`mongo host:port/db_name -u <dbuser> -p <dbpassword>`
** To connect using a driver via the standard MongoDB URI (what's this?):
`mongodb://<dbuser>:<dbpassword>host:port/db_name`
The code in this git, use a driver via the standard MongoDB URI. biuld your URI from your data, in the following format:
`uri = 'mongodb://user:pass@host:port/db'`
Install pymongo puthon livrary. I used:
```
conda install -c anaconda pymongo 
```
To create location table, for minig twets by location, run:
```
python py_mongodb_create_locations_table.py
```
### Working scheme
The idea is to run the python code, listening to twitter stream from few dockers, each for different location.
#### Step 1, Initialize
In this step we create the docker files.
Create mongoDB collection with the locations definition. Each app/python code, will take a location from this joined table, and mark is as taken.
This step run only once, prio to runing the python code.
#### Step 2.  Connect to mongodb, Get location from location table, mark it as taken
#### Step 3. Listen to a stream according to location from python code
#### Ste 4. insert filtered words from stram to mongodb collection, while updating word count.
#### Step 5. Output topN words for each location
View the notebook for details on each step.
For runing on dockers, we need to package the code in python files.
* pymongo_create_locations.py
* pymongo_collect_tweets.py
* pymongo_show_results.py

<!--stackedit_data:
eyJoaXN0b3J5IjpbOTI1NDI5Mzk2XX0=
-->
