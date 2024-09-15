import requests
from datetime import datetime, timedelta

def get_tickets_recently_updated(api_baseurl, api_key, days):
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    query_days = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    params = {'since_updated_at': query_days}

    all_syncro_tickets = []

    page = 1
    while True:
        response = requests.get(api_baseurl, headers=headers, params={**params, 'page': page})
        if response.status_code == 200:
            tickets_data = response.json().get('tickets', [])
            all_syncro_tickets.extend(tickets_data)

            meta = response.json().get('meta', {})
            total_pages = meta.get('total_pages', 0)
            if page >= total_pages:
                break
            else:
                page += 1
        else:
            raise Exception(f"Failed to fetch tickets from SyncroMSP API. Status code: {response.status_code}, Response: {response.text}")

    return all_syncro_tickets