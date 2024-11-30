import pandas
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from Processing import process_RT3100
from Sensors.Sqlite_Adapt import SqliteAdapt
import plotly.io as py

def create_table_for(df: pandas.DataFrame, index:str, elements:[str], title:str):
    for element in elements:
        df['squared_' + element] = df[element].apply(lambda x: x ** 2)
    df['squared'] = df[[f'squared_{element}' for element in elements]].sum(axis=1)
    df['sqrt_squared'] = np.sqrt(df['squared'])
    # Assuming df is your DataFrame and 'time' is your x-axis

    # Create the figure and add each trace
    fig = go.Figure()

    for element in elements:
        # Create a trace for each variable
        trace = go.Scatter(x=df[index], y=df[element], mode='lines', name=element)
        fig.add_trace(trace)

    trace_sq = go.Scatter(x=df['time'], y=df['sqrt_squared'], mode='lines', name='squared')

    fig.add_trace(trace_sq)

    # Set the title
    fig.update_layout(title=f"{title}: {str(elements)}")

    # Show the figure
    fig.show()
    py.write_image(fig, f'{title}_{"_".join(elements)}.png')



def main(adapt: SqliteAdapt):
    print("Starting Data Processing")
    # Connect to the SQLite database

    # Get the names of all tables in the database
    table_names = adapt.get_tables()

    # Filter table names
    table_names = [name for name in table_names if ('usbserial' in name or 'ttyUSB' in name) and 'raw_' not in name]
    print(table_names)
    # Loop over the tables and plot the data
    for table_name in table_names:
        # Read the table into a pandas DataFrame
        df = pd.read_sql_query(f"SELECT * from {table_name}", adapt.conn)

        # Convert the 'time' column to datetime
        df['time'] = pd.to_datetime(df['time'])


        create_table_for(df, "time", ["Hx","Hy","Hz"], table_name)
        create_table_for(df, "time", ["Ax", "Ay", "Az"], table_name)

    # Close the connection to the database
    adapt.close()


if __name__ == '__main__':
    adapter = SqliteAdapt("/Users/max/Downloads/2024-01-21_20-55-35_data.db") # /Users/max/Downloads/2024-01-21_20-57-23_data.db")
    data_post_process.main(adapter)
    main(adapter)
