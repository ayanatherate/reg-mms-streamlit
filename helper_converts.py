

def convert_df(df):
    """
    Converts a Pandas dataframe to csv

    """
        return df.to_csv(index=False).encode('utf-8')

if __name__=='__main__':
    convert_df(df)

