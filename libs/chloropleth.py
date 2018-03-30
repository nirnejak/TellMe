import datetime as dt

def chloropleth(date_from = dt.date(2000,1,1), date_to = dt.date.today()):
    import pandas as pd
    import sqlalchemy as sql
    conn = sql.create_engine('postgresql://fnqryfoivwpuxd:884e1a40af2227d023c58401914873dfea4d44530a34647bb5930872b1a21807@ec2-54-221-220-59.compute-1.amazonaws.com/db70oouohkh4bj')
    avg_color_values = pd.read_sql('''SELECT SUM(water_amount) as sum, COUNT(water_amount) AS count, state FROM location_dim, fact_table 
                                    WHERE location_dim.farm_id = fact_table.location_id AND irrigation_date >= \''''+
                                  str(date_from)+'\''+' AND irrigation_date <= '+'\''+str(date_to)+'\''+' GROUP BY state;', conn)
    avg_color_values['avg'] = avg_color_values['sum']/avg_color_values['count']
    avg_color_values.set_index('state', inplace=True)
    ret = {}
    for i in avg_color_values.index :
        ret[avg_color_values.loc[i].name] = avg_color_values.loc[i]['avg']
    return ret