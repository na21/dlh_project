# UIUC CS598 DLH Final Project

## Introduction

This repository is a reproduction study for the research paper below:

_Sun, Mengying, Tang, Fengyi, Yi, Jinfeng, Wang, Fei, & Zhou, Jiayu. Identify Susceptible Locations in Medical Records via Adversarial Attacks on Deep Predictive Models. Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, ()._ https://doi.org/10.1145/3219819.3219909

Utilizes code and scripts from the following repositories:
* https://github.com/illidanlab/med-attack
* https://github.com/illidanlab/urgent-care-comparative
* https://github.com/MIT-LCP/mimic-code

More information may be found at:
* [**Presentation**]()
* [**Final Report**]()

## Authors

* Name: Nissan Azizov & Nivedita Chatterjee
* Email: {nazizov2, nc19}@illinois.edu

## Requirements
* Python 3.4+
    * NumPy
    * Pandas
    * Gensim
    * Scikit-Learn
    * Keras
    * Tensorflow
    * Progressbar2
* PostgreSQL
* [MIMIC-III Clinical Database](https://physionet.org/content/mimiciii/1.4/)

Install Python requirements
```
conda create -n env-name pip
conda activate env-name
pip install -r requirements.txt
```

## Setup

Apply for access to [MIMIC-III Clinical Database](https://physionet.org/content/mimiciii/1.4/) and download to the root of this repository in directory ```mimic-iii-clinical-database-1.4```
```
git clone https://github.com/MIT-LCP/mimic-code.git
git clone https://github.com/illidanlab/urgent-care-comparative.git
```

## Data Preprocessing

Create MIMIC-III in a local Postgres database (db: mimic, user: postgres, password: postgres). Requiries ~100GB
```
cd mimic-code/mimic-iii/buildmimic/postgres/
make help
make create-user mimic datadir="../../../../mimic-iii-clinical-database-1.4/"
```

Run rest of preprocessing and urgent-care-comparative code
```
cd ../../../../
mkdir -p local_mimic/{views, tables, save}
psql --u postgres --d mimic

\i mimic-code/mimic-iii/concepts/postgres-functions.sql
\i sql_scripts/pivoted_bg.sql
\i sql_scripts/pivoted_lab.sql
\i sql_scripts/pivoted_vital.sql
\i sql_scripts/icustay_detail.sql

\copy (SELECT * FROM pivoted_bg) to 'local_mimic/views/pivoted_bg.csv' delimiter ',' csv header;
\copy (SELECT * FROM pivoted_lab) to 'local_mimic/views/pivoted_lab.csv' delimiter ',' csv header;
\copy (SELECT * FROM pivoted_vital) to 'local_mimic/views/pivoted_vital.csv' delimiter ',' csv header;
\copy (SELECT * FROM icustay_detail) to 'local_mimic/views/icustay_detail.csv' delimiter ',' csv header;
exit

awk 'NR==1{ print tolower($0) }NR>1' mimic-iii-clinical-database-1.4/ADMISSIONS.csv > local_mimic/tables/admissions.csv
awk 'NR==1{ print tolower($0) }NR>1' mimic-iii-clinical-database-1.4/DIAGNOSES_ICD.csv > local_mimic/tables/diagnoses_icd.csv
awk 'NR==1{ print tolower($0) }NR>1' mimic-iii-clinical-database-1.4/D_ICD_DIAGNOSES.csv > local_mimic/tables/d_icd_diagnoses.csv

python urgent-care-comparative/preprocess.py --path_tables local_mimic/tables --path_views local_mimic/views --path_save local_mimic/save

python prep_files.py
```
