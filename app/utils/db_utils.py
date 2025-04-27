
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

def batch_insert_or_update(data_list):
    """
    批量插入或更新推特数据。
    """
    try:
        # 提取所有需要插入或更新的数据
        insert_data = []
        update_ids = [data['user_id'] for data in data_list if 'user_id' in data]

        # 查询现有数据
        existing_records = session.query(TwitterData).filter(TwitterData.user_id.in_(update_ids)).all()
        existing_map = {record.user_id: record for record in existing_records}

        for data in data_list:
            if data['user_id'] in existing_map:
                # 更新现有记录
                record = existing_map[data['user_id']]
                # record.user_name = data['user_name']
                record.content = data['content']
                record.update_time = datetime.now()
            else:
                # 插入新记录
                insert_data.append(
                    TwitterData(
                        user_id=data['user_id'],
                        user_name=data['user_name'],
                        content=data['content']
                    )
                )

        # 批量插入新记录
        if insert_data:
            session.bulk_save_objects(insert_data)

        # 提交事务
        session.commit()
        logger.info(f"Inserted {len(insert_data)} records and updated {len(existing_map)} records.")

    except Exception as e:
        session.rollback()
        logger.error(f"Error during batch insert/update: {e}")
        raise