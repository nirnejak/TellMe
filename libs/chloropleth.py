def chloropleth(date_from, date_to):
    import pandas as pd
    import sqlalchemy as sql
    conn = sql.create_engine('postgresql://fnqryfoivwpuxd:884e1a40af2227d023c58401914873dfea4d44530a34647bb5930872b1a21807@ec2-54-221-220-59.compute-1.amazonaws.com/db70oouohkh4bj')
    avg_color_values = pd.read_sql('''select sum(water_amount) as sum, count(water_amount) as count, state from location_dim, fact_table 
                                    where location_dim.farm_id=fact_table.location_id and irrigation_date >= \''''+
                                  str(date_from)+'\''+' and irrigation_date <= '+'\''+str(date_to)+'\''+' group by state;', conn)
    avg_color_values['avg'] = avg_color_values['sum']/avg_color_values['count']
    avg_color_values.set_index('state', inplace=True)
    ret = {}
    for i in avg_color_values.index :
        ret[avg_color_values.loc[i].name] = avg_color_values.loc[i]['avg']
    return ret
