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

- Create a composer env with this details :
  - Location :  us-central1
  - Zone : us-central1
  - Node count : 3
  - Disk size (GB) : 20
  - Machine type : n1-standard-1
  - Cloud SQL machine type : db-n1-standard-2 (2 vCPU, 7.5 GB memory)
  - Web server machine type : composer-n1-webserver-2 (2 vCPU, 1.6 GB memory)<br>
  - US has the cheapest cost for running an environment.
- ![image](https://github.com/MahmoudAmgad88/composer-airflow/assets/54455617/4f756336-0f27-4482-9bdb-a85cdcbf1f40)

  - to create Environment choose Compse 1 or compse 2 [Cloud Composer versioning overview](https://cloud.google.com/composer/docs/concepts/versioning/composer-versioning-overview?_ga=2.232311903.-1169484772.1688163477&_gac=1.13708869.1688373034.CjwKCAjw44mlBhAQEiwAqP3eVvySMkBOtNCW3J95t3qkeogI31rm7rpXKIjN2dzSdu3Wfx8SBLH_rxoC9dcQAvD_BwE) just   - thyen you will choose Environment name and select you service account which we are creted before then we will kepp all configuration as default 
    
![image](https://github.com/MahmoudAmgad88/composer-airflow/assets/54455617/a5308423-94aa-4a86-b603-80c493b0c525)

 ### How to Use<br>
- Open google composer, and click `Airflow Server` and `DAG`
- Place your DAG into the folder `DAG` inside airflow bucket. <b> Note : Airflow bucket only for Airflow components only </b>
- Fill your variables in the Airflow UI by clicking Admin and then Variables.
- Change `bucket_path` and `project_id` as per your project and path name <br>
<img src='./result/variables.PNG'>
- Monitor your process trough Airflow UI
<img src='/result/airflow ui.PNG'>
<img src='/result/airflow ui 1.PNG'><br>
