Ah, got it! If your package is available on PyPI and can be installed via `pip`, here's how you can include usage instructions in your `README.md` file for users who install the package through `pip`. 

### `README.md`

```markdown
# SharePoint to DataFrame

This library provides a function to read SharePoint lists into pandas DataFrames.

## Installation

You can install the package from PyPI using pip:

```sh
pip install sharepoint-to-dataframe
```

## Usage

### Function: `get_list_view`

This function retrieves data from a SharePoint list and loads it into a pandas DataFrame.

#### Importing the Function

First, import the function from the installed package:

```python
from sharepoint_to_dataframe import get_list_view
```

#### Calling the Function

To call the function, use the following syntax:

```python
import pandas as pd
from sharepoint_to_dataframe import get_list_view

# Define your parameters
username = 'your_username'
password = 'your_password'
sharepoint_site = 'https://yourcompany.sharepoint.com/sites/yoursite'
list_name = 'Your List Name'
view_name = 'Your View Name'  # Optional: Default is "All Items"

# Call the function
df = get_list_view(username, password, sharepoint_site, list_name, view_name)

# Print the DataFrame
print(df)
```

#### Parameters

- `username` (str): Your SharePoint username.
- `password` (str): Your SharePoint password.
- `sharepoint_site` (str): The URL of your SharePoint site.
- `list_name` (str): The name of the SharePoint list you want to access.
- `view_name` (str, optional): The name of the view within the list. Defaults to `"All Items"`.

#### Returns

- `DataFrame`: A pandas DataFrame containing the data from the SharePoint list view.

### Example

Here's a complete example demonstrating how to use the `get_list_view` function:

```python
import pandas as pd
from sharepoint_to_dataframe import get_list_view

# Define your parameters
username = 'john.doe@example.com'
password = 'your_password'
sharepoint_site = 'https://example.sharepoint.com/sites/testsite'
list_name = 'Employee List'
view_name = 'Active Employees'

# Retrieve the DataFrame
df = get_list_view(username, password, sharepoint_site, list_name, view_name)

# Display the DataFrame
print(df)
```

This example fetches data from the "Active Employees" view of the "Employee List" on the specified SharePoint site and prints it as a pandas DataFrame.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any issues or questions, please contact Mutaz Younes at mutazyounes@gmail.com.
```

### Key Points

1. **Installation Instructions**: Use `pip` to install the package from PyPI.
2. **Function Import and Usage**: How to import the function and use it.
3. **Parameters and Return Values**: Detailed descriptions of function parameters and return values.
4. **Example Usage**: A full example to demonstrate how to call the function and use it.

This should help users understand how to install and use your library after installing it via `pip`.