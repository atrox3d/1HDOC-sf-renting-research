import sys
import logging

##################################################################################################################
# logging.NOTSET | "NOTSET" | 0:
#       Detailed information, typically of interest only when diagnosing problems.
# logging.DEBUG | "DEBUG" | 10:
#       Detailed information, typically of interest only when diagnosing problems.
# logging.INFO | "INFO" | 20:
#       Confirmation that things are working as expected.
# logging.WARNING | "WARNING" | 30:
#       An indication that something unexpected happened, or indicative of some problem in the near future
#       (e.g. ‘disk space low’). The software is still working as expected.
# logging.ERROR | "ERROR" | 40:
#       Due to a more serious problem, the software has not been able to perform some function.
# logging.CRITICAL | "CRITICAL" | 50:
#       A serious error, indicating that the program itself may be unable to continue running.
##################################################################################################################


def get_cli_logger(
        name=None,
        level="DEBUG",
        set_handler=True,
        # format_sring=f'%(asctime)s | %(levelname)-8s | %(name)-40s | %(message)s',
        format_sring=f'%(asctime)s | %(levelname)-8s | %(module)-15s | %(name)-40s | %(message)s',
        output_stream=sys.stderr,
) -> logging.Logger:
    """
    ########################################################################################################################
        - GET LOCAL (NON-ROOT) LOGGER INSTANCE THAT OUTPUTS TO CLI
        - SET LEVEL TO DEBUG (DEFAULT IS WARNING)
    ########################################################################################################################
    """
    _logger = logging.getLogger(name)  # get local logger
    _logger.setLevel(level)  # set logger level >= logger_level
    """
    ########################################################################################################################
        - GET SAME FORMATTER INSTANCE FOR ALL HANDLERS
    ########################################################################################################################
    """
    formatstring = format_sring
    formatter = logging.Formatter(formatstring)  # get formatter
    """
    ########################################################################################################################
        - GET CLI HANDLER INSTANCE
        - SET FORMATTER FOR CLI HANDLER INSTANCE
        - ADD HANDLER TO LOCAL LOGGER
    ########################################################################################################################
    """
    if set_handler and not _logger.hasHandlers():
        cli_handler = logging.StreamHandler(stream=output_stream)  # get CLI handler (default=stderr)
        cli_handler.setFormatter(formatter)  # set formatter for CLI handler
        _logger.addHandler(cli_handler)  # add CLI handler to logger

    return _logger
