"""
    First attempt at preprocessing based on reading paper, no longer needed/used.
"""

import pandas as pd


""" Handles data preprocessing """
def preprocessing():
    # Read all necessary MIMIC-3 data files
    chart_events = pd.read_csv('./mimic-iii-clinical-database-1.4/CHARTEVENTS.csv')
    lab_events = pd.read_csv('./mimic-iii-clinical-database-1.4/LABEVENTS.csv')
    items= pd.read_csv('./mimic-iii-clinical-database-1.4/D_ITEMS.csv')
    lab_items= pd.read_csv('./mimic-iii-clinical-database-1.4/D_LABITEMS.csv')
    patients = pd.read_csv('./mimic-iii-clinical-database-1.4/PATIENTS.csv')

    # IDs of 19 required variables stated in section 4.1 of the paper
    item_ids = [220045, 220210, 220277, 223761, 220179, 220180,
                50813, 50862, 50893, 50960, 50824, 51521, 51006,
                51265, 50971, 50809, 50912, 50882, 50818]
    
    # Remove all non-relevant items and create new dataframe
    i = items.loc[items['ITEMID'].isin(item_ids)]
    l = lab_items.loc[lab_items['ITEMID'].isin(item_ids)]
    variables = i.append(l, ignore_index=True)
    variables = variables.drop(
        [
            'ABBREVIATION', 'CATEGORY', 'CONCEPTID', 'DBSOURCE',
            'FLUID', 'LINKSTO', 'LOINC_CODE', 'PARAM_TYPE', 'ROW_ID',
            'UNITNAME'
        ],
        axis=1
    )

    # Merge chart_events and lab_events and clean non-relevant columns
    df = pd.merge(chart_events, variables, on='ITEMID', how='right')
    df2 = pd.merge(lab_events, variables, on='ITEMID', how='right')
    df3 =  df.append(df2, ignore_index=True)
    df3 = df3.drop(
        [
            'ICUSTAY_ID', 'HADM_ID', 'STOPPED', 'WARNING',
            'ERROR', 'CGID', 'FLAG', 'RESULTSTATUS', 'STORETIME',
            'ROW_ID', 'VALUE', 'VALUEUOM'
        ], 
        axis=1
    )

    # Remove non-relevant columns from patients and create a boolean "Alive" column
    patients['ALIVE'] = patients['DOD'].apply(lambda x: 1 if not pd.isna(x) else 0)
    patients = patients.drop(
        [
            'ROW_ID', 'GENDER', 'DOD', 'DOD_HOSP',
            'DOD_SSN', 'EXPIRE_FLAG', 'DOB'
        ],
        axis=1
    )


if __name__ == "__main__":
    preprocessing()
