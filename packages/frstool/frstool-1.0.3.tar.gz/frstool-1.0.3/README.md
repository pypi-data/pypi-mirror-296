**frstool** is a Python toolkit for providing the Financial Resilience Institute’s white-labelled
consumer financial resilience scoring, harnessing the **Seymour Consulting Index ®** and the Institute’s API
endpoints.

For more information, please visit:
- [Financial Resilience Score](https://financialresiliencescore.com/)
- [Financial Resilience Institute](https://www.finresilienceinstitute.org/)
- [Indicators and Scoring Model](https://www.finresilienceinstitute.org/indicators-and-scoring-model/)
- [Why We Created the Index](https://www.finresilienceinstitute.org/why-we-created-the-index/)


## Installation

Install package using pypi

```python
pip install frstool
```

Pypi project page https://pypi.org/project/frstool/

## Getting Started

```python
from frstool.apiclient import ApiClient
apiclient = ApiClient(api_key="demokey")
```

API access is currently open to all Canadians and global citizens for free financial resilience scoring. Please contact info@finresilienceinstitute.org for more information around B2B white-labelled solutions for your organization.

## Providing Score Tool Questions for Your Users

Collect the Institute’s indicator questions to enable consumer financial resilience scoring:

```python
questions = apiclient.collect_questions()
```

The result is a list of all questions along with available answer options, with each question formatted as a separate dictionary. For example:

```console
{'id': '1',
  'question': 'Overall, how confident are you that you can get through periods of financial hardship resulting from unplanned events?',
  'answers': [{'text': '1', 'value': 1},
   {'text': '2', 'value': 2},
   {'text': '3', 'value': 3},
   {'text': '4', 'value': 4},
   {'text': '5', 'value': 5},
   {'text': '6', 'value': 6},
   {'text': '7', 'value': 7},
   {'text': '8', 'value': 8},
   {'text': '9', 'value': 9},
   {'text': '10', 'value': 10}],
  'type': 'confidence',
  'extents': ['1 - Not at all confident', '10 - Extremely confident'],
  'title': 'Overall, how confident are you that you can get through periods of financial hardship resulting from unplanned events?',
  'isFirst': True}
```

## Formatting Answers

Format answers as a dictionary using question id as dictionary keys. For example:

```console
{0: {'answer': '10',
  'question': 'Overall, how confident are you that you can get through periods of financial hardship resulting from unplanned events?'}}
```

For testing purposes, generate a dictionary containing random answers to all of the questions in questionnaire as follows:

```console
answers = apiclient.generate_mock_answers(questions)
```

## Calculating Financial Resilience Scores

Score the answers using calculate_score() method:

```python
scores = apiclient.calculate_score(answers)
```

Scores will be a dictionary containing financial resilience scores for the questionnaire:

```console
{'index_score': 42,
 'index_score_value_to_compare': 32.87,
 'index_score_result': 28}
```
Where index_score is the final Resilience Score, index_score_value_to_compare is the mean Resilience Score value for all Canadians whom the Financial Resilience Institute polls and serves as the baseline for comparison, and index_score_result is the percentage difference between final index score and this mean value.

## Example

```python
from frstool.apiclient import ApiClient

apiclient = ApiClient(api_key="demokey")
questions = apiclient.collect_questions()
answers = apiclient.generate_mock_answers(questions)
scores = apiclient.calculate_score(answers)

if scores['index_score_result'] > 0:
    print(f"Your score is {scores['index_score']} which is {scores['index_score_result']}% higher than the average score {scores['index_score_value_to_compare']}")
else:
    print(f"Your score is {scores['index_score']} which is {abs(scores['index_score_result'])}% lower than the average score {scores['index_score_value_to_compare']}")
```

## Notes

**Seymour Financial Resilience Index ®** is a registered trademark used under license by the Financial Resilience Society.  
© 2024 Financial Resilience Society DBA Financial Resilience Institute. All rights reserved.

Household categories based on financial resilience scores:
- **Extremely Vulnerable**: Score of 0 to 30
- **Financially Vulnerable**: Score of 30.01 to 50
- **Approaching Resilience**: Score of 50.01 to 70
- **Financially Resilient**: Score of 70.01 to 100

For more information about index development and scoring methodology, visit [Why We Created the Index](https://www.finresilienceinstitute.org/why-we-created-the-index/).
