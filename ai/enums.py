from django_enumfield.enum import Enum as DjangoEnum


class Sentiment(DjangoEnum):
    positive = 1
    negative = 2
    neutral = 3

    __labels__ = {
        positive: "Positive",
        negative: "Negative",
        neutral: "Neutral",
    }
