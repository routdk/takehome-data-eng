# Bungalow Take Home Project for Data Engineer Role (V2. 2021-11-02)

Welcome to the Bungalow Takehome Challenge for Data Engineering! This is a barebones repo to get you started.

## What to build
A common task for data engineers at Bungalow involves the integration of the of third-party data, modelling data, storing it and making it available for downstream teams such as analytics, data science and ultimately the entire organization.
For this challenge we'd like to give a brief snapshot of a common workload may entail. Of course, this might become a big task. Therefore, to save time for you, we did some of the heavy lifting, like the set up and some scaffolding of the environment.

For this test we will collect the [current weather data](https://openweathermap.org/current) from [OpenWeatherMap](https://openweathermap.org/). The free API will work for this assignment. You shouldn’t pay for the API.

Please install [Docker Desktop](https://www.docker.com/get-started) on your laptop. It will contain the environment that we would need for the next steps.

The Docker compose would have two software applications and simple setup required for them.

- Airflow: To run your additions to the boilerplate DAGs.

- Postgres: To maintain your tables. (You can swap it with any other database or your choice, i.e. SQLite, MySQL)


Below are the steps in the data flow diagram:

- fetcher.py script, that represents the fetcher DAG, would retrieve the data from the current weather API.

- The fetcher script would process and clean the data, then stores it the Postgres database considering relationships, integrity, performance, and extendability.

- The transformer.py script, that represents the Transformer DAG, would transform the data from the previous step to prepare some derived dataset tables. You will have the choice to implement the transformations both in Python or SQL.

- The Transformer writes the datasets back to Postgres.

- The downstream customer(s) would read both original and derived tables. They will execute historical queries to run analytics and science models.


This project is meant to be flexible as to showcase your decision making capabilities and your overall technical experience. 

**Note:** If you are uncomfortable with Docker, Postgres or Airflow, please feel free to remove or replace them. They are meant to save time for you. As long as you can achieve the outcome feel free to use any additional tooling, programming language (i.e. Java or Scala) and approach you see fit. We will ask follow up questions about your decision mechanism in the follow up conversation.

We are more interested in seeing your thought process and approach to solving the problem!

##  Deliverables
We will expect to see the following items in your Github pull request:

- Your Python code for data fetcher and transformer.

- The data model SQL and your design for its data modelling

- Readme file with your notes

## Evaluation
We will use this project as our basis for our evaluation of your overall fit for a data engineering role from a technical viewpoint.

To do this, we will review your code with an eye for the following:

- Readability, scalability and usability

- Data processing and relational modelling

- Python and SQL know-how

## Time expectations
We know you are busy and likely have other commitments in your life, so we don't want to take too much of your time. We don't expect you to spend more than 2 hours working on this project. That being said, if you choose to put more or less time into it for whatever reason, that is your choice.

Feel free to indicate in your notes below if you worked on this for a different amount of time and we will keep that in mind while evaluating the project. You can also provide us with additional context if you would like to.

Additionally, we have left a spot below for you to note. If you have ideas for pieces that you would have done differently or additional things you would have implemented if you had more time, you can indicate those in your notes below as well, and we will use those as part of the evaluation.

## Public forks
We encourage you to try this project without looking at the solutions others may have posted. This will give the most honest representation of your abilities and skills. However, we also recognize that day-to-day programming often involves looking at solutions others have provided and iterating on them. Being able to pick out the best parts and truly understand them well enough to make good choices about what to copy and what to pass on by is a skill in and of itself. As such, if you do end up referencing someone else's work and building upon it, we ask that you note that as a comment. Provide a link to the source so we can see the original work and any modifications that you chose to make.

## Challenge instructions
Fork this repository and clone to your local environment

- Prepare your environment with Python and any other tools you may need. Docker can do it for you.
  - To run the docker-compose, you need to run the following commands:
      ```shell
      # Initializing the folders and the non-root user for Airflow
      mkdir -p  ./logs ./plugins
      echo -e "AIRFLOW_UID=$(id -u)" > .env
      # Initializing airflow database
      docker-compose up airflow-init
      # Running the docker-compose
      docker-compose up 
      # You can see the Airflow UI in http://localhost:8080 with username/password: airflow
      ```
  - If you run to any problems with the environment, please refer to [here](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html).
- Fill in the TODO in the repository. There are currently 6 TODOS, but you can go beyond and above.
  - Any problems with the DAGs? They are taken from [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html). Please take a look at the rest of tutorial if needed.
  - You can check Postgres operator from [here](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/operators/postgres_operator_howto_guide.html)
  - To keep it simple, let's use the Airflow database for the storage of your dataset
- Write down the notes, in the Readme.md file.
- Complete the challenge and push back to the repo
  - If you have any questions in any step, please reach out to your recruiter. A member of engineering team will be involved to support you, as if you were working for Bungalow.
- **Note:** If you are using Apple hardware with M1 processor, there is a common challenge with Docker. You can read more about it [here](https://javascript.plainenglish.io/which-docker-images-can-you-use-on-the-mac-m1-daba6bbc2dc5).

## Your notes (Readme.md) 
@TODO: Add any additional notes / documentation in this file.

### Time spent
Give us a rough estimate of the time you spent working on this. If you spent time learning in order to do this project please feel free to let us know that too. This makes sure that we are evaluating your work fairly and in context. It also gives us the opportunity to learn and adjust our process if needed.

### Assumptions
Did you find yourself needing to make assumptions to finish this? If so, what were they and how did they impact your design/code?

### Next steps
Provide us with some notes about what you would do next if you had more time. Are there additional features that you would want to add? Specific improvements to your code you would make?

### Instructions to the evaluator
Provide any end user documentation you think is necessary and useful here


\
&nbsp;
\
&nbsp;
\
&nbsp;
\
&nbsp;

# Preamble

Let me first present the the 1000ft view on the solution, then I will dig down to individual components on the solution explaning how they are stitched together, it's pros and cons and the reason for the design decisions I have taken.

# Philospohy 
My initial version of the data pipeline is built on my current understanding of the problem statement.
With time and more discussion my understanding of the problem would definitely evolve, the and solution would 
need iterative development cycles to improve and become more efficient.

## The 1,000-Foot View

* STEP1 : Extract the current weather data from the REST API avaialble to us.
* STEP2 : Parse, clean and re-structure the data elements useful for our business.
* STEP3 : Store the data in a place it can be combined with other datasets easily.
* STEP4 : Create summerized dataset(s) for efficient querying.
* STEP5 : Automate the process 

### Dataflow Diagram


![arch](https://user-images.githubusercontent.com/86860323/159840541-8de8a8e0-ef36-4da2-ac72-d80224c1c857.png)



## Tool Selection : 
* **Data Fetch, Parse and Restructure** : Python
* **Data Transformation** : SQL 
* **Data warehouse** : Postgres
* **Infrastructure** : Docker, Docker Compose
* **Pipeline Orchrestrator** : Airflow 
* Local Development : 
  -  python virtual environment
  -  Docker Desktop on Mac
  -  VS Code
  -  Git

## Environment Setup : 

- Created a virtual environment to avoid conflict with other local projects.
```
python3 -m venv env
source env/bin/activate
```
- Installed libraries inside virtual env : `requests` and `psycopg2-binary`
- Created requirements.txt `pip freeze > requirements.txt`. Pipenv or Poetry might be a modern and better way of implementing package/dependency management in production scenarios.
- Leverage .env (dot-env) for all secrets to be exported to the environment. Alternative would be a vault to store secrets and fetch when its needed.
Refer `.env.tmpl` for the details. This can be renamed to `.env` if someone clones the project and starts working on it.
- Minor changes to the `docker-compose.yaml` file. 
  - PYTHONPATH is needed as I created a package to store some utility modules.
  - Additional environment variables to be exported inside docker.
- Static lookup file (`lookup_data/usa_coordinates.json)
This is a JSON file containing all USA cities and their co-ordinates.
- Dockerfile to build image as I needed additional 3rd party libraries.


## Solution Walkthrough

### Data Extraction

OpenweatherMap restful API call requires Longitude and Latitude Geo Coordinates. 
Each call to the API returns one record with a set of weather related attributes for the current timestamp for a particular location(co-ordinates).
Geocoder API is a way to get (Longitude, Latitude) of a particular city. 
But instead of using this I tried to download a master list of geo coordinates and their corresponding city mapping from [here](https://bulk.openweathermap.org/sample/) and cleaned a bit 
(collected only USA cities to make the file size smaller), and uploaded the data in JSON format to code repo as a static lookup file. 
Though the code repo is not a suitable place for this (I would prefer a database), to make the assignment simple I have done this. 
We can consider the scope of our weather data to be all cities in the USA.


Now coming to the code part, accessing a REST API is straightforward, using the `requests` library in python and “GET” method to a specific endpoint and query params. 
For a toy example this works well, but in real world the API data extraction has below challenges :

- Rate Limit Throttles the API calls (retry is must). For the free account "Calls per minute: 60" which is quite less.
- API call is a sequential process (single threaded application unless we specifically write to code to make it parallel). 
Multithreading with a list of query params can give us a edge to make the data fetch run in parallel or 
if we have a distributed engine like spark we can make a data frame of endpoints (adding query params) and hit the API from different worker nodes to make the data fetch parallel.
But the free version rate limit is really low, so neither of the approach was taken here.
- Though this particular API returns 1 record per API call, most APIs have pagination and we have to loop through 
the pages to fetch results. Now the question is where to hold the output of the data returned. 
If we keep the json data in the form of a python dict we may eventually hit a memory limit. 
So writing the data to somewhere in the interim is essential.
For example every 100k rows or 1GB of data we can write to a storage and clean up memory for efficient processing. 
Again there will be decision decisions on the file format we want to store (row based - AVRO/ORC, columnar - PARQUET, simple CSV or JSON)

All these pain points are not addressed in my code. (Only point #1 is addressed). 
But if I have to develop iteration to the code I would focus on (point # 3) as decoupling extract and transformation steps are very important to address the job failure/re-run related issues and software practice in general. 
My code currently has a very close coupling of EtL(t here is the minor transformation like flattening the json and converting epoch timestamp to a formatted datetime etc). 
The close coupling of EtL is not a good decision as it involves extract (Network) transform (Compute) and load to DB (I/O) and it's happening in iteration for each record. 
Say there are 20k cities in the USA and we will repeat the IO 20k times. 
So point#3 is really important for reducing this I/O.

### Data Transformation

I have used python to convert JSON to a dict and do the minor transformations (I would like to call it technical transformation) 
to maintain a clean structure and adhering to the standards. 
There is no business transformation involved here. 
We have several options to do the transformation.
Dictionary processing is not a very intuitive way to transform data 
when the volume is large, so frameworks like spark are useful for distributed computing. 
Even the pattern of loading JSON(semi-structured) data to a database
(almost all DB these days have support and functions around it) and parse and do the transformation in the database layer is a 
commonly used pattern. If it's a well known third party API and we have a budget I would prefer tools 
like Fivetran, Stitch, Singer (provided there is a connector). 
This decision is not for this exercise but for parsing JSON results for API and the pain points(schema changes/ additional data elements requirement in future etc.) in general.

Key things that can be improved in my code : 

- Close coupling as I mentioned earlier. The only reason I did close coupling is to avoid data passing between tasks in airflow.
- Defining schema to the data (as we convert from semi structured to structured). Type casting at this phase is always a better option. 

### Data Loading

I would prefer bulk load features provided by the databases as opposed to dynamically generating and running insert statements for each row. Example : COPY command offered by Redshift and Snowflake.
I learned that generating the INSERT statements with a formatted string approach does not work in Postgres. There might be some trick to make it work,
but I had no luck. So I [googled around](https://stackoverflow.com/questions/61341246/psycopg2-dynamic-insert-query-issues-syntax-error-at-or-near-identifier) and found an alternative solution to build the SQL statement. 

2 key design decisions here
- Building History (how do we get it or will we build over time)
- Frequency of data ingestion (what are the end use cases)

### Derived Tables/ Aggregated Tables/ Summary Tables (Real Capital T of ELtT) 

This is the layer that gives the real business value. 
We need a robust data model and key relationships, insert/update strategy properly defined. 
Though in this particular assignment we are not building a data model (dimensional modeling is mostly used followed by Data Vault 2.0 in the modern data world). 
Also there is a recent trend of [OBT](https://www.fivetran.com/blog/star-schema-vs-obt) (One Big Table) holding everything to make the life of analysts easier. Probably the data model I created in this exercise falls under OBT category.

DBT really shines here. Writing a SQL and insert/update table might seem trivial but at scale maintaining those SQLs are challenging. 
We won’t have lineage if we write individual SQL DML to do data transformation. 
So the entire system would be a black box.

I am no expert in weather data and its trend analysis. 
But for this exercise I will try to create 1 dataset. 
Let’s focus only on the temperature aspect of weather for now, and the idea can be expanded to other attributes. 

`city_day_summary_temerature`:

gives a summary of daily aggregated temperature for a particular city and date. The strategy here is to upsert the record in order to avoid duplicates 
or full refresh of huge volume of data everyday. If we want multiple weather attibute (wind speed, snowflake etc) we can use a  window function rather than using group by.

Reduced the scope further to 5 USA cities and aggregation for 1 day.

![Screen Shot 2022-03-24 at 1 10 11 PM](https://user-images.githubusercontent.com/86860323/159972398-99c937ab-02b9-4149-9725-ed7e67d61a28.png)



Another idea I have is about time series analysis (sepecifically moving average) across
multiple hours (say 5 hrs moving average, 5 is just a random number). 
As we capture data entire day in small intervals there will be many data points and moving average will 
reduce noise and show us a clear pattern on the uptrend or downtrend(mostly cyclic
in our case as the temp goes up in day time and comes down in evening.
But moving average is a nice tool across many usecases. There is a standard way 
of writing SQL on moving average. Though as a part of this take home I did not do it but 
creating such an aggregated table can be useful.
Here is the highlevel idea : 
- Truncate the datetime to hour so that we can get hourly moving avg.
- If there is a gap in the data we can fill the rows to make it continious (one common way is to generate hourly calender type of dataset and doing a left join with original data).
- The attributes can be filled with some logic (may be lead/lag or even avg). This will reduce outlier.
- If we don't want to fill the data RANGE BETWEEN frame in window can be one an alternative. But sometimes it gives incorrect results. Its a bit tricky to use based on the database type.
- Moving average over specific interval can be found using `ROWS BETWEEN x PRECEDONG and CURRENT ROW`


### Things I wish I could have improved

- Testing...Testing...Testing (It’s important so I have written 3 times) - Code Unit Testing(pytest) and Data Testing(DBT Test or Great Expectations). 
I personally see more value in data testing as opposed to code testing because the code will run with fix set of parameters 
and no user is running the code as with varying inputs.
So in user facing application development unit and system testing is more critical but in data processing application development data testing(integrity/key relationships, null/dup check etc are more imp).
This is purely my personal opinion.
- Decouple the EtL piece and make Et and L separate.
- I have used .env(dot env) locally to store secrets and docker compose exports them to the environment(I did not know docker-compose has native support for it, learned it with this excercise), 
but setting secrets in a vault and fetching at runtime is a better idea in general than storing as env variables. 
- Using Pipenv or Poetry for virtual environment setting.
- Wanted to try other APIs like forecast. Bulk unload API(I guess free account does not have access there)
- A better data model. 
- Clear thinking on error and rejection handling scenarios and re-run edge cases.
- Good Analytics usecase and create a dataset which could have given lots of insights.


### Challenges I faced: 

- I tried to use poetry for dependency management. Building a docker container installing poetry and generating the requirements.txt file did not work. So I generated the requirements.txt from virtual environment and placed it under version control.
- Spent a relatively long time(30 ish min) debugging the issues of running DAG inside docker as PYTHONPATH was not set and the packages and modules I created were not getting recognized.
- I tried to use parameter in SQL query(table name) to run postgres operator, but it was adding a single quote around the table name and there was syntax error.
- Imagining a proper meaningful analytics usecase for the data. I could think of just moving averages using Windows functions. 
- API call is really slow. 60 calls per minute means 60 records per minute. We have to limit our scope(# of cities) or increase the interval of data fetch.
- I did not know merge does not exist in Postgres. Postgres's `INSERT ON CONFLICT` syntax was a learning for me.









