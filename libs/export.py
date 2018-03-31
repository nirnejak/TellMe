
def export_data(dt_from, dt_to, states = None, districts = None, crops = None, water_sources = None):
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
    query = 'SELECT * FROM fact_table, weather_dim, crop_dim, location_dim '+' WHERE fact_table.location_id=location_dim.location_id '+' irrigation_date >= '+'\''+str(dt_from)+'\' AND irrigation_date <= '+'\'' +str(dt_to)+'\''
    if states != None :
        query+=' AND state IN '+parse_string(states)
    if districts != None :
        query+=' AND district IN '+parse_string(districts)
    if crops != None :
        query+=' AND crop_name IN '+parse_string(crops)
    if water_sources != None :
        query+=' AND water_source IN '+parse_string(water_sources)
    conn.close()
    return pd.to_csv(pd.read_sql(query+';', conn))
    
