def export_data(dt_from, dt_to, states, districts, crops, water_sources, parameters):
    def parse_string(s):
        r = '('
        for i in s:
            r+=i+' ,'
        r=r[:-2]
        r+=')'
        return r
    import pandas as pd
    import sqlalchemy as sql
    conn = sql.create_engine('postgresql://fnqryfoivwpuxd:884e1a40af2227d023c58401914873dfea4d44530a34647bb5930872b1a21807@ec2-54-221-220-59.compute-1.amazonaws.com/db70oouohkh4bj')
    query = 'select '+parse_string(parameters)[1:-1]+' from fact_table, weather_dim, crop_dim, location_dim '+' where fact_table.location_id=location_dim.location_id '+' irrigation_date >= '+'\''+str(dt_from)+'\' and irrigation_date <= '+'\'' +str(dt_to)+'\''
    if states != None :
        query+=' and state in '+parse_string(states)
    if districts != None :
        query+=' and district in '+parse_string(districts)
    if crops != None :
        query+=' and crop_name in '+parse_string(crops)
    if water_sources != None :
        query+=' and water_source in '+parse_string(water_sources)
    conn.close()
    return pd.to_csv(pd.read_sql(query+';', conn))
    
