#!/usr/bin/env python
# coding: utf-8
import logging


# logging.basicConfig(filename="app.log", level=logging.DEBUG)
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh = logging.FileHandler("app.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(log_formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(log_formatter)
logger.addHandler(ch)


def info(line):
    logger.info(line)


def debug(line):
    logger.debug(line)


def warn(line):
    logger.warning(line)


def error(line):
    logger.error(line)
