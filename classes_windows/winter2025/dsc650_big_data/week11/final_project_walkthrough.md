# DSC650 Week 11 Final Project Walkthrough (Setup to Submission)

This walkthrough is designed to be followed step-by-step to complete all Week 11 objectives and produce a single final report that meets the `readme.MD` requirements.

It is based on your Week 11 materials:
- `week11/readme.MD`
- `week11/week11-final-project.docx`
- `week11/HDFS_Hive_Spark_HBase_Pipeline.docx`
- `week11/Final_Project.json` (NiFi template)
- previous-week command patterns in `commands.md` and Weeks 3/4/6 workflow

## Non-Negotiable Rules

1. Do **not** use `grades.csv` or any course-provided sample dataset.
2. Use your **own dataset** hosted on GitHub.
3. Use the **direct raw GitHub URL** in NiFi `InvokeHTTP`.
4. Use the required pipeline components: `NiFi -> HDFS -> Hive -> Spark (MLlib on YARN) -> HBase`.
5. After NiFi data load, **stop NiFi** to conserve VM resources.
6. Submit one comprehensive report (Word/PDF), not raw screenshots only.

---

## 0. Folder and Variable Setup

Run these on your VM host shell.

```bash
# adjust if your repo path differs
cd ~/dsc650-infra/bellevue-bigdata/hadoop-hive-spark-hbase

# set project-specific variables
export DATASET_RAW_URL="https://raw.githubusercontent.com/gabriel-joseph/bigdata/main/noshowappointments.csv"
export DATASET_FILENAME="noshowappointments.csv"
export HDFS_DIR="/tmp"
export HIVE_DB="final_project"
export HIVE_TABLE="noshowappointments"
export HBASE_TABLE="project_metrics"
```

Use the raw GitHub URL above in NiFi, not the GitHub `blob` page URL.

Validate URL before using it in NiFi:

```bash
curl -I "$DATASET_RAW_URL"
curl -L "$DATASET_RAW_URL" | head -n 5
```

**Take screenshot here:** dataset URL and first lines shown in terminal.

---

## 1. Start Infrastructure and Connect (Objective 1 prerequisite)

### 1.1 Start containers

```bash
cd ~/dsc650-infra/bellevue-bigdata/hadoop-hive-spark-hbase
docker compose up -d
# if your environment uses legacy command:
# docker-compose up -d
```

### 1.2 Optional SSH tunnel (if working from local laptop)

```bash
ssh -L 9870:localhost:9870 \
    -L 8088:localhost:8088 \
    -L 8080:localhost:8080 \
    -L 18080:localhost:18080 \
    -L 16010:localhost:16010 \
    -L 8983:localhost:8983 \
    -L 8443:localhost:8443 \
    <your-user>@<your-vm-ip>
```

### 1.3 Verify service UIs

- HDFS: `http://localhost:9870/dfshealth.html#tab-overview`
- Spark UI: `http://localhost:8080/`
- Spark History: `http://localhost:18080/`
- YARN: `http://localhost:8088/`
- HBase Master: `http://localhost:16010/master-status`
- NiFi: `https://localhost:8443/nifi/`

**Take screenshot here:** all containers up and at least HDFS + NiFi UI reachable.

---

## 2. NiFi -> HDFS Ingestion (Objective 1)

Use the required template `week11/Final_Project.json`.

### 2.1 Import the NiFi template/flow

In NiFi UI:
1. Import/upload `Final_Project.json`.
2. Open the imported process group `Final_Project`.
3. Confirm processors exist:
   - `Download File` (`InvokeHTTP`)
   - `Update File Name` (`UpdateAttribute`)
   - `Write File to HDFS` (`PutHDFS`)

### 2.2 Create/assign Parameter Context values

In parameter context `Final Project`, set:
- `DOWNLOAD FILE URL` = `$DATASET_RAW_URL`
- `FILENAME` = `$DATASET_FILENAME`
- `HDFS WRITE DIRECTORY` = `$HDFS_DIR`
- `USER` = output of:

