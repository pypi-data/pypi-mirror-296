from bits_aviso_python_sdk.services.sap import SAP


def test():
    """Test the SAP class."""
    sap = SAP('', '')
    print(sap.get_quote_details(''))


if __name__ == '__main__':
    test()
