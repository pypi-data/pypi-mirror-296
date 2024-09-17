from ..zendesk_api.base_request import get_ticket_page

def records(url:str
            ,email:str
            ,token:str):
    requests_list = []

    while True:
        data:dict[dict] = get_ticket_page(url, email, token)
        requests_list.append(data)

        print('current url', url)
        
        # Check if 'has_more' is in the meta, and if it is False, break the loop
        if 'meta' in data and 'has_more' in data['meta']:
            has_more = data['meta']['has_more']
            print(f'has_more: {has_more}')

            if not has_more:
                break
        else:
            # If 'has_more' is not found in 'meta', stop the loop
            print('No has_more key found, stopping the loop.')
            break

        # Update the URL for the next page
        if 'links' in data and 'next' in data['links']:
            url = data['links']['next']
        else:
            # If 'next' is not found in 'links', stop the loop
            print('No next link found, stopping the loop.')
            break
    
    return requests_list