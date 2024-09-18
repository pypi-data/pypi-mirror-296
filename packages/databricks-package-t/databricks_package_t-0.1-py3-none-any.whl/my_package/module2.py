# my_package/module2.py
def display_data(df):
    """
    Display the DataFrame.
    """
    if df is not None:
        print("DataFrame:")
        print(df.head())
    else:
        print("No data to display.")
