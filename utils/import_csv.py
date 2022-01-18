"""
DATABASE=> \copy table_name FROM csv_file.csv WITH (FORMAT CSV);
"""
import pandas as pd


def clean_csv(database: str = 'test_database.csv'):
    """
    Read csv file, apply transformations and save new csv files.
    """
    # read csv
    csv_file = database
    df = pd.read_csv(csv_file, header=0)

    # Fill nulls
    df['company'].fillna('unknown', inplace=True)

    # Validate
    df['status_approved'] = df['status_approved'].astype(bool)

    # Get final payment
    df['final_payment'] = [
        True if (
            status_transaction == 'closed' and status_approved == True)
        else False for status_transaction, status_approved in zip(
            df['status_transaction'],
            df['status_approved'])
    ]

    # create companies csv
    df['company'] = df['company'].str.casefold()
    companies_dict = {
        (
            id, name,
            'active' if name != 'unknown' else 'inactive') for id, name in enumerate(
                sorted(list(df['company'].unique()))
        )
    }
    companies_df = pd.DataFrame(
        companies_dict, columns=['id', 'name', 'status']
    )
    companies_df.index += 1
    companies_df.to_csv('companies.csv', index=False, header=False)

    # set company id in transactions
    df['company_id'] = df['company'].map(
        companies_df.set_index('name')['id'])
    df['id'] = [i for i in range(1, len(df) + 1)]
    df.drop(columns=['company'], inplace=True)

    # Order columns
    df = df[
        [
            'id',
            'price',
            'date',
            'status_transaction',
            'status_approved',
            'final_payment',
            'company_id',
        ]
    ]
    df.sort_values(by=['date'], inplace=True, ignore_index=True)

    # save csv
    df.to_csv('transactions.csv', index=False, header=False)


if __name__ == '__main__':
    clean_csv()
