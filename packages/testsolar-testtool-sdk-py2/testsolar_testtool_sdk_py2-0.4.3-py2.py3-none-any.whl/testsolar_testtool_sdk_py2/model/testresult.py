from datetime import datetime
from enum import Enum

from typing import List, Optional, Dict


class TestCase:
    __test__ = False

    def __init__(self, name, attributes):
        # type: (str, Dict[str,str]) -> None
        self.Name = name
        self.Attributes = attributes


class ResultType(str, Enum):
    UNKNOWN = "UNKNOWN"
    SUCCEED = "SUCCEED"
    FAILED = "FAILED"
    LOAD_FAILED = "LOAD_FAILED"
    IGNORED = "IGNORED"
    RUNNING = "RUNNING"
    WAITING = "WAITING"


class LogLevel(str, Enum):
    TRACE = "VERBOSE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARNNING"
    ERROR = "ERROR"


class AttachmentType(str, Enum):
    FILE = "FILE"
    URL = "URL"
    IFRAME = "IFRAME"


class TestCaseAssertError:
    __test__ = False

    def __init__(self, expected, actual, message):
        # type: (str, str, str) -> None
        self.Expect = expected
        self.Actual = actual
        self.Message = message


class TestCaseRuntimeError:
    __test__ = False

    def __init__(self, summary, detail):
        # type: (str, str) -> None
        self.Summary = summary
        self.Detail = detail


class Attachment:
    def __init__(self, name, url, attachment_type):
        # type: (str, str, AttachmentType) -> None
        self.Name = name
        self.Url = url
        self.AttachmentType = attachment_type


class TestCaseLog:
    __test__ = False

    def __init__(
        self,
        time,
        level,
        content,
        assert_error=None,
        runtime_error=None,
        attachments=None,
    ):
        # type: (datetime, LogLevel, str, Optional[TestCaseAssertError], Optional[TestCaseRuntimeError], Optional[List[Attachment]]) -> None
        self.Time = time
        self.Level = level
        self.Content = content
        self.AssertError = assert_error
        self.RuntimeError = runtime_error
        self.Attachments = attachments

    def is_error(self):
        # type: () -> bool
        """
        Checks if the log is an error
        """
        return self.Level in [
            LogLevel.ERROR,
        ]


class TestCaseStep:
    __test__ = False

    def __init__(self, start_time, title, result_type, end_time=None, logs=None):
        # type:(datetime, str, ResultType, Optional[datetime], Optional[List[TestCaseLog]]) -> None
        self.StartTime = start_time
        self.Title = title
        self.ResultType = result_type
        self.EndTime = end_time
        self.Logs = logs


class TestResult:
    __test__ = False

    def __init__(self, test, start_time, result_type, message, end_time=None, steps=None):
        # type: (TestCase, datetime, ResultType, str, Optional[datetime], Optional[List[TestCaseStep]]) -> None
        self.Test = test
        self.StartTime = start_time
        self.ResultType = result_type
        self.Message = message
        self.EndTime = end_time
        self.Steps = steps

    def is_final(self):
        # type: () -> bool
        return self.ResultType in [
            ResultType.SUCCEED,
            ResultType.FAILED,
            ResultType.IGNORED,
            ResultType.LOAD_FAILED,
            ResultType.UNKNOWN,
        ]
