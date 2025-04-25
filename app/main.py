from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from utils.logger import setup_logger
from utils.config_loader import load_config
from tasks.twitter_task import twitter_stats_task  # 假设所有任务都执行这个函数

logger = setup_logger('Main')
config = load_config()


def start_scheduler():
    scheduler = BackgroundScheduler()

    # 遍历配置文件中的所有任务
    for task in config['scheduler']['tasks']:
        task_name = task['name']

        try:
            if 'cron' in task:
                # 使用 CronTrigger
                trigger = CronTrigger.from_crontab(task['cron'])
                logger.info(f"Scheduled task '{task_name}' with cron: {task['cron']}")
            elif 'interval' in task:
                # 使用 IntervalTrigger
                trigger = IntervalTrigger(seconds=task['interval'])
                logger.info(f"Scheduled task '{task_name}' with interval: {task['interval']} seconds")

            # 添加任务到调度器
            scheduler.add_job(
                twitter_stats_task,
                trigger,
                kwargs={"task_name": task_name}  # 传递任务名称作为参数
            )
            logger.info(f"Scheduled task '{task_name}'")
        except Exception as e:
            logger.error(f"Failed to schedule task '{task_name}': {e}")

    # 启动调度器
    scheduler.start()
    logger.info("Scheduler started.")


if __name__ == "__main__":
    try:
        start_scheduler()
        while True:
            pass  # 保持主线程运行
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutting down...")