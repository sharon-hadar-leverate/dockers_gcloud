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

PATCH START:

## Step 1: Build the container image

run example hello word to understande kubernate and docker:
download hello word Go app:

```
git clone https://github.com/GoogleCloudPlatform/kubernetes-engine-samples
cd kubernetes-engine-samples/hello-app
```

Set the PROJECT_ID environment variable in your shell by retrieving the pre- configured project ID on gcloud by running the command below:
```
export PROJECT_ID="$(gcloud config get-value project -q)"
```
To build the container image of this application and tag it for uploading, run the following command:
```
sudo apt-get update
apt install docker.io
docker build -t gcr.io/${PROJECT_ID}/hello-app:v1 .
```

You can run docker images command to verify that the build was successful:
```
docker images
```

## Step 2: Upload the container image

You need to upload the container image to a registry so that Kubernetes Engine can download and run it. To upload the container image to Container Registry, running the following command:
```
gcloud docker -- push gcr.io/${PROJECT_ID}/hello-app:v1
```
`gcloud docker` will not be supported for Docker client versions above 18.03.
use `gcloud auth configure-docker` to configure `docker` to use `gcloud` as a credential helper
then use `docker` as you would for non-GCR registries, e.g. `docker pull gcr.io/project-id/my-image`.
```
docker pull gcr.io/${PROJECT_ID}/hello-app:v1
```
Add `--verbosity=error` to silence this warning, e.g. `gcloud docker --verbosity=error -- pull gcr.io/project-id/my-image`.

PATCH ENDS

