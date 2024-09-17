"""
Byte.gg API Wrapper

This module provides a Python wrapper for interacting with the Byte.gg bypass API.
It includes classes for handling API responses and a main Byte class for making API calls.

Classes:
    BypassResult: Represents the result of a successful bypass operation.
    TaskMetadata: Contains metadata about the task execution.
    SuccessResponse: Represents a successful API response.
    ErrorDetails: Contains additional error details if available.
    ErrorInfo: Provides detailed information about an error.
    ErrorResponse: Represents an error response from the API.
    ProcessingResponse: Indicates that a task is still being processed.
    Byte: Main class for interacting with the Byte.gg API.

Types:
    CreateTaskOptions: A dictionary of options for creating a bypass task.

Usage:
    from byte_gg_wrapper import Byte

    # Initialize the Byte client
    byte_client = Byte("your_api_key_here")

    # Create a bypass task
    task_id = byte_client.create_task({"url": "https://example.com"})

    # Get the task result
    result = byte_client.get_task_result(task_id)

    # Get supported services
    services = byte_client.get_supported_services()

    # Get the service for a specific URL
    service = byte_client.get_service("https://example.com")

"""

import requests
from typing import Any, Dict, Union, Optional
import time


class BypassResult:
    """
    Represents the result of a successful bypass operation.

    Attributes:
        bypassed_url (str): The URL after bypassing.
        bypass_result (str): Additional information about the bypass result.
    """

    def __init__(self, bypassed_url: str, bypass_result: str):
        self.bypassed_url = bypassed_url
        self.bypass_result = bypass_result


class TaskMetadata:
    """
    Contains metadata about the task execution.

    Attributes:
        execution_time (str): The time taken to execute the task.
        cached (bool): Whether the result was cached.
        task_id (str): The unique identifier for the task.
        additional_metadata (dict): Any additional metadata provided.
    """

    def __init__(self, execution_time: str, cached: bool, task_id: str, **kwargs: Any):
        self.execution_time = execution_time
        self.cached = cached
        self.task_id = task_id
        self.additional_metadata = kwargs


class SuccessResponse:
    """
    Represents a successful API response.

    Attributes:
        status (str): Always set to "success".
        result (BypassResult): The result of the bypass operation.
        metadata (TaskMetadata): Metadata about the task execution.
    """

    def __init__(self, result: BypassResult, metadata: TaskMetadata):
        self.status = "success"
        self.result = result
        self.metadata = metadata


class ErrorDetails:
    """
    Contains additional error details if available.

    Attributes:
        hint (Optional[str]): A hint about the error, if provided.
    """

    def __init__(self, hint: Optional[str] = None):
        self.hint = hint


class ErrorInfo:
    """
    Provides detailed information about an error.

    Attributes:
        code (int): The error code.
        message (str): A description of the error.
        details (Optional[ErrorDetails]): Additional error details, if available.
    """

    def __init__(self, code: int, message: str, details: Optional[ErrorDetails] = None):
        self.code = code
        self.message = message
        self.details = details


class ErrorResponse:
    """
    Represents an error response from the API.

    Attributes:
        status (str): Always set to "error".
        error (ErrorInfo): Detailed information about the error.
    """

    def __init__(self, error: ErrorInfo):
        self.status = "error"
        self.error = error


class ProcessingResponse:
    """
    Indicates that a task is still being processed.

    Attributes:
        status (str): Always set to "processing".
    """

    def __init__(self):
        self.status = "processing"


CreateTaskOptions = Dict[str, Union[str, bool]]


class Byte:
    """
    Main class for interacting with the Byte.gg API.

    This class provides methods to create bypass tasks, retrieve task results,
    get supported services, and determine the service for a given URL.

    Attributes:
        api_key (str): The API key for authentication.
        endpoint (str): The base URL for the Byte.gg API.

    """

    def __init__(self, api_key: str):
        """
        Initialize a new Byte instance.

        Args:
            api_key (str): The API key for authentication.

        """
        self.api_key = api_key
        self.endpoint = "https://byte.yxusinbot.com"

    def create_task(self, options: CreateTaskOptions) -> str:
        """
        Create a new bypass task.

        Args:
            options (CreateTaskOptions): The options for creating a task.

        Returns:
            str: The task ID.

        Raises:
            Exception: If the API returns an error response.

        """
        response = requests.post(
            f"{self.endpoint}/api/v1/createTask",
            json=options,
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        data = response.json()

        if data['status'] == "success":
            return data['result']['taskId']
        raise Exception(data['error']['message'])

    def get_task_result(self, task_id: str) -> Union[SuccessResponse, ErrorResponse]:
        """
        Retrieve the result of a bypass task.

        This method polls the API until a final result is available.

        Args:
            task_id (str): The ID of the task to retrieve results for.

        Returns:
            Union[SuccessResponse, ErrorResponse]: The task result.

        """
        while True:
            response = requests.post(
                f"{self.endpoint}/api/v1/getTaskResult",
                json={"taskId": task_id}
            )
            data = response.json()

            if data['status'] == "processing":
                time.sleep(0.5)  # Wait for 500 ms before retrying
                continue
            return data

    def get_supported_services(self) -> list[str]:
        """
        Retrieve a list of supported services.

        Returns:
            list[str]: An array of supported service names.

        """
        response = requests.get(f"{self.endpoint}/api/v1/utils/supported")
        return response.json()

    def get_service(self, link: str) -> str:
        """
        Determine the service associated with a given link.

        Args:
            link (str): The URL to check.

        Returns:
            str: The service name.

        """
        response = requests.post(
            f"{self.endpoint}/api/v1/utils/getService",
            json={"url": link}
        )
        return response.json()