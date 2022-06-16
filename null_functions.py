###### NULL FUNCTIONS #####
### count_nulls(df,by_column=True)
### handle_missing_values(df, prop_req_col=.75, prop_req_row=.75)

# Improvements to make
# 1) needs to be restructured to better handle lots of rows or columns (takes to long to run)
def count_nulls(df,by_column=True):
    ''''
    Finds number and percentage of nulls by column or by row

    Returns: Dataframe with null count per row/column
    Parameters:
            df: Dataframe to count the nulls in
      by_column: If True, counts the nulls per column, else counts the nulls per row. Default: True
    '''
    #intialize df
    df_nulls = pd.DataFrame()
    
    if by_column:
        #total rows
        num_rows = df.shape[0]
        #loop over each column
        for c in df.columns:
            #count # of nulls
            null_cnt = df[c].isna().sum()
            #calculate percent of nulls
            null_perc = null_cnt/num_rows
            #Populate DF
            df_nulls.loc[c,'num_nulls'] = null_cnt
            df_nulls.loc[c,'pct_nulls'] = null_perc
    else: 
        #total cols
        num_cols = df.shape[1]
        #loop over each row
        for i in df.index:
            #count # of nulls
            null_cnt = df.loc[i,:].isna().sum()
            #calculate percent of nulls
            null_perc = null_cnt/num_cols
            #Populate DF
            df_nulls.loc[i,'num_nulls'] = null_cnt
            df_nulls.loc[i,'pct_nulls'] = null_perc
    
    return df_nulls

def handle_missing_values(df, prop_req_col=.75, prop_req_row=.75):
    """
    Checks the rows and columns for missing values.  Drops any rows or columns less than the specified percentage.
    
    Returnss: Dataframe
    Parameters: 
                df: Dataframe to analyze
      prop_req_col: Proportion (between 0 and 1) of values in column that must exist (non-null). Default: .75
      prop_req_row: Proportion (between 0 and 1) of values in a row that must exist (non-null). Default: .75
    """
    #Determine number of required non-nulls in columns (prop * num_rows)
    col_thresh = int(round(prop_req_col*df.shape[0],0))
    #drop columns w/o enough info
    df.dropna(axis=1,thresh=col_thresh,inplace=True)
    
    #NOW DO ROWS - note, this on already trimmed df
    #Determine number of required non-nulls in rows (prop * num_cols)
    row_thresh = int(round(prop_req_row*df.shape[1],0))
    #drop rows w/o enough info
    df.dropna(axis=0,thresh=row_thresh,inplace=True)
    
    return df