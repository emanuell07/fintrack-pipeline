from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from etl.pipeline import run_pipeline
import logging
from datetime import datetime

# Configura o log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def executar_pipeline():
    logger.info(f"⏰ Iniciando pipeline agendado — {datetime.now()}")
    try:
        run_pipeline()
        logger.info("✅ Pipeline executado com sucesso!")
    except Exception as e:
        logger.error(f"❌ Erro ao executar pipeline: {e}")

if __name__ == "__main__":
    scheduler = BlockingScheduler()

    scheduler.add_job(
        executar_pipeline,
        trigger=IntervalTrigger(hours=24),  # roda a cada 24h para testar
        id='fintrack_pipeline',
        name='FinTrack ETL Pipeline',
        replace_existing=True
    )

    logger.info("🚀 Scheduler iniciado! Pipeline rodará a cada 1 minuto.")
    logger.info("   Pressione Ctrl+C para parar.")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("⛔ Scheduler encerrado.")
        scheduler.shutdown()