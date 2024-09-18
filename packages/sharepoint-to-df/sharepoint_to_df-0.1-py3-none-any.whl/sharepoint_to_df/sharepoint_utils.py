import pandas as pd
from office365.runtime.client_context import ClientContext
from office365.runtime.credentials import UserCredential

def get_list_view_test(username, password, sharepoint_site, list_name, view_name="All Items"):
    conn = ClientContext(sharepoint_site).with_credentials(UserCredential(username, password))
    web = conn.web
    conn.load(web)
    conn.execute_query()
    target_list = conn.web.lists.get_by_title(list_name)
    
    # Load fields to get their internal names
    fields = target_list.fields.get().execute_query()
    field_mapping = {field.internal_name: field.title for field in fields}
    
    view = target_list.views.get_by_title(view_name)
    view_fields = view.view_fields.get().execute_query()
    
    visible_fields = {field: field_mapping[field] for field in view_fields if field_mapping.get(field)}
    items = target_list.items.get().execute_query()
    data = []
    for item in items:
        item_data = {visible_fields[field]: item.properties.get(field) for field in visible_fields}
        data.append(item_data)
    df = pd.DataFrame(data)
    return df
