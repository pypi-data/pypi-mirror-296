import requests
from bits_aviso_python_sdk.helpers import convert_xml_to_dict
from bits_aviso_python_sdk.services.sap.payloads import *


class SAP:
    def __init__(self, username, password, url=None):
        """Initializes the SAP class.

        Args:
            username (str): The username to authenticate with.
            password (str): The password to authenticate with.
            url (str, optional): The URL of the SAP server. Defaults to None.
        """
        self.username = username
        self.password = password
        self.headers = {'Content-Type': 'text/xml; charset=utf-8'}

        if url:
            self.url = url
        else:
            self.url = 'https://pasteur.broadinstitute.org:8005'

    def api_handler(self, endpoint, payload):
        """Handles the API call to the SAP server.

        Args:
            endpoint (str): The endpoint to call.
            payload (str): The payload to send to the SAP server.

        Returns:
            dict, dict: The response data and the error payload.
        """
        # create the url
        url = f'{self.url}{endpoint}'

        # call the api
        response = requests.post(url, headers=self.headers, auth=(self.username, self.password), data=payload)

        # check the response
        if response.status_code != 200:
            return {}, {'Error': f'Unable to call the API. |Error Code {response.status_code}: {response.reason}'}

        else:
            # convert the xml response to json
            sap_data = convert_xml_to_dict(response.content.decode('utf-8'))
            return sap_data, {}

    def get_quote_details(self, quote_number):
        """Gets the quote details from the SAP server.

        Args:
            quote_number (str): The quote number.

        Returns:
            dict, dict: The quote data and the error payload.
        """
        # create the payload
        xml_str = payloads.get_quote_details(quote_number)

        # call the api
        endpoint = '/sap/bc/srt/rfc/sap/zapisdquotedetailsv3/100/zapisdquotedetailsv3service/zapisdquotedetailsv3binding'
        quote_details, quote_details_error = self.api_handler(endpoint, xml_str)

        # check the response
        if quote_details_error:  # add function name to the error payload
            quote_details_error['Function'] = 'get_quote_details'
            return {}, quote_details_error

        else:
            try:
                # parse the quote details
                quote_data = quote_details['soap-env:Envelope']['soap-env:Body']['n0:ZBAPISDQUOTEDETAILSV3Response'][
                    'FUNDINGDET']['item']
                return quote_data, {}

            except KeyError as e:
                quote_details_error['Function'] = 'get_quote_details'
                quote_details_error['Error'] = f'Unable to parse the quote details from the response. | {e}'
                return {}, quote_details_error

    def list_all_quotes(self, sales_org):
        """Lists all the quotes from a given sales org in the SAP server.

        Args:
            sales_org (str): The sales organization to list quotes for.

        Returns:
            list[dict], dict: The quote data and the error payload.
        """
        # create the payload
        xml_str = payloads.list_quotes(sales_org)

        # call the api
        endpoint = '/sap/bc/srt/rfc/sap/zapisdactivequotes/100/zapisdactivequotesservice/zapisdactivequotesbinding'
        quotes, quotes_error = self.api_handler(endpoint, xml_str)

        # check the response
        if quotes_error:
            quotes_error['Function'] = 'list_all_quotes'
            return [], quotes_error

        else:
            try:
                # parse the quotes
                print(quotes)
                quotes_data = quotes['soap-env:Envelope']['soap-env:Body']['n0:ZbapisdactivequotesResponse'][
                    'Newquotationlistd']['item']
                return quotes_data, {}

            except KeyError as e:
                quotes_error['Function'] = 'list_all_quotes'
                quotes_error['Error'] = f'Unable to parse the quotes from the response. | {e}'
                return [], quotes_error
