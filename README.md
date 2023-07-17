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

 #### Steps<br>
- Open google composer, and click `Airflow Server` and `DAG`
- we will use cloud sheel to create our `New DAG`
- Run below command for auth in cloud sheel.
  ```
  sudo su
  gcloud config set project [project id]
  ```
- we will creat a python code db_backup.py for new Dag then copy it to our bucket in DAG folder for deploying


- Place your DAG into the folder `DAG` inside airflow bucket. <b> Note : Airflow bucket only for Airflow components only </b>
- Fill your variables in the Airflow UI by clicking Admin and then Variables.
- Change `bucket_path` and `project_id` as per your project and path name <br>
<img src='./result/variables.PNG'>
- Monitor your process trough Airflow UI

 ### For further improvement :<br>
- I should make the destination table inside the query using variable to make the code more robust and cleaner. But after trying to use airflow module variable, it did not work. I have to learn more about it.
- I should get used to coding as per PEP-8 format. In this file, I'm using autopep8 library, but I think the best practice is by reading and writting more and more code.
- Explore more about dataflow

Thankyou and Happy Coding
