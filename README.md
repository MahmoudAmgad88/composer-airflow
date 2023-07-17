# ML Pipeline Using Airflow In GCP Composer

We will try to set Airflow in Google Cloud Platform Environment using Google Composer [Google Cloud Composer](https://cloud.google.com/composer/docs/composer-2/run-apache-airflow-dag) . It's actually a very powerfull tools to use so that all we need to do is choose the image we want to use in the google composer. 

### Requirements<br>
- First thing to do is to create Google Cloud Platform Account. Usually This is completely free. Even you got $300 USD balance to be ised in 90 days for the sake of learning in GCP Environment<br>

### Installation<br>
#### Cloud Composer 1 Guides:

[Installation Steps](https://cloud.google.com/composer/docs/run-apache-airflow-dag)

#### Cloud Composer 2 Guides:

[Installation Steps](https://cloud.google.com/composer/docs/composer-2/run-apache-airflow-dag)

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

  - to create Environment choose Cloud Composer [Cloud Composer versioning overview](https://cloud.google.com/composer/docs/concepts/versioning/composer-versioning-overview?_ga=2.232311903.-1169484772.1688163477&_gac=1.13708869.1688373034.CjwKCAjw44mlBhAQEiwAqP3eVvySMkBOtNCW3J95t3qkeogI31rm7rpXKIjN2dzSdu3Wfx8SBLH_rxoC9dcQAvD_BwE) and for Environment creation you can use [this guide](https://cloud.google.com/composer/docs/composer-2/create-environments)
  - After choosing Cloud Composer 2 then choose Environment name and select you service account which we are creted before then we will kepp all configuration as default then press create.
    
![image](https://github.com/MahmoudAmgad88/composer-airflow/assets/54455617/5d719511-d612-42a3-b84a-10b84b2491c3)


## Environment architecture:<br>
[Environment architecture.](https://cloud.google.com/static/composer/docs/images/composer-2-public-ip-architecture.svg)

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

### Clean up:

![image](https://github.com/MahmoudAmgad88/composer-airflow/assets/54455617/c4429440-6152-414a-ab5f-869b1a92c7b6)

#### Code task_1 Comments :<br>
```
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta

default_args = {
    'start_date': airflow.utils.dates.days_ago(0), #Sets the start date for the DAG to the current date and time.
    'retries': 1, #Sets the number of retries for failed tasks to 1
    'retry_delay': timedelta(minutes=5) #Sets the delay between retries for failed tasks to 5 minutes.
}

dag = DAG(
    'db_backup',
    default_args=default_args,
    description='db salakawy dag',
    schedule_interval='*/10 * * * *', #This specifies the schedule interval for the DAG(cron syntax). In this case, the DAG is scheduled to run every 10 minutes.
    max_active_runs=2,
    catchup=False, #meaning it will only run based on the schedule interval going forward.
                   #(avoid running old non-triggered diagrams between the start and current data )
    dagrun_timeout=timedelta(minutes=10) #Sets the timeout for each individual DAG run to 10 minutes.

stopvm = BashOperator(
    task_id='stopvm',
    bash_command='gcloud compute instances stop database --project=airflow-composer-392913 --zone=us-west4-b',
    dag=dag,
    depends_on_past=False,
    do_xcom_push=False)

create_image = BashOperator(
    task_id='create_image',
    bash_command='gcloud compute machine-images create databaseimage --source-instance=database --project=airflow-composer-392913 --source-instance-zone=us-west4-b',
    dag=dag,
    depends_on_past=False,
    do_xcom_push=False)


startvm = BashOperator(
    task_id='startvm',
    bash_command='gcloud compute instances start database --project=airflow-composer-392913 --zone=us-west4-b',
    dag=dag,
    depends_on_past=False,
    trigger_rule='one_success',
    do_xcom_push=False)

create_snapshot = BashOperator(
    task_id='create_snapshot',
    bash_command='gcloud compute snapshots create databasesnapshot --source-disk=database --project=airflow-composer-392913 --source-disk-zone=us-west4-b',
    dag=dag,
    trigger_rule='one_failed',
    depends_on_past=False,
    do_xcom_push=False)

#DAG Dependencies
stopvm >> create_image >> startvm
create_image >> create_snapshot
create_snapshot >> startvm
```

#### Code task_1 Comments :<br>
```
from airflow import DAG
from airflow.operators.python import PythonOperator #PythonOperator is an operator that executes a Python callable as a task in the DAG.
from datetime import datetime
from Preproces import importing
from Preproces import cleaning
from Preproces import transforming
from Preproces import AddingExternalData


with DAG("dag1", start_date = datetime(2023, 1, 4), #The DAG is scheduled to run daily starting January 4, 2023 
	schedule_interval="@daily", catchup=False) as dag: #  catchup set to False (meaning it won't backfill past DAG runs).

# Within the DAG context, tasks are defined using PythonOperator.
#Each task is assigned a unique task_id and a python_callable which is a Python function that will be executed as the task.

    import_csv_1= PythonOperator(
        task_id = 'importing',
        python_callable = importing,
        do_xcom_push=True,
    )
    clean_csv_1= PythonOperator(
        task_id = 'clean',
        python_callable = cleaning,
    )

    transform_csv_1= PythonOperator(
        task_id = 'transforming',
        python_callable = transforming,
    )

    externalData_csv_1= PythonOperator(
        task_id = 'AddingExternalData',
        python_callable = AddingExternalData,
        op_kwargs={
            "filename": "/opt/airflow/data/dft-road-casualty-statistics-vehicle-last-5-years.csv"
        },
    )


# The tasks are executed sequentially based on their dependencies
    import_csv_1 >> clean_csv_1 >> transform_csv_1 >> externalData_csv_1
```
 ### For further improvement :<br>
- I need to call python code from github repo then deolpy it automaticlly after every changes in repo.
- neeed to deply Airflow with MLflow
- Need to build a full automated Pipeline using Airflow , MLflow and github
- Explore more about full automated Pipeline

![WhatsApp Image 2023-07-16 at 8 56 54 PM](https://github.com/MahmoudAmgad88/composer-airflow/assets/54455617/87c2b2b7-47bc-4e0a-8965-6eb7a0596730)


### some useful command may be needed in GCE:
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


### GKE
```
gcloud config set project my-kubernetes-project-304910
gcloud container clusters get-credentials my-cluster --zone us-central1-c --project my-kubernetes-project-304910
kubectl create deployment hello-world-rest-api --image=in28min/hello-world-rest-api:0.0.1.RELEASE
kubectl get deployment
kubectl expose deployment hello-world-rest-api --type=LoadBalancer --port=8080
kubectl get services
kubectl get services --watch
curl 35.184.204.214:8080/hello-world
kubectl scale deployment hello-world-rest-api --replicas=3
gcloud container clusters resize my-cluster --node-pool default-pool --num-nodes=2 --zone=us-central1-c
kubectl autoscale deployment hello-world-rest-api --max=4 --cpu-percent=70
kubectl get hpa
kubectl create configmap hello-world-config --from-literal=RDS_DB_NAME=todos
kubectl get configmap
kubectl describe configmap hello-world-config
kubectl create secret generic hello-world-secrets-1 --from-literal=RDS_PASSWORD=dummytodos
kubectl get secret
kubectl describe secret hello-world-secrets-1
kubectl apply -f deployment.yaml
gcloud container node-pools list --zone=us-central1-c --cluster=my-cluster
kubectl get pods -o wide
 
kubectl set image deployment hello-world-rest-api hello-world-rest-api=in28min/hello-world-rest-api:0.0.2.RELEASE
kubectl get services
kubectl get replicasets
kubectl get pods
kubectl delete pod hello-world-rest-api-58dc9d7fcc-8pv7r
 
kubectl scale deployment hello-world-rest-api --replicas=1
kubectl get replicasets
gcloud projects list
 
kubectl delete service hello-world-rest-api
kubectl delete deployment hello-world-rest-api
gcloud container clusters delete my-cluster --zone us-central1-c
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
### Google Cloud Composer and Docker Compose:
both tools used for managing and orchestrating containerized applications, but they have some key differences:

Platform: Google Cloud Composer is a fully managed service provided by Google Cloud Platform (GCP) for running Apache Airflow. It is a cloud-based solution that handles infrastructure management, scalability, and maintenance. Docker Compose, on the other hand, is a local development tool that runs on your local machine or on-premises servers. It is primarily used for orchestrating containers in a local development or testing environment.

Infrastructure: With Google Cloud Composer, the underlying infrastructure is managed by Google Cloud Platform. You don't have to worry about provisioning servers, managing network configurations, or scaling resources. Docker Compose requires you to have Docker installed on your local machine or server and manages the containers on that specific host.

Scalability: Google Cloud Composer provides automatic scaling capabilities. It can handle scaling based on the workload and the number of tasks being executed. Docker Compose, being a local development tool, doesn't provide built-in scalability features. It is primarily focused on managing containers on a single host.

Integration with Google Cloud Platform: Google Cloud Composer seamlessly integrates with other Google Cloud services, such as Cloud Storage, BigQuery, Pub/Sub, and more. It provides built-in connectors and operators for interacting with these services. Docker Compose is not directly integrated with any cloud platform but can be used with other tools or services for cloud deployments.

Environment Management: Google Cloud Composer manages the underlying environment and dependencies for running Apache Airflow. It provides a web-based interface for managing DAGs, scheduling, and monitoring tasks. Docker Compose allows you to define and manage multi-container applications using a declarative YAML file. It focuses on orchestrating the containers defined in the docker-compose.yaml file.

Overall, Google Cloud Composer is a more comprehensive solution for running and managing Apache Airflow workflows in a cloud environment, while Docker Compose is suitable for local development and testing of containerized applications. The choice between them depends on your specific requirements, infrastructure, and deployment needs.

### Advantages of Airflow 
- Can handle upstream/downstream dependencies gracefully (Example: upstream missing tables)
- Easy to reprocess historical jobs by date, or re-run for specific intervals
- Jobs can pass parameters to other jobs downstream
- Handle errors and failures gracefully. Automatically retry when a task fails.
- Ease of deployment of workflow changes (continuous integration)
- Integrations with a lot of infrastructure (Hive, Presto, Druid, AWS, Google cloud, etc)
- Data sensors to trigger a DAG when data arrives
- Job testing through airflow itself
- Accessibility of log files and other meta-data through the web GUI
- Implement trigger rules for tasks
- Monitoring all jobs status in real time + Email alerts
- Community support

### Advantages of using Airflow in (GCP) VS local installation: 

Managed Service: GCP offers Cloud Composer, a managed service for Apache Airflow. With Cloud Composer, you don't need to worry about managing the infrastructure, installing dependencies, or scaling the environment. Google takes care of the underlying infrastructure, ensuring high availability and reliability.

Scalability: Cloud Composer allows you to easily scale your Airflow environment. You can increase the number of workers or adjust the machine types based on your workload requirements. GCP handles the scaling automatically, allowing your workflows to handle larger workloads efficiently.

Integration with GCP Services: Airflow in GCP integrates seamlessly with various GCP services. You can use GCP-specific operators and hooks to interact with services like BigQuery, Cloud Storage, Pub/Sub, Dataflow, and more. This integration simplifies the development of workflows that leverage GCP's powerful ecosystem of services.

Cloud Storage and Logging: Cloud Composer uses Cloud Storage as the default storage for storing DAGs, logs, and other artifacts. It provides reliable storage and versioning of your DAGs, making it easy to manage and collaborate on workflows. Additionally, the logs generated by Airflow tasks are automatically collected and stored in Cloud Logging, allowing for centralized monitoring and troubleshooting.

Security and Access Control: GCP offers robust security features and access control mechanisms. With Cloud Composer, you can leverage GCP's Identity and Access Management (IAM) to manage access to your Airflow environment and its resources. You can define granular permissions for users and service accounts, ensuring secure access to sensitive data and operations.

Monitoring and Alerting: GCP provides monitoring and alerting capabilities through Cloud Monitoring. You can set up monitoring dashboards, create custom metrics, and configure alerts based on specific thresholds or conditions. This allows you to monitor the health and performance of your Airflow environment and take proactive actions when necessary.

Seamless Integration with other GCP Services: Airflow in GCP integrates well with other GCP services like Cloud Scheduler, Cloud Pub/Sub, Cloud Functions, and Cloud Run. This enables you to build end-to-end data pipelines and trigger workflows based on events or schedules using native GCP services.

Overall, using Airflow in GCP provides a managed and scalable environment with seamless integration with GCP services, enhanced security, centralized logging and monitoring, and easier collaboration and management of workflows. These advantages make GCP an attractive choice for running Airflow and managing complex data workflows in a cloud-native environment.




Thankyou and Happy Coding
