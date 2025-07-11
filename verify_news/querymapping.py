
from .query import (
    query1, query2, query3, query4, query5, query6, query7, query8, query9, query10,
    query11, query12, query13, query14, query15, query16, query17, query18, query19, query20,
    query21, query22, query23, query24, query25, query26, query27, query28, query29, query30,
    query31, query32, query33, query34, query35, query36, query37, query38, query39, query40,
    query41, query42
)


QUERY_MAP = {
    'InternationalPolitics': {
        'persons': query15,
        'locations': query16,
        'events': query14,
        'organizations': query13,
    },
    'DomesticPolitics': {
        'persons': query19,
        'locations': query20,
        'events': query18,
        'organizations': query17,
    },
    'TechAndInnovation': {
        'persons': query23,
        'locations': query24,
        'events': query22,
        'organizations': query21,
    },
    'ResearchAndSpace': {
        'persons': query27,
        'locations': query28,
        'events': query26,
        'organizations': query25,
    },
    'ScreenAndStage': {
        'persons': query31,
        'locations': query32,
        'events': query30,
        'organizations': query29,
    },
    'MusicAndArts': {
        'persons': query35,
        'locations': query36,
        'events': query34,
        'organizations': query33,
    },
    'Cricket': {
        'persons': query2,
        'locations': query3,
        'events': query4,
        'organizations': query1,
    },
    'Football': {
        'persons': query6,
        'locations': query7,   # NOTE: This query7 appears to be misnamed in your code, double-check if it's for Football venues or Cricket!
        'events': query8,
        'organizations': query5,
    },
    'Other': {
        'persons': query10,
        'locations': query11,
        'events': query12,
        'organizations': query9,
    },
    'CrimeReport': {
        'persons': query38,          # query38 is for witnesses (general CrimeAndJustice persons)
        'locations': query40,
        'events': query39,
        'organizations': query37,    # query37 is for investigations (general CrimeAndJustice orgs)
    },
    'CourtsAndInvestigation': {
        'persons': query38,          # query38 is for witnesses (general CrimeAndJustice persons)
        'locations': query42,
        'events': query41,
        'organizations': query37,    # query37 is for investigations (general CrimeAndJustice orgs)
    }
}
