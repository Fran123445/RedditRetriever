# Reddit Retriever

A Python tool designed to extract data from the Reddit API (subreddits, posts, and comments) and load it into a SQL Server database using (kind of) an ETL approach.

## Requirements

*   Python >= 3.10
*   SQL Server instance
*   Reddit API Credentials (Client ID and Client Secret).

## Environment

1.  **Install Python Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Environment Variables:**

    Create a `.env` file in the project root directory with the following content, replacing the placeholders with your actual values:

    ```env
    CLIENT_ID=YOUR_REDDIT_CLIENT_ID
    CLIENT_SECRET=YOUR_REDDIT_CLIENT_SECRET
    USER_AGENT=YourAppName/1.0 by YourRedditUsername # Required by Reddit API. Use a unique, descriptive name.

    # SQL Server Database Connection*
    DRIVER={ODBC Driver 17 for SQL Server} # Or whatever driver you have installed
    SERVER=YOUR_SQL_SERVER_NAME # e.g., .\SQLEXPRESS, localhost, your_server_ip
    DATABASE=RedditRetriever # This is the database name that will be created by the script
    ```

    *Connection establishment in main.py assumes a local machine using windows authentication.
    

3.  **Create `subreddits.json`:**

    Create a file named `subreddits.json` in the /src/ directory containing a JSON array of subreddits you want to retrieve data from. Example:

    ```json
    [
      "nvidia",
      "devsarg",
      "nier",
      "singularity"
    ]
    ```
## Usage

The overall process is:
1.  Run the SQL creation script.
2.  Run python -m src.main from the root folder to fetch data and load it into the staging tables. You can press the Esc key at any time to interrupt the data fetching and loading process gracefully.
3.  Run the `usp_LoadTablesFromStaging` SP to move data from staging into the final schema.

That's it. Enjoy playing around with a bit of Reddit data.