# dockers_gcloud
build up multiple dockers and use twitter stream api to back twits to Mongodb base on location

Create Project enable billing and Google Cloud APIs

### Add API:
•	Compute Engine API
•	Cloud BigTable API
•	Cloud BigTable Table Admin API
•	Google Cloud DataProc API
•	Cloud BigTable Admin API


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
•	Choose indtance name: for example - sharon-mapreduce-bigtable
•	Write down the Instance id: for example - sharon-mapreduce-bigtable
•	In Instance type: Choode Development
•	In Storage type: Choose SSD
•	Zone: us-east1-b

### Open VM Instance SSH