```bash
whoami
```

### 2.3 Validate processor properties

- `Download File` (`InvokeHTTP`): `Remote URL = #{DOWNLOAD FILE URL}`
- `Update File Name`: `filename = #{FILENAME}`
- `Write File to HDFS`:
  - `Hadoop Configuration Resources = /home/#{USER}/dsc650-infra/bellevue-bigdata/nifi/hadoopconf/core-site.xml`
  - `Directory = #{HDFS WRITE DIRECTORY}`

### 2.4 Run flow

- Run `Download File` once, then start full flow.
- Wait for successful transfer and queue activity.

**Take screenshot here (Required):**
1. NiFi flow design with all processors.
2. Flow running with data visible in queues/provenance.

### 2.5 Verify file landed in HDFS

```bash
docker-compose exec master bash
hdfs dfs -ls "$HDFS_DIR"
hdfs dfs -cat "$HDFS_DIR/$DATASET_FILENAME" | head -n 5
exit
```

**Take screenshot here (Required):** `hdfs dfs -ls` showing ingested file.

### 2.6 Stop NiFi after load (resource requirement)

Use one of these methods:

```bash
# preferred if nifi is its own service
docker compose stop nifi

# or from NiFi bin (if you run it directly)
# cd nifi-1.25.0/bin
# ./nifi.sh stop
```

**Take screenshot here:** NiFi stopped confirmation.

---

## 3. Hive Managed Table (Objective 2)

### 3.1 Enter master and Hive shell

```bash
docker-compose exec master bash
hive
```

### 3.2 Create database and managed table

Use this Hive-safe schema for `noshowappointments.csv`:

```sql
CREATE DATABASE IF NOT EXISTS final_project;
USE final_project;

CREATE TABLE IF NOT EXISTS noshowappointments (
    patient_id STRING,
    appointment_id STRING,
    gender STRING,
    scheduled_day STRING,
    appointment_day STRING,
    age INT,
    neighbourhood STRING,
    scholarship INT,
    hipertension INT,
    diabetes INT,
    alcoholism INT,
    handcap INT,
    sms_received INT,
    no_show STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ('skip.header.line.count'='1');
```

This schema keeps the ID columns as `STRING` so the default Spark feature-selection step does not treat them as numeric predictors.

### 3.3 Load CSV from HDFS into managed table

```sql
LOAD DATA INPATH '/tmp/noshowappointments.csv' OVERWRITE INTO TABLE noshowappointments;
```

### 3.4 Validate with required queries

```sql
SELECT COUNT(*) AS n_rows FROM noshowappointments;

-- include at least one aggregation query for objective requirement
SELECT neighbourhood, COUNT(*) AS cnt
FROM noshowappointments
GROUP BY neighbourhood
ORDER BY cnt DESC
LIMIT 20;

-- optional sample rows
SELECT * FROM noshowappointments LIMIT 10;
```

Exit Hive/master:

```sql
exit;
```

```bash
exit
```

**Take screenshot here (Required):**
1. `CREATE TABLE` statement
2. data loaded successfully
3. aggregation query output

---

## 4. Environment Setup + HBase Thrift (Objective 3)

Install required Python libs on workers and master.

```bash
cd ~/dsc650-infra/bellevue-bigdata/hadoop-hive-spark-hbase

# worker1
docker-compose exec worker1 bash -lc "pip3 install numpy happybase"

# worker2
docker-compose exec worker2 bash -lc "pip3 install numpy happybase"

# master
docker-compose exec master bash -lc "pip3 install numpy happybase"
```

Start HBase Thrift server on master:

```bash
docker-compose exec master bash
nohup hbase thrift start > /tmp/hbase-thrift.log 2>&1 &
ps -ef | grep -i "hbase thrift" | grep -v grep
exit
```

**Take screenshot here (Required):**
1. package installs on nodes
2. HBase Thrift running process/log confirmation

---

