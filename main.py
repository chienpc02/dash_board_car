
import  requests
import pandas as pd
import nocodb
def load_data_nocodb(url_table, header):

    data = []
    try:

        # url = "https://app.nocodb.com/api/v1/db/data/noco/p8xw7nxlf3vb07v/Bu%C3%B4nB%C3%A1nPh%E1%BB%A5T%C3%
        # B9ng%C3%94T%C3%B4Csv/views/Bu%C3%B4nB%C3%A1nPh%E1%BB%A5T%C3%B9ng%C3%94T%C3%B4Csv"
        url = str(url_table)
        querystring = {"offset": "0", "limit": "1000", "where": ""}

        # headers = {"xc-auth": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBoYW1ja
        # GllbjAxMDQyMDAyQGdtYWlsLmNvbSIsImRpc3BsYXlfbmFtZSI6IlBo4bqhbSBWxINuIENoaeG6v24iLCJhdmF0YXIiOm51bGwsInVzZXJfbmFtZSI6bnVsbCwiaWQiOiJ1c2N3ODA2dTdkdjNkbGdnIiwicm9sZXMiOiJvcmctbGV2ZWwtdmlld2VyIiwidG9rZW5fdmVyc2lvbiI6Ijc3ZmUxNmJlYTJhOGQwMzM5MzFkZDc5YzEzNjU1ZjQ3NDQ5ZjcyN2IxYmUwMGVlYjI1YjM2YWViNGMyZDE1MWM5ZjU3MTI0NDFkOWJmNzhlIiwicHJvdmlkZXIiOiJjb2duaXRvIiwiaWF0IjoxNjk4MjE1ODA2LCJleHAiOjE2OTgyNTE4MDZ9.m4V_7Vwx-EFLl8A_8vnaz-vnprdOjbRXgw4PzII7pM0"}

        headers = {"xc-auth": str(header)}

        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 200:
            response_dict = response.json()

            if 'list' in response_dict and response_dict['list'] is not None:
                data.extend(response_dict['list'])

            is_last_page = False
            page = 1

            while not is_last_page:
                querystring = {"offset": f"{page * 1000}", "limit": "1000", "where": ""}
                response = requests.request("GET", url, headers=headers, params=querystring)
                response_dict = response.json()
                is_last_page = response_dict.get('pageInfo').get('isLastPage')
                page = page + 1
                data.extend(response_dict.get('list'))

            df = pd.DataFrame(data)

            df = df[['Name', 'TaxCode', 'Address', 'Phone', 'Province', 'Service']]

            return df
        else:
            print(f"Can't load data from url. Status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error during data loading: {str(e)}")
        return None

# df = load_data_nocodb("https://app.nocodb.com/api/v1/db/data/noco/p8xw7nxlf3vb07v/Bu%C3%B4nB%C3%A1nPh
# %E1%BB%A5T%C3%B9ng%C3%94T%C3%B4Csv/views/Bu%C3%B4nB%C3%A1nPh%E1%BB%A5T%C3%B9ng%C3%94T%C3%B4Csv",
#                  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBoYW1jaGllbjAxMDQyMDAyQGdtYWls
#                  LmNvbSIsImRpc3BsYXlfbmFtZSI6IlBo4bqhbSBWxINuIENoaeG6v24iLCJhdmF0YXIiOm51bGwsInVzZXJfbmFtZSI6bnVsbCwiaWQiOiJ1c2N3ODA2dTdkdjNkbGdnIiwicm9sZXMiOiJvcmctbGV2ZWwtdmlld2VyIiwidG9rZW5fdmVyc2lvbiI6Ijc3ZmUxNmJlYTJhOGQwMzM5MzFkZDc5YzEzNjU1ZjQ3NDQ5ZjcyN2IxYmUwMGVlYjI1YjM2YWViNGMyZDE1MWM5ZjU3MTI0NDFkOWJmNzhlIiwicHJvdmlkZXIiOiJjb2duaXRvIiwiaWF0IjoxNjk4MjE1ODA2LCJleHAiOjE2OTgyNTE4MDZ9.m4V_7Vwx-EFLl8A_8vnaz-vnprdOjbRXgw4PzII7pM0")

