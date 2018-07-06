# dockers_gcloud
### Build up an docker image that use twitter stream api to back twits to Mongodb base on location and run it on multiple vm with Kubernete cluster 

Create Project enable billing and Google Cloud APIs (or use Ubuntu)

### Add API:
•	Compute Engine API   
•	Google Cloud DataProc API   
•	Kubernetes Engine API  
•	Container Builder API  


### Create a VM instance
•	GCP menu-> Computing engine->VM instance->create  
•	Choose zone same one as before: us-east1-b  
•	Choose Machine type: 1vCPUs.  
•	Choose boot disk: ubuntu 16.04, boot disk type SSD disk  
•	in Identity and API access: Allow full access to all Cloud APIs  
•	In Firewall: allow both access, HTTP and HTTPs  

### Add IMA roles to youre user:
•	Project Billing Manager  
•	Compute Admin  
•	DataProc Editor  
•	Project Owner  
•	Storage Admin  
•	Logging Admin  
•	Cloud Container Builder  
•	Cloud Container Builder Editor  
•	Cloud Container Builder Viewer  

### Open VM Instance SSH or use Ubuntu

Initialize Google Cloud
```
gcloud init 
```
Git clone source files:
```
git clone https://github.com/sharon-hadar-leverate/dockers_gcloud.git
```
Go to project directory and ensure it is up to date:
```
cd dockers_gcloud
git pull
```

## Install mongodb
#### Create database @ mlab

- Create an account here: https://mlab.com/   
- Create new database: choose sand box free db, choose a name for it (for example "sharonhadar_db")
- Create a user to the database (you can use the same account details for it)
- Submit order  

#### Initialize location table 
##### Skip this part if youy allready have a location table.

Install python pip3:
```
sudo apt-get update
sudo apt-get -y install python3-pip
```

Install pymongo:
```
pip install pymongo 
```
Create a location table with running an existing python file:
```
python create_locations.py
```

## install docker:
Remove older versions of docker
```
sudo apt-get update
sudo apt-get remove docker docker-engine docker.i
```
Install packages to allow apt to use a repository over HTTPS
```
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
```
Add Docker’s official GPG key:
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

Verify that you now have the key with the fingerprint 9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88
```
sudo apt-key fingerprint 0EBFCD88

# should print:
pub   4096R/0EBFCD88 2017-02-22
      Key fingerprint = 9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88
uid                  Docker Release (CE deb) <docker@docker.com>
sub   4096R/F273FCD8 2017-02-22
```
Use the following command to set up the stable repository. 
```
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```
Install docker -ce
```
sudo apt-get update
sudo apt-get install docker-ce
```

Try to see if its working:
```
sudo docker run hello-world
# should print  "...Hello from Docker!..."
```

## Create Docker

##### (https://docs.docker.com/get-started/part2/#apppy)

### Build the app:
Run the build command. 
```
sudo docker build -t twitt_streamer .
```
The built image is in the machine local Docker image registry:
```
sudo docker image ls
# should print:
REPOSITORY            TAG                 IMAGE ID
twitt_streamer         latest              326387cea398
```
### Run the app: (optional)
#### This is only for checking that the image would work since it would run on the Kubernete cluster.

```
sudo docker run -p 4000:80 twitt_streamer
# or 
curl http://localhost:4000
```
Run it in the background add -d:
```
sudo docker run -d -p 4000:80 twitt_streamer
```
To stop the process:
get the container id:
```
sudo docker container ls
```
```
sudo docker container stop <container_id>
```
After running the image, it would change one of the locations in the database to "taken".
Go to the locations databse @ https://mlab.com/ and make sure all location "taken" property are set to zero.