## 5. HBase Table Creation (Objective 4)

```bash
docker-compose exec master bash
hbase shell
```

Create table for metrics:

```hbase
create 'project_metrics', 'cf'
scan 'project_metrics'
```

You should see an empty result before Spark writes.

Exit:

```hbase
exit
```

```bash
exit
```

**Take screenshot here (Required):**
1. `create` command
2. empty `scan` result

Include in report:
- row key design (example: `run_<timestamp>`)
- column family design (`cf` for metrics)

---

## 6. PySpark MLlib Job (Objective 5)

Create your script locally (VS Code) and place it on master container path (per your Week 4 workflow).

Suggested filename: `sparkml_final.py`

### 6.1 Example script template for `noshowappointments.csv`

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, RegressionEvaluator
import happybase
import time

# ===== EDIT THESE =====
HIVE_DB = "final_project"
HIVE_TABLE = "noshowappointments"
TARGET_COL = "no_show"              # "No" / "Yes" appointment outcome
PROBLEM_TYPE = "classification"     # classification or regression
HBASE_TABLE = "project_metrics"
# ======================

spark = SparkSession.builder \
    .appName("FinalProjectML_to_HBase") \
    .enableHiveSupport() \
    .getOrCreate()

print("Spark App ID:", spark.sparkContext.applicationId)

full_table = f"{HIVE_DB}.{HIVE_TABLE}"
df = spark.sql(f"SELECT * FROM {full_table}").dropna()

# Keep numeric feature columns only
numeric_types = {"int", "bigint", "double", "float", "smallint", "tinyint", "decimal"}
feature_cols = [
    f.name for f in df.schema.fields
    if f.name != TARGET_COL and any(t in f.dataType.simpleString().lower() for t in numeric_types)
]

if not feature_cols:
    raise ValueError("No numeric feature columns found. Update schema or feature selection.")

if PROBLEM_TYPE == "classification":
    # convert label if needed
    label_type = [f.dataType.simpleString().lower() for f in df.schema.fields if f.name == TARGET_COL][0]
    if "string" in label_type:
        indexer = StringIndexer(inputCol=TARGET_COL, outputCol="label")
        df2 = indexer.fit(df).transform(df)
    else:
        df2 = df.withColumn("label", col(TARGET_COL).cast("double"))

    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features", handleInvalid="skip")
    ml_df = assembler.transform(df2).select("features", "label")

    train, test = ml_df.randomSplit([0.8, 0.2], seed=42)
    model = LogisticRegression(featuresCol="features", labelCol="label", maxIter=50)
    fitted = model.fit(train)
    pred = fitted.transform(test)

    acc_eval = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
    f1_eval = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="f1")

    metrics = {
        "accuracy": float(acc_eval.evaluate(pred)),
        "f1": float(f1_eval.evaluate(pred))
    }

else:
    df2 = df.withColumn("label", col(TARGET_COL).cast("double"))
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features", handleInvalid="skip")
    ml_df = assembler.transform(df2).select("features", "label")

    train, test = ml_df.randomSplit([0.8, 0.2], seed=42)
    model = LinearRegression(featuresCol="features", labelCol="label")
    fitted = model.fit(train)
    pred = fitted.transform(test)

    rmse_eval = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="rmse")
    r2_eval = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="r2")

    metrics = {
        "rmse": float(rmse_eval.evaluate(pred)),
        "r2": float(r2_eval.evaluate(pred))
    }

print("Model metrics:", metrics)

# Write metrics to HBase
run_key = f"run_{int(time.time())}"
rows = [(run_key, f"cf:{k}", str(v)) for k, v in metrics.items()]

def write_partition(partition):
    conn = happybase.Connection("master")
    conn.open()
    table = conn.table(HBASE_TABLE)
    for row_key, col_name, val in partition:
        table.put(row_key, {col_name: val})
    conn.close()

spark.sparkContext.parallelize(rows, 1).foreachPartition(write_partition)

