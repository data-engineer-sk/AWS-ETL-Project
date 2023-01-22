# README.md 
## ETL Pipeline via AWS (S3/Lambda/Redshift/Grafana Services)
> Data Engineer Student Project about for a client café business (at Generation & Ireland UK)

<html>
<head></head>
<body data-gr-ext-installed="" data-new-gr-c-s-check-loaded="14.1087.0">
<h1><span style="color:#008000;"></span></h1>
<img src="https://github.com/data-engineer-sk/AWS-ETL-Project/blob/main/My%20ETL%20Process%20via%20AWS.png" ALIGN=”left” alt="ETL Processing on AWS" />
</body>
</html>

## BACKGROUND
The project provides service to our client who run his café business in various branches in UK.  However, the café has seen unprecedented growth and has expanded to hundreds of outlets across the country.  Due to the demand the company is receiving, they need to figure out how they can best target new and returning customers, and also understand which products are selling well.  They are experiencing issues with collating and analysing the data they are producing at each branch, as their technical setup is limited.  I am now to be requested to step in and provide consultation on what they need to do in order to grow their technical offerings, so that they can continue to accelerate their growth.

## PROBLEMS
The company currently has no way of identifying trends, meaning they are potentially losing out on major revenue streams.  They are in desperate need of help putting together a platform that will allow them to easily understand all of the data they are producing.  Due to the highly professional work you completed for them in the past, they are keen to work alongside your project in creating a solution to solve the problem their problems.

## REQUIREMENT
Every day, each branch has to prepare a CSV file containing data about every transaction they made for that day is generated.  At 8pm, the data is uploaded to a piece of software installed in the back office computers.  Daily, weekly or monthly reports for sales figures and other related business metrics are created.

## SKILLS AND TECHNOLOGIES REQUIRED
In this project, the following data engineering techs will be applied in order to successfully build the pipeline. Namely:
• Python
• ETL Techniques
• DataWarehousing
• DataAnalytics/Visualisations/BusinessIntelligence 
• Development Operations(DevOps tech such as unix scripting to prepare the cloudformation)
• AWS Services such as S3, EC2, Lambda, Redshift, and Cloudwatch
• Grafana for application monitoring
• GitHub for source control

#### 1. Extracting Data from CSV
Our client has given us an example CSV file for the type of data we will be dealing with. As part of the Point of conception stage we have used this file to create our Extract stage of the pipeline. Python pandas library was used to extract data from csv in dataframe format. 

#### 2. Transforming Data
Transformation of data was done using pandas to remove sensitive information that includes customer name and credit card.

#### 3. Normalizing Data
Below describe the area that we will normalize our data:
1. Convert the timestamp data type column to data time column data type
2. Remove the sensitive data (e.g. Customer name and Card Numbers)
3. Creating the header for the data sets
4. Creating a new index in the data sets
5. Split the large single colume in to multiple columns (e.g. Basket Items (Name, Size & Price) column into Busket items, item name, item size and item price, etc)
6. Clean the data in splited column (e.g. Remove the empty space, repeating data and '\n', etc)

#### 4. Loading Data to PostgreSQL Database
Transformed and normalized data was loaded to PostgreSQL using python library posq2 for database connection. Designed schema was implemented to model our data.

<img width="632" alt="Screenshot 2022-12-11 at 16 41 56" src="https://user-images.githubusercontent.com/78314396/213438420-0c854b75-5800-42e5-8c8c-9d349b41b68e.png">
<img width="910" alt="Screenshot 2022-12-11 at 16 43 39" src="https://user-images.githubusercontent.com/78314396/213438436-f0991a93-f1c5-4112-9150-02e920d0334f.png">

#### 5. Seting up CloudFormation
Prepare a CloudFormation Templates for lambda function, s3 bucket permission and notification was created using a .yaml file. Templates was loaded into a s3 bucket and a stack was created and updated using a shell scripting file. 

#### 6. ETL lambda and S3 Bucket
The client will be droping their csv file every evening into the s3 bucket. The Lambda has been triggered with the s3 bucket such that it can run the ETL code when a file lands the s3 bucket i.e. The Extract and Transformation processing on the data.  The Transformation will remove all the sensitive data and convert the data into the appropriated format for later use (in data visulatision to help the business's decision making).  After finishing the extract and transform processes, the consolidated file for all the branches will be stored back in to the S3 bucket for load processing to the AWS Redshift data warehouse.

#### 7. Modify Lambda to load data into Redshift
A separate lambda has been created to load the transformed data into the redshift data warehouse

#### 8. Grafana Setup for AWS Infrastruction and Data Sources
For Setup, an EC2 instance was created with a grafana i am role to be able to give access to grafana. The SSH key was used for connecting to the local host. Redshift and CloudWatch was connected to grafana as data source for easy monitoring. EC2, Lambda Invocations and Redshift was monitored.

#### 9. Visualization of Sales Data for Business Insights
The client wants to see a visualisation of products sold, they want to know:
- Volume (# products sold per time period)
- Volume (# products sold per branch)
- Revenue (per branch, per timescale

The grafana was able to monitor the lambda invocations using cloudwatch as data source:
<img width="1423" alt="Screenshot 2023-01-18 at 11 19 46" src="https://user-images.githubusercontent.com/78314396/213655299-9b9bb7b4-d152-4ac0-8cd5-bf29704e0685.png">

The Redshift Integrated chart has been used to visualize the data to get this findings:
![Total Spend](https://user-images.githubusercontent.com/78314396/213444252-8bffe39b-1444-4265-a8e4-538938d5e881.jpeg)
![Average Spend](https://user-images.githubusercontent.com/78314396/213444720-31339f07-46f6-47e7-b727-289f6d0d3040.jpeg)
![Quantity of Item All Stores](https://user-images.githubusercontent.com/78314396/213444756-5bb9c8aa-e4d0-456b-a0f5-431a12d1d3d7.jpeg)
