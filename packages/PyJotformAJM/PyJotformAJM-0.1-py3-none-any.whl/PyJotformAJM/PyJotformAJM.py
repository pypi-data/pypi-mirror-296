"""
PyJotformAJM.py

"""

from jotform import JotformAPIClient
from ApiKeyAJM import APIKey

from datetime import datetime
from logging import getLogger
from typing import Union
from urllib.error import HTTPError


class JotFormAuthenticationError(HTTPError):
    ...


class NoJotformClientError(Exception):
    ...


class JotForm(APIKey):
    DEFAULT_FORM_ID = None

    def __init__(self, **kwargs):
        """
        This code initializes an instance of a class and sets up various attributes and a logger.
        It also checks if a form ID is provided and raises an error if it is not found.
        Finally, it logs a message to indicate that the initialization is complete.

        Constructor:
            __init__(self, **kwargs)
                Initializes an instance of the class with the provided keyword arguments.

        Attributes:
            _has_new_entries : bool or None
                Stores whether there are new entries. Default value is None.
            _new_entries_total : int or None
                Stores the total number of new entries. Default value is None.
            _last_submission_id : int or None
                Stores the ID of the last submission. Default value is None.
            form_id : str
                Stores the ID of the form. It is set to the default value if not provided in the keyword arguments.
            logger : Logger
                Stores the logger object. If a logger object is provided in the keyword arguments, it is used. Otherwise, a 'dummy_logger' is created.
            client : JotformAPIClient
                Stores the Jotform API client object. If an API key is provided, it is used to create the client. Otherwise, the API key is retrieved from the specified location and used to create the client.

        Raises:
            AttributeError
                If form_id is not found and neither form_id nor DEFAULT_FORM_ID is set.

        Example usage:
            # Create an instance of MyClass with a custom logger
            logger = getLogger('my_logger')
            my_obj = MyClass(logger=logger)

            # Create an instance of MyClass with a custom form ID and API key
            my_obj = MyClass(form_id='my_form_id', api_key='my_api_key')

        This code should be used as a template for creating new instances of the class. It provides a basic structure for initialization and sets up important attributes and dependencies.
        """
        super().__init__(**kwargs)
        if hasattr(self, 'logger'):
            pass
        else:
            self.logger = kwargs.get('logger', getLogger('dummy_logger'))

        self._has_valid_client = False
        self._has_new_entries = None
        self._new_entries_total = None
        self._last_submission_id = None

        self.form_id = kwargs.get('form_id', self.DEFAULT_FORM_ID)

        self._initialize_client()

        if not self.form_id and not self.DEFAULT_FORM_ID:
            raise AttributeError('form_id not found, if form_id was not a keyword arg, '
                                 'check that DEFAULT_FORM_ID is set in any subclasses.')

        if not self.has_valid_client:
            raise NoJotformClientError('no valid JotForm client object found.')
        else:
            self.logger.info(f"{self.__class__.__name__} Initialization complete.")

    @property
    def has_new_entries(self):
        """
        This code defines a property called `has_new_entries` for a class. The property is used to determine whether there are new entries in a form.

        Attributes:
            - `client`: An object representing the client used to interact with forms.
            - `form_id`: The ID of the form to check for new entries.

        Returns:
            - `True` if there are new entries in the form.
            - `False` if there are no new entries in the form.

        Note:
        This property assumes that the `client` object has a method called `get_form` that returns information about the form specified by `form_id`. The information should include a field called 'new' representing the count of new entries.

        Usage:
        ```
        # Create an instance of the class
        client = Client()
        form_id = 123

        # Call the property to check for new entries
        is_new = client.has_new_entries
        ```
        """
        if int(self.client.get_form(self.form_id)['new']) > 0:
            self._has_new_entries = True
        else:
            self._has_new_entries = False
        return self._has_new_entries

    @property
    def new_entries_total(self):
        """
        @property
        def new_entries_total(self):
            """
        if self.has_new_entries:
            self._new_entries_total = {'total': int(self.client.get_form(self.form_id)['new']),
                                       'last_submission': self.client.get_form(self.form_id)['last_submission'],
                                       'last_submission_id': self.last_submission_id}
        else:
            self._new_entries_total = None
        return self._new_entries_total

    @property
    def last_submission_id(self):
        """
        Retrieves the last submission ID for the specified form.

        @return: The last submission ID as an integer.
        """
        self._last_submission_id = self._get_last_submission_id(self.client.get_form(self.form_id)['last_submission'])
        return self._last_submission_id

    @property
    def has_valid_client(self):
        if hasattr(self, 'client'):
            self._has_valid_client = True
        else:
            self._has_valid_client = False
        return self._has_valid_client

    @has_valid_client.setter
    def has_valid_client(self, value):
        self._has_valid_client = value

    def _initialize_client(self):
        if self.api_key:
            self.client = JotformAPIClient(self.api_key)
        else:
            self.client = JotformAPIClient(self._fetch_api_key(self.api_key_location))
        self._validate_client()

    def _validate_client(self):
        try:
            self.client.get_user()
            self.has_valid_client = True
        except HTTPError as e:
            raise JotFormAuthenticationError(
                url=e.url, code=e.code, msg=e.reason, hdrs=e.headers, fp=e.fp) from None

    def _get_last_submission_id(self, last_sub_datetime: Union[datetime, str]):
        """
        This method is used to get the last submission ID of a form based on the provided last submission datetime.

        Parameters:
        - last_sub_datetime: The last submission datetime to search for. It can be provided as a datetime object or a string in ISO format.

        Returns:
        - The last submission ID as an integer if it exists.
        - None if there is no submission matching the provided datetime.

        Note:
        - This method relies on the 'client' attribute which should be an instance of a client object that has the 'get_form_submissions' method.
        - The 'client.get_form_submissions' method returns a list of submissions for the provided form ID.
        - The method iterates through each submission and checks if the 'created_at' datetime matches the provided last submission datetime.
        - If a matching submission is found, its ID is stored in the 'last_sub_id' list.
        - The method returns the first ID from the 'last_sub_id' list if it is not empty.
        - If there are no matching submissions, None is returned.
        """
        last_sub_id = [x['id'] for x in self.client.get_form_submissions(self.form_id)
                       if datetime.fromisoformat(x['created_at']) == datetime.fromisoformat(last_sub_datetime)][0]
        if last_sub_id:
            return last_sub_id
        else:
            return None

    def get_new_submissions(self):
        """
        Returns the new submissions for a given form.

        This method retrieves new form submissions from the client based on the specified form ID. It filters the submissions to only return those with the 'new' attribute set to '1'.

        Returns:
            list: A list of new submissions, each represented as a dictionary.

                The dictionary contains attributes and their corresponding values for each submission.

                Example:
                {'id': 1, 'name': 'John Doe', 'age': 25, 'new': '1'}

                If no new submissions are found, it returns None.

            None: If no new submissions are found.
        """
        new_submissions = [x for x in self.client.get_form_submissions(self.form_id) if x['new'] == '1']
        if new_submissions:
            return new_submissions
        else:
            return None
        #print(dumps(new_submissions, indent=4))