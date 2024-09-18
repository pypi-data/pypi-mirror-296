import sdb_connector as sdb_conn
import time
import pandas as pd

def main():
    start = time.time()
    result = sdb_conn.select_additional_info_data("192.168.2.63", "8000", 
                "root", "root","main", "data", "amv_tag_49", "run_info:01J6F1DWRHJEGBXTQNP13CWBJW", "additional_info.xlsx", 1)
    df = pd.DataFrame(result, columns=['run_counter', 'len_trigger', 'channel', 'peak', 'peak_positon', \
                                       'positon_over', 'positon_under', 'offset_after', 'offset_before', 'timestamp']).sort_values(by=['run_counter', 'channel'])
    print(df)
    end = time.time()
    print("Time taken result: ", end - start)

    start = time.time()
    result = sdb_conn.select_measurement_data("192.168.2.63", "8000", 
                "root", "root","main", "data", "amv_tag_41", "run_info:01J6F1DWRHJEGBXTQNP13CWBJW", "measurement.xlsx", 1)
    df = pd.DataFrame(result, columns=['run_counter', 'channel', 'integral', 'mass',"offset", "offset1", "offset2", "tolerance_bottom",\
                                       "tolerance_top", "project", "timestamp", "status"]).sort_values(by=['run_counter', 'channel'])
    print(df)
    end = time.time()
    print("Time taken result: ", end - start)
    
    # start = time.time()
    # run_id = "run_info:01J6F1DWRHJEGBXTQNP13CWBJW"
    # result = sdb_conn.select_raw_data("192.168.2.63", "8000", 
    #             "root", "root","main", "data", "amv_raw_data", "run_info:01J6F1DWRHJEGBXTQNP13CWBJW")
    # df = pd.DataFrame(result, columns=['run_counter', 'channel', 'data', 'datetime']).sort_values(by=['run_counter', 'channel'])
    # df["run_id"] = "run_info:01J6F1DWRHJEGBXTQNP13CWBJW"
    # print(df)
    # end = time.time()
    # print("Time taken result: ", end - start)

if __name__ == "__main__":
    main()