# Recs Scripts
This repository contains a collection of scripts that are used for performing ad-hoc data manipulations required to address some of the recurring issues with reviewers recommender infrastructure.

These scripts contain a lot of duplicate code in their current iteration, since the intention of this project was never to establish a framework, but to provide a quick solution to the issue as soon as possible.

Currently scripts are organised by folders named after reviewer recommender services/components that they interact with.

### Overview

**API/** collection of scripts which interact with reviewers recommender API

* **enable.py** 

	Reads lines from acronyms.txt file which can be populated with excel columns sent over by EM/Evise teams to enable new journal acronyms. Required you to specify dev or live cmd arguments to enable journals for expected environment.

* **apiVersions.py**

	Fetches a list of api and dataset versions from dynamodb to check whether our apis were deployed with correct datasets
	
	! Not applicable to reviewers recommender api !
* **rrSubmit.py**

	Resubmits manuscripts that were previously rejected due to disabled acronyms
	
**S3/** collection of scripts that download and upload data to recs-reviewers-recommender S3 buckets

* **reflow.py**

	Reflows submitted manuscripts from S3. **Deprecated**, since data pump now has a resubmit option
* **reflow_unmerged.py**

	Downloads deltas with unmerged author column (authors field which contains main and corresponding authors) and merges this column to allow data to be consumed by the data pipeline. Downloaded data is stored locally and uploaded via AWS CLI.

* **s3dl.py**


	Downloads a list of submitted manuscripts from s3
* **safeS3Upload.py**

	Uploads deltas from the local storage to s3, while ignoring upload of deltas listed in toKeep.txt file

**SNS/** collection of scripts that trigger different SNS topics in reviewer recommender lambda setup

* **del_test.py** 

	A script that submits a reviewer deletion request to data pump lambda in order to do an end-to-end test of the deletion lambda.
* **gdprRemove.py**

	Reads a csv file with with manuscripts flagged for GDPR removal and removes them from reviewer recommender S3 buckets by triggering the remove action of the data pump.
* **piplineDump.py**

	Reads Evise data dump, splits it into a specified number of deltas and submits to the data pump. Was used for load and performance testing while working on the data pump lambda.
* **resubmitPilot.py**

	Resubmits all s3 records from a specified date to the data pump. This was initially done to reflow data after cleaning up the kinesis stream due to EM duplicate submissions emergency. Currently can be used to generate traffic in dev or live reviewer recommender systems.
* **submit\_to_sns.py**

	Submits a number of manuscripts stored locally to the data pump. Was used for performance testing on specific sets of deltas.

**Local/** collection of scripts to process S3 data locally, needed when records need to be modified individually and requires data downloaded through S3 scripts

* **removeDuplicates.py** 

	Compares manuscript deltas stored locally to those available in s3 and removes local deltas that also appear in S3
* **splitDump.py**

	Splits Evise data dump file into individual deltas, this script was used for migrating historical data from data dumps to the new data pump system

***Note:*** Some scripts require reading additional files and directories which have been added to .gitignore