import requests
from app.utils.db_utils import save_twitter_data
from app.utils.logger import setup_logger
from app.utils.config_loader import load_config
from datetime import datetime

logger = setup_logger('TwitterTask')
config = load_config()

API_URL = "http://127.0.0.1:5000/twitter"

def fetch_twitter_data(user_name):
    try:
        response = requests.get(f"{API_URL}/{user_name}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching data for user {user_name}: {e}")
        return None

def twitter_stats_task(task_name):
    from app.models.models import session, TwitterUser
    try:
        logger.info(f"Executing task '{task_name}'")
        logger.info(f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        users = session.query(TwitterUser).all()
        for user in users:
            logger.info(f"Fetching data for user: {user.user_name}")
            data = fetch_twitter_data(user.user_name)
            if data:
                save_twitter_data(data,user)
                logger.info(f"Saved data for user: {user.user_name}")
    except Exception as e:
        logger.error(f"Error in task '{task_name}': {e}")