from decorator import decorator

from .log import logger_factory


@decorator
def retry(func, max_retry=3, logger=None, *args, **kwargs):
    """Not stop retrying until reach max limit."""
    if not logger:
        logger = logger_factory(func)

    error = None
    for i in range(max_retry):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            logger.warning(f'Retrying [{i + 1} / {max_retry}]')
            error = e
    raise error
