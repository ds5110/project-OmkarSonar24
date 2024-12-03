# DB Setup

To ensure reproducibility , we creted an SQLite Local Database.

Below are the steps by which we were able to do it.

## Steps :

* Create an SQLite database called mydb.db in the desired folder.

<img src= "DB\DB_related_images\db_creation_step_1.png">

* Now navigate to [OHDSI's Eunomia Datasets github repository](https://github.com/ohdsi/EunomiaDatasets). It give us access to synthetic data that can be used to test out code.

<img src= "DB\DB_related_images\db_creation_step_2.png">

* Under the datasets folder , navigate to Synthea27Nj folder which contains a .zip file of all the .csv files. These .csv files are the schemas with prepopulated data inside them.

<img src="DB\DB_related_images\db_creation_step_3.png">

* Download the .zip file. 

<img src="DB\DB_related_images\db_creation_step_4.png">

* Exctract the .zip file and it will contain a folder that has all the csv files. Use the code at [dbsetup.py](DB\dbsetup.py) by providing the path of this folder and the path to the db.

* Run the above code and data along with schema will be populated inside the Database.

<img src= "DB\DB_related_images\db_creation_step_5.png">

* Use this video to understand this step : [DB Setup Video](DB/DB_setup_video/DB_setup_1.mp4)

* We can use these tables we just created to test our codes. 

* Aditionally , if we use tables such as "concept_ancestor" for instance , since it doesn't havve data in it , it will be a proble. To solve such issue follow the below steps.


# Additional Steps : 
### Necessary if you are using a table that doesn't have data.

* Navigate to [Athena's website](https://athena.ohdsi.org/search-terms/start) and register by providing details.

* Now under download section , check box everything and click on download vocabularies.

<img src= "DB\DB_related_images\db_creation_step_6.png">

* Now name the bundle as anything you want , and scroll to the bottom and click on download.

<img src= "DB\DB_related_images\db_creation_step_7.png">

* Click on download.

<img src= "DB\DB_related_images\db_creation_step_8.png">

* Now wait for a while and your .zip file will be packaged and sent to the mail you used to register. 

* Unzip it and use the required csv files by replacing them with the ones we saw before.

* Use this video to understand this step : [DB Setup Video](DB/DB_setup_video/DB_setup.mp4)


* Note : The data that you will get from athena will be huge , so if everything is not necessary , trim it down based on your requirement.


