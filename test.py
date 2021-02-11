import logging, sys

formatter = logging.Formatter(f"[%(asctime)s][test] %(message)s", datefmt="%H:%M:%S")
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

logger = logging.getLogger("test")
logger.propagate = False
logger.addHandler(stream_handler)
print("adasdsa")
logger.info('Test')