## Share docker image
Sign up at https://hub.docker.com/ 
Log in to the Docker public registry 
```
sudo docker login
```
Tag the image:
```
sudo docker tag image username/repository:tag
#for example:
sudo docker tag twitt_streamer sharonhadar/tweetstream:ver1
```
See the new image with:
```
sudo docker image ls
```
Upload the image to the repository:
```
sodu docker push username/repository:tag
#for example:
sudo docker push sharonhadar/tweetstream:ver1
```
Pull and run from the repository: (optional to see if its works)
```
sudo docker run -p 4000:80 username/repository:tag
#for example:
sudo docker run -p 4000:80 sharonhadar/tweetstream:ver1
```

## Create a Kubernete cluster

### At GCP go to Kubernetes engine and create cluster
•	choose zonal us-east1-b  
•	use 1 cpu machine type  
•	node image ubuntu  
•	size 5   

#### from now on use the GCP shell 

Once the cluster is ready -> click connect.
Command-line access:
```
gcloud container clusters get-credentials cluster-1 --zone us-east1-b --project sharon-project-204821
```
Git clone source files:
```
git clone https://github.com/sharon-hadar-leverate/dockers_gcloud.git
```
Go to project directory and ensure it is up to date:
```
cd dockers_gcloud
git pull
```
Create a Service
```
kubectl create -f service.yaml
```
Create a Replication Controller
```
kubectl create -f controller.yaml
```
Inspect your cluster, List the pods, replication controllers, and services
```
kubectl get pods
kubectl get rc
kubectl get services
```


## Quering mLab

mLab has the option to use MongoDB Extended JSON in strict mode.  
This option doesnt include aggregetion quering and map reduce.  
It is still very useful for simple quering and checking.   
Go to twit_by_location collection @ https://mlab.com/databases/sharonhadar_db/collections/twit_by_location

An index in the collection looks like:
```
{
    "_id": {
        "$oid": "5b3a8a3e815e8f8c5127ceaa"
    },
    "location": "United States of America",
    "token": "short",
    "count": 1
}
```
To see the collection as a table format choose 'table' and wirte:
```
{
    "location": "location",
    "token": "token",
    "count": "count"
}
```
A simple query could be:  
1# show all tokens by descending order:  
      choose "start new search"  
      under "sort order" wirte: {"count":-1}  

## Quering RoboMongo
#### Prepare RoboMongo
In order to use aggregation queries, a mongoclient is necessary..
Download RoboMongo from https://robomongo.org/download  
After installing it, MongoDB connections window will open.  
Choose "Create".  
To get the connection information go back to mLab,  
Under mLab database https://mlab.com/databases/sharonhadar_db, there are the connection information
```  
To connect using a driver via the standard MongoDB URI (what's this?):
mongodb://<dbuser>:<dbpassword>@ds125381.mlab.com:25381/sharonhadar_db
```
In robomongo, under the Connection tab enter following in the Address box:
```
ds125381.mlab.com
```
And for the port box
```
25381
```
- Go to the Authentication tab.  
- Click on 'Perform authentication'.  
- Enter database name (sharonhadar_db), username, and password.   
- Let the auth mechanism be SCRAM-SHA-1  

#### Quering in RoboMongo

### quering examples:
#### I've searched for the word "world" in 06.07.2018 when FIFA World Cup just entered quarter final stage 

#1: What is the most popular words regardless of the city:
```
db.twit_by_location.aggregate([
    {"$group" : {_id:"$token", count:{$sum:"$count"}}},
    {"$sort" : { "count": -1 } }
])
```
![alt text](https://github.com/sharon-hadar-leverate/dockers_gcloud/blob/master/assets/query1.PNG)

#2: What words appears in all cities?
```
db.twit_by_location.aggregate([
    {"$group" : {_id:"$token", count:{$sum:1}}},
    {"$match" : { "count" : 5 } }
])
```
![alt text](https://github.com/sharon-hadar-leverate/dockers_gcloud/blob/master/assets/query2.PNG)

#3: What words appear only in one city
```
db.twit_by_location.aggregate([
    {"$group" : {_id:"$token", count:{$sum:1}}},
    {"$match" : { "count" : 1 } }
])
```
![alt text](https://github.com/sharon-hadar-leverate/dockers_gcloud/blob/master/assets/query3.PNG)


