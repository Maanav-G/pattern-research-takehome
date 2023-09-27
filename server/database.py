import sqlite3
from typing import List

import pandas as pd


def _format_where_in_condtion(col_name: str, vals: List) -> str:
    '''
    This handles converting the provided column name and its associated values to a 'WHERE in ...' condition for SQL.
    Typically formatted as so:
        WHERE <column name> in (<value 1>, <value 2>, ...);
        or
        WHERE <column name> = value;

    Note: This function does not add the 'WHERE' keyword
    '''
    values = f"in {str(tuple(vals))}" if len(vals) > 1 else f"= '{vals[0]}'"
    return f'{col_name} {values}'


def _format_query(table_name: str, cols: List = None, where_cond: List = None) -> str:
    '''
    This handles converting the provided table name, columns, and where conditions to an executable SQL query.
    Attributes: 
        table_name: name of the SQL table
        cols: list of columns to query 
        where_cond: WHERE conditions to append to query
    '''
    query = f"""SELECT {str(cols)[1:-1] if cols else '*'} 
    FROM {table_name}
    {where_cond if where_cond else ''}"""

    return query


def _compute_pnl(col_names: List, data: List) -> pd.Series:
    '''
    This handles computing the PNL for a given dataset.

    The data is converted into a Pandas dataframe, and then based on the data, 
    a cumalative PNL series is generated and returned.
    '''
    df = pd.DataFrame(data, columns=col_names)
    df = df.sort_values(by='timestamp')
    
    df['pnl'] = df.apply(
        lambda row: 
        (row['fill_price'] - (df[df['timestamp'] < row['timestamp']]['fill_price'].sum())) * 
        (row['fill_quantity'] if row['side'] == 'SELL' else 0),
        axis=1
    )

    df['cum_pnl'] = df['pnl'].cumsum()
    df = df.set_index('timestamp')

    return df['cum_pnl']


class Database():
    def __init__(self, database=None) -> None:
        self.connection = None
        self.cursor = None
        if database:
            self.open(database)

    def open(self, database: str) -> None:
        '''
        Handles opening a connection to the provided database
        '''
        try: 
            self.connection = sqlite3.connect(database)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite database", error)
    
    def close(self) -> None:
        '''
        Given there is an active connection, this handles closing the connection
        '''
        if self.connection:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
        else:
            print("Error while closing connection. No connection found. ")

    def execute_query(self, query: str) -> List:
        '''
        Handles executing the provided query with the connection
        '''
        if self.cursor:
            self.cursor.execute(query)
            return self.cursor.fetchall()

    def get_col_names(self):
        '''
        Handles fetching all columns from database
        '''
        if self.cursor and self.cursor.description:
            field_names = [i[0] for i in self.cursor.description]
            return field_names

    def to_dataframe(self, query) -> pd.DataFrame:     
        raise NotImplementedError

    def to_json(self, query, file_name) -> None:     
        raise NotImplementedError

    def to_csv(self, query, file_name) -> None:     
        raise NotImplementedError


class TradesDatabase(Database):
    def __init__(self, database="trades.sqlite") -> None:
        super().__init__(database)

    def get_all(self):
        '''
        Get all data from table.
        '''
        return self.execute_query("""SELECT * FROM fills""")

    def get_pnl_by_filters(self, filters: dict) -> pd.Series:
        '''
        Get data from the database based on the provided filters.
        '''
        if filters and any([len(filter_vals) > 0 for _, filter_vals in filters.items()]):
            format_filters = [
                _format_where_in_condtion(filter_name, filter_vals)
                for filter_name, filter_vals in filters.items() 
                if filter_vals
            ]
            where_conditons = 'WHERE ' + (' AND ').join(format_filters) + ';'
            query = _format_query(table_name='fills', where_cond=where_conditons)
            data = self.execute_query(query)

        else:
            data = self.get_all()

        return _compute_pnl(self.get_col_names(), data)

    def get_unique(self, col_names: List) -> dict:
        '''
        Get all unqiue values found under the provided column.
        '''
        unique_values = {}
        for col_name in col_names:
            values = self.execute_query(f"""SELECT DISTINCT {col_name} FROM fills""")
            unique_values[col_name] = [val[0] for val in values]

        return unique_values
    
    def get_filters(self) -> dict:
        '''
        Handles getting all the unique possible options to be used as filters.
        '''
        col_names = ['exchange', 'symbol']
        unique_filters = self.get_unique(col_names)
        return unique_filters