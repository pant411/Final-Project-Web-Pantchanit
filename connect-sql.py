import os
from dotenv import load_dotenv
from google.cloud.sql.connector import Connector, IPTypes

# load env vars
load_dotenv()

# Cloud SQL Python Connector creator function
def getconn():
    # if env var PRIVATE_IP is set to True, use private IP Cloud SQL connections
    ip_type = IPTypes.PRIVATE if os.getenv("PRIVATE_IP") is True else IPTypes.PUBLIC
    # if env var DB_IAM_USER is set, use IAM database authentication
    user, enable_iam_auth = (
        (os.getenv("DB_IAM_USER"), True)
        if os.getenv("DB_IAM_USER")
        else (os.getenv("DB_USER"), False)
    )
    # initialize Cloud SQL Python connector object
    with Connector(ip_type=ip_type, enable_iam_auth=enable_iam_auth) as connector:
        conn = connector.connect(
            os.getenv("INSTANCE_CONNECTION_NAME"),
            "pg8000",
            user=user,
            password=os.getenv("DB_PASS", ""),
            db=os.getenv("DB_NAME"),
        )
        return conn
