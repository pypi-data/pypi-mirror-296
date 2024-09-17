from umcn_consent.core import AuthenticatedClient

client = AuthenticatedClient()

status = client.fetch_data(pid="1234567")
