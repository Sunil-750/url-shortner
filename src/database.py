"""MongoDB connection and CRUD operations for URL shortener"""
from pymongo import MongoClient
from typing import Optional
import os

# MongoDB Connection Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://127.0.0.1:27017/")
DATABASE_NAME = "url_shortener"
COLLECTION_NAME = "urls"

# Global client and database instances
client: Optional[MongoClient] = None
db = None
url_collection = None


def connect_to_mongo():
    """
    Establish connection to MongoDB
    """
    global client, db, url_collection
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
        # Verify connection
        client.admin.command('ping')
        db = client[DATABASE_NAME]
        url_collection = db[COLLECTION_NAME]
        
        # Create unique index on short_code for optimal lookups
        url_collection.create_index("short_code", unique=True)
        
        print("✓ Successfully connected to MongoDB")
    except Exception as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        raise


def close_mongo_connection():
    """
    Close the MongoDB connection
    """
    global client
    if client:
        client.close()
        print("✓ MongoDB connection closed")


def store_url(short_code: str, original_url: str) -> bool:
    """
    Store a short code and original URL mapping in MongoDB
    
    Args:
        short_code: The generated short code
        original_url: The original long URL
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        result = url_collection.insert_one({
            "short_code": short_code,
            "original_url": original_url
        })
        return result.inserted_id is not None
    except Exception as e:
        print(f"Error storing URL: {e}")
        return False


def get_url(short_code: str) -> Optional[str]:
    """
    Retrieve the original URL from a short code
    
    Args:
        short_code: The short code to look up
        
    Returns:
        str: The original URL if found, None otherwise
    """
    try:
        document = url_collection.find_one({"short_code": short_code})
        if document:
            return document.get("original_url")
        return None
    except Exception as e:
        print(f"Error retrieving URL: {e}")
        return None


def url_exists(short_code: str) -> bool:
    """
    Check if a short code already exists in the database
    
    Args:
        short_code: The short code to check
        
    Returns:
        bool: True if exists, False otherwise
    """
    try:
        return url_collection.find_one({"short_code": short_code}) is not None
    except Exception as e:
        print(f"Error checking URL existence: {e}")
        return False


def delete_url(short_code: str) -> bool:
    """
    Delete a short code and its mapping from the database
    
    Args:
        short_code: The short code to delete
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        result = url_collection.delete_one({"short_code": short_code})
        return result.deleted_count > 0
    except Exception as e:
        print(f"Error deleting URL: {e}")
        return False


def get_all_urls() -> list:
    """
    Retrieve all URL mappings from the database
    
    Returns:
        list: List of all URL documents
    """
    try:
        return list(url_collection.find({}, {"_id": 0}))
    except Exception as e:
        print(f"Error retrieving all URLs: {e}")
        return []


def clear_all_urls() -> bool:
    """
    Delete all URL mappings from the database (useful for testing)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        result = url_collection.delete_many({})
        print(f"Cleared {result.deleted_count} URLs from database")
        return True
    except Exception as e:
        print(f"Error clearing URLs: {e}")
        return False
