'''A simple logger'''

import os
import datetime
import uuid
from typing import Optional

def gen_uuid() -> str:
    '''Generates a UUID'''
    return str(uuid.uuid4())

class LoggerError(Exception):
    '''Exception raised for log file related errors'''

class Logger:
    '''A simple logger class'''

    cache: list[str] = None

    def __init__(
                self,
                file_path: Optional[str] = None,
                encoding: str = "utf-8-sig",
                time_format: str = "%Y.%m.%d %H:%M:%S",
                separator: str = "\t",
                silent: bool = False,
                cache_log: bool = False,
                enable_remove: bool = False,
                strip_content: bool = False
            ):
        '''
        Args:
            file_path: path of the log file
            encoding: encoding of the log file
            time_format: time format
            separator: separator
            silent: if True, it will not print the log, just write it to the file
            cache_log: if True, it will cache the log
            enable_remove: if True, it will enable the remove function
            strip_content: if True, it will strip the content
        '''
        self.file_path = file_path if file_path else os.path.join(os.getcwd(), f"{gen_uuid()}.log")
        self.encoding = encoding
        self.time_format = time_format
        self.separator = separator
        self.__silent = silent
        self.__cache_log = cache_log,
        if self.__cache_log:
            self.cache = self.read_list()
        self.__enable_remove = enable_remove
        self.__strip_content = strip_content

    def __str__(self) -> str:
        return f"Log file: {self.file_path}"

    def __error(self, message: str = "") -> None:
        '''Prints error message'''
        raise LoggerError(str(message))

    def __str_time(self) -> str:
        '''Returns the current time as a string'''
        current_time = datetime.datetime.now()
        try:
            return current_time.strftime(self.time_format)
        except Exception as e: # pylint: disable=broad-except
            print(f"Error: {e}")
            return current_time.strftime("%Y.%m.%d %H:%M:%S")

    def __log_to_file(self, content: str) -> None:
        '''Appends file'''
        with open(self.file_path, "a", encoding = self.encoding) as file:
            file.write(content)
            if self.__cache_log:
                self.cache.append(content)

    def __strip(self, content: str) -> str:
        '''Strips the content'''
        return content.strip() if self.__strip_content else content

    def log(self, content: str = "") -> str:
        '''Logs content to file'''
        content = self.__str_time() + self.separator + str(self.__strip(content)) + "\n"
        if not self.__silent:
            print(content)
        self.__log_to_file(content)
        return content

    def change_path(self, file_path: str) -> str:
        '''Changes the log file path'''
        self.file_path = file_path
        print(f"Changed path from {self.file_path} to {file_path}")

    def change_encoding(self, encoding: str) -> str:
        '''Changes the log file encoding'''
        self.encoding = encoding
        print(f"Changed encoding to {encoding}")

    def change_time_format(self, time_format: str) -> str:
        '''Changes the time format'''
        self.time_format = time_format
        print(f"Changed time format to {time_format}")

    def change_separator(self, separator: str) -> str:
        '''Changes the separator'''
        self.separator = separator
        print(f"Changed separator to {separator}")

    def read(self) -> None:
        '''Reads the log file'''
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding = self.encoding) as file:
                lines = file.readlines()
                return "".join(lines)
        self.__error(f"Log file does not exist ({self.file_path})")

    def read_list(self) -> list[str]:
        '''Reads the log file as a list'''
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding = self.encoding) as file:
                lines = [line.strip() for line in file.readlines()]
                return lines
        self.__error(f"Log file does not exist ({self.file_path})")

    def clear(self) -> None:
        '''Clears the log file'''
        if self.__enable_remove:
            if os.path.exists(self.file_path):
                with open(self.file_path, "w", encoding = self.encoding) as _:
                    print(f"Log file cleared ({self.file_path})")
            self.__error(f"Log file does not exist ({self.file_path})")
        self.__error("Removal is not enabled")

    def remove(self) -> None:
        '''Removes the log file'''
        if self.__enable_remove:
            if os.path.exists(self.file_path):
                os.remove(self.file_path)
                print(f"Log file removed ({self.file_path})")
            self.__error(f"Log file does not exist ({self.file_path})")
        self.__error("Removal is not enabled")

    def empty_cache(self) -> None:
        '''Empties the cache'''
        if self.__cache_log:
            self.cache = []
            print("Cache emptied")
        self.__error("Cache is not enabled")
