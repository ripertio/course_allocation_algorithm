
# Process Documentation
This files documents the working steps taken after the initial meeting with Alex and Adam

#### Before 2022.06.27 (Meeting with Adam and Alex); Short Presentation of Project Aim
- Finding project Idea -> Implementation of Serial Dictatorship Algorithm
- Data Acquisition - from an youth organization - Permission to use the data
- First thoughts (stored in Obsidian) how to implement the algorithm + how to analysis the results
  

#### Feedback to short presentation:
- Basically interesting and possible project idea
- Tasks and Remarks:
- [x] Getting the Data (except number of trainers needed per course)
- Possibility to access time-series data (different allocations from different years)?
	-> Unfortunately not possible these are no longer available or where constantly manipulated (re-staffing)
- [x] Doing first explorative Analysis of the initial allocation (my Ground-Truth)
- [x] Thinking about useful DataManagement, handeling
	- Due to size of data -> selecting .json files (one for trainers_application and one for allocation)
- [x] Description and Explantation for process of Serial Dictatorship Algorithm

#### 2022.06.28

- Working on function for loading the Excel Files; reducing the extant to the necessary parts (courses with applications) and converting them to dictionary (for storing in .json format)
- Thinking about + "playing" through different possible ways and forms of Data-management -> which is most suitable? Sum of Considerations:
  - Storing in (nested) JSON: 
    - (+) Implementation of Serial Dictatorship through using key-value pairs
    - (-) Preparation of data for DataAnalysis more difficult
  - Storing in SQL:
    - (-) "oversized" for the data volumes of the project
    - (-) I did not found a way of Implementing the SD
    - (+) Linking Courses Table with Trainers table  via foreign Key -> reducing duplications
    - (++) Preparation of data for Data Analysis 
  - Storing in CSV:
    - (+) Structured tables
    - (+) Preparation of data for Data Analysis
    - (-) Implementation of Serial Dictatorship more difficult, complex programing structure 


#### 2022.06.29
- Pseudonimizn the data (clients, trainers, pay-rate)
- Continue working on data handling 

#### 2022.07.01
- Working on Explorative Analysis for initial allocation
  - Ratio of Assigned Trainers/ Required Trainers per Course
  - Groupby - Course_Type 

- [x] -> writing function!! for grouping by
- [x] Thinking about (how to deal with some variables e.g. duration, payrate) -> numeric var or categorical?


#### 2022.07.03 
- Continue Working on Explorative Analysis
- unfortunately I still miss the required information -> needed trainer per course
- Some progress in plotting , grouping the initial allocation
#### 2022.07.04
- Combining Applications from Trainers and Assignments of Initial-Allocation (Ground Truth)
- Processing with Initial Allocation explorative Analysis 

#### 2022.07.05
- working on implementation for Serial Dictatorship (harder than I thought!)
- Further engagement with existing literature: Serial Dictatorship with more goods than agents, in several picking rounds = Round Robin
- Scetching out workflow for implementing different possible allocation mechanisms

#### 2022.07.06
- [x] Implementing the serial dictatorship / round robin! NICE!!
- Working on implementation other allocation mechanisms
- thinking about ( and working on ) repeating allocation + storing the results in one DF -> more precise data analysis


#### 2022.07.07
- "Finishing" explorative analysis of project data
  - Basic numbers (sum of course, sum of seats, ....)
  - Crosstable Course type, Duration 
  - Application Ratio for course type
  - Clustering Trainers (workhorses, Allrounder, "Others")
- Progress with the implementation of other mechanisms
  - [x] re-permutate between picking rounds
  - [x] Serial Dictatorship (picking all preferences at once)
- [x] Implementing repeated allocation + storing in on DF 

#### 2022.07.08
- Implementing all other allocation mechanisms:
  - [x] Total Random selection of trainers
  - [x] Random selection from trainers who applied to the respective course
  - [x] Implementing quota (picking more than one course per picking round)
- Working on plotting and analysis
- Thinking about next steps:
  - IDEA: returning the "best" allocation -> question how to judge which is the best allocation? mean, sd, median ... combining them in a way 

#### 2022.07.09
- Working on presentation for Monday
- Working on Analysis 

#### 2022.07.09
- Working on presentation for Monday
- Thinking about measuring the best allocation 
- -->divide mean/std 

#### 2022.07.10
- Presentation Feedback:
  - using coefficient of variation as measurement of "best allocation"
  - Focusing more on explanation (variables, allocation mechanisms (with graphs, ....))
  - Fixing deadlines
- Working on code for returning the best allocation mechanisms
- Starting to think about report, structured content ...
- Reducing current analysis to mean, std

#### 2022.07.12
- implementing coefficient of variation in analysis 
- working on returning the best allocation (I run into sum "stupid" issues ....)
- starting to sketch the allocation mechanisms & workflow

#### 2022.07.12
- implementing returning the best allocation mechanism!!
- working on report
- Finishing draft of visuals for allocation mechanisms


#### 2022.07.13
- Working on Report
- Working on Analysis

#### 2022.07.14
- Working on Report
- Working on Analysis
- Idea - separating data parsing, cleaning -> saving cleaned data to .csv & Data analysis

#### 2022.07.15
- Working on Report
- calculating ratio of assigned course seats
- Working on independency tests
- Implementing separation of data parsing, cleaning & Data analysis 

#### 2022.07.16
- Working on Report
- spotted an error in returning the best allocation -> removing it
- Finishing Analysis
- Working on independence tests
  
#### 2022.07.17
- Working on Report
- Checking and cleaning code 
- Checking analysis and results
- Draft - Report NICE!!
