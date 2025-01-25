from connectors.dark_connector import DarkConnector
from connectors.eht_connector import EurohitConnector
from connectors.eht_new_year_connector import EhtNewYearConnector
from connectors.tcc_ny_connector import TccNewYearConnector
from connectors.tcc_connector import TopClubChartConnector


class ConnectorFactory:
	def get_connector(self, chart_type: str):
		if chart_type == 'eht':
			return EurohitConnector()
		if chart_type == 'tcc':
			return TopClubChartConnector()
		if chart_type == 'dark':
			return DarkConnector()
		if chart_type == 'eht_ny':
			return EhtNewYearConnector()
		if chart_type == 'tcc_ny':
			return TccNewYearConnector()

		raise ValueError(f'ConnectorFactory doesn`t know passed chart type: {chart_type}')
