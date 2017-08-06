import logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
handler = logging.FileHandler('Log_Report.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
