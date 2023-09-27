# Pattern Research Full-Stack Takehome

This repository contains a full stack application for Pattern Research's take-home assessment.


## Prompt

SQLite dump of a small trades table. The schema is as follows:

``` SQL
CREATE TABLE fills(
     order_id INT NOT NULL,
     fill_price DOUBLE NOT NULL,
     fill_quantity DOUBLE NOT NULL,
     side TEXT CHECK (side IN ('BUY', 'SELL')) NOT NULL,
     exchange TEXT NOT NULL,
     symbol TEXT NOT NULL,
     fees DOUBLE NOT NULL,
     timestamp DATETIME PRIMARY KEY
);
```

Create a visualization for displaying the PNL of these trades. We envision a static graph of the PNL tracked over the lifetime of the trades. Optionally - include different ways to slice/view the data, this can include filtering by desk, filtering by symbol, grouping by date (second, minute, day granularity), etc. We leave this and any other improvements or modifications up to you. Note that we are not looking for anything crazy fancy, just something functional to display the rudimentary data.


## Overview

To run the application, the user needs to spin up the backend python server, as well as the react frontend. 

- `./server`: Contains the Python backend - Instructions can be found in the sub-directory
- `./frontend`: Contains the React frontedn - Instructions can be found in the sub-directory



