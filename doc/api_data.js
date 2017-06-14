define({ "api": [
  {
    "type": "get",
    "url": "/p/getAllSpeeches/{id}/{?date}",
    "title": "MP's speeches",
    "name": "getAllSpeeches",
    "group": "MPs",
    "description": "<p>This function returns a list of all dates when the MP spoke as well as speech ids that happened on those days. The function returns the list as it was compiled on a given date, if no date is supplied the date is today.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>MP's Parladata id.</p>"
          },
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>What historic date does this data correspond with?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results",
            "description": "<p>MP's speeches.</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "results.date",
            "description": "<p>The date of the speech.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results.speeches",
            "description": "<p>List of speeches that happened on this day.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.speeches.session_name",
            "description": "<p>The name of the session at which the speech took place.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.speech_id",
            "description": "<p>Parladata id of the speech.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.session_id",
            "description": "<p>Parladata id of the session at which the speech took place.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"person\": {\n        \"is_active\": false,\n        \"district\": [15],\n        \"name\": \"Luka Mesec\",\n        \"gov_id\": \"P273\",\n        \"gender\": \"m\",\n        \"party\": {\n        \"acronym\": \"ZL\",\n        \"is_coalition\": false,\n        \"id\": 8,\n        \"name\": \"PS Zdru\\u017eena Levica\"\n        },\n        \"type\": \"mp\",\n        \"id\": 58,\n        \"has_function\": false\n    },\n    \"created_at\": \"22. 11. 2016\",\n    \"created_for\": \"28. 8. 2014\",\n    \"results\": [{\n        \"date\": \"28. 8. 2014\",\n        \"speeches\": [{\n        \"session_name\": \"2. izredna seja\",\n        \"speech_id\": 524522,\n        \"session_id\": 5619\n        }, {\n        \"session_name\": \"2. izredna seja\",\n        \"speech_id\": 524403,\n        \"session_id\": 5619\n        }]\n    }, {\n        \"date\": \"25. 8. 2014\",\n        \"speeches\": [{\n        \"session_name\": \"1. izredna seja\",\n        \"speech_id\": 524582,\n        \"session_id\": 5620\n        }, {\n        \"session_name\": \"1. izredna seja\",\n        \"speech_id\": 524665,\n        \"session_id\": 5620\n        }, {\n        \"session_name\": \"1. izredna seja\",\n        \"speech_id\": 524690,\n        \"session_id\": 5620\n        }]\n    }, {\n        \"date\": \"22. 8. 2014\",\n        \"speeches\": [{\n        \"session_name\": \"1. redna seja\",\n        \"speech_id\": 529141,\n        \"session_id\": 5729\n        }, {\n        \"session_name\": \"1. redna seja\",\n        \"speech_id\": 529131,\n        \"session_id\": 5729\n        }]\n    }]\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getAllSpeeches/12",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getAllSpeeches/12/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "MPs"
  },
  {
    "type": "get",
    "url": "/p/getAverageNumberOfSpeechesPerSession/{id}/{?date}",
    "title": "MP's average number of speeches per session",
    "name": "getAverageNumberOfSpeechesPerSession",
    "group": "MPs",
    "description": "<p>This function returns an object with the MPs calculated average number of speeches per session. The function returns the score as it was calculated for a given date, if no date is supplied the date is today.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>MP's Parladata id.</p>"
          },
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>What historic date does this data correspond with?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results",
            "description": "<p>MP's average number of speeches per session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.max",
            "description": "<p>MP (or MPs) who has the highest speeches per session and their score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.max.score",
            "description": "<p>Max MP's score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results.max.mps",
            "description": "<p>A list of MP's with the same maximum score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.max.mps.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "results.max.mps.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.max.mps.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.max.mps.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.max.mps.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.max.mps.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.average",
            "description": "<p>The average score for this metric accross the parliament.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.score",
            "description": "<p>Score for the MP in question.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"person\": {\n        \"is_active\": false,\n        \"district\": [15],\n        \"name\": \"Luka Mesec\",\n        \"gov_id\": \"P273\",\n        \"gender\": \"m\",\n        \"party\": {\n        \"acronym\": \"ZL\",\n        \"is_coalition\": false,\n        \"id\": 8,\n        \"name\": \"PS Zdru\\u017eena Levica\"\n        },\n        \"type\": \"mp\",\n        \"id\": 58,\n        \"has_function\": false\n    },\n    \"created_at\": \"02.11.2016\",\n    \"created_for\": \"06.09.2014\",\n    \"results\": {\n        \"max\": {\n        \"score\": 31.0,\n        \"mps\": [{\n            \"is_active\": false,\n            \"district\": [76],\n            \"name\": \"Milan Brglez\",\n            \"gov_id\": \"P243\",\n            \"gender\": \"m\",\n            \"party\": {\n            \"acronym\": \"SMC\",\n            \"is_coalition\": true,\n            \"id\": 1,\n            \"name\": \"PS Stranka modernega centra\"\n            },\n            \"type\": \"mp\",\n            \"id\": 11,\n            \"has_function\": true\n        }]\n        },\n        \"average\": 2.0,\n        \"score\": 2.0\n    }\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getAverageNumberOfSpeechesPerSession/12",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getAverageNumberOfSpeechesPerSession/12/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "MPs"
  },
  {
    "type": "get",
    "url": "/p/getLastActivity/{id}/{?date}",
    "title": "MP's last activity",
    "name": "getLastActivity",
    "group": "MPs",
    "description": "<p>This function returns an object with the MPs &quot;last activity&quot;. This includes all ballots cast, questions asked and speeches spoken in the past ten days. This function returns the activity as it was calculated for a given date, if no date is supplied the date is today.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>MP's Parladata id.</p>"
          },
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>What historic date does this data correspond with?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "results.date",
            "description": "<p>The date of the events in this object.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results.events",
            "description": "<p>List of event objects for this date.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.events.option",
            "description": "<p>The option on the ballot, if the event was a ballot.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.session_id",
            "description": "<p>Parladata id of the session at which the event took place, if the event was a ballot.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.result",
            "description": "<p>Returns true if the motion was passed, if the event was a ballot.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.vote_name",
            "description": "<p>The name of the vote / text of the motion, if the event was a ballot.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.vote_id",
            "description": "<p>Parladata id of the vote, if the event was a ballot.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.recipient_text",
            "description": "<p>Who was the question addressed to, if the event was a question.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.title",
            "description": "<p>The title of the question, if the event was a question.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.content_url",
            "description": "<p>The url to the PDF of the question, if the event was a question.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.session",
            "description": "<p>Session object, if the event was a question. Currently returns null.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.question_id",
            "description": "<p>Parladata id of the question, if the event was a question.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.session.name",
            "description": "<p>Session name, if the event was a speech.</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "results.session.date_ts",
            "description": "<p>UTF-8 date, if the event was a speech.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results.session.orgs",
            "description": "<p>List of organizations this session belongs to, if the event was a speech.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.session.orgs.acronym",
            "description": "<p>Organization acronym, if the event was a speech.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.session.orgs.is_coalition",
            "description": "<p>If the event was a speech answers the question: Is this organization in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.session.orgs.id",
            "description": "<p>Parladata id of the organization, if the event was a speech.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.session.orgs.name",
            "description": "<p>Name of the organization, if the event was a speech.</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "results.session.date",
            "description": "<p>Slovenian date of the session, if the event was a speech.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.session.org",
            "description": "<p>The primary organization for this session, if the event was a speech.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.session.org.acronym",
            "description": "<p>Organization acronym, if the event was a speech.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.session.org.is_coalition",
            "description": "<p>If the event was a speech answers the question: Is this organization in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.session.org.id",
            "description": "<p>Parladata id of the organization, if the event was a speech.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.session.org.name",
            "description": "<p>Name of the organization, if the event was a speech.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.session.id",
            "description": "<p>Parladata id of the session, if the event ws a speech.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.type",
            "description": "<p>Denotes the type of event (ballot/speech/question).</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"person\": {\n        \"is_active\": false,\n        \"district\": [15],\n        \"name\": \"Luka Mesec\",\n        \"gov_id\": \"P273\",\n        \"gender\": \"m\",\n        \"party\": {\n        \"acronym\": \"ZL\",\n        \"is_coalition\": false,\n        \"id\": 8,\n        \"name\": \"PS Zdru\\u017eena Levica\"\n        },\n        \"type\": \"mp\",\n        \"id\": 58,\n        \"has_function\": false\n    },\n    \"created_at\": \"20. 3. 2017\",\n    \"created_for\": \"20. 3. 2017\",\n    \"results\": [{\n        \"date\": \"20. 3. 2017\",\n        \"events\": [{\n        \"option\": \"za\",\n        \"session_id\": 9379,\n        \"result\": true,\n        \"vote_name\": \"Dnevni red v celoti\",\n        \"vote_id\": 6900,\n        \"type\": \"ballot\"\n        }]\n    }, {\n        \"date\": \"17. 3. 2017\",\n        \"events\": [{\n        \"recipient_text\": \"ministrica za zdravje\",\n        \"title\": \"v zvezi z zakonskim omejevanjem vsebnosti transma\\u0161\\u010dob v \\u017eivilh\",\n        \"content_url\": \"http://imss.dz-rs.si/IMiS/ImisAdmin.nsf/ImisnetAgent?OpenAgent&2&DZ-MSS-01/ca20e0052e10f59269cd589241144a04f18728b6e6935124c6df30d7331d1f5f\",\n        \"session\": null,\n        \"type\": \"question\",\n        \"question_id\": 10180\n        }]\n    }, {\n        \"date\": \"10. 3. 2017\",\n        \"events\": [{\n        \"session\": {\n            \"name\": \"88. redna seja\",\n            \"date_ts\": \"2017-03-10T01:00:00\",\n            \"orgs\": [{\n            \"acronym\": \"\",\n            \"is_coalition\": false,\n            \"id\": 9,\n            \"name\": \"Kolegij predsednika dr\\u017eavnega zbora\"\n            }],\n            \"date\": \"10. 3. 2017\",\n            \"org\": {\n            \"acronym\": \"\",\n            \"is_coalition\": false,\n            \"id\": 9,\n            \"name\": \"Kolegij predsednika dr\\u017eavnega zbora\"\n            },\n            \"id\": 9358,\n            \"in_review\": true\n        },\n        \"speech_id\": 1118501,\n        \"type\": \"speech\"\n        }]\n    }]\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getLastActivity/12",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getLastActivity/12/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "MPs"
  },
  {
    "type": "get",
    "url": "/p/getLeastEqualVoters/{id}/{?date}",
    "title": "MP's least similar voters",
    "name": "getLeastEqualVoters",
    "group": "MPs",
    "description": "<p>This function returns an object with the MPs top 5 least similar voters. The function returns the score as it was calculated for a given date, if no date is supplied the date is today.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>MP's Parladata id.</p>"
          },
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>What historic date does this data correspond with?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results",
            "description": "<p>List of 5 person objects representing MP's least similar voters.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "results.person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "results.ratio",
            "description": "<p>The euclidean distance between the chosen MP and this one.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"person\": {\n        \"is_active\": false,\n        \"district\": [15],\n        \"name\": \"Luka Mesec\",\n        \"gov_id\": \"P273\",\n        \"gender\": \"m\",\n        \"party\": {\n        \"acronym\": \"ZL\",\n        \"is_coalition\": false,\n        \"id\": 8,\n        \"name\": \"PS Zdru\\u017eena Levica\"\n        },\n        \"type\": \"mp\",\n        \"id\": 58,\n        \"has_function\": false\n    },\n    \"created_at\": \"03.11.2016\",\n    \"created_for\": \"28.08.2014\",\n    \"results\": [{\n        \"person\": {\n        \"is_active\": false,\n        \"district\": [60],\n        \"name\": \"Branko Grims\",\n        \"gov_id\": \"P016\",\n        \"gender\": \"m\",\n        \"party\": {\n            \"acronym\": \"SDS\",\n            \"is_coalition\": false,\n            \"id\": 5,\n            \"name\": \"PS Slovenska Demokratska Stranka\"\n        },\n        \"type\": \"mp\",\n        \"id\": 26,\n        \"has_function\": false\n        },\n        \"ratio\": -0.588580815327302\n    }, {\n        \"person\": {\n        \"is_active\": false,\n        \"district\": [94],\n        \"name\": \"An\\u017ee Logar\",\n        \"gov_id\": \"P238\",\n        \"gender\": \"m\",\n        \"party\": {\n            \"acronym\": \"SDS\",\n            \"is_coalition\": false,\n            \"id\": 5,\n            \"name\": \"PS Slovenska Demokratska Stranka\"\n        },\n        \"type\": \"mp\",\n        \"id\": 54,\n        \"has_function\": false\n        },\n        \"ratio\": -0.475334337037446\n    }, {\n        \"person\": {\n        \"is_active\": false,\n        \"district\": [26],\n        \"name\": \"Suzana Lep \\u0160imenko\",\n        \"gov_id\": \"P268\",\n        \"gender\": \"f\",\n        \"party\": {\n            \"acronym\": \"SDS\",\n            \"is_coalition\": false,\n            \"id\": 5,\n            \"name\": \"PS Slovenska Demokratska Stranka\"\n        },\n        \"type\": \"mp\",\n        \"id\": 51,\n        \"has_function\": false\n        },\n        \"ratio\": -0.475334337037446\n    }, {\n        \"person\": {\n        \"is_active\": false,\n        \"district\": [44],\n        \"name\": \"Bojan Podkraj\\u0161ek\",\n        \"gov_id\": \"P277\",\n        \"gender\": \"m\",\n        \"party\": {\n            \"acronym\": \"SDS\",\n            \"is_coalition\": false,\n            \"id\": 5,\n            \"name\": \"PS Slovenska Demokratska Stranka\"\n        },\n        \"type\": \"mp\",\n        \"id\": 64,\n        \"has_function\": false\n        },\n        \"ratio\": -0.475334337037446\n    }, {\n        \"person\": {\n        \"is_active\": false,\n        \"district\": [7],\n        \"name\": \"Anja Bah \\u017dibert\",\n        \"gov_id\": \"P239\",\n        \"gender\": \"f\",\n        \"party\": {\n            \"acronym\": \"SDS\",\n            \"is_coalition\": false,\n            \"id\": 5,\n            \"name\": \"PS Slovenska Demokratska Stranka\"\n        },\n        \"type\": \"mp\",\n        \"id\": 2,\n        \"has_function\": false\n        },\n        \"ratio\": -0.475334337037446\n    }]\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getLeastEqualVoters/12",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getLeastEqualVoters/12/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "MPs"
  },
  {
    "type": "get",
    "url": "/p/getMPStatic/{id}/{?date}",
    "title": "MP's static info",
    "name": "getMPStatic",
    "group": "MPs",
    "description": "<p>This function returns an object with all &quot;static&quot; data belonging to an MP. By static we mean that it is entered and maintained by hand and rarely, if ever, changes.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>MP's Parladata id.</p>"
          },
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>What historic date does this data correspond with?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.voters",
            "description": "<p>Number of voters who voted for this MP at the last election.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.acronym",
            "description": "<p>This MP's party acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.mandate",
            "description": "<p>Number of this MP's mandates in the national assembly (including their current one).</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.party_id",
            "description": "<p>This MP's party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results.groups",
            "description": "<p>List of groups this MP is a member of (other than their party). #TODO refactor</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.groups.id",
            "description": "<p>Group's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.groups.group_name",
            "description": "<p>Group's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.education",
            "description": "<p>A string describing the education of this person.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results.working_bodies_functions",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.working_bodies_functions.role",
            "description": "<p>The person's role in this working body.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.working_bodies_functions.wb",
            "description": "<p>Working body object.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.working_bodies_functions.wb.acronym",
            "description": "<p>Working body's acronym (usually an empty string).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.working_bodies_functions.wb.is_coalition",
            "description": "<p>Answers the question: Does this working body belong to the coalition?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.working_bodies_functions.wb.id",
            "description": "<p>Working body's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.working_bodies_functions.wb.name",
            "description": "<p>The working body's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.previous_occupation",
            "description": "<p>MP's occupation before becoming an MP.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.name",
            "description": "<p>MP's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "results.district",
            "description": "<p>List of strings representing district names.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.age",
            "description": "<p>MP's age calculated from their birthday.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results.social",
            "description": "<p>An array containing the object with social keys. #TODO refactor</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.social.twitter",
            "description": "<p>MP's Twitter url.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.social.facebook",
            "description": "<p>MP's Facebook url.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.social.linkedin",
            "description": "<p>MP's Linkedin url.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.party",
            "description": "<p>MP's party name.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"person\": {\n        \"is_active\": true,\n        \"district\": [15],\n        \"name\": \"Luka Mesec\",\n        \"gov_id\": \"P273\",\n        \"gender\": \"m\",\n        \"party\": {\n        \"acronym\": \"ZL\",\n        \"is_coalition\": false,\n        \"id\": 8,\n        \"name\": \"PS Zdru\\u017eena Levica\"\n        },\n        \"type\": \"mp\",\n        \"id\": 58,\n        \"has_function\": false\n    },\n    \"created_at\": \"08.03.2017\",\n    \"created_for\": \"06.08.2014\",\n    \"results\": {\n        \"voters\": 919,\n        \"acronym\": \"ZL\",\n        \"mandates\": 1,\n        \"party_id\": 8,\n        \"groups\": [{\n        \"group_id\": 9,\n        \"group_name\": \"Kolegij predsednika dr\\u017eavnega zbora\"\n        }, {\n        \"group_id\": 34,\n        \"group_name\": \"Delegacija Dr\\u017eavnega zbora v Parlamentarni skup\\u0161\\u010dini Unije za Sredozemlje\"\n        }],\n        \"education\": \"diplomant univerzitetnega programa\\r\\n\",\n        \"working_bodies_functions\": [{\n        \"role\": \"vice_president\",\n        \"wb\": {\n            \"acronym\": \"\",\n            \"is_coalition\": false,\n            \"id\": 10,\n            \"name\": \"Komisija za nadzor javnih financ\"\n        }\n        }],\n        \"previous_occupation\": \"\\u0161tudent\",\n        \"name\": \"Luka Mesec\",\n        \"district\": [\"Trbovlje\"],\n        \"age\": 29,\n        \"social\": [{\n        \"twitter\": \"https://twitter.com/lukamesec\",\n        \"facebook\": \"https://www.facebook.com/mesec.luka\",\n        \"linkedin\": null\n        }],\n        \"party\": \"PS Zdru\\u017eena Levica\"\n    }\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getMPStatic/12",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getMPStatic/12/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "MPs"
  },
  {
    "type": "get",
    "url": "/p/getMembershipsOfMember/{?date}",
    "title": "MP's memberships",
    "name": "getMembershipsOfMember",
    "group": "MPs",
    "description": "<p>This function returns an object with all the memberships the MP holds in various organizations. The function returns the memberships as they were calculated for a given date, if no date is supplied it is assumed the date is today.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>MP's Parladata id</p>"
          },
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "memberships",
            "description": "<p>MP's memberships categorised by organization type.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "memberships.kolegij",
            "description": "<p>MP's memberships in &quot;kolegij&quot;-type organizations.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.kolegij.url",
            "description": "<p>Organization's url.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.kolegij.org_type",
            "description": "<p>Organization type.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "memberships.kolegij.org_id",
            "description": "<p>Organization's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.kolegij.name",
            "description": "<p>The name of the organization.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "memberships.skupina_prijateljstva",
            "description": "<p>MP's memberships in &quot;skupina prijateljstva&quot;-type organizations.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.skupina_prijateljstva.url",
            "description": "<p>Organization's url.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.skupina_prijateljstva.org_type",
            "description": "<p>Organization type.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "memberships.skupina_prijateljstva.org_id",
            "description": "<p>Organization's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.skupina_prijateljstva.name",
            "description": "<p>The name of the organization.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "memberships.delegacija",
            "description": "<p>MP's memberships in &quot;delegacija&quot;-type organizations.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.delegacija.url",
            "description": "<p>Organization's url.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.delegacija.org_type",
            "description": "<p>Organization type.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "memberships.delegacija.org_id",
            "description": "<p>Organization's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.delegacija.name",
            "description": "<p>The name of the organization.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "memberships.komisija",
            "description": "<p>MP's memberships in &quot;komisija&quot;-type organizations.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.komisija.url",
            "description": "<p>Organization's url.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.komisija.org_type",
            "description": "<p>Organization type.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "memberships.komisija.org_id",
            "description": "<p>Organization's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.komisija.name",
            "description": "<p>The name of the organization.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "memberships.poslanska_skupina",
            "description": "<p>MP's memberships in &quot;poslanska skupina&quot;-type organizations.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.poslanska_skupina.url",
            "description": "<p>Organization's url.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.poslanska_skupina.org_type",
            "description": "<p>Organization type.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "memberships.poslanska_skupina.org_id",
            "description": "<p>Organization's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.poslanska_skupina.name",
            "description": "<p>The name of the organization.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "memberships.odbor",
            "description": "<p>MP's memberships in &quot;odbor&quot;-type organizations.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.odbor.url",
            "description": "<p>Organization's url.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.odbor.org_type",
            "description": "<p>Organization type.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "memberships.odbor.org_id",
            "description": "<p>Organization's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.odbor.name",
            "description": "<p>The name of the organization.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "memberships.preiskovalna_komisija",
            "description": "<p>MP's memberships in &quot;preiskovalna komisija&quot;-type organizations.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.preiskovalna_komisija.url",
            "description": "<p>Organization's url.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.preiskovalna_komisija.org_type",
            "description": "<p>Organization type.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "memberships.preiskovalna_komisija.org_id",
            "description": "<p>Organization's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "memberships.preiskovalna_komisija.name",
            "description": "<p>The name of the organization.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>What historic date does this data correspond with?</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"created_at\": \"21.03.2017\",\n    \"created_for\": \"17.02.2017\",\n    \"data\": [{\n        \"person\": {\n        \"is_active\": false,\n        \"district\": [7],\n        \"name\": \"Anja Bah \\u017dibert\",\n        \"gov_id\": \"P239\",\n        \"gender\": \"f\",\n        \"party\": {\n            \"acronym\": \"SDS\",\n            \"is_coalition\": false,\n            \"id\": 5,\n            \"name\": \"PS Slovenska Demokratska Stranka\"\n        },\n        \"type\": \"mp\",\n        \"id\": 2,\n        \"has_function\": false\n        },\n        \"score\": {\n        \"vT1\": 0.18281964948320664,\n        \"vT2\": -0.05594373814997616\n        }\n    }, {\n        \"person\": {\n        \"is_active\": false,\n        \"district\": [8],\n        \"name\": \"Ur\\u0161ka Ban\",\n        \"gov_id\": \"P240\",\n        \"gender\": \"f\",\n        \"party\": {\n            \"acronym\": \"SMC\",\n            \"is_coalition\": true,\n            \"id\": 1,\n            \"name\": \"PS Stranka modernega centra\"\n        },\n        \"type\": \"mp\",\n        \"id\": 3,\n        \"has_function\": false\n        },\n        \"score\": {\n        \"vT1\": -0.06505089721256502,\n        \"vT2\": -0.1438729944923539\n        }\n    }]\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getMembershipsOfMember/",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getMembershipsOfMember/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "MPs"
  },
  {
    "type": "get",
    "url": "/p/getMostEqualVoters/{id}/{?date}",
    "title": "MP's most similar voters",
    "name": "getMostEqualVoters",
    "group": "MPs",
    "description": "<p>This function returns an object with the MPs top 5 most similar voters. The function returns the score as it was calculated for a given date, if no date is supplied the date is today.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>MP's Parladata id.</p>"
          },
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>What historic date does this data correspond with?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results",
            "description": "<p>List of 5 person objects representing MP's most similar voters.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "results.person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "results.ratio",
            "description": "<p>The euclidean distance between the chosen MP and this one.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"person\": {\n        \"is_active\": false,\n        \"district\": [15],\n        \"name\": \"Luka Mesec\",\n        \"gov_id\": \"P273\",\n        \"gender\": \"m\",\n        \"party\": {\n        \"acronym\": \"ZL\",\n        \"is_coalition\": false,\n        \"id\": 8,\n        \"name\": \"PS Zdru\\u017eena Levica\"\n        },\n        \"type\": \"mp\",\n        \"id\": 58,\n        \"has_function\": false\n    },\n    \"created_at\": \"03.11.2016\",\n    \"created_for\": \"28.08.2014\",\n    \"results\": [{\n        \"person\": {\n        \"is_active\": false,\n        \"district\": [103],\n        \"name\": \"Violeta Tomi\\u0107\",\n        \"gov_id\": \"P289\",\n        \"gender\": \"f\",\n        \"party\": {\n            \"acronym\": \"ZL\",\n            \"is_coalition\": false,\n            \"id\": 8,\n            \"name\": \"PS Zdru\\u017eena Levica\"\n        },\n        \"type\": \"mp\",\n        \"id\": 80,\n        \"has_function\": false\n        },\n        \"ratio\": 0.584624087008587\n    }, {\n        \"person\": {\n        \"is_active\": false,\n        \"district\": [49],\n        \"name\": \"Franc Tr\\u010dek \",\n        \"gov_id\": \"P290\",\n        \"gender\": \"m\",\n        \"party\": {\n            \"acronym\": \"ZL\",\n            \"is_coalition\": false,\n            \"id\": 8,\n            \"name\": \"PS Zdru\\u017eena Levica\"\n        },\n        \"type\": \"mp\",\n        \"id\": 82,\n        \"has_function\": false\n        },\n        \"ratio\": 0.541776627164668\n    }, {\n        \"person\": {\n        \"is_active\": false,\n        \"district\": [76],\n        \"name\": \"Matja\\u017e Han\\u017eek\",\n        \"gov_id\": \"P256\",\n        \"gender\": \"m\",\n        \"party\": {\n            \"acronym\": \"ZL\",\n            \"is_coalition\": false,\n            \"id\": 8,\n            \"name\": \"PS Zdru\\u017eena Levica\"\n        },\n        \"type\": \"mp\",\n        \"id\": 31,\n        \"has_function\": false\n        },\n        \"ratio\": 0.538931817860966\n    }, {\n        \"person\": {\n        \"is_active\": false,\n        \"district\": [83],\n        \"name\": \"Matej Ta\\u0161ner Vatovec\",\n        \"gov_id\": \"P288\",\n        \"gender\": \"m\",\n        \"party\": {\n            \"acronym\": \"ZL\",\n            \"is_coalition\": false,\n            \"id\": 8,\n            \"name\": \"PS Zdru\\u017eena Levica\"\n        },\n        \"type\": \"mp\",\n        \"id\": 79,\n        \"has_function\": false\n        },\n        \"ratio\": 0.494254483850995\n    }, {\n        \"person\": {\n        \"is_active\": false,\n        \"district\": [46],\n        \"name\": \"Branislav Raji\\u0107\",\n        \"gov_id\": \"P281\",\n        \"gender\": \"m\",\n        \"party\": {\n            \"acronym\": \"SMC\",\n            \"is_coalition\": true,\n            \"id\": 1,\n            \"name\": \"PS Stranka modernega centra\"\n        },\n        \"type\": \"mp\",\n        \"id\": 70,\n        \"has_function\": false\n        },\n        \"ratio\": 0.384675997982625\n    }]\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getMostEqualVoters/12",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getMostEqualVoters/12/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "MPs"
  },
  {
    "type": "get",
    "url": "/p/getNumberOfQuestions/{id}/{?date}",
    "title": "MP's number of questions",
    "name": "getNumberOfQuestions",
    "group": "MPs",
    "description": "<p>This function returns an object with the MPs calculated number of questions (like PM's questions in the UK). The function returns the score as it was calculated for a given date, if no date is supplied the date is today.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>MP's Parladata id.</p>"
          },
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>What historic date does this data correspond with?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results",
            "description": "<p>MP's number of questions.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.max",
            "description": "<p>MP (or MPs) who has the highest number of questions and their score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.max.score",
            "description": "<p>Max MP's score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results.max.mps",
            "description": "<p>A list of MP's with the same maximum score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.max.mps.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "results.max.mps.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.max.mps.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.max.mps.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.max.mps.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.max.mps.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "results.average",
            "description": "<p>The average score for this metric accross the parliament.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.score",
            "description": "<p>Score for the MP in question.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"person\": {\n        \"is_active\": false,\n        \"district\": [15],\n        \"name\": \"Luka Mesec\",\n        \"gov_id\": \"P273\",\n        \"gender\": \"m\",\n        \"party\": {\n        \"acronym\": \"ZL\",\n        \"is_coalition\": false,\n        \"id\": 8,\n        \"name\": \"PS Zdru\\u017eena Levica\"\n        },\n        \"type\": \"mp\",\n        \"id\": 58,\n        \"has_function\": false\n    },\n    \"created_at\": \"21.03.2017\",\n    \"created_for\": \"20.03.2017\",\n    \"results\": {\n        \"max\": {\n        \"score\": 672449,\n        \"mps\": [{\n            \"is_active\": false,\n            \"district\": [17],\n            \"name\": \"Jo\\u017eef Horvat\",\n            \"gov_id\": \"P020\",\n            \"gender\": \"m\",\n            \"party\": {\n            \"acronym\": \"NSI\",\n            \"is_coalition\": false,\n            \"id\": 6,\n            \"name\": \"PS Nova Slovenija\"\n            },\n            \"type\": \"mp\",\n            \"id\": 32,\n            \"has_function\": false\n        }]\n        },\n        \"average\": 177115,\n        \"score\": 381389\n    }\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getNumberOfQuestions/12",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getNumberOfQuestions/12/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "MPs"
  },
  {
    "type": "get",
    "url": "/p/getNumberOfSpokenWords/{id}/{?date}",
    "title": "MP's number of spoken words",
    "name": "getNumberOfSpokenWords",
    "group": "MPs",
    "description": "<p>This function returns an object with the MPs calculated number of spoken words. The function returns the score as it was calculated for a given date, if no date is supplied the date is today.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>MP's Parladata id.</p>"
          },
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>What historic date does this data correspond with?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results",
            "description": "<p>MP's number of spoken words.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.max",
            "description": "<p>MP (or MPs) who has the highest number of spoken words and their score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "results.max.score",
            "description": "<p>Max MP's score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results.max.mps",
            "description": "<p>A list of MP's with the same maximum score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.max.mps.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "results.max.mps.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.max.mps.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.max.mps.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.max.mps.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.max.mps.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "results.average",
            "description": "<p>The average score for this metric accross the parliament.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "results.score",
            "description": "<p>Score for the MP in question.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"person\": {\n        \"is_active\": false,\n        \"district\": [15],\n        \"name\": \"Luka Mesec\",\n        \"gov_id\": \"P273\",\n        \"gender\": \"m\",\n        \"party\": {\n        \"acronym\": \"ZL\",\n        \"is_coalition\": false,\n        \"id\": 8,\n        \"name\": \"PS Zdru\\u017eena Levica\"\n        },\n        \"type\": \"mp\",\n        \"id\": 58,\n        \"has_function\": false\n    },\n    \"created_at\": \"21.03.2017\",\n    \"created_for\": \"20.03.2017\",\n    \"results\": {\n        \"max\": {\n        \"score\": 672449,\n        \"mps\": [{\n            \"is_active\": false,\n            \"district\": [17],\n            \"name\": \"Jo\\u017eef Horvat\",\n            \"gov_id\": \"P020\",\n            \"gender\": \"m\",\n            \"party\": {\n            \"acronym\": \"NSI\",\n            \"is_coalition\": false,\n            \"id\": 6,\n            \"name\": \"PS Nova Slovenija\"\n            },\n            \"type\": \"mp\",\n            \"id\": 32,\n            \"has_function\": false\n        }]\n        },\n        \"average\": 177115,\n        \"score\": 381389\n    }\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getNumberOfSpokenWords/12",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getNumberOfSpokenWords/12/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "MPs"
  },
  {
    "type": "get",
    "url": "/p/getPresence/{id}/{?date}",
    "title": "MP's presence",
    "name": "getPresence",
    "group": "MPs",
    "description": "<p>This function returns an object with the MPs calculated presence scores. There are two scores, one for their presence at voting events and one for their presence at sessions overall. The function returns the score as it was calculated for a given date, if no date is supplied the date is today.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>MP's Parladata id.</p>"
          },
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>What historic date does this data correspond with?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.votes",
            "description": "<p>MP's calculated presence at voting events.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.votes.max",
            "description": "<p>MP (or MPs) who has the highest attendance and their score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "results.votes.max.score",
            "description": "<p>Max MP's score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results.votes.max.mps",
            "description": "<p>A list of MP's with the same maximum score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.votes.max.mps.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "results.votes.max.mps.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.votes.max.mps.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.votes.max.mps.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.votes.max.mps.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.votes.max.mps.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.votes.max.mps.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.votes.max.mps.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.votes.max.mps.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.votes.max.mps.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.votes.max.mps.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.votes.max.mps.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "results.votes.average",
            "description": "<p>The average score for this metric accross the parliament.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "results.votes.score",
            "description": "<p>Score for the MP in question.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.sessions",
            "description": "<p>MP's calculated presence at sessions.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.sessions.max",
            "description": "<p>MP (or MPs) who has the highest attendance and their score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "results.sessions.max.score",
            "description": "<p>Max MP's score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results.sessions.max.mps",
            "description": "<p>A list of MP's with the same maximum score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.sessions.max.mps.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "results.sessions.max.mps.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.sessions.max.mps.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.sessions.max.mps.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.sessions.max.mps.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.sessions.max.mps.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.sessions.max.mps.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.sessions.max.mps.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.sessions.max.mps.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.sessions.max.mps.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.sessions.max.mps.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.sessions.max.mps.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"person\": {\n        \"is_active\": false,\n        \"district\": [15],\n        \"name\": \"Luka Mesec\",\n        \"gov_id\": \"P273\",\n        \"gender\": \"m\",\n        \"party\": {\n        \"acronym\": \"ZL\",\n        \"is_coalition\": false,\n        \"id\": 8,\n        \"name\": \"PS Zdru\\u017eena Levica\"\n        },\n        \"type\": \"mp\",\n        \"id\": 58,\n        \"has_function\": false\n    },\n    \"created_at\": \"21.03.2017\",\n    \"created_for\": \"17.02.2017\",\n    \"results\": {\n        \"votes\": {\n        \"max\": {\n            \"score\": 98.5804416403786,\n            \"mps\": [{\n            \"is_active\": false,\n            \"district\": [8],\n            \"name\": \"Ur\\u0161ka Ban\",\n            \"gov_id\": \"P240\",\n            \"gender\": \"f\",\n            \"party\": {\n                \"acronym\": \"SMC\",\n                \"is_coalition\": true,\n                \"id\": 1,\n                \"name\": \"PS Stranka modernega centra\"\n            },\n            \"type\": \"mp\",\n            \"id\": 3,\n            \"has_function\": false\n            }]\n        },\n        \"average\": 80.5083236752256,\n        \"score\": 76.9716088328076\n        },\n        \"sessions\": {\n        \"max\": {\n            \"score\": 100.0,\n            \"mps\": [{\n            \"is_active\": false,\n            \"district\": [84],\n            \"name\": \"Vlasta Po\\u010dkaj\",\n            \"gov_id\": \"P303\",\n            \"gender\": \"f\",\n            \"party\": {\n                \"acronym\": \"SMC\",\n                \"is_coalition\": true,\n                \"id\": 1,\n                \"name\": \"PS Stranka modernega centra\"\n            },\n            \"type\": \"mp\",\n            \"id\": 2934,\n            \"has_function\": false\n            }, {\n            \"is_active\": false,\n            \"district\": [85],\n            \"name\": \"Teja Ljubi\\u010d\",\n            \"gov_id\": \"P304\",\n            \"gender\": \"f\",\n            \"party\": {\n                \"acronym\": \"SMC\",\n                \"is_coalition\": true,\n                \"id\": 1,\n                \"name\": \"PS Stranka modernega centra\"\n            },\n            \"type\": \"mp\",\n            \"id\": 2933,\n            \"has_function\": false\n            }, {\n            \"is_active\": false,\n            \"district\": [48],\n            \"name\": \"Jasna Murgel\",\n            \"gov_id\": \"P274\",\n            \"gender\": \"f\",\n            \"party\": {\n                \"acronym\": \"SMC\",\n                \"is_coalition\": true,\n                \"id\": 1,\n                \"name\": \"PS Stranka modernega centra\"\n            },\n            \"type\": \"mp\",\n            \"id\": 60,\n            \"has_function\": false\n            }, {\n            \"is_active\": false,\n            \"district\": [66],\n            \"name\": \"Julijana Bizjak Mlakar\",\n            \"gov_id\": \"P158\",\n            \"gender\": \"f\",\n            \"party\": {\n                \"acronym\": \"DeSUS\",\n                \"is_coalition\": true,\n                \"id\": 3,\n                \"name\": \"PS Demokratska Stranka Upokojencev Slovenije\"\n            },\n            \"type\": \"mp\",\n            \"id\": 5,\n            \"has_function\": false\n            }]\n        },\n        \"average\": 88.5490589303276,\n        \"score\": 85.5072463768116\n        }\n    }\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getPresence/12",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getPresence/12/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "MPs"
  },
  {
    "type": "get",
    "url": "/p/getPresenceThroughTime/{id}/{?date}",
    "title": "MP's presence through time",
    "name": "getPresenceThroughTime",
    "group": "MPs",
    "description": "<p>This function returns an object with the MPs calculated presence at votes through time. The function returns the score as it was calculated for a given date, if no date is supplied the date is today.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>MP's Parladata id.</p>"
          },
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>What historic date does this data correspond with?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results",
            "description": "<p>List of objects for MP's presence for every month since the beginning of the current Parliament's term.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.vote_count",
            "description": "<p>Total number of votes that happened this month.</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "results.date_ts",
            "description": "<p>UTF-8 formatted date - first of the month.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.not_member",
            "description": "<p>Percentage of votes where this person was not yet a MP.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "results.presence",
            "description": "<p>Percentage of votes this person attended.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"person\": {\n        \"is_active\": false,\n        \"district\": [15],\n        \"name\": \"Luka Mesec\",\n        \"gov_id\": \"P273\",\n        \"gender\": \"m\",\n        \"party\": {\n        \"acronym\": \"ZL\",\n        \"is_coalition\": false,\n        \"id\": 8,\n        \"name\": \"PS Zdru\\u017eena Levica\"\n        },\n        \"type\": \"mp\",\n        \"id\": 58,\n        \"has_function\": false\n    },\n    \"created_at\": \"28.02.2017\",\n    \"created_for\": \"28.02.2017\",\n    \"results\": [{\n        \"vote_count\": 17,\n        \"date_ts\": \"2014-08-01T00:00:00\",\n        \"not_member\": 0,\n        \"presence\": 70.58823529411765\n    }, {\n        \"vote_count\": 15,\n        \"date_ts\": \"2014-09-01T00:00:00\",\n        \"not_member\": 0,\n        \"presence\": 60.0\n    }, {\n        \"vote_count\": 4,\n        \"date_ts\": \"2014-10-01T00:00:00\",\n        \"not_member\": 0,\n        \"presence\": 100.0\n    }, {\n        \"vote_count\": 58,\n        \"date_ts\": \"2014-11-01T00:00:00\",\n        \"not_member\": 0,\n        \"presence\": 70.6896551724138\n    }, {\n        \"vote_count\": 61,\n        \"date_ts\": \"2014-12-01T00:00:00\",\n        \"not_member\": 0,\n        \"presence\": 27.86885245901639\n    }]\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getPresenceThroughTime/12",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getPresenceThroughTime/12/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "MPs"
  },
  {
    "type": "get",
    "url": "/p/getQuestions/{id}/{?date}",
    "title": "MP's questions",
    "name": "getQuestions",
    "group": "MPs",
    "description": "<p>This function returns an object with the MPs questions, ordered by date, grouped by day. The function returns the ballots until a given date, if no date is supplied it is assumed the date is today.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>MP's Parladata id.</p>"
          },
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>What historic date does this data correspond with?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results",
            "description": "<p>MP's questions grouped by date.</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "results.date",
            "description": "<p>The date in question.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results.questions",
            "description": "<p>Questions the MP submitted on that day.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.questions.recipient_text",
            "description": "<p>Recipient in text form as written on www.dz-rs.si.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.questions.url",
            "description": "<p>URL to the relevant question document.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.questions.title",
            "description": "<p>Question title.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.questions.id",
            "description": "<p>Parladata id of the question.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.questions.session_id",
            "description": "<p>Parladata id of the session where this question was asked.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.questions.session_name",
            "description": "<p>Name of the session where this question was asked.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"person\": {\n        \"is_active\": false,\n        \"district\": [15],\n        \"name\": \"Luka Mesec\",\n        \"gov_id\": \"P273\",\n        \"gender\": \"m\",\n        \"party\": {\n        \"acronym\": \"ZL\",\n        \"is_coalition\": false,\n        \"id\": 8,\n        \"name\": \"PS Zdru\\u017eena Levica\"\n        },\n        \"type\": \"mp\",\n        \"id\": 58,\n        \"has_function\": false\n    },\n    \"created_at\": \"11. 1. 2017\",\n    \"created_for\": \"12. 12. 2014\",\n    \"results\": [{\n        \"date\": \"12. 12. 2014\",\n        \"questions\": [{\n        \"recipient_text\": \"minister za gospodarski razvoj in tehnologijo, ministrica za okolje in prostor\",\n        \"title\": \"v zvezi s problematiko Cinkarne Celje in z njo povezanim okoljskim stanjem v Celju\",\n        \"url\": \"http://imss.dz-rs.si/IMiS/ImisAdmin.nsf/ImisnetAgent?OpenAgent&2&DZ-MSS-01/ca20e0052d5fcd92e4bdfad7c16c7458916c91f48725827616fb01493db37336\",\n        \"session_id\": \"Unknown\",\n        \"session_name\": \"Unknown\",\n        \"id\": 5401\n        }]\n    }, {\n        \"date\": \"14. 11. 2014\",\n        \"questions\": [{\n        \"recipient_text\": \"predsednik Vlade\",\n        \"title\": \"v zvezi s pripravami na privatizacijo DARS-a in strategijo upravljanja z dr\\u017eavnim premo\\u017eenjem\",\n        \"url\": \"http://imss.dz-rs.si/IMiS/ImisAdmin.nsf/ImisnetAgent?OpenAgent&2&DZ-MSS-01/ca20e00560147f954c0d998b6c8f4da8aacddff0adf58593742b0fa62dc39b11\",\n        \"session_id\": \"Unknown\",\n        \"session_name\": \"Unknown\",\n        \"id\": 5232\n        }, {\n        \"recipient_text\": \"minister za infrastrukturo\",\n        \"title\": \"v zvezi z ohranitvijo delovnih mest v Zasavju\",\n        \"url\": \"http://imss.dz-rs.si/IMiS/ImisAdmin.nsf/ImisnetAgent?OpenAgent&2&DZ-MSS-01/ca20e00544d15404319afbf78aa095c9c6cc3d29459887062737389aab9c7829\",\n        \"session_id\": \"Unknown\",\n        \"session_name\": \"Unknown\",\n        \"id\": 5234\n        }]\n    }, {\n        \"date\": \"29. 10. 2014\",\n        \"questions\": [{\n        \"recipient_text\": \"minister za finance v funkciji ministra za gospodarski razvoj in tehnologijo\",\n        \"title\": \"z zvezi z vrnitvijo glasovalnih pravic RS in povezanih dru\\u017eb v dru\\u017ebah Telekom d.d. in Zavarovalnico Triglav d.d.\",\n        \"url\": \"http://imss.dz-rs.si/IMiS/ImisAdmin.nsf/ImisnetAgent?OpenAgent&2&DZ-MSS-01/ca20e0052e4c3e7a939ddd5a2c137009af60900edcdabf8632dd7d796f2f8bcd\",\n        \"session_id\": 5615,\n        \"session_name\": \"6. izredna seja\",\n        \"id\": 5109\n        }]\n    }]\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getQuestions/12",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getQuestions/12/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "MPs"
  },
  {
    "type": "get",
    "url": "/p/getStyleScores/{id}/{?date}",
    "title": "MP's style scores",
    "name": "getStyleScores",
    "group": "MPs",
    "description": "<p>This function returns an object with the MPs style scores. The function returns the scores as they were calculated for a given date. If no date is supplied it is assumed the date is today.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>MP's Parladata id.</p>"
          },
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>What historic date does this data correspond with?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results",
            "description": "<p>MP's style scores.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "results.problematicno",
            "description": "<p>MP's &quot;problematic&quot; language score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "results.preprosto",
            "description": "<p>MP's &quot;simple&quot; language score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "results.privzdignjeno",
            "description": "<p>MP's &quot;fancy&quot; language score.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"person\": {\n        \"is_active\": false,\n        \"district\": [15],\n        \"name\": \"Luka Mesec\",\n        \"gov_id\": \"P273\",\n        \"gender\": \"m\",\n        \"party\": {\n        \"acronym\": \"ZL\",\n        \"is_coalition\": false,\n        \"id\": 8,\n        \"name\": \"PS Zdru\\u017eena Levica\"\n        },\n        \"type\": \"mp\",\n        \"id\": 58,\n        \"has_function\": false\n    },\n    \"created_at\": \"02.11.2016\",\n    \"created_for\": \"06.09.2014\",\n    \"results\": {\n        \"problematicno\": 0.6451263190481497,\n        \"preprosto\": 1.0269481824385878,\n        \"privzdignjeno\": 0\n    }\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getStyleScores/12",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getStyleScores/12/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "MPs"
  },
  {
    "type": "get",
    "url": "/p/getTFIDF/{id}/{?date}",
    "title": "MP's top TFIDF terms",
    "name": "getTFIDF",
    "group": "MPs",
    "description": "<p>This function returns an object with the MPs top TFIDF terms. It returns between 10 and 15 terms, depending on the topical overlap of the top 15 terms. The function returns the score as it was calculated for a given date, if no date is supplied it is assumed the date is today.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>MP's Parladata id.</p>"
          },
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>What historic date does this data correspond with?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results",
            "description": "<p>MP's top TFIDF words (between 10 and 15).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.term",
            "description": "<p>The term in question.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.scores",
            "description": "<p>TFIDF scores</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.scores.tf",
            "description": "<p>Term frequency.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.scores.df",
            "description": "<p>Document frequency.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "results.scores.tf-idf",
            "description": "<p>TF/DF.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"person\": {\n        \"is_active\": false,\n        \"district\": [15],\n        \"name\": \"Luka Mesec\",\n        \"gov_id\": \"P273\",\n        \"gender\": \"m\",\n        \"party\": {\n        \"acronym\": \"ZL\",\n        \"is_coalition\": false,\n        \"id\": 8,\n        \"name\": \"PS Zdru\\u017eena Levica\"\n        },\n        \"type\": \"mp\",\n        \"id\": 58,\n        \"has_function\": false\n    },\n    \"created_at\": \"20.02.2017\",\n    \"created_for\": \"20.02.2017\",\n    \"results\": [{\n        \"term\": \"transma\\u0161\\u010doba\",\n        \"scores\": {\n        \"tf\": 27,\n        \"df\": 30,\n        \"tf-idf\": 0.9\n        }\n    }, {\n        \"term\": \"transma\\u0161\\u010doben\",\n        \"scores\": {\n        \"tf\": 12,\n        \"df\": 14,\n        \"tf-idf\": 0.8571428571428571\n        }\n    }, {\n        \"term\": \"borznoposredni\\u0161ki\",\n        \"scores\": {\n        \"tf\": 47,\n        \"df\": 59,\n        \"tf-idf\": 0.7966101694915254\n        }\n    }, {\n        \"term\": \"soupravljanje\",\n        \"scores\": {\n        \"tf\": 82,\n        \"df\": 126,\n        \"tf-idf\": 0.6507936507936508\n        }\n    }, {\n        \"term\": \"trgovalen\",\n        \"scores\": {\n        \"tf\": 49,\n        \"df\": 80,\n        \"tf-idf\": 0.6125\n        }\n    }, {\n        \"term\": \"Cinven\",\n        \"scores\": {\n        \"tf\": 35,\n        \"df\": 63,\n        \"tf-idf\": 0.5555555555555556\n        }\n    }, {\n        \"term\": \"borzen\",\n        \"scores\": {\n        \"tf\": 60,\n        \"df\": 114,\n        \"tf-idf\": 0.5263157894736842\n        }\n    }, {\n        \"term\": \"Alpina\",\n        \"scores\": {\n        \"tf\": 37,\n        \"df\": 82,\n        \"tf-idf\": 0.45121951219512196\n        }\n    }, {\n        \"term\": \"kislina\",\n        \"scores\": {\n        \"tf\": 14,\n        \"df\": 32,\n        \"tf-idf\": 0.4375\n        }\n    }, {\n        \"term\": \"obvezni\\u010dar\",\n        \"scores\": {\n        \"tf\": 11,\n        \"df\": 26,\n        \"tf-idf\": 0.4230769230769231\n        }\n    }, {\n        \"term\": \"registrski\",\n        \"scores\": {\n        \"tf\": 73,\n        \"df\": 175,\n        \"tf-idf\": 0.41714285714285715\n        }\n    }, {\n        \"term\": \"Lahovnikov zakon\",\n        \"scores\": {\n        \"tf\": 20,\n        \"df\": 49,\n        \"tf-idf\": 0.40816326530612246\n        }\n    }, {\n        \"term\": \"\\u010cate\\u017e\",\n        \"scores\": {\n        \"tf\": 12,\n        \"df\": 30,\n        \"tf-idf\": 0.4\n        }\n    }, {\n        \"term\": \"cigareta\",\n        \"scores\": {\n        \"tf\": 32,\n        \"df\": 81,\n        \"tf-idf\": 0.3950617283950617\n        }\n    }, {\n        \"term\": \"progresija\",\n        \"scores\": {\n        \"tf\": 15,\n        \"df\": 43,\n        \"tf-idf\": 0.3488372093023256\n        }\n    }, {\n        \"term\": \"neizpla\\u010dan\",\n        \"scores\": {\n        \"tf\": 28,\n        \"df\": 82,\n        \"tf-idf\": 0.34146341463414637\n        }\n    }, {\n        \"term\": \"delavski\",\n        \"scores\": {\n        \"tf\": 197,\n        \"df\": 582,\n        \"tf-idf\": 0.3384879725085911\n        }\n    }, {\n        \"term\": \"Helios\",\n        \"scores\": {\n        \"tf\": 38,\n        \"df\": 116,\n        \"tf-idf\": 0.3275862068965517\n        }\n    }, {\n        \"term\": \"predkupen\",\n        \"scores\": {\n        \"tf\": 25,\n        \"df\": 80,\n        \"tf-idf\": 0.3125\n        }\n    }, {\n        \"term\": \"Telekom\",\n        \"scores\": {\n        \"tf\": 201,\n        \"df\": 648,\n        \"tf-idf\": 0.3101851851851852\n        }\n    }, {\n        \"term\": \"Siriza\",\n        \"scores\": {\n        \"tf\": 14,\n        \"df\": 46,\n        \"tf-idf\": 0.30434782608695654\n        }\n    }, {\n        \"term\": \"prekeren\",\n        \"scores\": {\n        \"tf\": 33,\n        \"df\": 109,\n        \"tf-idf\": 0.30275229357798167\n        }\n    }, {\n        \"term\": \"pregrevanje\",\n        \"scores\": {\n        \"tf\": 27,\n        \"df\": 90,\n        \"tf-idf\": 0.3\n        }\n    }, {\n        \"term\": \"klasificirati\",\n        \"scores\": {\n        \"tf\": 25,\n        \"df\": 84,\n        \"tf-idf\": 0.2976190476190476\n        }\n    }]\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getTFIDF/12",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getTFIDF/12/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "MPs"
  },
  {
    "type": "get",
    "url": "/p/getTaggedBallots/{id}/{?date}",
    "title": "MP's tagged ballots",
    "name": "getTaggedBallots",
    "group": "MPs",
    "description": "<p>This function returns an object with the MPs ballots and their tags, ordered by date, grouped by day. The function returns the ballots until a given date, if no date is supplied it is assumed the date is today.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>MP's Parladata id.</p>"
          },
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>What historic date does this data correspond with?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results",
            "description": "<p>MP's tagged ballots grouped by date.</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "results.date",
            "description": "<p>The date in question.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results.ballots",
            "description": "<p>Ballots the MP submitted on that day.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.ballots.ballot_id",
            "description": "<p>Ballot's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.ballots.option",
            "description": "<p>The ballot option (&quot;za&quot;/&quot;proti&quot;/&quot;ni&quot;/&quot;kvorum&quot;).</p>"
          },
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "results.ballots.tags",
            "description": "<p>List of tags this ballot was tagged with.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.ballots.session_id",
            "description": "<p>Parladata id of the session where this ballot was submitted.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.ballots.motion",
            "description": "<p>The text of the motion (what was the vote about).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.ballots.result",
            "description": "<p>Answers the question: Did the motion pass?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.ballots.vote_id",
            "description": "<p>Parladata id of the vote this ballot belongs to.</p>"
          },
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "all_tags",
            "description": "<p>List of all tags used for tagging ballots.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"person\": {\n        \"is_active\": false,\n        \"district\": [15],\n        \"name\": \"Luka Mesec\",\n        \"gov_id\": \"P273\",\n        \"gender\": \"m\",\n        \"party\": {\n        \"acronym\": \"ZL\",\n        \"is_coalition\": false,\n        \"id\": 8,\n        \"name\": \"PS Zdru\\u017eena Levica\"\n        },\n        \"type\": \"mp\",\n        \"id\": 58,\n        \"has_function\": false\n    },\n    \"created_at\": \"23. 11. 2016\",\n    \"created_for\": \"4. 12. 2014\",\n    \"results\": [{\n        \"date\": \"4. 12. 2014\",\n        \"ballots\": [{\n        \"ballot_id\": 592963,\n        \"option\": \"ni\",\n        \"tags\": [\"Odbor za notranje zadeve, javno upravo in lokalno samoupravo\"],\n        \"session_id\": 5614,\n        \"motion\": \"Zakon o spremembah in dopolnitvah Zakona o dr\\u017eavni upravi - Glasovanje o zakonu v celoti\",\n        \"result\": true,\n        \"vote_id\": 6591\n        }, {\n        \"ballot_id\": 593053,\n        \"option\": \"ni\",\n        \"tags\": [\"Odbor za notranje zadeve, javno upravo in lokalno samoupravo\"],\n        \"session_id\": 5614,\n        \"motion\": \"Zakon o spremembah in dopolnitvah Zakona o dr\\u017eavni upravi - Amandma: K 19. \\u010dlenu 4.12.2014 [ZL - Poslanska skupina Zdru\\u017eena levica]\",\n        \"result\": false,\n        \"vote_id\": 6592\n        }]\n    }, {\n        \"date\": \"17. 11. 2014\",\n        \"ballots\": [{\n        \"ballot_id\": 564575,\n        \"option\": \"ni\",\n        \"tags\": [\"Mandatno-volilna komisija\"],\n        \"session_id\": 6683,\n        \"motion\": \"Sklep o imenovanju \\u010dlana Slovenske nacionalne komisije za UNESCO - Glasovanje\",\n        \"result\": true,\n        \"vote_id\": 6274\n        }, {\n        \"ballot_id\": 564665,\n        \"option\": \"ni\",\n        \"tags\": [\"Mandatno-volilna komisija\"],\n        \"session_id\": 6683,\n        \"motion\": \"Sklep o imenovanju predsednika in dveh \\u010dlanov Upravnega odbora Sklada za financiranje razgradnje NEK in za odlaganje radioaktivnih odpadkov iz NEK - Glasovanje\",\n        \"result\": true,\n        \"vote_id\": 6275\n        }, {\n        \"ballot_id\": 564755,\n        \"option\": \"ni\",\n        \"tags\": [\"Mandatno-volilna komisija\"],\n        \"session_id\": 6683,\n        \"motion\": \"Sklep o imenovanju \\u010dlanice Dr\\u017eavne revizijske komisije - Glasovanje\",\n        \"result\": true,\n        \"vote_id\": 6276\n        }]\n    }],\n    \"all_tags\": [\"Komisija za nadzor javnih financ\", \"Kolegij predsednika Dr\\u017eavnega zbora\", \"Komisija za narodni skupnosti\", \"Komisija za odnose s Slovenci v zamejstvu in po svetu\", \"Komisija za poslovnik\", \"Mandatno-volilna komisija\", \"Odbor za delo, dru\\u017eino, socialne zadeve in invalide\", \"Odbor za finance in monetarno politiko\", \"Odbor za gospodarstvo\", \"Odbor za infrastrukturo, okolje in prostor\", \"Odbor za izobra\\u017eevanje, znanost, \\u0161port in mladino\", \"Odbor za kmetijstvo, gozdarstvo in prehrano\", \"Odbor za kulturo\", \"Odbor za notranje zadeve, javno upravo in lokalno samoupravo\", \"Odbor za obrambo\", \"Odbor za pravosodje\", \"Odbor za zadeve Evropske unije\", \"Odbor za zdravstvo\", \"Odbor za zunanjo politiko\", \"Preiskovalna komisija o ugotavljanju zlorab v slovenskem ban\\u010dnem sistemu ter ugotavljanju vzrokov in\", \"Preiskovalna komisija za ugotavljanje politi\\u010dne odgovornosti nosilcev javnih funkcij pri investiciji\", \"Ustavna komisija\", \"Proceduralna glasovanja\", \"Zunanja imenovanja\", \"Poslanska vpra\\u0161anja\", \"Komisija za nadzor obve\\u0161\\u010devalnih in varnostnih slu\\u017eb\", \"Preiskovalne komisije\", \"Komisija za peticije ter za \\u010dlovekove pravice in enake mo\\u017enosti\", \"Interpelacija\", \" Preiskovalna komisija za ugotavljanje politi\\u010dne odgovornosti nosilcev javnih funkcij pri investicij\"]\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getTaggedBallots/12",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getTaggedBallots/12/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "MPs"
  },
  {
    "type": "get",
    "url": "/p/getVocabularySize/{id}/{?date}",
    "title": "MP's vocabulary size",
    "name": "getVocabularySize",
    "group": "MPs",
    "description": "<p>This function returns an object with the MPs calculated vocabulary size. The function returns the score as it was calculated for a given date, if no date is supplied it is assumed the date is today.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>MP's Parladata id.</p>"
          },
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>What historic date does this data correspond with?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results",
            "description": "<p>MP's vocabulary size.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.max",
            "description": "<p>MP (or MPs) who has the highest vocabulary size and their score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "results.max.score",
            "description": "<p>Max MP's score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results.max.mps",
            "description": "<p>A list of MP's with the same maximum score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.max.mps.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "results.max.mps.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.max.mps.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.max.mps.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.max.mps.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.max.mps.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.max.mps.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "results.average",
            "description": "<p>The average score for this metric accross the parliament.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "results.score",
            "description": "<p>Score for the MP in question.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"person\": {\n        \"is_active\": false,\n        \"district\": [15],\n        \"name\": \"Luka Mesec\",\n        \"gov_id\": \"P273\",\n        \"gender\": \"m\",\n        \"party\": {\n        \"acronym\": \"ZL\",\n        \"is_coalition\": false,\n        \"id\": 8,\n        \"name\": \"PS Zdru\\u017eena Levica\"\n        },\n        \"type\": \"mp\",\n        \"id\": 58,\n        \"has_function\": false\n    },\n    \"created_at\": \"14.11.2016\",\n    \"created_for\": \"10.09.2014\",\n    \"results\": {\n        \"max\": {\n        \"score\": 744.915094339623,\n        \"mps\": [{\n            \"is_active\": false,\n            \"district\": [40],\n            \"name\": \"Benedikt Kopmajer\",\n            \"gov_id\": \"P261\",\n            \"gender\": \"m\",\n            \"party\": {\n            \"acronym\": \"DeSUS\",\n            \"is_coalition\": true,\n            \"id\": 3,\n            \"name\": \"PS Demokratska Stranka Upokojencev Slovenije\"\n            },\n            \"type\": \"mp\",\n            \"id\": 41,\n            \"has_function\": false\n        }]\n        },\n        \"average\": 388.298609949473,\n        \"score\": 592.0\n    }\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getVocabularySize/12",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getVocabularySize/12/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "MPs"
  },
  {
    "type": "get",
    "url": "/p/getAllActiveMembers",
    "title": "Get all active MPs",
    "name": "getAllActiveMembers",
    "group": "Other",
    "description": "<p>This function returns a list of all MPs currently active in the parliament.</p>",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "/",
            "description": "<p>list of MPs</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "/.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "/.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "/.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "/.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "/.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "/.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "/.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "/.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "/.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "/.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "/.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "/.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "/.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "[{\n    \"is_active\": false,\n    \"district\": [48],\n    \"name\": \"Jasna Murgel\",\n    \"gov_id\": \"P274\",\n    \"gender\": \"f\",\n    \"party\": {\n        \"acronym\": \"SMC\",\n        \"is_coalition\": true,\n        \"id\": 1,\n        \"name\": \"PS Stranka modernega centra\"\n    },\n    \"type\": \"mp\",\n    \"id\": 60,\n    \"has_function\": false\n    }, {\n    \"is_active\": false,\n    \"district\": [40],\n    \"name\": \"Ivan \\u0160kodnik\",\n    \"gov_id\": \"P286\",\n    \"gender\": \"m\",\n    \"party\": {\n        \"acronym\": \"SMC\",\n        \"is_coalition\": true,\n        \"id\": 1,\n        \"name\": \"PS Stranka modernega centra\"\n    },\n    \"type\": \"mp\",\n    \"id\": 76,\n    \"has_function\": false\n    }, {\n    \"is_active\": false,\n    \"district\": [46],\n    \"name\": \"Branislav Raji\\u0107\",\n    \"gov_id\": \"P281\",\n    \"gender\": \"m\",\n    \"party\": {\n        \"acronym\": \"SMC\",\n        \"is_coalition\": true,\n        \"id\": 1,\n        \"name\": \"PS Stranka modernega centra\"\n    },\n    \"type\": \"mp\",\n    \"id\": 70,\n    \"has_function\": false\n}]",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getAllActiveMembers/",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "Other"
  },
  {
    "type": "get",
    "url": "/p/getSlugs",
    "title": "Get slugs for parlameter.si",
    "name": "getAllActiveMembers",
    "group": "Other",
    "description": "<p>This function returns slugs for our site at parlameter.si</p>",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "partyLink",
            "description": "<p>Party url paths.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "partyLink.govori",
            "description": "<p>Party speeches url.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "partyLink.base",
            "description": "<p>Party pages base url.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "partyLink.pregled",
            "description": "<p>Party overview url.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "partyLink.glasovanja",
            "description": "<p>Party votes url.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "personLink",
            "description": "<p>Person url paths.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "personLink.govori",
            "description": "<p>Person speeches url.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "personLink.base",
            "description": "<p>Person pages base url.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "personLink.pregled",
            "description": "<p>Person overview url.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "personLink.glasovanja",
            "description": "<p>Person votes url.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "sessionLink",
            "description": "<p>Session url paths.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "sessionLink.prisotnos",
            "description": "<p>Session attendance url.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "sessionLink.glasovanje",
            "description": "<p>Session vote url.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "sessionLink.transkript",
            "description": "<p>Session transcript url.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "sessionLink.glasovanja",
            "description": "<p>Session votes url.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person",
            "description": "<p>Slugs for people. Keys are Parladata ids.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person.PERSON_ID",
            "description": "<p>Person's slugs object.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.PERSON_ID.slug",
            "description": "<p>Person's url slug.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "base",
            "description": "<p>Url base.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "party",
            "description": "<p>Slugs for organizations. Keys are Parladata ids.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "party.PARTY_ID",
            "description": "<p>Party's slug object.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "party.PARTY_ID.acronym",
            "description": "<p>Party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "party.PARTY_ID.realAcronym",
            "description": "<p>Party's acronym with proper capitalisation.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "party.PARTY_ID.slug",
            "description": "<p>Party's slug</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"partyLink\": {\n        \"govori\": \"/govori/\",\n        \"base\": \"/poslanska-skupina/\",\n        \"pregled\": \"/pregled/\",\n        \"glasovanja\": \"/glasovanja/\"\n    },\n    \"personLink\": {\n        \"govori\": \"/govori/\",\n        \"base\": \"/poslanec/\",\n        \"pregled\": \"/pregled/\",\n        \"glasovanja\": \"/glasovanja/\"\n    },\n    \"sessionLink\": {\n        \"prisotnost\": \"/seja/prisotnost/\",\n        \"glasovanje\": \"/seja/glasovanje/\",\n        \"transkript\": \"/seja/transkript/\",\n        \"glasovanja\": \"/seja/glasovanja/\"\n    },\n    \"person\": {\n        \"2\": {\n        \"slug\": \"anja-bah-zibert\"\n        },\n        \"3\": {\n        \"slug\": \"urska-ban\"\n        },\n        \"4\": {\n        \"slug\": \"roberto-battelli\"\n        }\n    },\n    \"base\": \"https://parlameter.si\",\n    \"party\": {\n        \"1\": {\n        \"acronym\": \"smc\",\n        \"realAcronym\": \"SMC\",\n        \"slug\": \"ps-stranka-modernega-centra\"\n        },\n        \"2\": {\n        \"acronym\": \"imns\",\n        \"realAcronym\": \"IMNS\",\n        \"slug\": \"ps-italijanske-in-madzarske-narodne-skupnosti\"\n        },\n        \"3\": {\n        \"acronym\": \"desus\",\n        \"realAcronym\": \"DeSUS\",\n        \"slug\": \"ps-demokratska-stranka-upokojencev-slovenije\"\n        },\n        \"4\": {\n        \"acronym\": \"zaab\",\n        \"realAcronym\": \"ZAAB\",\n        \"slug\": \"ps-zaveznistvo-alenke-bratusek\"\n        }\n    }\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getSlugs/",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "Other"
  },
  {
    "type": "get",
    "url": "/p/getCompass/{?date}",
    "title": "Political compass",
    "name": "getCompass",
    "group": "Other",
    "description": "<p>This function returns a list of objects representing MPs and their coordinates on the &quot;political compass&quot;. The function returns the scores as it was calculated for a given date, if no date is supplied it is assumed the date is today.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>What historic date does this data correspond with?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "data",
            "description": "<p>list of MPs and their coordinates</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "data.person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "data.person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "data.person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "data.person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "data.person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "data.person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.score.vT1",
            "description": "<p>First coordinate</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.score.vT2",
            "description": "<p>Second coordinate</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"created_at\": \"21.03.2017\",\n    \"created_for\": \"17.02.2017\",\n    \"data\": [{\n        \"person\": {\n        \"is_active\": false,\n        \"district\": [7],\n        \"name\": \"Anja Bah \\u017dibert\",\n        \"gov_id\": \"P239\",\n        \"gender\": \"f\",\n        \"party\": {\n            \"acronym\": \"SDS\",\n            \"is_coalition\": false,\n            \"id\": 5,\n            \"name\": \"PS Slovenska Demokratska Stranka\"\n        },\n        \"type\": \"mp\",\n        \"id\": 2,\n        \"has_function\": false\n        },\n        \"score\": {\n        \"vT1\": 0.18281964948320664,\n        \"vT2\": -0.05594373814997616\n        }\n    }, {\n        \"person\": {\n        \"is_active\": false,\n        \"district\": [8],\n        \"name\": \"Ur\\u0161ka Ban\",\n        \"gov_id\": \"P240\",\n        \"gender\": \"f\",\n        \"party\": {\n            \"acronym\": \"SMC\",\n            \"is_coalition\": true,\n            \"id\": 1,\n            \"name\": \"PS Stranka modernega centra\"\n        },\n        \"type\": \"mp\",\n        \"id\": 3,\n        \"has_function\": false\n        },\n        \"score\": {\n        \"vT1\": -0.06505089721256502,\n        \"vT2\": -0.1438729944923539\n        }\n    }]\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getCompass/",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getCompass/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "Other"
  },
  {
    "type": "get",
    "url": "/p/getListOfMembers/{?date}",
    "title": "List of MPs and their scores",
    "name": "getListOfMembers",
    "group": "Other",
    "description": "<p>This function returns an object with all MPs and their scores for all analyses along with an object containing all districts (for filtering purposes https://parlameter.si/poslanci).</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "districts",
            "description": "<p>List of objects representing districts.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "districts.DISTRICT_ID",
            "description": "<p>Each object contains a single key, that key being the district's Parladata id and its value the district's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "data",
            "description": "<p>List of MPs and their scores.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "data.person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "data.person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "data.person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "data.person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "data.person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "data.person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "data.results",
            "description": "<p>Analysis results for this person.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.results.privzdignjeno",
            "description": "<p>&quot;Elevated&quot; language style score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.speeches_per_session",
            "description": "<p>Average number of speeches per session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.number_of_questions",
            "description": "<p>Number of questions this MP has asked.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.presence_votes",
            "description": "<p>Percentage of votes this MP attended.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.presence_sessions",
            "description": "<p>Percentage of sessions this MP attended.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.problematicno",
            "description": "<p>&quot;Problematic&quot; language style score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.vocabulary_size",
            "description": "<p>MP's calculated vocabulary size.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.spoken_words",
            "description": "<p>Number of words this MP has spoken.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.preprosto",
            "description": "<p>&quot;Simple&quot; language style score.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"districts\": [{\n        \"91\": \"Lendava 1\"\n    }, {\n        \"102\": \"Ljubljana-\\u0160i\\u0161ka I\"\n    }, {\n        \"101\": \"Ljubljana-\\u0160i\\u0161ka II\"\n    }, {\n        \"100\": \"Ljubljana-\\u0160i\\u0161ka III\"\n    }],\n    \"data\": [{\n        \"person\": {\n        \"name\": \"Aleksander Kav\\u010di\\u010d\",\n        \"gov_id\": \"P259\",\n        \"gender\": \"m\",\n        \"is_active\": false,\n        \"district\": [19],\n        \"party\": {\n            \"acronym\": \"SMC\",\n            \"is_coalition\": true,\n            \"name\": \"PS Stranka modernega centra\",\n            \"id\": 1\n        },\n        \"type\": \"mp\",\n        \"id\": 39,\n        \"has_function\": false\n        },\n        \"results\": {\n        \"privzdignjeno\": 2.7438091511157987,\n        \"speeches_per_session\": 1.0,\n        \"number_of_questions\": 5.0,\n        \"presence_votes\": 89.589905362776,\n        \"presence_sessions\": 89.8550724637681,\n        \"problematicno\": 2.516673651070962,\n        \"vocabulary_size\": 135.0,\n        \"spoken_words\": 10837,\n        \"preprosto\": 3.377309423797745\n        }\n    }, {\n        \"person\": {\n        \"name\": \"Alenka Bratu\\u0161ek\",\n        \"gov_id\": \"P166\",\n        \"gender\": \"f\",\n        \"is_active\": false,\n        \"district\": [62],\n        \"party\": {\n            \"acronym\": \"PS NP\",\n            \"is_coalition\": false,\n            \"name\": \"PS nepovezanih poslancev \",\n            \"id\": 109\n        },\n        \"type\": \"mp\",\n        \"id\": 9,\n        \"has_function\": false\n        },\n        \"results\": {\n        \"privzdignjeno\": 0.32064092814348816,\n        \"speeches_per_session\": 5.0,\n        \"number_of_questions\": 49.0,\n        \"presence_votes\": 46.6876971608833,\n        \"presence_sessions\": 72.463768115942,\n        \"problematicno\": 0.31498556069390254,\n        \"vocabulary_size\": 96.0,\n        \"spoken_words\": 282204,\n        \"preprosto\": 0.411863764711025\n        }\n    }, {\n        \"person\": {\n        \"name\": \"Andrej \\u010cu\\u0161\",\n        \"gov_id\": \"P225\",\n        \"gender\": \"m\",\n        \"is_active\": false,\n        \"district\": [28],\n        \"party\": {\n            \"acronym\": \"NeP - A\\u010c\",\n            \"is_coalition\": false,\n            \"name\": \"Nepovezani poslanec Andrej \\u010cu\\u0161\",\n            \"id\": 108\n        },\n        \"type\": \"mp\",\n        \"id\": 15,\n        \"has_function\": false\n        },\n        \"results\": {\n        \"privzdignjeno\": 0.6844781070961635,\n        \"speeches_per_session\": 3.0,\n        \"number_of_questions\": 284.0,\n        \"presence_votes\": 52.944269190326,\n        \"presence_sessions\": 69.5652173913043,\n        \"problematicno\": 0.5026381764433223,\n        \"vocabulary_size\": 115.0,\n        \"spoken_words\": 122238,\n        \"preprosto\": 0.8868782609371512\n        }\n    }]\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getListOfMembers",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getListOfMembers/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "Other"
  },
  {
    "type": "get",
    "url": "/p/getListOfMembersTickers/{?date}",
    "title": "List of MPs and their scores with differences from last regular plenary session",
    "name": "getListOfMembersTickers",
    "group": "Other",
    "description": "<p>This function returns an object with all MPs and their scores for all analyses along with an object containing all districts (for filtering purposes https://parlameter.si/poslanci). The score objects contain scores, MP's ranks as well as the difference in their scores between the last two regular plenary session (Redna seja).</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "districts",
            "description": "<p>List of objects representing districts.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "districts.DISTRICT_ID",
            "description": "<p>Each object contains a single key, that key being the district's Parladata id and its value the district's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "data",
            "description": "<p>List of MPs and their scores.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "data.person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "data.person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "data.person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "data.person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "data.person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "data.person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "data.results",
            "description": "<p>Analysis results for this person.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "data.results.privzdignjeno",
            "description": "<p>&quot;Elevated&quot; language style score object.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.results.privzdignjeno.diff",
            "description": "<p>&quot;Elevated&quot; language style score difference.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.results.privzdignjeno.score",
            "description": "<p>&quot;Elevated&quot; language style score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.results.privzdignjeno.rank",
            "description": "<p>&quot;Elevated&quot; language style score rank.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "data.results.speeches_per_session",
            "description": "<p>Average number of speeches per session object.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.results.speeches_per_session.diff",
            "description": "<p>Average number of speeches per session difference.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.results.speeches_per_session.score",
            "description": "<p>Average number of speeches per session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.results.speeches_per_session.rank",
            "description": "<p>Average number of speeches per session rank.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "data.results.number_of_questions",
            "description": "<p>Number of questions this MP has asked object.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.results.number_of_questions.diff",
            "description": "<p>Number of questions this MP has asked difference.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.results.number_of_questions.score",
            "description": "<p>Number of questions this MP has asked.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.results.number_of_questions.rank",
            "description": "<p>Number of questions this MP has asked rank.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "data.results.presence_votes",
            "description": "<p>Percentage of votes this MP attended object.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.results.presence_votes.diff",
            "description": "<p>Percentage of votes this MP attended difference.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.results.presence_votes.score",
            "description": "<p>Percentage of votes this MP attended.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.results.presence_votes.rank",
            "description": "<p>Percentage of votes this MP attended rank.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "data.results.presence_sessions",
            "description": "<p>Percentage of sessions this MP attended object.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.results.presence_sessions.diff",
            "description": "<p>Percentage of sessions this MP attended difference.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.results.presence_sessions.score",
            "description": "<p>Percentage of sessions this MP attended.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.results.presence_sessions.rank",
            "description": "<p>Percentage of sessions this MP attended rank.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "data.results.problematicno",
            "description": "<p>&quot;Problematic&quot; language style score object.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.results.problematicno.diff",
            "description": "<p>&quot;Problematic&quot; language style score difference.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.results.problematicno.score",
            "description": "<p>&quot;Problematic&quot; language style score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.results.problematicno.rank",
            "description": "<p>&quot;Problematic&quot; language style score rank.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "data.results.vocabulary_size",
            "description": "<p>MP's calculated vocabulary size object.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.results.vocabulary_size.diff",
            "description": "<p>MP's calculated vocabulary size difference.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.results.vocabulary_size.score",
            "description": "<p>MP's calculated vocabulary size.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.results.vocabulary_size.rank",
            "description": "<p>MP's calculated vocabulary size rank.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "data.results.spoken_words",
            "description": "<p>Number of words this MP has spoken.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.results.spoken_words.diff",
            "description": "<p>Number of words this MP has spoken difference.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.results.spoken_words.score",
            "description": "<p>Number of words this MP has spoken.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.results.spoken_words.rank",
            "description": "<p>Number of words this MP has spoken rank.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "data.results.preprosto",
            "description": "<p>&quot;Simple&quot; language style score object.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.results.preprosto.diff",
            "description": "<p>&quot;Simple&quot; language style score difference.</p>"
          },
          {
            "group": "Success 200",
            "type": "Float",
            "optional": false,
            "field": "data.results.preprosto.score",
            "description": "<p>&quot;Simple&quot; language style score.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.results.preprosto.rank",
            "description": "<p>&quot;Simple&quot; language style score rank.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"districts\": [{\n        \"91\": \"Lendava 1\"\n    }, {\n        \"102\": \"Ljubljana-\\u0160i\\u0161ka I\"\n    }, {\n        \"101\": \"Ljubljana-\\u0160i\\u0161ka II\"\n    }, {\n        \"100\": \"Ljubljana-\\u0160i\\u0161ka III\"\n    }, {\n        \"99\": \"Ljubljana-\\u0160i\\u0161ka IV\"\n    }],\n    \"created_at\": \"2017-03-21T10:35:29.257\",\n    \"created_for\": \"2017-03-21\",\n    \"data\": [{\n        \"person\": {\n        \"name\": \"Aleksander Kav\\u010di\\u010d\",\n        \"gov_id\": \"P259\",\n        \"gender\": \"m\",\n        \"is_active\": false,\n        \"district\": [19],\n        \"party\": {\n            \"acronym\": \"SMC\",\n            \"is_coalition\": true,\n            \"name\": \"PS Stranka modernega centra\",\n            \"id\": 1\n        },\n        \"type\": \"mp\",\n        \"id\": 39,\n        \"has_function\": false\n        },\n        \"results\": {\n        \"privzdignjeno\": {\n            \"diff\": -0.07080984812327795,\n            \"score\": 2.7438091511157987,\n            \"rank\": 62\n        },\n        \"speeches_per_session\": {\n            \"diff\": 0.0,\n            \"score\": 1.0,\n            \"rank\": 74\n        },\n        \"number_of_questions\": {\n            \"diff\": 0.0,\n            \"score\": 5.0,\n            \"rank\": 62\n        },\n        \"presence_votes\": {\n            \"diff\": 0.0681428694927888,\n            \"score\": 89.589905362776,\n            \"rank\": 37\n        },\n        \"presence_sessions\": {\n            \"diff\": -1.1897036556349008,\n            \"score\": 89.8550724637681,\n            \"rank\": 42\n        },\n        \"problematicno\": {\n            \"diff\": 0.04653717835381821,\n            \"score\": 2.516673651070962,\n            \"rank\": 62\n        },\n        \"vocabulary_size\": {\n            \"diff\": 0.0,\n            \"score\": 135.0,\n            \"rank\": 14\n        },\n        \"spoken_words\": {\n            \"diff\": 0,\n            \"score\": 10837,\n            \"rank\": 86\n        },\n        \"preprosto\": {\n            \"diff\": 0.016475585916483126,\n            \"score\": 3.377309423797745,\n            \"rank\": 62\n        }\n        }\n    }, {\n        \"person\": {\n        \"name\": \"Alenka Bratu\\u0161ek\",\n        \"gov_id\": \"P166\",\n        \"gender\": \"f\",\n        \"is_active\": false,\n        \"district\": [62],\n        \"party\": {\n            \"acronym\": \"PS NP\",\n            \"is_coalition\": false,\n            \"name\": \"PS nepovezanih poslancev \",\n            \"id\": 109\n        },\n        \"type\": \"mp\",\n        \"id\": 9,\n        \"has_function\": false\n        },\n        \"results\": {\n        \"privzdignjeno\": {\n            \"diff\": 0.0022796756059407786,\n            \"score\": 0.32064092814348816,\n            \"rank\": 26\n        },\n        \"speeches_per_session\": {\n            \"diff\": 0.0,\n            \"score\": 5.0,\n            \"rank\": 26\n        },\n        \"number_of_questions\": {\n            \"diff\": 6.0,\n            \"score\": 49.0,\n            \"rank\": 26\n        },\n        \"presence_votes\": {\n            \"diff\": -1.0823189594820946,\n            \"score\": 46.6876971608833,\n            \"rank\": 88\n        },\n        \"presence_sessions\": {\n            \"diff\": 0.8219770711659038,\n            \"score\": 72.463768115942,\n            \"rank\": 87\n        },\n        \"problematicno\": {\n            \"diff\": 0.005426527504002687,\n            \"score\": 0.31498556069390254,\n            \"rank\": 26\n        },\n        \"vocabulary_size\": {\n            \"diff\": 0.0,\n            \"score\": 96.0,\n            \"rank\": 72\n        },\n        \"spoken_words\": {\n            \"diff\": 2326,\n            \"score\": 282204,\n            \"rank\": 19\n        },\n        \"preprosto\": {\n            \"diff\": 0.0014815186579075212,\n            \"score\": 0.411863764711025,\n            \"rank\": 26\n        }\n        }\n    }]\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getListOfMembersTickers",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getListOfMembersTickers/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "Other"
  },
  {
    "type": "get",
    "url": "/p/getUniqueWordsLanding/{?date}",
    "title": "[DEPRECATED] Number of unique words spoken by MPs",
    "name": "getUniqueWordsLanding",
    "group": "Other",
    "description": "<p>This function returns a list of objects representing MPs and the number of unique words. The function returns the scores as it was calculated for a given date, if no date is supplied it is assumed the date is today.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "/",
            "description": "<p>list of MPs and their scores</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "/.person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "/.person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "/.person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "/.person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "/.person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "/.person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "/.person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "/.person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "/.person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "/.person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "/.person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "/.person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "/.person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "/.person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "[\n    {\n        \"person\": {\n        \"is_active\": false,\n        \"district\": [84],\n        \"name\": \"Vlasta Po\\u010dkaj\",\n        \"gov_id\": \"P303\",\n        \"gender\": \"f\",\n        \"party\": {\n            \"acronym\": \"SMC\",\n            \"is_coalition\": true,\n            \"id\": 1,\n            \"name\": \"PS Stranka modernega centra\"\n        },\n        \"type\": \"mp\",\n        \"id\": 2934,\n        \"has_function\": false\n        },\n        \"score\": 263.0\n    }, {\n        \"person\": {\n        \"is_active\": false,\n        \"district\": [85],\n        \"name\": \"Teja Ljubi\\u010d\",\n        \"gov_id\": \"P304\",\n        \"gender\": \"f\",\n        \"party\": {\n            \"acronym\": \"SMC\",\n            \"is_coalition\": true,\n            \"id\": 1,\n            \"name\": \"PS Stranka modernega centra\"\n        },\n        \"type\": \"mp\",\n        \"id\": 2933,\n        \"has_function\": false\n        },\n        \"score\": 310.0\n    }, {\n        \"person\": {\n        \"is_active\": false,\n        \"district\": [52],\n        \"name\": \"Ivan Prelog\",\n        \"gov_id\": \"P279\",\n        \"gender\": \"m\",\n        \"party\": {\n            \"acronym\": \"SMC\",\n            \"is_coalition\": true,\n            \"id\": 1,\n            \"name\": \"PS Stranka modernega centra\"\n        },\n        \"type\": \"mp\",\n        \"id\": 68,\n        \"has_function\": false\n        },\n        \"score\": 2007.0\n    }\n]",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getUniqueWordsLanding/",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getUniqueWordsLanding/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "Other"
  },
  {
    "type": "get",
    "url": "/p/getVocabularySizeLanding/{?date}",
    "title": "Vocabulary sizes of all MPs",
    "name": "getVocabularySizeLanding",
    "group": "Other",
    "description": "<p>This function returns a list of objects representing MPs and their vocabulary size scores. The function returns the scores as it was calculated for a given date, if no date is supplied it is assumed the date is today.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>What historic date does this data correspond with?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "data",
            "description": "<p>list of MPs and their coordinates</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "data.person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "data.person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "data.person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "data.person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "data.person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data.person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "data.person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "data.person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n    \"created_at\": \"21.03.2017\",\n    \"created_for\": \"20.03.2017\",\n    \"data\": [{\n        \"person\": {\n        \"is_active\": false,\n        \"district\": [71],\n        \"name\": \"Janez Jan\\u0161a\",\n        \"gov_id\": \"P025\",\n        \"gender\": \"m\",\n        \"party\": {\n            \"acronym\": \"SDS\",\n            \"is_coalition\": false,\n            \"id\": 5,\n            \"name\": \"PS Slovenska Demokratska Stranka\"\n        },\n        \"type\": \"mp\",\n        \"id\": 36,\n        \"has_function\": false\n        },\n        \"score\": 81.0\n    }, {\n        \"person\": {\n        \"is_active\": false,\n        \"district\": [83],\n        \"name\": \"Marko Ferluga\",\n        \"gov_id\": \"P250\",\n        \"gender\": \"m\",\n        \"party\": {\n            \"acronym\": \"SMC\",\n            \"is_coalition\": true,\n            \"id\": 1,\n            \"name\": \"PS Stranka modernega centra\"\n        },\n        \"type\": \"mp\",\n        \"id\": 21,\n        \"has_function\": false\n        },\n        \"score\": 84.0\n    }, {\n        \"person\": {\n        \"is_active\": false,\n        \"district\": [40],\n        \"name\": \"Ivan \\u0160kodnik\",\n        \"gov_id\": \"P286\",\n        \"gender\": \"m\",\n        \"party\": {\n            \"acronym\": \"SMC\",\n            \"is_coalition\": true,\n            \"id\": 1,\n            \"name\": \"PS Stranka modernega centra\"\n        },\n        \"type\": \"mp\",\n        \"id\": 76,\n        \"has_function\": false\n        },\n        \"score\": 87.0\n    }]\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getVocabularySizeLanding/",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/p/getVocabularySizeLanding/12.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaposlanci/views.py",
    "groupTitle": "Other"
  },
  {
    "type": "get",
    "url": "/getSpeech/{speech_id}",
    "title": "Speech info",
    "name": "GetSpeech",
    "group": "Session",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "speech_id",
            "optional": false,
            "field": "speech",
            "description": "<p>id is parameter which returns exactly specified speech</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing). *</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>For when was this data created? *</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.quote_id",
            "description": "<p>Id of quote if exists.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.content",
            "description": "<p>Content of speech. *</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.session",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.session.name",
            "description": "<p>Name of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "results.session.date_ts",
            "description": "<p>Date and time of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "results.session.date",
            "description": "<p>Date of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.session.id",
            "description": "<p>Id of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.session.in_review",
            "description": "<p>Return true or false if session is in review.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results.session.orgs",
            "description": "<p>Organization object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.session.orgs.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.session.orgs.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.session.orgs.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.session.orgs.name",
            "description": "<p>Name of organization *</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.quoted_text",
            "description": "<p>Content of quoted text.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.speech_id",
            "description": "<p>Id of speech.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.end_idx",
            "description": "<p>End intex of quoted text.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.start_idx",
            "description": "<p>End intex of quoted text. *</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n\"person\": {\n\"is_active\": false,\n\"district\": [\n103\n],\n\"name\": \"Violeta Tomić\",\n\"gov_id\": \"P289\",\n\"gender\": \"f\",\n\"party\": {\n\"acronym\": \"ZL\",\n\"is_coalition\": false,\n\"id\": 8,\n\"name\": \"PS Združena Levica\"\n},\n\"type\": \"mp\",\n\"id\": 80,\n\"has_function\": false\n},\n\"created_at\": \"20.02.2017\",\n\"created_for\": \"09.02.2017\",\n\"results\": {\n\"quote_id\": null,\n\"content\": \"Spoštovani predsednik, hvala za besedo. Kolegice in kolegi! ...\n\"session\": {\n\"name\": \"42. izredna seja\",\n\"date_ts\": \"2017-02-02T01:00:00\",\n\"orgs\": [\n{\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"id\": 95,\n\"name\": \"Državni zbor\"\n}\n],\n\"date\": \"2. 2. 2017\",\n\"org\": {\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"id\": 95,\n\"name\": \"Državni zbor\"\n},\n\"id\": 8972,\n\"in_review\": false\n},\n\"quoted_text\": null,\n\"speech_id\": 1118139,\n\"end_idx\": null,\n\"start_idx\": null\n}\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/s/getSpeech/1118139",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaseje/views.py",
    "groupTitle": "Session"
  },
  {
    "type": "get",
    "url": "/getLastSessionLanding/{?date}",
    "title": "Data from last session",
    "name": "getLastSessionLanding",
    "group": "Session",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>For when was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "presence",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "presence.percent",
            "description": "<p>Percent of presence on session for each PG.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "presence.org",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "presence.org.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "presence.org.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "presence.org.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "presence.org.name",
            "description": "<p>Name of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "tfidf",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "tfidf.created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "tfidf.created_for",
            "description": "<p>For when was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "tfidf.session",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "tfidf.session.name",
            "description": "<p>Name of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "tfidf.session.date_ts",
            "description": "<p>Date and time of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "tfidf.session.date",
            "description": "<p>Date of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "tfidf.session.id",
            "description": "<p>Id of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "tfidf.session.in_review",
            "description": "<p>Return true or false if session is in review.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "tfidf.session.orgs",
            "description": "<p>Organization object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "tfidf.session.orgs.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "tfidf.session.orgs.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "tfidf.session.orgs.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "tfidf.session.orgs.name",
            "description": "<p>Name of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "tfidf.results",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "tfidf.results.term",
            "description": "<p>Term that is analyzed.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "tfidf.results.scores",
            "description": "<p>Scores of TFIDF</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "tfidf.results.scores.tf",
            "description": "<p>Term frequency</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "tfidf.results.scores.df",
            "description": "<p>Document frequency</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "tfidf.results.scores.tf-idf",
            "description": "<p>Term frequency / Document frequency</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "session",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "session.name",
            "description": "<p>Name of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "session.date_ts",
            "description": "<p>Date and time of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "session.date",
            "description": "<p>Date of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.id",
            "description": "<p>Id of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "session.in_review",
            "description": "<p>Return true or false if session is in review.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "session.orgs",
            "description": "<p>Organization object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "session.orgs.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "session.orgs.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.orgs.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "session.orgs.name",
            "description": "<p>Name of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "motion",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "motion.results.session",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "motion.results.session.name",
            "description": "<p>Name of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "motion.results.session.date_ts",
            "description": "<p>Date and time of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "motion.results.session.date",
            "description": "<p>Date of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "motion.results.session.id",
            "description": "<p>Id of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "motion.results.session.in_review",
            "description": "<p>Return true or false if session is in review.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "motion.results.session.orgs",
            "description": "<p>Organization object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "motion.results.session.orgs.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "motion.results.session.orgs.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "motion.results.session.orgs.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "motion.results.session.orgs.name",
            "description": "<p>Name of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "motion.results.results",
            "description": "<p>IDs of all speeches on session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "motion.results.abstain",
            "description": "<p>Number of MPs that abstain on voting.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "motion.results.against",
            "description": "<p>Number of MPs that are against on voting.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "motion.results.motion_id",
            "description": "<p>ID of motion.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "motion.results.text",
            "description": "<p>Text of motion</p>"
          },
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "motion.results.tags",
            "description": "<p>Array of tags of motion.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "motion.results.is_outlier",
            "description": "<p>Analaysis if person is outlier.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "motion.results.not_present",
            "description": "<p>Number of MPs that were not present.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "motion.results.votes_for",
            "description": "<p>Number of MPs that voted with yes.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "motion.results.result",
            "description": "<p>True or False if the motion was successful.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n\"created_for\": \"20.03.2017\",\n\"presence\": [\n{\n\"org\": {\n\"acronym\": \"PS NP\",\n\"is_coalition\": false,\n\"id\": 109,\n\"name\": \"PS nepovezanih poslancev \"\n},\n\"percent\": 100\n},\n{\n\"org\": {\n\"acronym\": \"SMC\",\n\"is_coalition\": true,\n\"id\": 1,\n\"name\": \"PS Stranka modernega centra\"\n},\n\"percent\": 99\n},\n...\n\"created_at\": \"16.04.2017\",\n\"tfidf\": {\n\"session\": {\n\"name\": \"28. redna seja\",\n\"date_ts\": \"2017-03-20T01:00:00\",\n\"org\": {\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"name\": \"Državni zbor\",\n\"id\": 95\n},\n\"date\": \"20. 3. 2017\",\n\"orgs\": [\n{\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"name\": \"Državni zbor\",\n\"id\": 95\n}\n],\n\"id\": 9379,\n\"in_review\": true\n},\n\"session\": {\n\"name\": \"28. redna seja\",\n\"date_ts\": \"2017-03-20T01:00:00\",\n\"orgs\": [\n{\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"id\": 95,\n\"name\": \"Državni zbor\"\n}\n],\n\"date\": \"20. 3. 2017\",\n\"org\": {\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"id\": 95,\n\"name\": \"Državni zbor\"\n},\n\"id\": 9379,\n\"in_review\": true\n},\n\"motions\": [\n{\n\"session\": {\n\"name\": \"28. redna seja\",\n\"date_ts\": \"2017-03-20T01:00:00\",\n\"org\": {\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"name\": \"Državni zbor\",\n\"id\": 95\n},\n\"date\": \"20. 3. 2017\",\n\"orgs\": [\n{\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"name\": \"Državni zbor\",\n\"id\": 95\n}\n],\n\"id\": 9379,\n\"in_review\": true\n},\n\"results\": {\n\"abstain\": 0,\n\"tags\": [\n\"Proceduralna glasovanja\"\n],\n\"text\": \"Dnevni red v celoti\",\n\"motion_id\": 6900,\n\"against\": 1,\n\"votes_for\": 83,\n\"is_outlier\": true,\n\"not_present\": 6,\n\"result\": true\n}\n}\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/s/getLastSessionLanding",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/s/getLastSessionLanding/21.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaseje/views.py",
    "groupTitle": "Session"
  },
  {
    "type": "get",
    "url": "/getMotionGraph/{id_mo}/{?date}",
    "title": "Information on a specific motion",
    "name": "getMotionGraph",
    "group": "Session",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "id_mo",
            "optional": false,
            "field": "session",
            "description": "<p>id is parameter which returns exactly specified motion</p>"
          },
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>For when was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "session",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "session.name",
            "description": "<p>Name of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "session.date_ts",
            "description": "<p>Date and time of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "session.date",
            "description": "<p>Date of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.id",
            "description": "<p>Id of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "session.in_review",
            "description": "<p>Return true or false if session is in review.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "session.orgs",
            "description": "<p>Organization object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "session.orgs.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "session.orgs.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.orgs.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.orgs.name",
            "description": "<p>Name of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "name",
            "description": "<p>Name of motion</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "id",
            "description": "<p>Motions id</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "required",
            "description": "<p>Number of required votes to pass the motion.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "result",
            "description": "<p>Result of motion.</p>"
          },
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "documents",
            "description": "<p>Links to the documents of motion.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "all",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "all.kvorum",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.kvorum.option",
            "description": "<p>Name of option</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "all.kvorum.total_votes",
            "description": "<p>Total votes for this option</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "all.kvorum.breakdown",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "all.kvorum.breakdown.pg",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "rall.kvorum.breakdown.pg.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "rall.kvorum.breakdown.pg.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "all.kvorum.breakdown.pg.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "all.kvorum.breakdown.pg.name",
            "description": "<p>Name of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "all.kvorum.breakdown.mps",
            "description": "<p>MP's person object</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "all.kvorum.breakdown.mps.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "all.kvorum.breakdown.mps.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.kvorum.breakdown.mps.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.kvorum.breakdown.mps.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.kvorum.breakdown.mps.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "all.kvorum.breakdown.mps.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.kvorum.breakdown.mps.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "all.kvorum.breakdown.mps.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "all.kvorum.breakdown.mps.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.kvorum.breakdown.mps.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.kvorum.breakdown.mps.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "all.kvorum.breakdown.mps.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "all.kvorum.breakdown.mps.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "all.not_present",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.not_present.option",
            "description": "<p>Name of option</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "all.not_present.total_votes",
            "description": "<p>Total votes for this option</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "all.not_present.breakdown",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "all.not_present.breakdown.pg",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "rall.not_present.breakdown.pg.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "rall.not_present.breakdown.pg.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "all.not_present.breakdown.pg.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "all.not_present.breakdown.pg.name",
            "description": "<p>Name of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "all.not_present.breakdown.mps",
            "description": "<p>MP's person object</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "all.not_present.breakdown.mps.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "all.not_present.breakdown.mps.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.not_present.breakdown.mps.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.not_present.breakdown.mps.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.not_present.breakdown.mps.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "all.not_present.breakdown.mps.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.not_present.breakdown.mps.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "all.not_present.breakdown.mps.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "all.not_present.breakdown.mps.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.not_present.breakdown.mps.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.not_present.breakdown.mps.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "all.not_present.breakdown.mps.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "all.not_present.breakdown.mps.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "all.against",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.against.option",
            "description": "<p>Name of option</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "all.against.total_votes",
            "description": "<p>Total votes for this option</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "all.against.breakdown",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "all.against.breakdown.pg",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "rall.against.breakdown.pg.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "rall.against.breakdown.pg.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "all.against.breakdown.pg.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "all.against.breakdown.pg.name",
            "description": "<p>Name of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "all.against.breakdown.mps",
            "description": "<p>MP's person object</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "all.against.breakdown.mps.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "all.against.breakdown.mps.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.against.breakdown.mps.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.against.breakdown.mps.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.against.breakdown.mps.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "all.against.breakdown.mps.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.against.breakdown.mps.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "all.against.breakdown.mps.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "all.against.breakdown.mps.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.against.breakdown.mps.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.against.breakdown.mps.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "all.against.breakdown.mps.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "all.against.breakdown.mps.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "all.for",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.for.option",
            "description": "<p>Name of option</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "all.for.total_votes",
            "description": "<p>Total votes for this option</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "all.for.breakdown",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "all.for.breakdown.pg",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "rall.for.breakdown.pg.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "rall.for.breakdown.pg.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "all.for.breakdown.pg.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "all.for.breakdown.pg.name",
            "description": "<p>Name of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "all.for.breakdown.mps",
            "description": "<p>MP's person object</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "all.for.breakdown.mps.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "all.for.breakdown.mps.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.for.breakdown.mps.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.for.breakdown.mps.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.for.breakdown.mps.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "all.for.breakdown.mps.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.for.breakdown.mps.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "all.for.breakdown.mps.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "all.for.breakdown.mps.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.for.breakdown.mps.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "all.for.breakdown.mps.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "all.for.breakdown.mps.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "all.for.breakdown.mps.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n\"session\": {\n\"name\": \"28. redna seja\",\n\"date_ts\": \"2017-03-20T01:00:00\",\n\"orgs\": [\n{\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"id\": 95,\n\"name\": \"Državni zbor\"\n}\n],\n\"date\": \"20. 3. 2017\",\n\"org\": {\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"id\": 95,\n\"name\": \"Državni zbor\"\n},\n\"id\": 9379,\n\"in_review\": true\n},\n\"all\": {\n\"kvorum\": {\n\"breakdown\": [],\n\"option\": \"kvorum\",\n\"total_votes\": 0\n},\n\"not_present\": {},\n\"against\": {},\n\"for\": {}\n},\n\"created_for\": \"20.03.2017\",\n\"name\": \"Dnevni red v celoti\",\n\"documents\": [],\n\"created_at\": \"21.03.2017\",\n\"required\": \"62\",\n\"id\": \"6900\",\n\"result\": true\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/s/getMotionGraph/6900",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/s/getMotionGraph/6900/21.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaseje/views.py",
    "groupTitle": "Session"
  },
  {
    "type": "get",
    "url": "/getMotionOfSession/{session_id}/{?date}",
    "title": "All motions from a specific session",
    "name": "getMotionOfSession",
    "group": "Session",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "speech_id",
            "optional": false,
            "field": "session",
            "description": "<p>id is parameter which returns exactly specified session</p>"
          },
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>For when was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "session",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "session.name",
            "description": "<p>Name of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "session.date_ts",
            "description": "<p>Date and time of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "session.date",
            "description": "<p>Date of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.id",
            "description": "<p>Id of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "session.in_review",
            "description": "<p>Return true or false if session is in review.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "session.orgs",
            "description": "<p>Organization object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "session.orgs.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "session.orgs.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.orgs.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.orgs.name",
            "description": "<p>Name of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results",
            "description": "<p>IDs of all speeches on session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.session",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.session.name",
            "description": "<p>Name of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "results.session.date_ts",
            "description": "<p>Date and time of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "results.session.date",
            "description": "<p>Date of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.session.id",
            "description": "<p>Id of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.session.in_review",
            "description": "<p>Return true or false if session is in review.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results.session.orgs",
            "description": "<p>Organization object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.session.orgs.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.session.orgs.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.session.orgs.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.session.orgs.name",
            "description": "<p>Name of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.results",
            "description": "<p>IDs of all speeches on session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.abstain",
            "description": "<p>Number of MPs that abstain on voting.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.against",
            "description": "<p>Number of MPs that are against on voting.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.motion_id",
            "description": "<p>ID of motion.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.text",
            "description": "<p>Text of motion</p>"
          },
          {
            "group": "Success 200",
            "type": "String[]",
            "optional": false,
            "field": "results.tags",
            "description": "<p>Array of tags of motion.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.is_outlier",
            "description": "<p>Analaysis if person is outlier.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.not_present",
            "description": "<p>Number of MPs that were not present.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.votes_for",
            "description": "<p>Number of MPs that voted with yes.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.result",
            "description": "<p>True or False if the motion was successful.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n\"created_at\": null,\n\"created_for\": \"05.04.2017\",\n\"session\": {\n\"name\": \"33. redna seja\",\n\"date_ts\": \"2017-04-05T02:00:00\",\n\"orgs\": [\n{\n\"acronym\": \"\",\n\"is_coalition\": false,\n\"id\": 25,\n\"name\": \"Odbor za pravosodje\"\n}\n],\n\"date\": \"5. 4. 2017\",\n\"org\": {\n\"acronym\": \"\",\n\"is_coalition\": false,\n\"id\": 25,\n\"name\": \"Odbor za pravosodje\"\n},\n\"id\": 9408,\n\"in_review\": true\n},\n\"results\": [],\n\"tags\": [\n\"Komisija za nadzor javnih financ\",\n\"Kolegij predsednika Državnega zbora\",\n\"Komisija za narodni skupnosti\",\n\"Komisija za odnose s Slovenci v zamejstvu in po svetu\",\n\"Komisija za poslovnik\",\n\"Mandatno-volilna komisija\",\n\"Odbor za delo, družino, socialne zadeve in invalide\",\n\"Odbor za finance in monetarno politiko\",\n\"Odbor za gospodarstvo\",\n\"Odbor za infrastrukturo, okolje in prostor\",\n\"Odbor za izobraževanje, znanost, šport in mladino\",\n\"Odbor za kmetijstvo, gozdarstvo in prehrano\",\n\"Odbor za kulturo\",\n\"Odbor za notranje zadeve, javno upravo in lokalno samoupravo\",\n\"Odbor za obrambo\",\n\"Odbor za pravosodje\",\n\"Odbor za zadeve Evropske unije\",\n\"Odbor za zdravstvo\",\n\"Odbor za zunanjo politiko\",\n\"Preiskovalna komisija o ugotavljanju zlorab v slovenskem bančnem sistemu ter ugotavljanju vzrokov in\",\n\"Preiskovalna komisija za ugotavljanje politične odgovornosti nosilcev javnih funkcij pri investiciji\",\n\"Ustavna komisija\",\n\"Proceduralna glasovanja\",\n\"Zunanja imenovanja\",\n\"Poslanska vprašanja\",\n\"Komisija za nadzor obveščevalnih in varnostnih služb\",\n\"Preiskovalne komisije\",\n\"Komisija za peticije ter za človekove pravice in enake možnosti\",\n\"Interpelacija\",\n\" Preiskovalna komisija za ugotavljanje politične odgovornosti nosilcev javnih funkcij pri investicij\"\n]\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/s/getMotionOfSession/9427",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/s/getMotionOfSession/9427/21.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaseje/views.py",
    "groupTitle": "Session"
  },
  {
    "type": "get",
    "url": "/getPresenceOfPG/{session_id}/{?date}",
    "title": "PGs' presence on a specific session",
    "name": "getPresenceOfPG",
    "group": "Session",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "session_id",
            "optional": false,
            "field": "session",
            "description": "<p>id is parameter which returns exactly specified session</p>"
          },
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>For when was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "session",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "session.name",
            "description": "<p>Name of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "session.date_ts",
            "description": "<p>Date and time of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "session.date",
            "description": "<p>Date of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.id",
            "description": "<p>Id of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "session.in_review",
            "description": "<p>Return true or false if session is in review.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "session.orgs",
            "description": "<p>Organization object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "session.orgs.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "session.orgs.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.orgs.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.orgs.name",
            "description": "<p>Name of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.percent",
            "description": "<p>Percent of presence on session for each PG.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.organization",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.organization.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.organization.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.organization.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.organization.name",
            "description": "<p>Name of organization</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n\"session\": {\n\"name\": \"28. redna seja\",\n\"date_ts\": \"2017-03-20T01:00:00\",\n\"orgs\": [\n{\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"id\": 95,\n\"name\": \"Državni zbor\"\n}\n],\n\"date\": \"20. 3. 2017\",\n\"org\": {\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"id\": 95,\n\"name\": \"Državni zbor\"\n},\n\"id\": 9379,\n\"in_review\": true\n},\n\"created_at\": \"12.04.2017\",\n\"created_for\": \"20.03.2017\",\n\"results\": [\n{\n\"organization\": {\n\"acronym\": \"IMNS\",\n\"is_coalition\": false,\n\"id\": 2,\n\"name\": \"PS italijanske in madžarske narodne skupnosti\"\n},\n\"percent\": 96\n},\n...\n]\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/s/getPresenceOfPG/9379",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/s/getPresenceOfPG/9379/21.12.2016",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaseje/views.py",
    "groupTitle": "Session"
  },
  {
    "type": "get",
    "url": "/getQuote/{quote_id}",
    "title": "Get quote",
    "name": "getQuote",
    "group": "Session",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "quote_id",
            "optional": false,
            "field": "quote",
            "description": "<p>id is parameter which returns exactly specified quote</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person",
            "description": "<p>MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing). *</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>For when was this data created? *</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.quote_id",
            "description": "<p>Id of quote if exists.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.content",
            "description": "<p>Content of speech. *</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.session",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.session.name",
            "description": "<p>Name of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "results.session.date_ts",
            "description": "<p>Date and time of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "results.session.date",
            "description": "<p>Date of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.session.id",
            "description": "<p>Id of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.session.in_review",
            "description": "<p>Return true or false if session is in review.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results.session.orgs",
            "description": "<p>Organization object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.session.orgs.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.session.orgs.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.session.orgs.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.session.orgs.name",
            "description": "<p>Name of organization *</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.quoted_text",
            "description": "<p>Content of quoted text.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.speech_id",
            "description": "<p>Id of speech.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.end_idx",
            "description": "<p>End intex of quoted text.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.start_idx",
            "description": "<p>End intex of quoted text.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n\"person\": {\n\"is_active\": false,\n\"district\": [\n76\n],\n\"name\": \"Milan Brglez\",\n\"gov_id\": \"P243\",\n\"gender\": \"m\",\n\"party\": {\n\"acronym\": \"SMC\",\n\"is_coalition\": true,\n\"id\": 1,\n\"name\": \"PS Stranka modernega centra\"\n},\n\"type\": \"mp\",\n\"id\": 11,\n\"has_function\": true\n},\n\"created_at\": \"16.04.2017\",\n\"created_for\": \"16.04.2017\",\n\"results\": {\n\"quote_id\": 354,\n\"content\": \"Spoštovane kolegice poslanke in kolegi poslanci, gospe in gospodje! ...\n\"session\": {\n\"name\": \"28. redna seja\",\n\"date_ts\": \"2017-03-20T01:00:00\",\n\"orgs\": [\n{\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"id\": 95,\n\"name\": \"Državni zbor\"\n}\n],\n\"date\": \"20. 3. 2017\",\n\"org\": {\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"id\": 95,\n\"name\": \"Državni zbor\"\n},\n\"id\": 9379,\n\"in_review\": true\n},\n\"quoted_text\": \"pozdravljam. Prehajamo na določitev dnevnega reda 28. seje Državnega zbora....\n\"speech_id\": 1178191,\n\"end_idx\": 1947,\n\"start_idx\": 898\n}\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/s/getQuote/354",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaseje/views.py",
    "groupTitle": "Session"
  },
  {
    "type": "get",
    "url": "/getSessionsByClassification/",
    "title": "All sessions grouped by classification",
    "name": "getSessionsByClassification",
    "group": "Session",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "kolegij",
            "description": "<p>Classification of session</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "kolegij.name",
            "description": "<p>Name of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "kolegij.date_ts",
            "description": "<p>Date and time of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "kolegij.date",
            "description": "<p>Date of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "kolegij.id",
            "description": "<p>Id of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "kolegij.in_review",
            "description": "<p>Returns true or false if session is in review.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "kolegij.votes",
            "description": "<p>Returns true or false if session has votes.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "kolegij.speeches",
            "description": "<p>Returns true or false if session has speeches.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "kolegij.orgs",
            "description": "<p>Organization object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "kolegij.orgs.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "kolegij.orgs.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "kolegij.orgs.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "kolegij.orgs.name",
            "description": "<p>Name of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "dt",
            "description": "<p>Classification of session</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "dt.name",
            "description": "<p>Name of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "dt.date_ts",
            "description": "<p>Date and time of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "dt.date",
            "description": "<p>Date of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "dt.id",
            "description": "<p>Id of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "dt.in_review",
            "description": "<p>Returns true or false if session is in review.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "dt.votes",
            "description": "<p>Returns true or false f session has votes.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "dt.speeches",
            "description": "<p>Returns true or false if session has speeches.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "dt.orgs",
            "description": "<p>Organization object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "dt.orgs.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "dt.orgs.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "dt.orgs.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "dt.orgs.name",
            "description": "<p>Name of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "dz",
            "description": "<p>Classification of session</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "dz.name",
            "description": "<p>Name of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "dz.date_ts",
            "description": "<p>Date and time of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "dz.date",
            "description": "<p>Date of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "dz.id",
            "description": "<p>Id of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "dz.in_review",
            "description": "<p>Returns true or false if session is in review.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "dz.votes",
            "description": "<p>Returns true or false f session has votes.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "dz.speeches",
            "description": "<p>Returns true or false if session has speeches.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "dz.orgs",
            "description": "<p>Organization object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "dz.orgs.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "dz.orgs.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "dz.orgs.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "dz.orgs.name",
            "description": "<p>Name of organization</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n\"kolegij\": [\n{\n\"votes\": false,\n\"name\": \"91. redna seja\",\n\"date_ts\": \"2017-04-13T02:00:00\",\n\"speeches\": true,\n\"orgs\": [\n{\n\"acronym\": \"\",\n\"is_coalition\": false,\n\"id\": 9,\n\"name\": \"Kolegij predsednika državnega zbora\"\n}\n],\n\"date\": \"13. 4. 2017\",\n\"org\": {\n\"acronym\": \"\",\n\"is_coalition\": false,\n\"id\": 9,\n\"name\": \"Kolegij predsednika državnega zbora\"\n},\n\"id\": 9419,\n\"in_review\": true\n},\n\"dt\": [\n{\n\"acronym\": \"\",\n\"sessions\": [\n{\n\"votes\": false,\n\"name\": \"39. redna seja\",\n\"date_ts\": \"2017-03-31T02:00:00\",\n\"speeches\": false,\n\"orgs\": [\n{\n\"acronym\": \"\",\n\"is_coalition\": false,\n\"id\": 101,\n\"name\": \"Preiskovalna komisija za ugotavljanje politične odgovornosti nosilcev javnih funkcij pri investiciji v blok 6 Termoelektrarne Šoštanj\"\n}\n],\n\"date\": \"31. 3. 2017\",\n\"org\": {\n\"acronym\": \"\",\n\"is_coalition\": false,\n\"id\": 101,\n\"name\": \"Preiskovalna komisija za ugotavljanje politične odgovornosti nosilcev javnih funkcij pri investiciji v blok 6 Termoelektrarne Šoštanj\"\n},\n\"id\": 9397,\n\"in_review\": false\n},\n\"dz\": [\n{\n\"votes\": true,\n\"name\": \"28. redna seja\",\n\"date_ts\": \"2017-03-20T01:00:00\",\n\"speeches\": true,\n\"orgs\": [\n{\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"id\": 95,\n\"name\": \"Državni zbor\"\n}\n],\n\"date\": \"20. 3. 2017\",\n\"org\": {\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"id\": 95,\n\"name\": \"Državni zbor\"\n},\n\"id\": 9379,\n\"in_review\": true\n}\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/s/getSessionsByClassification",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaseje/views.py",
    "groupTitle": "Session"
  },
  {
    "type": "get",
    "url": "/getSessionsList/",
    "title": "List all sessions",
    "name": "getSessionsList",
    "group": "Session",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          },
          {
            "group": "Parameter",
            "type": "Boolean",
            "optional": false,
            "field": "force_render",
            "description": "<p>Optional force render.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>For when was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "session",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "session.name",
            "description": "<p>Name of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "session.date_ts",
            "description": "<p>Date and time of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "session.date",
            "description": "<p>Date of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "session.updated_at_ts",
            "description": "<p>Last update of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.id",
            "description": "<p>Id of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "session.in_review",
            "description": "<p>Return true or false if session is in review.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "session.speeches",
            "description": "<p>Return true or false if session has speeches.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "session.votes",
            "description": "<p>Return true or false if session has votes_for.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "session.orgs",
            "description": "<p>Organization object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "session.orgs.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "session.orgs.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.orgs.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.orgs.name",
            "description": "<p>Name of organization</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n\"created_at\": \"24.04.2017\",\n\"created_for\": \"24.04.2017\",\n\"sessions\": [\n{\n\"updated_at_ts\": \"2017-04-24T20:39:11.782\",\n\"speeches\": true,\n\"name\": \"29. redna seja\",\n\"date_ts\": \"2017-04-20T02:00:00\",\n\"votes\": true,\n\"updated_at\": \"24.04.2017\",\n\"org\": {\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"name\": \"Državni zbor\",\n\"id\": 95\n},\n\"date\": \"20. 4. 2017\",\n\"orgs\": [\n{\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"name\": \"Državni zbor\",\n\"id\": 95\n}\n],\n\"id\": 9427,\n\"in_review\": true\n},\n{\n\"updated_at_ts\": \"2017-04-20T01:26:40.675\",\n\"speeches\": true,\n\"name\": \"93. redna seja\",\n\"date_ts\": \"2017-04-19T02:00:00\",\n\"votes\": false,\n\"updated_at\": \"20.04.2017\",\n\"org\": {\n\"acronym\": \"\",\n\"is_coalition\": false,\n\"name\": \"Kolegij predsednika državnega zbora\",\n\"id\": 9\n},\n\"date\": \"19. 4. 2017\",\n\"orgs\": [\n{\n\"acronym\": \"\",\n\"is_coalition\": false,\n\"name\": \"Kolegij predsednika državnega zbora\",\n\"id\": 9\n}\n],\n\"id\": 9424,\n\"in_review\": true\n}\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/s/getSessionsList/",
        "type": "curl"
      },
      {
        "title": "Example with date:",
        "content": "curl -i https://analize.parlameter.si/v1/s/getSessionsList/21.12.2016",
        "type": "curl"
      },
      {
        "title": "Example with force_render:",
        "content": "curl -i https://analize.parlameter.si/v1/s/getSessionsList/True",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaseje/views.py",
    "groupTitle": "Session"
  },
  {
    "type": "get",
    "url": "/getSpeechesIDsOfSession/{session_id}",
    "title": "IDs of all speeches from a specific session",
    "name": "getSpeechesIDsOfSession",
    "group": "Session",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "session_id",
            "optional": false,
            "field": "session",
            "description": "<p>id is parameter which returns specific session</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>For when was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "session",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "session.name",
            "description": "<p>Name of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "session.date_ts",
            "description": "<p>Date and time of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "session.date",
            "description": "<p>Date of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.id",
            "description": "<p>Id of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "session.in_review",
            "description": "<p>Return true or false if session is in review.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "session.orgs",
            "description": "<p>Organization object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "session.orgs.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "session.orgs.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.orgs.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.orgs.name",
            "description": "<p>Name of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "results",
            "description": "<p>IDs of all speeches on session. *</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n\"created_for\": \"05.04.2017\",\n\"session\": {\n\"name\": \"33. redna seja\",\n\"date_ts\": \"2017-04-05T02:00:00\",\n\"orgs\": [\n{\n\"acronym\": \"\",\n\"is_coalition\": false,\n\"id\": 25,\n\"name\": \"Odbor za pravosodje\"\n}\n],\n\"date\": \"5. 4. 2017\",\n\"org\": {\n\"acronym\": \"\",\n\"is_coalition\": false,\n\"id\": 25,\n\"name\": \"Odbor za pravosodje\"\n},\n\"id\": 9408,\n\"in_review\": true\n},\n\"created_at\": \"16.04.2017\",\n\"results\": [\n1176731,\n1176732,\n1176733,\n1176734,\n...\n]}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/s/getSpeechesIDsOfSession/9408",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaseje/views.py",
    "groupTitle": "Session"
  },
  {
    "type": "get",
    "url": "/getSpeechesOfSession/{session_id}",
    "title": "All speeches from a session",
    "name": "getSpeechesOfSession",
    "group": "Session",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "session_id",
            "optional": false,
            "field": "session",
            "description": "<p>id is parameter which returns specific session</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>For when was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "session",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "session.name",
            "description": "<p>Name of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "session.date_ts",
            "description": "<p>Date and time of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "session.date",
            "description": "<p>Date of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.id",
            "description": "<p>Id of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "session.in_review",
            "description": "<p>Return true or false if session is in review.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "session.orgs",
            "description": "<p>Organization object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "session.orgs.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "session.orgs.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.orgs.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.orgs.name",
            "description": "<p>Name of organization *</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results",
            "description": "<p>Array of persons and speeches of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.person",
            "description": "<p>person MP's person object (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.person.is_active",
            "description": "<p>Answer the question: Is this MP currently active?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "results.person.district",
            "description": "<p>List of Parladata ids for districts this person was elected in.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.person.name",
            "description": "<p>MP's full name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.person.gov_id",
            "description": "<p>MP's id on www.dz-rs.si</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.person.gender",
            "description": "<p>MP's gender (f/m) used for grammar</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.person.party",
            "description": "<p>This MP's standard party objects (comes with most calls).</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.person.party.acronym",
            "description": "<p>The MP's party's acronym.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.person.party.is_coalition",
            "description": "<p>Answers the question: Is this party in coalition with the government?</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.person.party.id",
            "description": "<p>This party's Parladata (organization) id.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.person.party.name",
            "description": "<p>The party's name.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.person.type",
            "description": "<p>The person's parlalize type. Always &quot;mp&quot; for MPs.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.person.id",
            "description": "<p>The person's Parladata id.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.person.has_function",
            "description": "<p>Answers the question: Is this person the president or vice president of the national assembly (speaker of the house kind of thing).</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.results",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.results.quote_id",
            "description": "<p>Id of quote if exists.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.results.content",
            "description": "<p>Content of speech. *</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.results.session",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.results.session.name",
            "description": "<p>Name of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "results.results.session.date_ts",
            "description": "<p>Date and time of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "results.results.session.date",
            "description": "<p>Date of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.results.session.id",
            "description": "<p>Id of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.results.session.in_review",
            "description": "<p>Return true or false if session is in review.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results.results.session.orgs",
            "description": "<p>Organization object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.results.session.orgs.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.results.session.orgs.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.results.session.orgs.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.results.session.orgs.name",
            "description": "<p>Name of organization *</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.results.quoted_text",
            "description": "<p>Content of quoted text.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.results.speech_id",
            "description": "<p>Id of speech.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.results.end_idx",
            "description": "<p>End intex of quoted text.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.results.start_idx",
            "description": "<p>End intex of quoted text. * *</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n\"created_for\": \"05.04.2017\",\n\"session\": {\n\"name\": \"33. redna seja\",\n\"date_ts\": \"2017-04-05T02:00:00\",\n\"orgs\": [\n{\n\"acronym\": \"\",\n\"is_coalition\": false,\n\"id\": 25,\n\"name\": \"Odbor za pravosodje\"\n}\n],\n\"date\": \"5. 4. 2017\",\n\"org\": {\n\"acronym\": \"\",\n\"is_coalition\": false,\n\"id\": 25,\n\"name\": \"Odbor za pravosodje\"\n},\n\"id\": 9408,\n\"in_review\": true\n},\n\"created_at\": \"16.04.2017\",\n\"results\": [\n{\n\"person\": {\n\"is_active\": false,\n\"district\": [\n36\n],\n\"name\": \"Jan Škoberne\",\n\"gov_id\": \"P301\",\n\"gender\": \"m\",\n\"party\": {\n\"acronym\": \"SD\",\n\"is_coalition\": true,\n\"id\": 7,\n\"name\": \"PS Socialni Demokrati\"\n},\n\"type\": \"mp\",\n\"id\": 1356,\n\"has_function\": false\n},\n\"results\": {\n\"quote_id\": null,\n\"content\": \"Spoštovane kolegice in kolegi, dragi in cenjeni gostje, dobro jutro, dobrodošli! ...\n\"session\": {\n\"name\": \"33. redna seja\",\n\"date_ts\": \"2017-04-05T02:00:00\",\n\"orgs\": [\n{\n\"acronym\": \"\",\n\"is_coalition\": false,\n\"id\": 25,\n\"name\": \"Odbor za pravosodje\"\n}\n],\n\"date\": \"5. 4. 2017\",\n\"org\": {\n\"acronym\": \"\",\n\"is_coalition\": false,\n\"id\": 25,\n\"name\": \"Odbor za pravosodje\"\n},\n\"id\": 9408,\n\"in_review\": true\n},\n\"quoted_text\": null,\n\"speech_id\": 1176731,\n\"end_idx\": null,\n\"start_idx\": null\n}\n},\n{\n\"person\": {\n\"is_active\": null,\n\"district\": null,\n\"name\": \"Tina Brecelj\",\n\"gov_id\": \"G1373\",\n\"gender\": null,\n\"party\": {\n\"acronym\": null,\n\"is_coalition\": null,\n\"id\": null,\n\"name\": null\n},\n\"type\": \"visitor\",\n\"id\": 1373,\n\"has_function\": false\n},\n\"results\": {\n\"quote_id\": null,\n\"content\": \"Najlepša hvala gospod predsednik za besedo. Spoštovane poslanke, poslanci, spoštovani gostje,...\n\"session\": {\n\"name\": \"33. redna seja\",\n\"date_ts\": \"2017-04-05T02:00:00\",\n\"orgs\": [\n{\n\"acronym\": \"\",\n\"is_coalition\": false,\n\"id\": 25,\n\"name\": \"Odbor za pravosodje\"\n}\n],\n\"date\": \"5. 4. 2017\",\n\"org\": {\n\"acronym\": \"\",\n\"is_coalition\": false,\n\"id\": 25,\n\"name\": \"Odbor za pravosodje\"\n},\n\"id\": 9408,\n\"in_review\": true\n},\n\"quoted_text\": null,\n\"speech_id\": 1176732,\n\"end_idx\": null,\n\"start_idx\": null\n}\n}\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/s/getSpeechesOfSession/9408",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaseje/views.py",
    "groupTitle": "Session"
  },
  {
    "type": "get",
    "url": "/getTFIDF/{session_id}",
    "title": "TFIDF analysis of a specific session",
    "name": "getTFIDF",
    "group": "Session",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "date",
            "optional": false,
            "field": "date",
            "description": "<p>Optional date.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Json",
            "optional": false,
            "field": "returns",
            "description": "<p>data of TFIDF analysis.</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_at",
            "description": "<p>When was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>For when was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "session",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "session.name",
            "description": "<p>Name of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "session.date_ts",
            "description": "<p>Date and time of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "session.date",
            "description": "<p>Date of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.id",
            "description": "<p>Id of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "session.in_review",
            "description": "<p>Return true or false if session is in review.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "session.orgs",
            "description": "<p>Organization object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "session.orgs.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "session.orgs.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.orgs.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.orgs.name",
            "description": "<p>Name of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "results",
            "description": ""
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.term",
            "description": "<p>Term that is analyzed.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results.scores",
            "description": "<p>Scores of TFIDF</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.scores.tf",
            "description": "<p>Term frequency</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.scores.df",
            "description": "<p>Document frequency</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.scores.tf-idf",
            "description": "<p>Term frequency / Document frequency</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "{\n\"created_at\": \"22.03.2017\",\n\"created_for\": \"22.03.2017\",\n\"session\": {\n\"name\": \"28. redna seja\",\n\"date_ts\": \"2017-03-20T01:00:00\",\n\"orgs\": [\n{\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"id\": 95,\n\"name\": \"Državni zbor\"\n}\n],\n\"date\": \"20. 3. 2017\",\n\"org\": {\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"id\": 95,\n\"name\": \"Državni zbor\"\n},\n\"id\": 9379,\n\"in_review\": true\n},\n\"results\": [\n{\n\"term\": \"filharmonija\",\n\"scores\": {\n\"tf\": 18,\n\"df\": 28,\n\"tf-idf\": 0.6428571428571429\n}\n},\n{\n\"term\": \"Plečnikov\",\n\"scores\": {\n\"tf\": 15,\n\"df\": 55,\n\"tf-idf\": 0.2727272727272727\n}\n}\n]\n}",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/s/getTFIDF/9379",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaseje/views.py",
    "groupTitle": "Session"
  },
  {
    "type": "get",
    "url": "/getVotesData/{votes}",
    "title": "Requests detailed data of votes",
    "name": "getVotesData",
    "group": "Session",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "votes",
            "optional": false,
            "field": "votes",
            "description": "<p>is parameter which returns detailed data of all comma separated votes ids given as a parameter</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "date",
            "optional": false,
            "field": "created_for",
            "description": "<p>For when was this data created?</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "session",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "session.name",
            "description": "<p>Name of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "session.date_ts",
            "description": "<p>Date and time of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Date",
            "optional": false,
            "field": "session.date",
            "description": "<p>Date of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.id",
            "description": "<p>Id of session.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "session.in_review",
            "description": "<p>Return true or false if session is in review.</p>"
          },
          {
            "group": "Success 200",
            "type": "Object[]",
            "optional": false,
            "field": "session.orgs",
            "description": "<p>Organization object</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "session.orgs.acronym",
            "description": "<p>Organization acronym</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "session.orgs.is_coalition",
            "description": "<p>True of False if organization is in coalition</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.orgs.id",
            "description": "<p>Id of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "session.orgs.name",
            "description": "<p>Name of organization</p>"
          },
          {
            "group": "Success 200",
            "type": "Object",
            "optional": false,
            "field": "results",
            "description": "<p>object</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.motion_id",
            "description": "<p>ID of motion.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "results.text",
            "description": "<p>Text of motion</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.not_present",
            "description": "<p>Number of MPs that were not present.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.votes_for",
            "description": "<p>Number of MPs that voted with yes.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.abstain",
            "description": "<p>Number of MPs that abstain on voting.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "results.against",
            "description": "<p>Number of MPs that are against on voting.</p>"
          },
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "results.result",
            "description": "<p>True or False if the motion was successful.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "[\n{\n\"session\": {\n\"name\": \"1. redna seja\",\n\"date_ts\": \"2014-08-01T02:00:00\",\n\"orgs\": [\n{\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"id\": 95,\n\"name\": \"Državni zbor\"\n}\n],\n\"date\": \"1. 8. 2014\",\n\"org\": {\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"id\": 95,\n\"name\": \"Državni zbor\"\n},\n\"id\": 6684,\n\"in_review\": false\n},\n\"created_for\": \"2014-08-01\",\n\"results\": {\n\"abstain\": 0,\n\"text\": \"Proceduralni predlog za prekinitev 1. točke dnevnega reda\",\n\"against\": 59,\n\"votes_for\": 26,\n\"motion_id\": 6512,\n\"not_present\": 5,\n\"result\": false\n}\n},\n{\n\"session\": {\n\"name\": \"1. redna seja\",\n\"date_ts\": \"2014-08-01T02:00:00\",\n\"orgs\": [\n{\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"id\": 95,\n\"name\": \"Državni zbor\"\n}\n],\n\"date\": \"1. 8. 2014\",\n\"org\": {\n\"acronym\": \"DZ\",\n\"is_coalition\": false,\n\"id\": 95,\n\"name\": \"Državni zbor\"\n},\n\"id\": 6684,\n\"in_review\": false\n},\n\"created_for\": \"2014-08-01\",\n\"results\": {\n\"abstain\": 0,\n\"text\": \"Dnevni red v celoti\",\n\"against\": 0,\n\"votes_for\": 84,\n\"motion_id\": 6513,\n\"not_present\": 6,\n\"result\": true\n}\n}\n]",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i https://analize.parlameter.si/v1/s/getVotesData/6512,6513",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaseje/views.py",
    "groupTitle": "Session"
  },
  {
    "type": "get",
    "url": "/getWorkingBodies/",
    "title": "List all working bodies",
    "name": "getWorkingBodies",
    "group": "Session",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Json",
            "optional": false,
            "field": "returns",
            "description": "<p>data of all working bodies.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>Id of working bodie.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "name",
            "description": "<p>Name of working bodie.</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Example response:",
          "content": "[\n{\n\"id\": 101,\n\"name\": \"Preiskovalna komisija za ugotavljanje politične odgovornosti nosilcev javnih funkcij pri investiciji v blok 6 Termoelektrarne Šoštanj\"\n},\n{\n\"id\": 106,\n\"name\": \"Preiskovalna komisija o ugotavljanju zlorab v slovenskem zdravstvenem sistemu na področju prodaje in nakupa žilnih opornic\"\n},\n{\n\"id\": 105,\n\"name\": \"Komisija za nadzor obveščevalnih in varnostnih služb\"\n}\n]",
          "type": "json"
        }
      ]
    },
    "examples": [
      {
        "title": "Example:",
        "content": "curl -i",
        "type": "curl"
      }
    ],
    "version": "0.0.0",
    "filename": "./parlaseje/views.py",
    "groupTitle": "Session"
  },
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "./doc/main.js",
    "group": "_home_muki_code_djnd_parlalize_doc_main_js",
    "groupTitle": "_home_muki_code_djnd_parlalize_doc_main_js",
    "name": ""
  },
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "./doc/template/main.js",
    "group": "_home_muki_code_djnd_parlalize_doc_template_main_js",
    "groupTitle": "_home_muki_code_djnd_parlalize_doc_template_main_js",
    "name": ""
  }
] });
