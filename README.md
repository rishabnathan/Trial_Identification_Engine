## README

### Assumptions

In building this Trial Identfication Engine, I made a few assumptions about the data that will be presented in a _clinical\_trial.csv_ and a _patient\_feed.csv_ file.
- The .csv files that are input to this program have the same format as the given _clinical\_trial.csv_ and _patient\_feed.csv_, meaning the same column names (spelling, capitalization, and format including underscores) are given in the .csv files.
- A clinical trial will only have 1 _anatomic\_site_
- A patient will only have 1 _diagnosis_ (no delimiters)
- The _age\_requirement_ field will always be presented as [symbol][number] (Clarified in a question to Matt Smith)
- There exists a match between the _diagnoses_ field in _clinical\_trial.csv_ and _diagnosis_ field in _patient\_feed.csv_ as long as one of the words in the _diagnosis_ field matches with the diagnoses presented in _clinical\_trial.csv_. (Ex. carcinoma matches with Pseudosarcomatous carcinoma)
- As long as the _anatomic\_site_ presented in the _clinical\_trial.csv_ is present in the _anatomic\_site_ of the _patient\_feed.csv_, then there is a match between those fields. (Ex. 'lung' matches with 'lower lobe of right lung')

### Requirements to Run

The requirements for this Trial Identification Engine are to have the latest version of [Python](https://www.python.org/downloads/) installed.

Another requirement for this Trial Identification Engine is to have Python Pandas installed. This can be done using the following command:
```
pip install pandas
```

### Instructions to Run

The Trial Identification Engine can be run by performing the following command in a terminal session from the project top level directory:
```
python3 main.py </path/to/clinical_trial_file> </path/to/patient_feed_file> <txt_file_for_output_log>
```

### Instructions to Run Tests

The test.py file can be run by running the following command in a terminal session from the project top level directory:
```
python -m unittest discover -s tests
```

** Note: This was developed on a Mac, and is compressed using the Mac compress feature. To unzip the .zip file in windows, use WinZip.