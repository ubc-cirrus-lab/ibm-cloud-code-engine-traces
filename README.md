# IBM Cloud Code Engine Traces

Data associated with the following publication. Please cite the paper if you use this data in your research.

Nima Nasiri, Nalin Munshi, Simon D Moser, Marius Pirvu, Vijay Sundaresan, Daryl Maier, Thatta Premnath, Norman Böwing, Sathish Gopalakrishnan, and Mohammad Shahrad, "In-Production Characterization of an Open Source Serverless Platform and New Scaling Strategies", 2026 ACM European Conference on Computer Systems (EuroSys '26).


## Decompressing the Data

To decompress the data files, run the `decompress.sh` script. 
This will extract all the weekly traffic data files as well as app configuration dataframe into a directory named `data`.
The clone size of this repository is about 6GB, however, after decompression, the size of the `data` directory will be around 52GB.

```bash
bash decompress.sh
``` 

## Workload Size

- 62 days
- 1780 applications

## Information Included 

- Hashed Namespace
- Hashed Application Name
- Daily Application Configurations (see `app_configs.pickle`)
    - 'NamespaceHash'
    - 'AppHash'
    - 'AppContainerRequestCpu'
    - 'AppContainerRequestMemory'
    - 'AppContainerConcurrency'
    - 'AppMinScale'
- Weekly Traffic Data (10 weeks, see `week_*.pickle`)
    - 'NamespaceHash'
    - 'AppHash'
    - 'NumEvents'
    - 'InvocationTimes': a list of size `NumEvents` containing the invocation timestamps
    - 'AppExecTimes': a list of size `NumEvents` containing the application execution times
    - 'TotalExecTimes': a list of size `NumEvents` containing the total execution times
    - 'PodHash': a list of size `NumEvents` containing the pod hashes. Each app can have multiple pods, so this column allows to identify which pod served which request. Note that the ordering of requests across the these four lists is consistent.

## Using the Data

All data is stored in pickle format and sgould be loaded using Python Pandas library as DataFrames.

```python
import pandas as pd
df_configs = pd.read_pickle('data/app_configs.pickle')
df_week1 = pd.read_pickle('data/week_1.pickle')
...
```

Loading all the weekly traffic data files will require a high amount of RAM. 
Depending on your machine's capabilities, you might want to load part of the data or process the data in chunks.