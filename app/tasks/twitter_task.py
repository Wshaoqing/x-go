import requests
from app.utils.db_utils import batch_insert_or_update
from app.utils.db_utils import save_twitter_data
from app.utils.logger import setup_logger
from app.utils.config_loader import load_config
from datetime import datetime
import concurrent.futures

logger = setup_logger('TwitterTask')
config = load_config()
# 配置
BATCH_SIZE = 1000  # 每批次处理的用户数量
MAX_WORKERS = 10   # 并发线程数

API_URL = "http://127.0.0.1:5000/twitter"

def fetch_twitter_data(user_name):
    try:
        response = requests.get(f"{API_URL}/{user_name}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching data for user {user_name}: {e}")
        return None

def process_user(user):
    """
    处理单个用户的逻辑：- 调用外部接口获取推特数据- 保存推特数据到数据库
    """
    try:
        logger.info(f"Fetching data for user: {user.user_name}")
        data = fetch_twitter_data(user.user_name)
        if data:
            return { "user_id": user.id, "user_name": data['user_name'], "content": data['content']}
        return None
    except Exception as e:
        logger.error(f"Error processing user {user.user_name}: {e}")
        return None

def process_batch(users):
    """
    使用多线程并发处理一批用户。收集twitter用户数据
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_user, user) for user in users]
        results = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

        # 批量插入或更新推特数据
    if results:
        batch_insert_or_update(results)

def twitter_stats_task(task_name):
    from app.models.models import session, TwitterUser
    try:
        logger.info(f"Executing task '{task_name}'")
        logger.info(f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        # 获取所有的TwitterUser
        users = session.query(TwitterUser).all()

        total_users = len(users)
        logger.info(f"Got ----- {total_users} --------Twitter users from database.")
        # 分批次处理
        for i in range(0, total_users, BATCH_SIZE):
            batch_users = users[i:i + BATCH_SIZE]
            logger.info(f"Processing batch {i // BATCH_SIZE + 1} of {len(batch_users)} users.")
            process_batch(batch_users)

    except Exception as e:
        logger.error(f"Error in task '{task_name}': {e}")