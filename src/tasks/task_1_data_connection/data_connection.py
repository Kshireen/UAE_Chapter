import os
import requests
import pandas as pd
import json
from io import BytesIO
from handle_exceptions import handle_exceptions as h_e


BASE_URL='https://data.abudhabi/opendata'
class DataConnection:

    def __init__(self):
        self.curr_dir=os.path.dirname(__file__)

    @h_e
    def get_dataset(self, dataset_name):
        """ this method is to load dataset in to the dataframe using api calls
            params: string type 'dataset_name'
        """
        json_path=os.path.join(self.curr_dir,'end_points.json')
        with open(json_path) as end_points_file:
            datasets = json.load(end_points_file)
            if dataset_name in datasets:
                endpoint_path = datasets[dataset_name]
                api_url = f"{BASE_URL}{endpoint_path}"
                response= requests.get(api_url)
                if response.status_code==200:
                    data = response.json()
                    distributions = data.get('distribution')
                    download_url = distributions[0].get('downloadURL')
                    # print(download_url)
                    root, extension = os.path.splitext(download_url)
                    # print(root, extension)
                    dataset = requests.get(download_url)
                    # reading the dataset based on extension into dataframe
                    with BytesIO(dataset.content) as buffer:
                        # return pd.read_excel(buffer, engine='openpyxl')
                        if extension.lower() == '.csv':
                            return pd.read_csv(buffer)
                        else:
                            return pd.read_excel(buffer, engine='openpyxl')
            else:
                return None


# def main():
#     d_c=DataConnection()
#     dset = 'Dubai Civil Defence Fire Stations'
#     df = d_c.get_dataset(dset)
#     print(df.head())

# if __name__=='__main__':
#     main()