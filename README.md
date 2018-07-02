# dockers_gcloud
build up multiple dockers and use twitter stream api to back twits to Mongodb base on location

Create Project enable billing and Google Cloud APIs

### Add API:
•	Compute Engine API  
•	Cloud BigTable API  
•	Cloud BigTable Table Admin API  
•	Google Cloud DataProc API  
•	Cloud BigTable Admin API  
•	Kubernetes Engine API  
•	Container Builder API  


### Create a VM instance
•	GCP menu-> Computing engine->VM instance->create  
•	Choose zone same one as before: us-east1-b  
•	Choose Machine type: 2vCPUs.  
•	Choose boot disk: ubuntu 16.04, boot disk type SSD disk  
•	in Identity and API access: Allow full access to all Cloud APIs  
•	In Firewall: allow both access, HTTP and HTTPs  

### Add IMA roles to youre user:
•	Project Billing Manager  
•	BigTable Administrator  
•	Compute Admin  
•	DataProc Editor  
•	Project Owner  
•	Storage Admin  
•	Logging Admin  
•	Cloud Container Builder  
•	Cloud Container Builder Editor  
•	Cloud Container Builder Viewer  

### Create a big table instance:
•	Choose indtance name: for example - sharon-docker-bigtable  
•	Write down the Instance id: for example - sharon-docker-bigtable  
•	In Instance type: Choode Development  
•	In Storage type: Choose SSD  
•	Zone: us-east1-b  

### Open VM Instance SSH

Sudo it:
```
sudo -s
```

Initialize Google Cloud
```
gcloud init 
```
git clone source files:
```
git clone https://github.com/sharon-hadar-leverate/dockers_gcloud.git
git pull
```

## install mongodb

Create an account here: https://mlab.com/   
Create new database: choose sand box free db, choose a name for it (for example "sharonhadar_db")  
Submit order  

#### Connect to MongoDB data base
To connect using the mongo shell:
```
mongo ds125381.mlab.com:25381/sharonhadar_db -u <dbuser> -p <dbpassword>
```
To connect using a driver via the standard MongoDB URI (what's this?):
```
mongodb://<dbuser>:<dbpassword>@ds125381.mlab.com:25381/sharonhadar_db
```
Create user for the DB inside the databas (use same user as the account)  

Install pymongo:
```
pip install pymongo 
```
Create a location table with running an existing python file:
```
python create_locations.py
```

### install docker:
remove older versions of docker
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
$ sudo apt-key fingerprint 0EBFCD88

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
install docker -ce
```
sudo apt-get update
sudo apt-get install docker-ce
```

try to see if its working:
```
sudo docker run hello-world
```
## Create Docker

### git clone source files (option1):
```
git clone https://github.com/sharon-hadar-leverate/dockers_gcloud.git
```
or preper it like below:
##### Preparing source files (option2) (https://docs.docker.com/get-started/part2/#apppy)

### Build the app:
run the build command. 
```
docker build -t friendlyhello .
```
The built image is in the machine local Docker image registry:
```
$ docker image ls
#prints:
REPOSITORY            TAG                 IMAGE ID
friendlyhello         latest              326387cea398
```
### Run the app:
```
docker run -p 4000:80 friendlyhello
# or 
$ curl http://localhost:4000
```
Run it in the background add -d:
```
docker run -d -p 4000:80 friendlyhello
```
To stop the process:
get the container id:
```
docker container ls
```
```
docker container stop <container_id>
```

# Share docker image
Sign up at https://hub.docker.com/ 
Log in to the Docker public registry 
```
docker login
```
Tag the image:
```
docker tag image username/repository:tag
#for example:
docker tag friendlyhello sharonhadar/get-started:part2
```
see the new image with:
```
docker image ls
```
upload the image to the repository:
```
docker push username/repository:tag
#for example:
docker push friendlyhello sharonhadar/get-started:part2
```
pull and run from the repository:
```
docker run -p 4000:80 username/repository:tag
#for example:
docker run -p 4000:80 sharonhadar/get-started:part2
```





  


