# ML Pipeline Using Airflow In GCP Composer

We will try to set Airflow in Google Cloud Platform Environment using Google Composer [Google Cloud Composer](https://cloud.google.com/composer/docs/composer-2/run-apache-airflow-dag) . It's actually a very powerfull tools to use so that all we need to do is choose the image we want to use in the google composer. 

### Requirements<br>
- First thing to do is to create Google Cloud Platform Account. Usually This is completely free. Even you got $300 USD balance to be ised in 90 days for the sake of learning in GCP Environment<br>

### Installation<br>
- Create a project and you can give it any name with certain regulation<br>
- Create service account for your GCP: please follow the steps <a href='https://cloud.google.com/iam/docs/creating-managing-service-accounts'> how to create google service account</a><br>

![image](https://github.com/MahmoudAmgad88/composer-airflow/assets/54455617/0152e209-bdc6-41a7-b128-61a9bb981c85)

- Create IAM role for your GCP service account
  
![image](https://github.com/MahmoudAmgad88/composer-airflow/assets/54455617/487fc643-0ab1-43ee-8742-7d9754ffbb2b)

- Create a composer Environment with this details it wil take about `20 minutes` to be created: 
  - Location :  us-central1
  - Zone : us-central1
  - Node count : 3
  - Disk size (GB) : 20
  - Machine type : n1-standard-1
  - Cloud SQL machine type : db-n1-standard-2 (2 vCPU, 7.5 GB memory)
  - Web server machine type : composer-n1-webserver-2 (2 vCPU, 1.6 GB memory)<br>
  - US has the cheapest cost for running an environment.
- ![image](https://github.com/MahmoudAmgad88/composer-airflow/assets/54455617/4f756336-0f27-4482-9bdb-a85cdcbf1f40)

  - to create Environment choose Cloud Composer 1 or 2 [Cloud Composer versioning overview](https://cloud.google.com/composer/docs/concepts/versioning/composer-versioning-overview?_ga=2.232311903.-1169484772.1688163477&_gac=1.13708869.1688373034.CjwKCAjw44mlBhAQEiwAqP3eVvySMkBOtNCW3J95t3qkeogI31rm7rpXKIjN2dzSdu3Wfx8SBLH_rxoC9dcQAvD_BwE) just   - we will choose Cloud Composer 2 then choose Environment name and select you service account which we are creted before then we will kepp all configuration as default then press create.
    
![image](https://github.com/MahmoudAmgad88/composer-airflow/assets/54455617/a5308423-94aa-4a86-b603-80c493b0c525)

 ### How to Use AirFlow<br>
- i use project from this Video [Create first Dag in Cloud Composer(Airflow)](https://youtu.be/YgodScEIbOc)

  ![image](https://github.com/MahmoudAmgad88/composer-airflow/assets/54455617/3a4a307c-0e11-4950-a5b9-344d89e376f0)

 #### Steps :<br>
- Open google composer, and click `Airflow Server` and `DAG`
- we will use cloud sheel to create our `New DAG`
- Run below command for auth in cloud sheel.
  ```
  sudo su
  gcloud config set project [project id]
  ```
- we will creat a python code db_backup.py for new Dag then copy it to our bucket in DAG folder for deploying
- Place your DAG into the folder `DAG` inside airflow bucket. <b> Note : copy db_backup.py to our bucket in DAG folder for deployingy </b>

![image](https://github.com/MahmoudAmgad88/composer-airflow/assets/54455617/02d5e000-ff32-4211-a2ca-9222e7f9859a)

- Monitor your process trough Airflow UI





 ### For further improvement :<br>
- I need to call python code from github repo then deolpy it automaticlly after every changes in repo.
- neeed to deply Airflow with MLflow
- Need to build a full automated Pipeline using Airflow , MLflow and github
- Explore more about full automated Pipeline

![WhatsApp Image 2023-07-16 at 8 56 54 PM](https://github.com/MahmoudAmgad88/composer-airflow/assets/54455617/87c2b2b7-47bc-4e0a-8965-6eb7a0596730)


### some useful command may be needed in GCP:
```
sudo su
gcloud config set project [project id]
gcloud compute instances create my-test-vm --source-instance-template=my-instance-template-with-custom-image
gcloud compute instance-groups managed list
gcloud compute instance-groups managed delete my-managed-instance-group
gcloud compute instance-groups managed create my-mig --zone us-central1-a --template my-instance-template-with-custom-image --size 1
gcloud compute instance-groups managed set-autoscaling my-mig --max-num-replicas=2 --zone us-central1-a
gcloud compute instance-groups managed stop-autoscaling my-mig --zone us-central1-a
gcloud compute instance-groups managed resize my-mig --size=1 --zone=us-central1-a
gcloud compute instance-groups managed recreate-instances my-mig --instances=my-mig-85fb --zone us-central1-a
gcloud compute instance-groups managed delete my-managed-instance-group --region=us-central1
```
### IAM:
```
gcloud compute project-info describe
gcloud auth list
gcloud projects get-iam-policy glowing-furnace-304608
gcloud projects add-iam-policy-binding glowing-furnace-304608 --member=user:in28minutes@gmail.com --role=roles/storage.objectAdmin
gcloud projects remove-iam-policy-binding glowing-furnace-304608 --member=user:in28minutes@gmail.com --role=roles/storage.objectAdmin
gcloud iam roles describe roles/storage.objectAdmin
gcloud iam roles copy --source=roles/storage.objectAdmin --destination=my.custom.role --dest-project=glowing-furnace-304608
```
Thankyou and Happy Coding
