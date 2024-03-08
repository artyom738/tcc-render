from datetime import datetime

from charts.top_club_chart import TopClubChart
from model.entity.chart import Chart


def __main__(chart: Chart):
	TopClubChart(chart).render()


if __name__ == '__main__':
	# Chart date format YYYY-MM-DD
	chart = Chart(data={
		'chart_number': 455,
		'chart_date': datetime(2024, 3, 2)
	})
	__main__(chart)
