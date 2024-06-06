from connectors.dark_connector import DarkConnector
from connectors.eht_connector import EurohitConnector
from connectors.tcc_connector import TopClubChartConnector


class ConnectorFactory:
	def get_connector(self, chart_type: str):
		if chart_type == 'eht':
			return EurohitConnector()
		if chart_type == 'tcc':
			return TopClubChartConnector()
		if chart_type == 'dark':
			return DarkConnector()

		raise ValueError(f'ConnectorFactory doesn`t know passed chart type: {chart_type}')
