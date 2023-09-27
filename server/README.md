# Server

This directory contains the backend server for the assessment. 

# Run 
``` zsh
source env/bin/activate  
pip install -r requirements.txt
python server.py
```

# Improvements
- Add an endpoint that allows the client/front-end to specify what database to access. This would allow us to scale this further. 
- Add a layer of caching for filters - Given that the client/front-end qieries using the same data, this would entail a faster response. 
- Add additional error validation.
- Implement the ability to convert data to pandas dataframe, json, and/or csv file