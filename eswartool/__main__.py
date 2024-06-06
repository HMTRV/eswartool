from eswartool.utils.enums.aws import services
import pandas as pd
import aws_sso_lib
import dotenv
import os

dotenv.load_dotenv('.env',override=True)

sso_region = os.getenv('sso_region')
start_url = os.getenv('start_url')


def process(account_id, account_name, role_name):
    session = aws_sso_lib.get_boto3_session(start_url, sso_region, account_id, role_name, region='us-east-1')

    return {
        "account_name": account_name,
        "account_id": account_id,
        "dfs": {k: pd.DataFrame(f.get_data(session)) for k, f in services.items()}
    }


def main():
    dfs_dict = {}
    aws_sso_lib.login(start_url, sso_region)

    values = aws_sso_lib.list_available_roles(start_url, sso_region,  login=False)
    rows = [process(*value) for value in values]
    
    for row in rows:
        for key, df in row['dfs'].items():
            dfs_dict.setdefault(key, [])
            df['account_name'] = row['account_name']
            df['account_id'] = row['account_id']
            dfs_dict[key].append(df)

    for key, dfs in dfs_dict.items():
        df = pd.concat(dfs)
        df.to_parquet(f'{key}.parquet')

    
if __name__ == "__main__":
    main()
