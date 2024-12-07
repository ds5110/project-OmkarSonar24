# A Comparative Study of Ischemic vs Hemorrhagic Stroke Patients' Treatment Pathways -
## Team and Stakeholders -
This project was a part of DS5110 - Introduction to Data Management and Processing, offered by Professor [Philip Bogden, PhD](https://roux.northeastern.edu/people/philip-bogden/). 
The project team consist of -
- Akash Dhande
- Omkar Sonar
- Rama Krishna Cavali
- Jermine German

Stakeholder - [Rob Cavanaugh, PhD](https://roux.northeastern.edu/people/rob-cavanaugh/) -- Roux Institute
## Primary Deliverables -
1. [README.md](README.md) - Provides instructions to reproduce the findings of this project, in Amazon Workspaces required for access to the OHDSI Pharmetrics+ Database.
2. [REPORT.md](REPORT.md) - Provides detailed information about the methods and insights achieved in this process.

## Dataset Used - 
The dataset used is the OHDSI Pharmetrics+ database which is a medical and pharmacy claims database consisting of 105,009,000 patients and their claims history. The data used for the scope of this project offered per patient includes information related to -
- Medical Conditions
- Treatment and Diagnosis services taken by the patient. 
- Visits to establishments related to treatments, diagnosis and emergency visits such as Hospitals, Clinics, Laboratories, etc.

The OHDSI Pharmetrics+ Database follows the [OMOP Common Data Model](https://www.ohdsi.org/data-standardization) as a design standard for structuring this large database.

## Reproducibily and Instructions -
The access to OHDSI Pharmetrics+ database is only possible through Amazon Workspaces. The user must have access to Amazon Workspaces to reproduce the following results on it.

### Step 1 Install Dependencies -
1. Install Git
2. Install Conda
3. Setup Conda environment
4. Install Make
### Step 2 Reproduce the EDA -
1. make eda
### Step 3 Reproduce the Findings -
1. make discharges
2. make demographics ...

## Resources -
-  [The Book of OHDSI](https://ohdsi.github.io/TheBookOfOhdsi/)
-  [OMOP CDM v5.4 Schema & Table Details](https://ohdsi.github.io/CommonDataModel/cdm54.html)
-  [OHDSI Forum](https://forums.ohdsi.org/)

## References - 
- [Aging and Ischemic Stroke](https://doi.org/10.18632/aging.101931)
- 