spark.stop()
```

**Take screenshot here (Required):**
1. code open in VS Code/IDE
2. training/evaluation output (`accuracy/f1` or `rmse/r2`)

Also include GitHub link to your code in report.

---

## 7. Submit Spark Job to YARN + Logs (Objective 6)

From master container in directory containing `sparkml_final.py`:

```bash
spark-submit \
  --master yarn \
  --deploy-mode client \
  --name FinalProjectML_to_HBase \
  sparkml_final.py
```

Capture app id and logs:

```bash
# option 1: from spark-submit output (recommended)
# option 2: list applications
yarn application -list

# then fetch logs
yarn logs -applicationId <APP_ID> | tee spark_job_<APP_ID>.log
```

**Take screenshot here (Required):**
1. `spark-submit` command
2. YARN job logs and final output

---

## 8. Verify HBase Metrics Written (Objective 7)

```bash
docker-compose exec master bash
hbase shell
scan 'project_metrics'
```

You should see row(s) like `run_<timestamp>` with columns such as `cf:accuracy`, `cf:f1`, `cf:rmse`, or `cf:r2`.

**Take screenshot here (Required):** populated `scan` output.

---

## 9. Build the Final Report (Required `readme.MD` format)

Use these exact section labels:

1. `Introduction`
2. `Dataset`
3. `Pipeline Overview`
4. `Issues Encountered`
5. `Screenshots`
6. `Code`
7. `Conclusion`

### 9.1 What to include in each section

#### Introduction
- project objective
- end-to-end architecture (`NiFi -> HDFS -> Hive -> Spark/YARN -> HBase`)
- why this dataset/algorithm fits the task

#### Dataset
- GitHub direct raw URL
- dataset size, columns, target variable
- why dataset is unique (not course provided)

#### Pipeline Overview
- NiFi processor roles (`InvokeHTTP`, `UpdateAttribute`, `PutHDFS`)
- Hive schema choices and managed-table rationale
- Spark ML approach and algorithm justification
- HBase metric storage design (`run_<timestamp>`, `cf`)

#### Issues Encountered
- what worked
- what failed initially
- fixes applied (schema mismatch, memory, nulls, etc.)

#### Screenshots
Use numbered captions and map each to objective deliverables:
- Obj1: NiFi design + running queues + `hdfs dfs -ls`
- Obj2: `CREATE TABLE` + load + query result
- Obj3: installs + Thrift running
- Obj4: HBase create + empty scan
- Obj5: code + training + evaluation metric
- Obj6: spark-submit + YARN logs
- Obj7: populated HBase scan

#### Code
- NiFi template reference (`Final_Project.json`)
- Hive DDL/DML
- full PySpark script
- spark-submit command

#### Conclusion
- summarize pipeline success
- interpret model metrics
- confirm end-to-end validation via HBase metrics

---

## 10. Final Objective Checklist (Submission Gate)

- [ ] Obj1: NiFi flow + running queue + HDFS file proof
- [ ] Obj2: Hive managed table + load + aggregation query
- [ ] Obj3: libraries installed + HBase Thrift running
- [ ] Obj4: HBase table create + empty scan
- [ ] Obj5: full PySpark MLlib code + metrics screenshot + GitHub link
- [ ] Obj6: spark-submit command + logs/output screenshot
- [ ] Obj7: populated HBase scan screenshot
- [ ] Report has required sections and challenge discussion
- [ ] Report submitted as one single file (Word or PDF)

---

## 11. Quick Command Reference

```bash
# Start stack
docker compose up -d

# Master shell
docker-compose exec master bash

# HDFS check
hdfs dfs -ls /tmp

# Hive
hive

# HBase shell
hbase shell

# Start thrift
nohup hbase thrift start > /tmp/hbase-thrift.log 2>&1 &

# Spark submit
spark-submit --master yarn --deploy-mode client --name FinalProjectML_to_HBase sparkml_final.py

# YARN logs
yarn logs -applicationId <APP_ID>
```
