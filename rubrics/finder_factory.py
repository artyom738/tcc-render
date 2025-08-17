class RubricFinderFactory:
    @staticmethod
    def get_rubric_finder(chart_type):
        if chart_type == 'tcc':
            from rubrics.tcc_rubric_finder import TccRubricFinder
            return TccRubricFinder()
        elif chart_type == 'eht':
            from rubrics.eht_rubric_finder import EhtRubricFinder
            return EhtRubricFinder()
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")