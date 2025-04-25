
from app.models.models import session, TwitterData
from sqlalchemy.exc import SQLAlchemyError
from utils.logger import setup_logger
from datetime import datetime

logger = setup_logger('db_utils')


def save_twitter_data(data,user):
    """
    如果数据库中已存在相同 ID 的数据，则更新；否则插入新数据。
    """
    try:
        # 检查是否已存在相同 ID 的数据
        existing = session.query(TwitterData).filter_by(user_id=user.id).first()

        if existing:
            # 更新现有记录
            existing.user_name = data['user_name']
            existing.content = data['content']
            existing.update_time = datetime.now()
            logger.info(f"Updated existing record with ID: {user.id}")
        else:
            # 插入新记录
            new_data = TwitterData(
                user_id=user.id,
                user_name=data['user_name'],
                content=data['content']
            )
            session.add(new_data)
            logger.info(f"Inserted new record with ID: {user.id}")

        # 提交事务
        session.commit()

    except SQLAlchemyError as e:
        # 回滚事务并记录错误
        session.rollback()
        logger.error(f"Error saving/updating Twitter data: {e}")
        raise e