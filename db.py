from pymongo import MongoClient

# Azure MongoDB connection string
DATABASE_URL = "mongodb+srv://user:Root1234@h3hitema.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
DB_NAME = "db"

# Create a MongoClient instance using the connection string
client = MongoClient(DATABASE_URL)

# Access the database (creates it if it doesn't exist)
db = client[DB_NAME]

# Access the "product" collection within the database
products_collection = db["product"]
