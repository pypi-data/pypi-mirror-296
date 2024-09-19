# Sheet Logger

`SheetLogger` is a simple, efficient, and configurable logging utility that writes logs to specific Google Sheets tabs. It supports batching, automatic timestamping, and Google Sheets API rate limit protection.

## Installation

You can install the package directly from PyPI:

```bash
pip install sheet-logger
```

## Example Output
2024-09-18 17:54:37 - This message will be written to Logs sheet.  
2024-09-18 17:54:38 - This message will be written to Logs sheet2.  
2024-09-18 17:54:39 - This message will be written to Logs sheet3.  

## Usage

Once installed, you can use `SheetLogger` as follows:  
First import the package, then initiate the class and then use the write_to_sheet method for log prints.  
Example below:  

```python
from sheet_logger import SheetLogger

if __name__ == "__main__":

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    LOGSHEET_ID = "123123123123123123123123123"

    ## Instantiate the logger
    sheet_logger = SheetLogger(LOGSHEET_ID, SCOPES, subfolder="auth", token_file_name="token.json")

    ERROR_LOGS = "Logs"
    EXECUTION_LOGS = "Execution_logs"
    OTHER_LOGS = "test"

    sheet_logger.write_to_sheet(ERROR_LOGS, "Example Message 1.")
    sheet_logger.write_to_sheet(ERROR_LOGS, "Example Message 2.")
    sheet_logger.write_to_sheet(ERROR_LOGS, "Example Message 3.")

    sheet_logger.write_to_sheet(EXECUTION_LOGS, "Example Message 4.")
    sheet_logger.write_to_sheet(OTHER_LOGS, "Example Message 5.")
```

### Features

- **Timestamps**: Automatically adds timestamps (`"YYYY-MM-DD HH:MM:SS"`) to each log message.
- **Batching**: Accumulates log entries and writes them in batches to reduce API calls. You can specify the batch size (default is 5).
- **API Rate Limit Protection**: Protects against exceeding Google's limit of 60 requests per user per minute by automatically pausing for 60 seconds if necessary.
- **Multiple Tabs**: Supports writing logs to multiple tabs in the same Google Spreadsheet.
- **Multiple Instances**: If multiple spreadsheets need to be used, you can instantiate separate `SheetLogger` instances for each.

### Initialization Arguments

When initializing the `SheetLogger`, you have two options for specifying the Google OAuth token:

1. **Full Token Path**: Provide the full path to the token file by using the `token_file_name` argument.
   
2. **Subfolder and Token Name**: If your token file is located in a specific subfolder, provide the `subfolder` and the token file name using the `subfolder` and `token_file_name` arguments.

Example initialization with subfolder:

```python
sheet_logger = SheetLogger(
    spreadsheet_id=LOGSHEET_ID, 
    scopes=SCOPES, 
    subfolder="auth", 
    token_file_name="token.json"
)
```

Example initialization with full token path:

```python
sheet_logger = SheetLogger(
    spreadsheet_id=LOGSHEET_ID, 
    scopes=SCOPES, 
    token_file_name="/full/path/to/token.json"
)
```

### API Rate Limit Protection

Google Sheets has a rate limit of 60 API requests per minute. `SheetLogger` monitors and enforces this limit by tracking the number of API write calls. If the limit is reached, it automatically pauses for 60 seconds before resuming.

### Batching

You can configure the batch size when initializing the logger. Instead of making individual API calls for each log entry, logs are collected and sent in batches, reducing the number of API requests. Once the batch size is reached, the logs are flushed to the sheet.

Example with a batch size of 10:

```python
sheet_logger = SheetLogger(
    spreadsheet_id=LOGSHEET_ID, 
    scopes=SCOPES, 
    batch_size=10
)
```

### Multiple Tabs

You can log messages to different tabs by passing the tab name to the `write_to_sheet()` method. Each log entry is automatically timestamped and written to the specified tab.

### Multiple Instances for Multiple Spreadsheets

If you need to log to multiple Google Spreadsheets, you can create separate instances of the `SheetLogger` for each spreadsheet.

Example:

```python
logger1 = SheetLogger(LOGSHEET_ID_1, SCOPES)
logger2 = SheetLogger(LOGSHEET_ID_2, SCOPES)

logger1.write_to_sheet("Logs", "Message for Spreadsheet 1")
logger2.write_to_sheet("Logs", "Message for Spreadsheet 2")
```

### Publishing and Updating the Package

To publish the package or update it with a new version, follow these steps:

1. **Build the package**:

```bash
python setup.py sdist bdist_wheel
```

2. **Upload to PyPI**:

```bash
twine upload dist/*
```

This will upload the package to PyPI, making it available for installation via `pip install sheet-logger`.