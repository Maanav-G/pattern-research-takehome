import json
from functools import lru_cache

import pandas as pd
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import TradesDatabase


class Body(BaseModel):
    filters: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache
def get_trades_db():
    return TradesDatabase()


@app.post("/get_data")
async def get_data(body_details: Body):
    '''
    Endpoint handles getting the computed PNL data from the database.

    Attributes: 
        body_details: filters for what data to query on
    '''

    db = get_trades_db()
    filters = json.loads(body_details.filters)
    result = db.get_pnl_by_filters(filters)

    return result.to_json()


@app.get("/get_filter_options")
async def get_filter_options():
    '''
    Endpoint handles returning all possible filters.
    '''
    db = get_trades_db()
    return db.get_filters()


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0', log_level='debug')