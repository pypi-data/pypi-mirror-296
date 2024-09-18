# SPDX-FileCopyrightText: PhiBo DinoTools (2024)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os.path
import queue
from typing import Any, Dict, List, TextIO
from datetime import datetime

from . import Output
from .format import Format
from ..exception import ConfigError
from ..fetcher import LogMessage

logger = logging.getLogger("output.file")


class FileOutput(Output):
    name = "file"

    def __init__(self, filename_pattern: str, output_format: Format):
        super().__init__()

        self._filename_pattern: str = filename_pattern
        self._fp_cache: Dict[str, List] = {}
        self._clean_fp_lastrun = datetime.now()

        self.output_format = output_format

        self._should_terminate = False

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> Output:
        file_config = config.get("file_config")
        if not isinstance(file_config, dict):
            raise ConfigError("file_config not a dict")

        raw_filename = file_config.get("filename")
        if not isinstance(raw_filename, str):
            raise ConfigError("Filename not set or not a string")
        filename = raw_filename

        raw_log_dir = file_config.get("dir", "")
        if not isinstance(raw_log_dir, str):
            raise ConfigError("log_dir not set or not a string")
        log_dir = raw_log_dir
        filename_pattern = os.path.join(log_dir, filename)

        format_name = config.get("format")
        if not isinstance(format_name, str):
            raise ConfigError("format must be set and a string")

        format_cls = Format.registered_formats.get(format_name)
        if format_cls is None:
            raise ConfigError(f"Unable to find format with name '{format_name}'")

        return cls(
            filename_pattern=filename_pattern,
            output_format=format_cls(config=config.get("format_config", {}))
        )

    def _get_fp(self, filename) -> TextIO:
        cached_fp = self._fp_cache.get(filename)
        if cached_fp is None:
            logger.info(f"Open file {filename} ...")
            cached_fp = [open(filename, "a"), datetime.now()]
        else:
            cached_fp[1] = datetime.now()
        self._fp_cache[filename] = cached_fp
        return cached_fp[0]

    def _clean_fp(self):
        now = datetime.now()
        lastrun_ago = now - self._clean_fp_lastrun
        if lastrun_ago.total_seconds() < 600:
            return
        logger.info("File cache cleaning started")
        for filename in list(self._fp_cache.keys()):
            cached_fp = self._fp_cache[filename]
            idle_time = now - cached_fp[1]
            if idle_time.total_seconds() > 600:
                logger.info(f"Closing unused file {filename} ...")
                cached_fp[0].close()
                del self._fp_cache[filename]
        self._clean_fp_lastrun = now
        logger.info("File cache cleaning finished")

    def write(self, message: LogMessage):
        metadata = {
            "hostname": message.fetcher.hostname,
        }

        filename = self._filename_pattern.format(**metadata)
        fp = self._get_fp(filename)
        fp.write(self.output_format.process(message.as_dict))

    def run(self):
        while not self._should_terminate:
            try:
                message = self._queue.get(timeout=2)
            except queue.Empty:
                continue
            self._queue.task_done()
            self.write(message)
            self._clean_fp()

    def stop(self):
        self._should_terminate = True


Output.register("file", FileOutput)
