we have various txt/pdf documents under /workspaces/data_science_classes_windows/winter2025/dsc650_big_data that show big data tools using docker. this shows various uses of the tools and commands run. 


considering the previous steps run in previous weeks and the week11 readme, draft a markdown that shows a walkthrough from setup to completion of all tasks. the walkthrough should have commands to execute as well as indications such as "take a screenshot here". I should be able to follow the pdf step by step and deliver the complete report for the final project. make sure you meet all requirements for the readme


Assignment Materials



Download the Week 11 Final Project assignment document and follow all instructions carefully.

This is your capstone project. You will design and implement a full data pipeline that integrates at least four major components from the big data ecosystem (NiFi, HDFS, Hive, HBase, Spark). Your pipeline must demonstrate end-to-end data flow, processing, and analysis using a dataset of your choice.

Be sure to complete all required deliverables listed in the assignment document. You may not reuse datasets provided earlier in the course.

Week 11 Final Project – Objectives and Points (660 pts)

Objective 1 – NiFi Data Ingestion into HDFS (220 pts)
Use NiFi to load your dataset into HDFS. Show the NiFi flow, successful run, and data written into HDFS.
Objective 2 – Hive Managed Table (100 pts)
Take the data in HDFS and create a Hive managed table. Show the CREATE TABLE statement, data load, and at least one query returning results.
Objective 3 – Environment Setup (40 pts)
Install required libraries on worker and master nodes. Start the HBase Thrift server. Provide screenshots verifying installs and startup.
Objective 4 – HBase Table Creation (40 pts)
Create an HBase table for storing metrics. Provide the CREATE statement and a scan showing the empty table before Spark writes data.
Objective 5 – PySpark ML Code (220 pts)
Submit your working PySpark ML code developed in VS Code (or another IDE). The code must use Spark MLlib with an algorithm of your choice, applied to your dataset.
Objective 6 – Spark Submit & Output (20 pts)
Submit your PySpark ML job to YARN using spark-submit. Provide the command, logs, and output demonstrating successful execution.
Objective 7 – HBase Scan Verification (20 pts)
After Spark runs, scan your HBase table to show that metrics were successfully written. Provide a screenshot of the populated table.
Total: 660 points



Important Warning



 You may NOT use the grades.csv dataset from the  example walkthrough provided for the project. Doing so will result in an automatic 0 for the project.

For the final project, you must:

Use your own dataset, not one provided in earlier assignments.
Load that dataset into HDFS using NiFi as the first step of your pipeline.
Failure to follow this requirement will cause your project to be given a grade of 0.






Submission Guidelines



Submit a single, comprehensive report (Word or PDF).
Your submission must include:
A detailed write-up of what you attempted, what worked, and what did not.
A discussion of challenges and issues encountered.
The GitHub direct URL for your dataset.
Screenshots showing successful execution at each stage (NiFi, HDFS, Hive, Spark, HBase).
The full code used (NiFi templates, PySpark scripts, Hive queries, etc.).
A well-structured format with labeled sections:
Introduction
Dataset
Pipeline Overview
Issues Encountered
Screenshots
Code
Conclusion
Submit as a single file or archive. Do not upload multiple raw screenshots.
Assignments are due Sunday, 11:59 p.m. CT.