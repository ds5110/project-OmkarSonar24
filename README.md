## DS5110 Project -
### Project Group Members -
Akash Dhande, Omkar Sonar(Team Lead), Rama Krishna Chavali, Jermine German
### OHDSI Pharmetrics+ Dataset based EDA - 
- Stakeholder : Rob Cavanaugh, PhD -- Roux Institute
- Story : Care for Stroke Survivors

    - Every 40 seconds, someone in the United States has a stroke, with 1 in 6 resulting in death and 800,000 new strokes every year. Stroke-related costs (e.g., cost of healthcare services, missed work, disability) in the US exceed 55 billion dollars every year, and stroke is the leading cause of long-term disability, and often results in life-altering deficits in mobility, cognition, independence in daily activities, and communication.
    - Stroke survivors (about 85% of strokes) receive rehabilitation services (physical therapy, occupational therapy, and speech-language therapy) along a continuum of care in the year following their stroke, which may include care provided in the acute inpatient hospital, inpatient rehabilitation facilities, skilled nursing facilities, long-term acute care hospitals, home health services, and outpatient care. However, transitions between these levels of care has consistently been identified as an obstacle to quality stroke rehabilitation and optimizing stroke outcomes. One critical missing piece of information in improving care transitions is to better understand the pathways stroke survivors take across these levels of care.
    - The goal of this long-term project is to better understand patterns in care transitions using a large commercial health insurance claims database (called IQVIA Pharmetrics+). This goal could be achieved by visualizing different patterns of journeys across care pathways, using machine learning to identify different groups of stroke survivors who receive care in different ways, and/or evaluating what factors are associated with different progressions across the continuum of care.
    - I am interested in understanding both where stroke survivors receive care (e.g, inpatient rehabilitation, skilled nursing facilities) and what care is received (how often do stroke survivors see certain physician specialists like neurologists, physical medicine and rehabilitation doctors, cardiologists) and rehabilitation providers (physical therapists, occupational therapists, and speech-language pathologists).

## Solutions and EDA performed have been noted as follows - 
1. [EDA Document](Markdown_files/eda.md)

### Reproducibility - 
Note: Since the OHDSI Pharmetrics+ dataset is not accessible from any local machine, it enforces the use of a Amazon Workspace instance, where in you can use `make` commands as mentioned below to save and show the plots mentioned in the above eda document. Further instructions to generate the figures individually have been provided in the EDA document itself.

```
make all
```
