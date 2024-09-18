from ctgenerics import connect
import pandas as pd

test_data = pd.DataFrame({'a':[1,2,3],'b':[3,4,5]})

connect_object = connect.Redshift('dw-live')

connect_object.write_to_sql(test_data,'ct_squared')
connect_object.run_sql('drop table corpdev.ct_squared')