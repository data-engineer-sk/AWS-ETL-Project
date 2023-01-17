# ETL Pipeline via AWS (S3/Lambda/Redshift/Grafana Services)

<html>
<head></head>
<body data-gr-ext-installed="" data-new-gr-c-s-check-loaded="14.1087.0">
<h1><span style="color:#008000;">README.md</span></h1>
<img src="https://github.com/data-engineer-sk/AWS-ETL-Project/blob/main/ETL%20Pipeline%20via%20AWS.png" ALIGN=”left” alt="ETL Processing via Nasdaq API" />
</body>
</html>
  
<h2><span style="color:#008000;">Project Aims</span></h2>
<p>
 Simulate a ETL pipeline process to collect data for data analysis.  By using the API from Nasdaq.com, extract the histical stocks data, consumer price index, and the  market capacity for further analysis.
 <ul>
  <li>APPLE Inc.</li>
  <li>VISA</li>
  <li>COST</li>
  <li>MASTER CARD</li>
</ul>
</p>
<h2><span style="color:#008000;">How it works</span></h2>
<p>Write a CLI program with python.  Use the API function call provided by Nasdaq.com to extract csv file.  Use packages such as  pandas / numpy to transform the data complie with the user requirement.  Store the results to the PostgreSQL / MysQL Server which act as a data warehouse (Can be stored to RDS in AWS or local machine).  Use SQL to furthur transform the data into a new data table (**Perform unit test to ensure the data are clearn to use in future.
</p>
<h2><span style="color:#008000;">System Requirement</span></h2>
<p>This system requires the following setting:
  <li>Python 3.10 or above</li>
  <li>Nasdaq API (Click <a href="https://data.nasdaq.com/tools/api">here</a> link to the website)
  <li>PostgreSQL / MySQL</li>
  <Li>Tableau Public (for data visualization)</li>
  <li>Any program editor (e.g. Pycharm / VS Code)</li>  
</p>

