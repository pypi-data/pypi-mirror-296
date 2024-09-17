<div align="center">

[![Visit Humanloop](https://raw.githubusercontent.com/humanloop/humanloop-python/HEAD/python/header.png)](https://humanloop.com)

# Humanloop<a id="humanloop"></a>


[![PyPI](https://img.shields.io/badge/PyPI-v0.7.0beta.40-blue)](https://pypi.org/project/humanloop/0.7.0-beta.40)
[![README.md](https://img.shields.io/badge/README-Click%20Here-green)](https://github.com/humanloop/humanloop-python#readme)

</div>

> [!WARNING]
> This SDK has breaking changes in `>= 0.6.0` versions.
> All methods now return Pydantic models.
>
> ### Before (`< 0.6.0`)
>
> Previously, you had to use the `[]` syntax to access response values. This
> required a little more code for every property access.
>
> ```python
> chat_response = humanloop.chat(
>         # parameters
>     )
> print(chat_response.body["project_id"])
> ```
>
> ### After (`>= 0.6.0`)
>
> With Pydantic-based response values, you can use the `.` syntax to access. This
> is slightly less verbose and looks more Pythonic.
>
> ```python
> chat_response = humanloop.chat(
>         # parameters
>     )
> print(chat_response.project_id)
> ```
>
> To reuse existing implementations from `< 0.6.0`, use the `.raw` namespace as specified in the [Raw HTTP Response](#raw-http-response) section.

## Table of Contents<a id="table-of-contents"></a>

<!-- toc -->

- [Requirements](#requirements)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Async](#async)
- [Raw HTTP Response](#raw-http-response)
- [Streaming](#streaming)
- [Reference](#reference)
  * [`humanloop.chat`](#humanloopchat)
  * [`humanloop.chat_deployed`](#humanloopchat_deployed)
  * [`humanloop.chat_model_config`](#humanloopchat_model_config)
  * [`humanloop.complete`](#humanloopcomplete)
  * [`humanloop.complete_deployed`](#humanloopcomplete_deployed)
  * [`humanloop.complete_model_configuration`](#humanloopcomplete_model_configuration)
  * [`humanloop.datapoints.delete`](#humanloopdatapointsdelete)
  * [`humanloop.datapoints.get`](#humanloopdatapointsget)
  * [`humanloop.datapoints.update`](#humanloopdatapointsupdate)
  * [`humanloop.datasets.create`](#humanloopdatasetscreate)
  * [`humanloop.datasets.create_datapoint`](#humanloopdatasetscreate_datapoint)
  * [`humanloop.datasets.delete`](#humanloopdatasetsdelete)
  * [`humanloop.datasets.get`](#humanloopdatasetsget)
  * [`humanloop.datasets.list`](#humanloopdatasetslist)
  * [`humanloop.datasets.list_all_for_project`](#humanloopdatasetslist_all_for_project)
  * [`humanloop.datasets.list_datapoints`](#humanloopdatasetslist_datapoints)
  * [`humanloop.datasets.update`](#humanloopdatasetsupdate)
  * [`humanloop.evaluations.add_evaluators`](#humanloopevaluationsadd_evaluators)
  * [`humanloop.evaluations.create`](#humanloopevaluationscreate)
  * [`humanloop.evaluations.get`](#humanloopevaluationsget)
  * [`humanloop.evaluations.list`](#humanloopevaluationslist)
  * [`humanloop.evaluations.list_all_for_project`](#humanloopevaluationslist_all_for_project)
  * [`humanloop.evaluations.list_datapoints`](#humanloopevaluationslist_datapoints)
  * [`humanloop.evaluations.log`](#humanloopevaluationslog)
  * [`humanloop.evaluations.result`](#humanloopevaluationsresult)
  * [`humanloop.evaluations.update_status`](#humanloopevaluationsupdate_status)
  * [`humanloop.evaluators.create`](#humanloopevaluatorscreate)
  * [`humanloop.evaluators.delete`](#humanloopevaluatorsdelete)
  * [`humanloop.evaluators.get`](#humanloopevaluatorsget)
  * [`humanloop.evaluators.list`](#humanloopevaluatorslist)
  * [`humanloop.evaluators.update`](#humanloopevaluatorsupdate)
  * [`humanloop.feedback`](#humanloopfeedback)
  * [`humanloop.logs.delete`](#humanlooplogsdelete)
  * [`humanloop.logs.get`](#humanlooplogsget)
  * [`humanloop.logs.list`](#humanlooplogslist)
  * [`humanloop.log`](#humanlooplog)
  * [`humanloop.logs.update`](#humanlooplogsupdate)
  * [`humanloop.logs.update_by_ref`](#humanlooplogsupdate_by_ref)
  * [`humanloop.model_configs.deserialize`](#humanloopmodel_configsdeserialize)
  * [`humanloop.model_configs.export`](#humanloopmodel_configsexport)
  * [`humanloop.model_configs.get`](#humanloopmodel_configsget)
  * [`humanloop.model_configs.register`](#humanloopmodel_configsregister)
  * [`humanloop.model_configs.serialize`](#humanloopmodel_configsserialize)
  * [`humanloop.projects.create`](#humanloopprojectscreate)
  * [`humanloop.projects.create_feedback_type`](#humanloopprojectscreate_feedback_type)
  * [`humanloop.projects.deactivate_config`](#humanloopprojectsdeactivate_config)
  * [`humanloop.projects.delete`](#humanloopprojectsdelete)
  * [`humanloop.projects.delete_deployed_config`](#humanloopprojectsdelete_deployed_config)
  * [`humanloop.projects.deploy_config`](#humanloopprojectsdeploy_config)
  * [`humanloop.projects.export`](#humanloopprojectsexport)
  * [`humanloop.projects.get`](#humanloopprojectsget)
  * [`humanloop.projects.get_active_config`](#humanloopprojectsget_active_config)
  * [`humanloop.projects.list`](#humanloopprojectslist)
  * [`humanloop.projects.list_configs`](#humanloopprojectslist_configs)
  * [`humanloop.projects.list_deployed_configs`](#humanloopprojectslist_deployed_configs)
  * [`humanloop.projects.update`](#humanloopprojectsupdate)
  * [`humanloop.projects.update_feedback_types`](#humanloopprojectsupdate_feedback_types)
  * [`humanloop.sessions.create`](#humanloopsessionscreate)
  * [`humanloop.sessions.get`](#humanloopsessionsget)
  * [`humanloop.sessions.list`](#humanloopsessionslist)

<!-- tocstop -->

## Requirements<a id="requirements"></a>

Python >=3.7

## Installation<a id="installation"></a>

```sh
pip install humanloop==0.7.0-beta.40
```

## Getting Started<a id="getting-started"></a>

```python
from pprint import pprint
from humanloop import Humanloop, ApiException

humanloop = Humanloop(
    api_key="YOUR_API_KEY",
    openai_api_key="YOUR_OPENAI_API_KEY",
    anthropic_api_key="YOUR_ANTHROPIC_API_KEY",
)

try:
    # Chat
    chat_response = humanloop.chat(
        project="sdk-example",
        messages=[
            {
                "role": "user",
                "content": "Explain asynchronous programming.",
            }
        ],
        model_config={
            "model": "gpt-3.5-turbo",
            "max_tokens": -1,
            "temperature": 0.7,
            "chat_template": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant who replies in the style of {{persona}}.",
                },
            ],
        },
        inputs={
            "persona": "the pirate Blackbeard",
        },
        stream=False,
    )
    print(chat_response)
except ApiException as e:
    print("Exception when calling .chat: %s\n" % e)
    pprint(e.body)
    if e.status == 422:
        pprint(e.body["detail"])
    pprint(e.headers)
    pprint(e.status)
    pprint(e.reason)
    pprint(e.round_trip_time)

try:
    # Complete
    complete_response = humanloop.complete(
        project="sdk-example",
        inputs={
            "text": "Llamas that are well-socialized and trained to halter and lead after weaning and are very friendly and pleasant to be around. They are extremely curious and most will approach people easily. However, llamas that are bottle-fed or over-socialized and over-handled as youth will become extremely difficult to handle when mature, when they will begin to treat humans as they treat each other, which is characterized by bouts of spitting, kicking and neck wrestling.[33]",
        },
        model_config={
            "model": "gpt-3.5-turbo",
            "max_tokens": -1,
            "temperature": 0.7,
            "prompt_template": "Summarize this for a second-grade student:\n\nText:\n{{text}}\n\nSummary:\n",
        },
        stream=False,
    )
    print(complete_response)
except ApiException as e:
    print("Exception when calling .complete: %s\n" % e)
    pprint(e.body)
    if e.status == 422:
        pprint(e.body["detail"])
    pprint(e.headers)
    pprint(e.status)
    pprint(e.reason)
    pprint(e.round_trip_time)

try:
    # Feedback
    feedback_response = humanloop.feedback(
        type="rating",
        value="good",
        data_id="data_[...]",
        user="user@example.com",
    )
    print(feedback_response)
except ApiException as e:
    print("Exception when calling .feedback: %s\n" % e)
    pprint(e.body)
    if e.status == 422:
        pprint(e.body["detail"])
    pprint(e.headers)
    pprint(e.status)
    pprint(e.reason)
    pprint(e.round_trip_time)

try:
    # Log
    log_response = humanloop.log(
        project="sdk-example",
        inputs={
            "text": "Llamas that are well-socialized and trained to halter and lead after weaning and are very friendly and pleasant to be around. They are extremely curious and most will approach people easily. However, llamas that are bottle-fed or over-socialized and over-handled as youth will become extremely difficult to handle when mature, when they will begin to treat humans as they treat each other, which is characterized by bouts of spitting, kicking and neck wrestling.[33]",
        },
        output="Llamas can be friendly and curious if they are trained to be around people, but if they are treated too much like pets when they are young, they can become difficult to handle when they grow up. This means they might spit, kick, and wrestle with their necks.",
        source="sdk",
        config={
            "model": "gpt-3.5-turbo",
            "max_tokens": -1,
            "temperature": 0.7,
            "prompt_template": "Summarize this for a second-grade student:\n\nText:\n{{text}}\n\nSummary:\n",
            "type": "model",
        },
    )
    print(log_response)
except ApiException as e:
    print("Exception when calling .log: %s\n" % e)
    pprint(e.body)
    if e.status == 422:
        pprint(e.body["detail"])
    pprint(e.headers)
    pprint(e.status)
    pprint(e.reason)
    pprint(e.round_trip_time)
```

## Async<a id="async"></a>

`async` support is available by prepending `a` to any method.

```python
import asyncio
from pprint import pprint
from humanloop import Humanloop, ApiException

humanloop = Humanloop(
    api_key="YOUR_API_KEY",
    openai_api_key="YOUR_OPENAI_API_KEY",
    anthropic_api_key="YOUR_ANTHROPIC_API_KEY",
)


async def main():
    try:
        complete_response = await humanloop.acomplete(
            project="sdk-example",
            inputs={
                "text": "Llamas that are well-socialized and trained to halter and lead after weaning and are very friendly and pleasant to be around. They are extremely curious and most will approach people easily. However, llamas that are bottle-fed or over-socialized and over-handled as youth will become extremely difficult to handle when mature, when they will begin to treat humans as they treat each other, which is characterized by bouts of spitting, kicking and neck wrestling.[33]",
            },
            model_config={
                "model": "gpt-3.5-turbo",
                "max_tokens": -1,
                "temperature": 0.7,
                "prompt_template": "Summarize this for a second-grade student:\n\nText:\n{{text}}\n\nSummary:\n",
            },
            stream=False,
        )
        print(complete_response)
    except ApiException as e:
        print("Exception when calling .complete: %s\n" % e)
        pprint(e.body)
        if e.status == 422:
            pprint(e.body["detail"])
        pprint(e.headers)
        pprint(e.status)
        pprint(e.reason)
        pprint(e.round_trip_time)


asyncio.run(main())
```

## Raw HTTP Response<a id="raw-http-response"></a>

To access raw HTTP response values, use the `.raw` namespace.

```python
from pprint import pprint
from humanloop import Humanloop, ApiException

humanloop = Humanloop(
    openai_api_key="OPENAI_API_KEY",
    openai_azure_api_key="OPENAI_AZURE_API_KEY",
    openai_azure_endpoint_api_key="OPENAI_AZURE_ENDPOINT_API_KEY",
    anthropic_api_key="ANTHROPIC_API_KEY",
    cohere_api_key="COHERE_API_KEY",
    api_key="YOUR_API_KEY",
)

try:
    # Chat
    create_response = humanloop.chats.raw.create(
        messages=[
            {
                "role": "user",
            }
        ],
        model_config={
            "provider": "openai",
            "model": "model_example",
            "max_tokens": -1,
            "temperature": 1,
            "top_p": 1,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "endpoint": "complete",
        },
        project="string_example",
        project_id="string_example",
        session_id="string_example",
        session_reference_id="string_example",
        parent_id="string_example",
        parent_reference_id="string_example",
        inputs={},
        source="string_example",
        metadata={},
        save=True,
        source_datapoint_id="string_example",
        provider_api_keys={},
        num_samples=1,
        stream=False,
        user="string_example",
        seed=1,
        return_inputs=True,
        tool_choice="string_example",
        tool_call="string_example",
        response_format={
            "type": "string_example",
        },
    )
    pprint(create_response.body)
    pprint(create_response.body["data"])
    pprint(create_response.body["provider_responses"])
    pprint(create_response.body["project_id"])
    pprint(create_response.body["num_samples"])
    pprint(create_response.body["logprobs"])
    pprint(create_response.body["suffix"])
    pprint(create_response.body["user"])
    pprint(create_response.body["usage"])
    pprint(create_response.body["metadata"])
    pprint(create_response.body["provider_request"])
    pprint(create_response.body["session_id"])
    pprint(create_response.body["tool_choice"])
    pprint(create_response.headers)
    pprint(create_response.status)
    pprint(create_response.round_trip_time)
except ApiException as e:
    print("Exception when calling ChatsApi.create: %s\n" % e)
    pprint(e.body)
    if e.status == 422:
        pprint(e.body["detail"])
    pprint(e.headers)
    pprint(e.status)
    pprint(e.reason)
    pprint(e.round_trip_time)
```


## Streaming<a id="streaming"></a>

Streaming support is available by suffixing a `chat` or `complete` method with `_stream`.

```python
import asyncio
from humanloop import Humanloop

humanloop = Humanloop(
    api_key="YOUR_API_KEY",
    openai_api_key="YOUR_OPENAI_API_KEY",
    anthropic_api_key="YOUR_ANTHROPIC_API_KEY",
)


async def main():
    response = await humanloop.chat_stream(
        project="sdk-example",
        messages=[
            {
                "role": "user",
                "content": "Explain asynchronous programming.",
            }
        ],
        model_config={
            "model": "gpt-3.5-turbo",
            "max_tokens": -1,
            "temperature": 0.7,
            "chat_template": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant who replies in the style of {{persona}}.",
                },
            ],
        },
        inputs={
            "persona": "the pirate Blackbeard",
        },
    )
    async for token in response.content:
        print(token)


asyncio.run(main())
```


## Reference<a id="reference"></a>
### `humanloop.chat`<a id="humanloopchat"></a>

Get a chat response by providing details of the model configuration in the request.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = humanloop.chat(
    messages=[
        {
            "role": "user",
        }
    ],
    model_config={
        "provider": "openai",
        "model": "model_example",
        "max_tokens": -1,
        "temperature": 1,
        "top_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "endpoint": "complete",
    },
    project="string_example",
    project_id="string_example",
    session_id="string_example",
    session_reference_id="string_example",
    parent_id="string_example",
    parent_reference_id="string_example",
    inputs={},
    source="string_example",
    metadata={},
    save=True,
    source_datapoint_id="string_example",
    provider_api_keys={},
    num_samples=1,
    stream=False,
    user="string_example",
    seed=1,
    return_inputs=True,
    tool_choice="string_example",
    tool_call="string_example",
    response_format={
        "type": "string_example",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### messages: List[`ChatMessageWithToolCall`]<a id="messages-listchatmessagewithtoolcall"></a>

The messages passed to the to provider chat endpoint.

##### model_config: [`ModelConfigChatRequest`](./humanloop/type/model_config_chat_request.py)<a id="model_config-modelconfigchatrequesthumanlooptypemodel_config_chat_requestpy"></a>


The model configuration used to create a chat response.

##### project: `str`<a id="project-str"></a>

Unique project name. If no project exists with this name, a new project will be created.

##### project_id: `str`<a id="project_id-str"></a>

Unique ID of a project to associate to the log. Either this or `project` must be provided.

##### session_id: `str`<a id="session_id-str"></a>

ID of the session to associate the datapoint.

##### session_reference_id: `str`<a id="session_reference_id-str"></a>

A unique string identifying the session to associate the datapoint to. Allows you to log multiple datapoints to a session (using an ID kept by your internal systems) by passing the same `session_reference_id` in subsequent log requests. Specify at most one of this or `session_id`.

##### parent_id: `str`<a id="parent_id-str"></a>

ID associated to the parent datapoint in a session.

##### parent_reference_id: `str`<a id="parent_reference_id-str"></a>

A unique string identifying the previously-logged parent datapoint in a session. Allows you to log nested datapoints with your internal system IDs by passing the same reference ID as `parent_id` in a prior log request. Specify at most one of this or `parent_id`. Note that this cannot refer to a datapoint being logged in the same request.

##### inputs: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="inputs-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

The inputs passed to the prompt template.

##### source: `str`<a id="source-str"></a>

Identifies where the model was called from.

##### metadata: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="metadata-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

Any additional metadata to record.

##### save: `bool`<a id="save-bool"></a>

Whether the request/response payloads will be stored on Humanloop.

##### source_datapoint_id: `str`<a id="source_datapoint_id-str"></a>

ID of the source datapoint if this is a log derived from a datapoint in a dataset.

##### provider_api_keys: [`ProviderApiKeys`](./humanloop/type/provider_api_keys.py)<a id="provider_api_keys-providerapikeyshumanlooptypeprovider_api_keyspy"></a>


API keys required by each provider to make API calls. The API keys provided here are not stored by Humanloop. If not specified here, Humanloop will fall back to the key saved to your organization.

##### num_samples: `int`<a id="num_samples-int"></a>

The number of generations.

##### stream: `bool`<a id="stream-bool"></a>

If true, tokens will be sent as data-only server-sent events. If num_samples > 1, samples are streamed back independently.

##### user: `str`<a id="user-str"></a>

End-user ID passed through to provider call.

##### seed: `int`<a id="seed-int"></a>

Deprecated field: the seed is instead set as part of the request.config object.

##### return_inputs: `bool`<a id="return_inputs-bool"></a>

Whether to return the inputs in the response. If false, the response will contain an empty dictionary under inputs. This is useful for reducing the size of the response. Defaults to true.

##### tool_choice: Union[`str`, `str`, `str`, `ToolChoice`]<a id="tool_choice-unionstr-str-str-toolchoice"></a>


Controls how the model uses tools. The following options are supported: 'none' forces the model to not call a tool; the default when no tools are provided as part of the model config. 'auto' the model can decide to call one of the provided tools; the default when tools are provided as part of the model config. Providing {'type': 'function', 'function': {name': <TOOL_NAME>}} forces the model to use the named function.

##### tool_call: Union[`str`, [`Dict[str, str]`](./humanloop/type/typing_dict_str_str.py)]<a id="tool_call-unionstr-dictstr-strhumanlooptypetyping_dict_str_strpy"></a>


NB: Deprecated with new tool_choice. Controls how the model uses tools. The following options are supported: 'none' forces the model to not call a tool; the default when no tools are provided as part of the model config. 'auto' the model can decide to call one of the provided tools; the default when tools are provided as part of the model config. Providing {'name': <TOOL_NAME>} forces the model to use the provided tool of the same name.

##### response_format: [`ResponseFormat`](./humanloop/type/response_format.py)<a id="response_format-responseformathumanlooptyperesponse_formatpy"></a>


The format of the response. Only type json_object is currently supported for chat.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ChatRequest`](./humanloop/type/chat_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ChatResponse`](./humanloop/pydantic/chat_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/chat` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.chat_deployed`<a id="humanloopchat_deployed"></a>

Get a chat response using the project's active deployment.

The active deployment can be a specific model configuration.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_deployed_response = humanloop.chat_deployed(
    messages=[
        {
            "role": "user",
        }
    ],
    project="string_example",
    project_id="string_example",
    session_id="string_example",
    session_reference_id="string_example",
    parent_id="string_example",
    parent_reference_id="string_example",
    inputs={},
    source="string_example",
    metadata={},
    save=True,
    source_datapoint_id="string_example",
    provider_api_keys={},
    num_samples=1,
    stream=False,
    user="string_example",
    seed=1,
    return_inputs=True,
    tool_choice="string_example",
    tool_call="string_example",
    response_format={
        "type": "string_example",
    },
    environment="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### messages: List[`ChatMessageWithToolCall`]<a id="messages-listchatmessagewithtoolcall"></a>

The messages passed to the to provider chat endpoint.

##### project: `str`<a id="project-str"></a>

Unique project name. If no project exists with this name, a new project will be created.

##### project_id: `str`<a id="project_id-str"></a>

Unique ID of a project to associate to the log. Either this or `project` must be provided.

##### session_id: `str`<a id="session_id-str"></a>

ID of the session to associate the datapoint.

##### session_reference_id: `str`<a id="session_reference_id-str"></a>

A unique string identifying the session to associate the datapoint to. Allows you to log multiple datapoints to a session (using an ID kept by your internal systems) by passing the same `session_reference_id` in subsequent log requests. Specify at most one of this or `session_id`.

##### parent_id: `str`<a id="parent_id-str"></a>

ID associated to the parent datapoint in a session.

##### parent_reference_id: `str`<a id="parent_reference_id-str"></a>

A unique string identifying the previously-logged parent datapoint in a session. Allows you to log nested datapoints with your internal system IDs by passing the same reference ID as `parent_id` in a prior log request. Specify at most one of this or `parent_id`. Note that this cannot refer to a datapoint being logged in the same request.

##### inputs: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="inputs-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

The inputs passed to the prompt template.

##### source: `str`<a id="source-str"></a>

Identifies where the model was called from.

##### metadata: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="metadata-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

Any additional metadata to record.

##### save: `bool`<a id="save-bool"></a>

Whether the request/response payloads will be stored on Humanloop.

##### source_datapoint_id: `str`<a id="source_datapoint_id-str"></a>

ID of the source datapoint if this is a log derived from a datapoint in a dataset.

##### provider_api_keys: [`ProviderApiKeys`](./humanloop/type/provider_api_keys.py)<a id="provider_api_keys-providerapikeyshumanlooptypeprovider_api_keyspy"></a>


API keys required by each provider to make API calls. The API keys provided here are not stored by Humanloop. If not specified here, Humanloop will fall back to the key saved to your organization.

##### num_samples: `int`<a id="num_samples-int"></a>

The number of generations.

##### stream: `bool`<a id="stream-bool"></a>

If true, tokens will be sent as data-only server-sent events. If num_samples > 1, samples are streamed back independently.

##### user: `str`<a id="user-str"></a>

End-user ID passed through to provider call.

##### seed: `int`<a id="seed-int"></a>

Deprecated field: the seed is instead set as part of the request.config object.

##### return_inputs: `bool`<a id="return_inputs-bool"></a>

Whether to return the inputs in the response. If false, the response will contain an empty dictionary under inputs. This is useful for reducing the size of the response. Defaults to true.

##### tool_choice: Union[`str`, `str`, `str`, `ToolChoice`]<a id="tool_choice-unionstr-str-str-toolchoice"></a>


Controls how the model uses tools. The following options are supported: 'none' forces the model to not call a tool; the default when no tools are provided as part of the model config. 'auto' the model can decide to call one of the provided tools; the default when tools are provided as part of the model config. Providing {'type': 'function', 'function': {name': <TOOL_NAME>}} forces the model to use the named function.

##### tool_call: Union[`str`, [`Dict[str, str]`](./humanloop/type/typing_dict_str_str.py)]<a id="tool_call-unionstr-dictstr-strhumanlooptypetyping_dict_str_strpy"></a>


NB: Deprecated with new tool_choice. Controls how the model uses tools. The following options are supported: 'none' forces the model to not call a tool; the default when no tools are provided as part of the model config. 'auto' the model can decide to call one of the provided tools; the default when tools are provided as part of the model config. Providing {'name': <TOOL_NAME>} forces the model to use the provided tool of the same name.

##### response_format: [`ResponseFormat`](./humanloop/type/response_format.py)<a id="response_format-responseformathumanlooptyperesponse_formatpy"></a>


The format of the response. Only type json_object is currently supported for chat.

##### environment: `str`<a id="environment-str"></a>

The environment name used to create a chat response. If not specified, the default environment will be used.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ChatDeployedRequest`](./humanloop/type/chat_deployed_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ChatResponse`](./humanloop/pydantic/chat_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/chat-deployed` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.chat_model_config`<a id="humanloopchat_model_config"></a>

Get chat response for a specific model configuration.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_model_config_response = humanloop.chat_model_config(
    messages=[
        {
            "role": "user",
        }
    ],
    model_config_id="string_example",
    project="string_example",
    project_id="string_example",
    session_id="string_example",
    session_reference_id="string_example",
    parent_id="string_example",
    parent_reference_id="string_example",
    inputs={},
    source="string_example",
    metadata={},
    save=True,
    source_datapoint_id="string_example",
    provider_api_keys={},
    num_samples=1,
    stream=False,
    user="string_example",
    seed=1,
    return_inputs=True,
    tool_choice="string_example",
    tool_call="string_example",
    response_format={
        "type": "string_example",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### messages: List[`ChatMessageWithToolCall`]<a id="messages-listchatmessagewithtoolcall"></a>

The messages passed to the to provider chat endpoint.

##### model_config_id: `str`<a id="model_config_id-str"></a>

Identifies the model configuration used to create a chat response.

##### project: `str`<a id="project-str"></a>

Unique project name. If no project exists with this name, a new project will be created.

##### project_id: `str`<a id="project_id-str"></a>

Unique ID of a project to associate to the log. Either this or `project` must be provided.

##### session_id: `str`<a id="session_id-str"></a>

ID of the session to associate the datapoint.

##### session_reference_id: `str`<a id="session_reference_id-str"></a>

A unique string identifying the session to associate the datapoint to. Allows you to log multiple datapoints to a session (using an ID kept by your internal systems) by passing the same `session_reference_id` in subsequent log requests. Specify at most one of this or `session_id`.

##### parent_id: `str`<a id="parent_id-str"></a>

ID associated to the parent datapoint in a session.

##### parent_reference_id: `str`<a id="parent_reference_id-str"></a>

A unique string identifying the previously-logged parent datapoint in a session. Allows you to log nested datapoints with your internal system IDs by passing the same reference ID as `parent_id` in a prior log request. Specify at most one of this or `parent_id`. Note that this cannot refer to a datapoint being logged in the same request.

##### inputs: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="inputs-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

The inputs passed to the prompt template.

##### source: `str`<a id="source-str"></a>

Identifies where the model was called from.

##### metadata: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="metadata-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

Any additional metadata to record.

##### save: `bool`<a id="save-bool"></a>

Whether the request/response payloads will be stored on Humanloop.

##### source_datapoint_id: `str`<a id="source_datapoint_id-str"></a>

ID of the source datapoint if this is a log derived from a datapoint in a dataset.

##### provider_api_keys: [`ProviderApiKeys`](./humanloop/type/provider_api_keys.py)<a id="provider_api_keys-providerapikeyshumanlooptypeprovider_api_keyspy"></a>


API keys required by each provider to make API calls. The API keys provided here are not stored by Humanloop. If not specified here, Humanloop will fall back to the key saved to your organization.

##### num_samples: `int`<a id="num_samples-int"></a>

The number of generations.

##### stream: `bool`<a id="stream-bool"></a>

If true, tokens will be sent as data-only server-sent events. If num_samples > 1, samples are streamed back independently.

##### user: `str`<a id="user-str"></a>

End-user ID passed through to provider call.

##### seed: `int`<a id="seed-int"></a>

Deprecated field: the seed is instead set as part of the request.config object.

##### return_inputs: `bool`<a id="return_inputs-bool"></a>

Whether to return the inputs in the response. If false, the response will contain an empty dictionary under inputs. This is useful for reducing the size of the response. Defaults to true.

##### tool_choice: Union[`str`, `str`, `str`, `ToolChoice`]<a id="tool_choice-unionstr-str-str-toolchoice"></a>


Controls how the model uses tools. The following options are supported: 'none' forces the model to not call a tool; the default when no tools are provided as part of the model config. 'auto' the model can decide to call one of the provided tools; the default when tools are provided as part of the model config. Providing {'type': 'function', 'function': {name': <TOOL_NAME>}} forces the model to use the named function.

##### tool_call: Union[`str`, [`Dict[str, str]`](./humanloop/type/typing_dict_str_str.py)]<a id="tool_call-unionstr-dictstr-strhumanlooptypetyping_dict_str_strpy"></a>


NB: Deprecated with new tool_choice. Controls how the model uses tools. The following options are supported: 'none' forces the model to not call a tool; the default when no tools are provided as part of the model config. 'auto' the model can decide to call one of the provided tools; the default when tools are provided as part of the model config. Providing {'name': <TOOL_NAME>} forces the model to use the provided tool of the same name.

##### response_format: [`ResponseFormat`](./humanloop/type/response_format.py)<a id="response_format-responseformathumanlooptyperesponse_formatpy"></a>


The format of the response. Only type json_object is currently supported for chat.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ChatModelConfigRequest`](./humanloop/type/chat_model_config_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ChatResponse`](./humanloop/pydantic/chat_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/chat-model-config` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.complete`<a id="humanloopcomplete"></a>

Create a completion by providing details of the model configuration in the request.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = humanloop.complete(
    model_config={
        "provider": "openai",
        "model": "model_example",
        "max_tokens": -1,
        "temperature": 1,
        "top_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "endpoint": "complete",
        "prompt_template": "{{question}}",
    },
    project="string_example",
    project_id="string_example",
    session_id="string_example",
    session_reference_id="string_example",
    parent_id="string_example",
    parent_reference_id="string_example",
    inputs={},
    source="string_example",
    metadata={},
    save=True,
    source_datapoint_id="string_example",
    provider_api_keys={},
    num_samples=1,
    stream=False,
    user="string_example",
    seed=1,
    return_inputs=True,
    logprobs=1,
    suffix="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### model_config: [`ModelConfigCompletionRequest`](./humanloop/type/model_config_completion_request.py)<a id="model_config-modelconfigcompletionrequesthumanlooptypemodel_config_completion_requestpy"></a>


The model configuration used to generate.

##### project: `str`<a id="project-str"></a>

Unique project name. If no project exists with this name, a new project will be created.

##### project_id: `str`<a id="project_id-str"></a>

Unique ID of a project to associate to the log. Either this or `project` must be provided.

##### session_id: `str`<a id="session_id-str"></a>

ID of the session to associate the datapoint.

##### session_reference_id: `str`<a id="session_reference_id-str"></a>

A unique string identifying the session to associate the datapoint to. Allows you to log multiple datapoints to a session (using an ID kept by your internal systems) by passing the same `session_reference_id` in subsequent log requests. Specify at most one of this or `session_id`.

##### parent_id: `str`<a id="parent_id-str"></a>

ID associated to the parent datapoint in a session.

##### parent_reference_id: `str`<a id="parent_reference_id-str"></a>

A unique string identifying the previously-logged parent datapoint in a session. Allows you to log nested datapoints with your internal system IDs by passing the same reference ID as `parent_id` in a prior log request. Specify at most one of this or `parent_id`. Note that this cannot refer to a datapoint being logged in the same request.

##### inputs: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="inputs-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

The inputs passed to the prompt template.

##### source: `str`<a id="source-str"></a>

Identifies where the model was called from.

##### metadata: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="metadata-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

Any additional metadata to record.

##### save: `bool`<a id="save-bool"></a>

Whether the request/response payloads will be stored on Humanloop.

##### source_datapoint_id: `str`<a id="source_datapoint_id-str"></a>

ID of the source datapoint if this is a log derived from a datapoint in a dataset.

##### provider_api_keys: [`ProviderApiKeys`](./humanloop/type/provider_api_keys.py)<a id="provider_api_keys-providerapikeyshumanlooptypeprovider_api_keyspy"></a>


API keys required by each provider to make API calls. The API keys provided here are not stored by Humanloop. If not specified here, Humanloop will fall back to the key saved to your organization.

##### num_samples: `int`<a id="num_samples-int"></a>

The number of generations.

##### stream: `bool`<a id="stream-bool"></a>

If true, tokens will be sent as data-only server-sent events. If num_samples > 1, samples are streamed back independently.

##### user: `str`<a id="user-str"></a>

End-user ID passed through to provider call.

##### seed: `int`<a id="seed-int"></a>

Deprecated field: the seed is instead set as part of the request.config object.

##### return_inputs: `bool`<a id="return_inputs-bool"></a>

Whether to return the inputs in the response. If false, the response will contain an empty dictionary under inputs. This is useful for reducing the size of the response. Defaults to true.

##### logprobs: `int`<a id="logprobs-int"></a>

Include the log probabilities of the top n tokens in the provider_response

##### suffix: `str`<a id="suffix-str"></a>

The suffix that comes after a completion of inserted text. Useful for completions that act like inserts.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CompletionRequest`](./humanloop/type/completion_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`CompletionResponse`](./humanloop/pydantic/completion_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/completion` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.complete_deployed`<a id="humanloopcomplete_deployed"></a>

Create a completion using the project's active deployment.

The active deployment can be a specific model configuration.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_deployed_response = humanloop.complete_deployed(
    project="string_example",
    project_id="string_example",
    session_id="string_example",
    session_reference_id="string_example",
    parent_id="string_example",
    parent_reference_id="string_example",
    inputs={},
    source="string_example",
    metadata={},
    save=True,
    source_datapoint_id="string_example",
    provider_api_keys={},
    num_samples=1,
    stream=False,
    user="string_example",
    seed=1,
    return_inputs=True,
    logprobs=1,
    suffix="string_example",
    environment="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project: `str`<a id="project-str"></a>

Unique project name. If no project exists with this name, a new project will be created.

##### project_id: `str`<a id="project_id-str"></a>

Unique ID of a project to associate to the log. Either this or `project` must be provided.

##### session_id: `str`<a id="session_id-str"></a>

ID of the session to associate the datapoint.

##### session_reference_id: `str`<a id="session_reference_id-str"></a>

A unique string identifying the session to associate the datapoint to. Allows you to log multiple datapoints to a session (using an ID kept by your internal systems) by passing the same `session_reference_id` in subsequent log requests. Specify at most one of this or `session_id`.

##### parent_id: `str`<a id="parent_id-str"></a>

ID associated to the parent datapoint in a session.

##### parent_reference_id: `str`<a id="parent_reference_id-str"></a>

A unique string identifying the previously-logged parent datapoint in a session. Allows you to log nested datapoints with your internal system IDs by passing the same reference ID as `parent_id` in a prior log request. Specify at most one of this or `parent_id`. Note that this cannot refer to a datapoint being logged in the same request.

##### inputs: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="inputs-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

The inputs passed to the prompt template.

##### source: `str`<a id="source-str"></a>

Identifies where the model was called from.

##### metadata: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="metadata-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

Any additional metadata to record.

##### save: `bool`<a id="save-bool"></a>

Whether the request/response payloads will be stored on Humanloop.

##### source_datapoint_id: `str`<a id="source_datapoint_id-str"></a>

ID of the source datapoint if this is a log derived from a datapoint in a dataset.

##### provider_api_keys: [`ProviderApiKeys`](./humanloop/type/provider_api_keys.py)<a id="provider_api_keys-providerapikeyshumanlooptypeprovider_api_keyspy"></a>


API keys required by each provider to make API calls. The API keys provided here are not stored by Humanloop. If not specified here, Humanloop will fall back to the key saved to your organization.

##### num_samples: `int`<a id="num_samples-int"></a>

The number of generations.

##### stream: `bool`<a id="stream-bool"></a>

If true, tokens will be sent as data-only server-sent events. If num_samples > 1, samples are streamed back independently.

##### user: `str`<a id="user-str"></a>

End-user ID passed through to provider call.

##### seed: `int`<a id="seed-int"></a>

Deprecated field: the seed is instead set as part of the request.config object.

##### return_inputs: `bool`<a id="return_inputs-bool"></a>

Whether to return the inputs in the response. If false, the response will contain an empty dictionary under inputs. This is useful for reducing the size of the response. Defaults to true.

##### logprobs: `int`<a id="logprobs-int"></a>

Include the log probabilities of the top n tokens in the provider_response

##### suffix: `str`<a id="suffix-str"></a>

The suffix that comes after a completion of inserted text. Useful for completions that act like inserts.

##### environment: `str`<a id="environment-str"></a>

The environment name used to create a chat response. If not specified, the default environment will be used.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CompletionDeployedRequest`](./humanloop/type/completion_deployed_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`CompletionResponse`](./humanloop/pydantic/completion_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/completion-deployed` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.complete_model_configuration`<a id="humanloopcomplete_model_configuration"></a>

Create a completion for a specific model configuration.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_model_config_response = humanloop.complete_model_configuration(
    model_config_id="string_example",
    project="string_example",
    project_id="string_example",
    session_id="string_example",
    session_reference_id="string_example",
    parent_id="string_example",
    parent_reference_id="string_example",
    inputs={},
    source="string_example",
    metadata={},
    save=True,
    source_datapoint_id="string_example",
    provider_api_keys={},
    num_samples=1,
    stream=False,
    user="string_example",
    seed=1,
    return_inputs=True,
    logprobs=1,
    suffix="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### model_config_id: `str`<a id="model_config_id-str"></a>

Identifies the model configuration used to create a chat response.

##### project: `str`<a id="project-str"></a>

Unique project name. If no project exists with this name, a new project will be created.

##### project_id: `str`<a id="project_id-str"></a>

Unique ID of a project to associate to the log. Either this or `project` must be provided.

##### session_id: `str`<a id="session_id-str"></a>

ID of the session to associate the datapoint.

##### session_reference_id: `str`<a id="session_reference_id-str"></a>

A unique string identifying the session to associate the datapoint to. Allows you to log multiple datapoints to a session (using an ID kept by your internal systems) by passing the same `session_reference_id` in subsequent log requests. Specify at most one of this or `session_id`.

##### parent_id: `str`<a id="parent_id-str"></a>

ID associated to the parent datapoint in a session.

##### parent_reference_id: `str`<a id="parent_reference_id-str"></a>

A unique string identifying the previously-logged parent datapoint in a session. Allows you to log nested datapoints with your internal system IDs by passing the same reference ID as `parent_id` in a prior log request. Specify at most one of this or `parent_id`. Note that this cannot refer to a datapoint being logged in the same request.

##### inputs: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="inputs-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

The inputs passed to the prompt template.

##### source: `str`<a id="source-str"></a>

Identifies where the model was called from.

##### metadata: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="metadata-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

Any additional metadata to record.

##### save: `bool`<a id="save-bool"></a>

Whether the request/response payloads will be stored on Humanloop.

##### source_datapoint_id: `str`<a id="source_datapoint_id-str"></a>

ID of the source datapoint if this is a log derived from a datapoint in a dataset.

##### provider_api_keys: [`ProviderApiKeys`](./humanloop/type/provider_api_keys.py)<a id="provider_api_keys-providerapikeyshumanlooptypeprovider_api_keyspy"></a>


API keys required by each provider to make API calls. The API keys provided here are not stored by Humanloop. If not specified here, Humanloop will fall back to the key saved to your organization.

##### num_samples: `int`<a id="num_samples-int"></a>

The number of generations.

##### stream: `bool`<a id="stream-bool"></a>

If true, tokens will be sent as data-only server-sent events. If num_samples > 1, samples are streamed back independently.

##### user: `str`<a id="user-str"></a>

End-user ID passed through to provider call.

##### seed: `int`<a id="seed-int"></a>

Deprecated field: the seed is instead set as part of the request.config object.

##### return_inputs: `bool`<a id="return_inputs-bool"></a>

Whether to return the inputs in the response. If false, the response will contain an empty dictionary under inputs. This is useful for reducing the size of the response. Defaults to true.

##### logprobs: `int`<a id="logprobs-int"></a>

Include the log probabilities of the top n tokens in the provider_response

##### suffix: `str`<a id="suffix-str"></a>

The suffix that comes after a completion of inserted text. Useful for completions that act like inserts.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CompletionModelConfigRequest`](./humanloop/type/completion_model_config_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`CompletionResponse`](./humanloop/pydantic/completion_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/completion-model-config` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.datapoints.delete`<a id="humanloopdatapointsdelete"></a>
![Deprecated](https://img.shields.io/badge/deprecated-yellow)

Delete a list of datapoints by their IDs.

WARNING: This endpoint has been decommissioned and no longer works. Please use the v5 datasets API instead.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
humanloop.datapoints.delete()
```

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/datapoints` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.datapoints.get`<a id="humanloopdatapointsget"></a>

Get a datapoint by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = humanloop.datapoints.get(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of datapoint.

#### 🔄 Return<a id="🔄-return"></a>

[`DatapointResponse`](./humanloop/pydantic/datapoint_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/datapoints/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.datapoints.update`<a id="humanloopdatapointsupdate"></a>
![Deprecated](https://img.shields.io/badge/deprecated-yellow)

Edit the input, messages and criteria fields of a datapoint.

WARNING: This endpoint has been decommissioned and no longer works. Please use the v5 datasets API instead.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_response = humanloop.datapoints.update(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of datapoint.

#### 🔄 Return<a id="🔄-return"></a>

[`DatapointResponse`](./humanloop/pydantic/datapoint_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/datapoints/{id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.datasets.create`<a id="humanloopdatasetscreate"></a>

Create a new dataset for a project.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = humanloop.datasets.create(
    description="string_example",
    name="string_example",
    project_id="project_id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### description: `str`<a id="description-str"></a>

The description of the dataset.

##### name: `str`<a id="name-str"></a>

The name of the dataset.

##### project_id: `str`<a id="project_id-str"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CreateDatasetRequest`](./humanloop/type/create_dataset_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`DatasetResponse`](./humanloop/pydantic/dataset_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/projects/{project_id}/datasets` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.datasets.create_datapoint`<a id="humanloopdatasetscreate_datapoint"></a>

Create a new datapoint for a dataset.

Here in the v4 API, this has the following behaviour:
* Retrieve the current latest version of the dataset.
* Construct a new version of the dataset with the new testcases added.
* Store that latest version as a committed version with an autogenerated commit
  message and return the new datapoints

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_datapoint_response = humanloop.datasets.create_datapoint(
    body={
        "log_ids": ["log_ids_example"],
    },
    dataset_id="dataset_id_example",
    log_ids=["string_example"],
    inputs={
        "key": "string_example",
    },
    messages=[
        {
            "role": "user",
        }
    ],
    target={
        "key": "string_example",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### dataset_id: `str`<a id="dataset_id-str"></a>

String ID of dataset. Starts with `evts_`.

##### requestBody: [`DatasetsCreateDatapointRequest`](./humanloop/type/datasets_create_datapoint_request.py)<a id="requestbody-datasetscreatedatapointrequesthumanlooptypedatasets_create_datapoint_requestpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`DatasetsCreateDatapointResponse`](./humanloop/pydantic/datasets_create_datapoint_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/datasets/{dataset_id}/datapoints` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.datasets.delete`<a id="humanloopdatasetsdelete"></a>

Delete a dataset by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
delete_response = humanloop.datasets.delete(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of dataset. Starts with `evts_`.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/datasets/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.datasets.get`<a id="humanloopdatasetsget"></a>

Get a single dataset by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = humanloop.datasets.get(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of dataset. Starts with `evts_`.

#### 🔄 Return<a id="🔄-return"></a>

[`DatasetResponse`](./humanloop/pydantic/dataset_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/datasets/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.datasets.list`<a id="humanloopdatasetslist"></a>

Get all Datasets for an organization.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = humanloop.datasets.list()
```

#### 🔄 Return<a id="🔄-return"></a>

[`DatasetsListResponse`](./humanloop/pydantic/datasets_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/datasets` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.datasets.list_all_for_project`<a id="humanloopdatasetslist_all_for_project"></a>
![Deprecated](https://img.shields.io/badge/deprecated-yellow)

Get all datasets for a project.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_all_for_project_response = humanloop.datasets.list_all_for_project(
    project_id="project_id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_id: `str`<a id="project_id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`DatasetsListAllForProjectResponse`](./humanloop/pydantic/datasets_list_all_for_project_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/projects/{project_id}/datasets` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.datasets.list_datapoints`<a id="humanloopdatasetslist_datapoints"></a>

Get datapoints for a dataset.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_datapoints_response = humanloop.datasets.list_datapoints(
    dataset_id="dataset_id_example",
    page=0,
    size=50,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### dataset_id: `str`<a id="dataset_id-str"></a>

String ID of dataset. Starts with `evts_`.

##### page: `int`<a id="page-int"></a>

##### size: `int`<a id="size-int"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`PaginatedDataDatapointResponse`](./humanloop/pydantic/paginated_data_datapoint_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/datasets/{dataset_id}/datapoints` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.datasets.update`<a id="humanloopdatasetsupdate"></a>

Update a testset by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_response = humanloop.datasets.update(
    id="id_example",
    description="string_example",
    name="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of testset. Starts with `evts_`.

##### description: `str`<a id="description-str"></a>

The description of the dataset.

##### name: `str`<a id="name-str"></a>

The name of the dataset.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`UpdateDatasetRequest`](./humanloop/type/update_dataset_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`DatasetResponse`](./humanloop/pydantic/dataset_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/datasets/{id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.evaluations.add_evaluators`<a id="humanloopevaluationsadd_evaluators"></a>

Add evaluators to an existing evaluation run.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
add_evaluators_response = humanloop.evaluations.add_evaluators(
    id="id_example",
    evaluator_ids=["string_example"],
    evaluator_version_ids=["string_example"],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of evaluation run. Starts with `ev_`.

##### evaluator_ids: [`AddEvaluatorsRequestEvaluatorIds`](./humanloop/type/add_evaluators_request_evaluator_ids.py)<a id="evaluator_ids-addevaluatorsrequestevaluatoridshumanlooptypeadd_evaluators_request_evaluator_idspy"></a>

##### evaluator_version_ids: [`AddEvaluatorsRequestEvaluatorVersionIds`](./humanloop/type/add_evaluators_request_evaluator_version_ids.py)<a id="evaluator_version_ids-addevaluatorsrequestevaluatorversionidshumanlooptypeadd_evaluators_request_evaluator_version_idspy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`AddEvaluatorsRequest`](./humanloop/type/add_evaluators_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`EvaluationResponse`](./humanloop/pydantic/evaluation_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/evaluations/{id}/evaluators` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.evaluations.create`<a id="humanloopevaluationscreate"></a>

Create an evaluation.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = humanloop.evaluations.create(
    config_id="string_example",
    evaluator_ids=["string_example"],
    dataset_id="string_example",
    project_id="project_id_example",
    provider_api_keys={},
    hl_generated=True,
    name="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### config_id: `str`<a id="config_id-str"></a>

ID of the config to evaluate. Starts with `config_`.

##### evaluator_ids: [`CreateEvaluationRequestEvaluatorIds`](./humanloop/type/create_evaluation_request_evaluator_ids.py)<a id="evaluator_ids-createevaluationrequestevaluatoridshumanlooptypecreate_evaluation_request_evaluator_idspy"></a>

##### dataset_id: `str`<a id="dataset_id-str"></a>

ID of the dataset to use in this evaluation. Starts with `evts_`.

##### project_id: `str`<a id="project_id-str"></a>

String ID of project. Starts with `pr_`.

##### provider_api_keys: [`ProviderApiKeys`](./humanloop/type/provider_api_keys.py)<a id="provider_api_keys-providerapikeyshumanlooptypeprovider_api_keyspy"></a>


API keys required by each provider to make API calls. The API keys provided here are not stored by Humanloop. If not specified here, Humanloop will fall back to the key saved to your organization. Ensure you provide an API key for the provider for the model config you are evaluating, or have one saved to your organization.

##### hl_generated: `bool`<a id="hl_generated-bool"></a>

Whether the log generations for this evaluation should be performed by Humanloop. If `False`, the log generations should be submitted by the user via the API.

##### name: `str`<a id="name-str"></a>

Name of the Evaluation to help identify it.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CreateEvaluationRequest`](./humanloop/type/create_evaluation_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`EvaluationResponse`](./humanloop/pydantic/evaluation_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/projects/{project_id}/evaluations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.evaluations.get`<a id="humanloopevaluationsget"></a>

Get evaluation by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = humanloop.evaluations.get(
    id="id_example",
    evaluator_aggregates=True,
    evaluatee_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of evaluation run. Starts with `ev_`.

##### evaluator_aggregates: `bool`<a id="evaluator_aggregates-bool"></a>

Whether to include evaluator aggregates in the response.

##### evaluatee_id: `str`<a id="evaluatee_id-str"></a>

String ID of evaluatee version to return. If not defined, the first evaluatee will be returned. Starts with `evv_`.

#### 🔄 Return<a id="🔄-return"></a>

[`EvaluationResponse`](./humanloop/pydantic/evaluation_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/evaluations/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.evaluations.list`<a id="humanloopevaluationslist"></a>

Get the evaluations associated with a project.

Sorting and filtering are supported through query params for categorical columns
and the `created_at` timestamp.

Sorting is supported for the `dataset`, `config`, `status` and `evaluator-{evaluator_id}` columns.
Specify sorting with the `sort` query param, with values `{column}.{ordering}`.
E.g. ?sort=dataset.asc&sort=status.desc will yield a multi-column sort. First by dataset then by status.

Filtering is supported for the `id`, `dataset`, `config` and `status` columns.

Specify filtering with the `id_filter`, `dataset_filter`, `config_filter` and `status_filter` query params.

E.g. ?dataset_filter=my_dataset&dataset_filter=my_other_dataset&status_filter=running
will only show rows where the dataset is "my_dataset" or "my_other_dataset", and where the status is "running".

An additional date range filter is supported for the `created_at` column. Use the `start_date` and `end_date`
query parameters to configure this.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = humanloop.evaluations.list(
    project_id="project_id_example",
    id=["string_example"],
    start_date="1970-01-01",
    end_date="1970-01-01",
    size=50,
    page=0,
    evaluatee_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_id: `str`<a id="project_id-str"></a>

String ID of project. Starts with `pr_`.

##### id: List[`str`]<a id="id-liststr"></a>

A list of evaluation run ids to filter on. Starts with `ev_`.

##### start_date: `date`<a id="start_date-date"></a>

Only return evaluations created after this date.

##### end_date: `date`<a id="end_date-date"></a>

Only return evaluations created before this date.

##### size: `int`<a id="size-int"></a>

##### page: `int`<a id="page-int"></a>

##### evaluatee_id: `str`<a id="evaluatee_id-str"></a>

String ID of evaluatee version to return. If not defined, the first evaluatee will be returned. Starts with `evv_`.

#### 🔄 Return<a id="🔄-return"></a>

[`PaginatedDataEvaluationResponse`](./humanloop/pydantic/paginated_data_evaluation_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/evaluations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.evaluations.list_all_for_project`<a id="humanloopevaluationslist_all_for_project"></a>
![Deprecated](https://img.shields.io/badge/deprecated-yellow)

Get all the evaluations associated with your project.

Deprecated: This is a legacy unpaginated endpoint. Use `/evaluations` instead, with appropriate
sorting, filtering and pagination options.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_all_for_project_response = humanloop.evaluations.list_all_for_project(
    project_id="project_id_example",
    evaluatee_id="string_example",
    evaluator_aggregates=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_id: `str`<a id="project_id-str"></a>

String ID of project. Starts with `pr_`.

##### evaluatee_id: `str`<a id="evaluatee_id-str"></a>

String ID of evaluatee version to return. If not defined, the first evaluatee will be returned. Starts with `evv_`.

##### evaluator_aggregates: `bool`<a id="evaluator_aggregates-bool"></a>

Whether to include evaluator aggregates in the response.

#### 🔄 Return<a id="🔄-return"></a>

[`EvaluationsGetForProjectResponse`](./humanloop/pydantic/evaluations_get_for_project_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/projects/{project_id}/evaluations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.evaluations.list_datapoints`<a id="humanloopevaluationslist_datapoints"></a>

Get testcases by evaluation ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_datapoints_response = humanloop.evaluations.list_datapoints(
    id="id_example",
    page=1,
    size=10,
    evaluatee_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of evaluation. Starts with `ev_`.

##### page: `int`<a id="page-int"></a>

Page to fetch. Starts from 1.

##### size: `int`<a id="size-int"></a>

Number of evaluation results to retrieve.

##### evaluatee_id: `str`<a id="evaluatee_id-str"></a>

String ID of evaluatee version to return. If not defined, the first evaluatee will be returned. Starts with `evv_`.

#### 🔄 Return<a id="🔄-return"></a>

[`PaginatedDataEvaluationDatapointSnapshotResponse`](./humanloop/pydantic/paginated_data_evaluation_datapoint_snapshot_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/evaluations/{id}/datapoints` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.evaluations.log`<a id="humanloopevaluationslog"></a>

Log an external generation to an evaluation run for a datapoint.

The run must have status 'running'.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
log_response = humanloop.evaluations.log(
    datapoint_id="string_example",
    log={
        "save": True,
    },
    evaluation_id="evaluation_id_example",
    evaluatee_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### datapoint_id: `str`<a id="datapoint_id-str"></a>

The datapoint for which a log was generated. Must be one of the datapoints in the dataset being evaluated.

##### log: [`LogRequest`](./humanloop/type/log_request.py)<a id="log-logrequesthumanlooptypelog_requestpy"></a>


The log generated for the datapoint.

##### evaluation_id: `str`<a id="evaluation_id-str"></a>

ID of the evaluation run. Starts with `evrun_`.

##### evaluatee_id: `str`<a id="evaluatee_id-str"></a>

String ID of evaluatee version to return. If not defined, the first evaluatee will be returned. Starts with `evv_`.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CreateEvaluationLogRequest`](./humanloop/type/create_evaluation_log_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`CreateLogResponse`](./humanloop/pydantic/create_log_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/evaluations/{evaluation_id}/log` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.evaluations.result`<a id="humanloopevaluationsresult"></a>

Log an evaluation result to an evaluation run.

The run must have status 'running'. One of `result` or `error` must be provided.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
result_response = humanloop.evaluations.result(
    log_id="string_example",
    evaluator_id="string_example",
    evaluation_id="evaluation_id_example",
    result=True,
    error="string_example",
    evaluatee_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### log_id: `str`<a id="log_id-str"></a>

The log that was evaluated. Must have as its `source_datapoint_id` one of the datapoints in the dataset being evaluated.

##### evaluator_id: `str`<a id="evaluator_id-str"></a>

ID of the evaluator that evaluated the log. Starts with `evfn_`. Must be one of the evaluator IDs associated with the evaluation run being logged to.

##### evaluation_id: `str`<a id="evaluation_id-str"></a>

ID of the evaluation run. Starts with `evrun_`.

##### result: Union[`bool`, `int`, `Union[int, float]`]<a id="result-unionbool-int-unionint-float"></a>


The result value of the evaluation.

##### error: `str`<a id="error-str"></a>

An error that occurred during evaluation.

##### evaluatee_id: `str`<a id="evaluatee_id-str"></a>

String ID of evaluatee version to return. If not defined, the first evaluatee will be returned. Starts with `evv_`.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CreateEvaluationResultLogRequest`](./humanloop/type/create_evaluation_result_log_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`EvaluationResultResponse`](./humanloop/pydantic/evaluation_result_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/evaluations/{evaluation_id}/result` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.evaluations.update_status`<a id="humanloopevaluationsupdate_status"></a>

Update the status of an evaluation run.

Can only be used to update the status of an evaluation run that uses external or human evaluators.
The evaluation must currently have status 'running' if swithcing to completed, or it must have status
'completed' if switching back to 'running'.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_status_response = humanloop.evaluations.update_status(
    status="pending",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### status: [`EvaluationStatus`](./humanloop/type/evaluation_status.py)<a id="status-evaluationstatushumanlooptypeevaluation_statuspy"></a>

The new status of the evaluation.

##### id: `str`<a id="id-str"></a>

String ID of evaluation run. Starts with `ev_`.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`UpdateEvaluationStatusRequest`](./humanloop/type/update_evaluation_status_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`EvaluationResponse`](./humanloop/pydantic/evaluation_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/evaluations/{id}/status` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.evaluators.create`<a id="humanloopevaluatorscreate"></a>

Create an evaluator within your organization.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = humanloop.evaluators.create(
    description="string_example",
    name="a",
    arguments_type="target_free",
    return_type="boolean",
    type="python",
    code="string_example",
    model_config={
        "provider": "openai",
        "model": "model_example",
        "max_tokens": -1,
        "temperature": 1,
        "top_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "endpoint": "complete",
        "prompt_template": "{{question}}",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### description: `str`<a id="description-str"></a>

The description of the evaluator.

##### name: `str`<a id="name-str"></a>

The name of the evaluator.

##### arguments_type: [`EvaluatorArgumentsType`](./humanloop/type/evaluator_arguments_type.py)<a id="arguments_type-evaluatorargumentstypehumanlooptypeevaluator_arguments_typepy"></a>

Whether this evaluator is target-free or target-required.

##### return_type: [`EvaluatorReturnTypeEnum`](./humanloop/type/evaluator_return_type_enum.py)<a id="return_type-evaluatorreturntypeenumhumanlooptypeevaluator_return_type_enumpy"></a>

The type of the return value of the evaluator.

##### type: [`EvaluatorType`](./humanloop/type/evaluator_type.py)<a id="type-evaluatortypehumanlooptypeevaluator_typepy"></a>

The type of the evaluator.

##### code: `str`<a id="code-str"></a>

The code for the evaluator. This code will be executed in a sandboxed environment.

##### model_config: [`ModelConfigCompletionRequest`](./humanloop/type/model_config_completion_request.py)<a id="model_config-modelconfigcompletionrequesthumanlooptypemodel_config_completion_requestpy"></a>


The model configuration used to generate.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CreateEvaluatorRequest`](./humanloop/type/create_evaluator_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`EvaluatorResponse`](./humanloop/pydantic/evaluator_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/evaluators` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.evaluators.delete`<a id="humanloopevaluatorsdelete"></a>

Delete an evaluator within your organization.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
humanloop.evaluators.delete(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/evaluators/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.evaluators.get`<a id="humanloopevaluatorsget"></a>

Get an evaluator within your organization.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = humanloop.evaluators.get(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`EvaluatorResponse`](./humanloop/pydantic/evaluator_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/evaluators/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.evaluators.list`<a id="humanloopevaluatorslist"></a>

Get all evaluators within your organization.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = humanloop.evaluators.list()
```

#### 🔄 Return<a id="🔄-return"></a>

[`EvaluatorsListResponse`](./humanloop/pydantic/evaluators_list_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/evaluators` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.evaluators.update`<a id="humanloopevaluatorsupdate"></a>

Update an evaluator within your organization.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_response = humanloop.evaluators.update(
    id="id_example",
    description="string_example",
    name="string_example",
    arguments_type="target_free",
    return_type="boolean",
    code="string_example",
    model_config={
        "provider": "openai",
        "model": "model_example",
        "max_tokens": -1,
        "temperature": 1,
        "top_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "endpoint": "complete",
        "prompt_template": "{{question}}",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

##### description: `str`<a id="description-str"></a>

The description of the evaluator.

##### name: `str`<a id="name-str"></a>

The name of the evaluator.

##### arguments_type: [`EvaluatorArgumentsType`](./humanloop/type/evaluator_arguments_type.py)<a id="arguments_type-evaluatorargumentstypehumanlooptypeevaluator_arguments_typepy"></a>

Whether this evaluator is target-free or target-required.

##### return_type: [`EvaluatorReturnTypeEnum`](./humanloop/type/evaluator_return_type_enum.py)<a id="return_type-evaluatorreturntypeenumhumanlooptypeevaluator_return_type_enumpy"></a>

The type of the return value of the evaluator.

##### code: `str`<a id="code-str"></a>

The code for the evaluator. This code will be executed in a sandboxed environment.

##### model_config: [`ModelConfigCompletionRequest`](./humanloop/type/model_config_completion_request.py)<a id="model_config-modelconfigcompletionrequesthumanlooptypemodel_config_completion_requestpy"></a>


The model configuration used to generate.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`UpdateEvaluatorRequest`](./humanloop/type/update_evaluator_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`EvaluatorResponse`](./humanloop/pydantic/evaluator_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/evaluators/{id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.feedback`<a id="humanloopfeedback"></a>

Submit an array of feedback for existing `data_ids`

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
feedback_response = humanloop.feedback(
    body=[
        {
            "type": "string_example",
        }
    ],
    type="string_example",
    value=True,
    data_id="string_example",
    user="string_example",
    created_at="1970-01-01T00:00:00.00Z",
    unset=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### type: Union[[`FeedbackType`](./humanloop/type/feedback_type.py), `str`]<a id="type-unionfeedbacktypehumanlooptypefeedback_typepy-str"></a>


The type of feedback. The default feedback types available are 'rating', 'action', 'issue', 'correction', and 'comment'.

##### value: Union[`bool`, `Union[int, float]`, `List[str]`, `str`]<a id="value-unionbool-unionint-float-liststr-str"></a>


The feedback value to be set. This field should be left blank when unsetting 'rating', 'correction' or 'comment', but is required otherwise.

##### data_id: `str`<a id="data_id-str"></a>

ID to associate the feedback to a previously logged datapoint.

##### user: `str`<a id="user-str"></a>

A unique identifier to who provided the feedback.

##### created_at: `datetime`<a id="created_at-datetime"></a>

User defined timestamp for when the feedback was created. 

##### unset: `bool`<a id="unset-bool"></a>

If true, the value for this feedback is unset.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FeedbackSubmitRequest`](./humanloop/type/feedback_submit_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`FeedbackSubmitResponse`](./humanloop/pydantic/feedback_submit_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/feedback` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.logs.delete`<a id="humanlooplogsdelete"></a>

Delete

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
humanloop.logs.delete(
    id=["string_example"],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: List[`str`]<a id="id-liststr"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/logs` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.logs.get`<a id="humanlooplogsget"></a>

Retrieve a log by log id.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = humanloop.logs.get(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of log to return. Starts with `data_`.

#### 🔄 Return<a id="🔄-return"></a>

[`LogResponse`](./humanloop/pydantic/log_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/logs/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.logs.list`<a id="humanlooplogslist"></a>

Retrieve paginated logs from the server.

Sorting and filtering are supported through query params.

Sorting is supported for the `source`, `model`, `timestamp`, and `feedback-{output_name}` columns.
Specify sorting with the `sort` query param, with values `{column}.{ordering}`.
E.g. ?sort=source.asc&sort=model.desc will yield a multi-column sort. First by source then by model.

Filtering is supported for the `source`, `model`, `feedback-{output_name}`,
`evaluator-{evaluator_external_id}` columns.

Specify filtering with the `source_filter`, `model_filter`, `feedback-{output.name}_filter` and
`evaluator-{evaluator_external_id}_filter` query params.

E.g. `?source_filter=AI&source_filter=user_1234&feedback-explicit_filter=good`
will only show rows where the source is "AI" or "user_1234", and where the latest feedback for the "explicit" output
group is "good".

An additional date range filter is supported for the `Timestamp` column (i.e. `Log.created_at`).
These are supported through the `start_date` and `end_date` query parameters.
The date format could be either date: `YYYY-MM-DD`, e.g. 2024-01-01
or datetime: YYYY-MM-DD[T]HH:MM[:SS[.ffffff]][Z or [±]HH[:]MM], e.g. 2024-01-01T00:00:00Z.

Searching is supported for the model inputs and output.
Specify a search term with the `search` query param.
E.g. `?search=hello%20there` will cause a case-insensitive search across model inputs and output.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = humanloop.logs.list(
    project_id="project_id_example",
    search="string_example",
    metadata_search="string_example",
    version_status="uncommitted",
    start_date="1970-01-01",
    end_date="1970-01-01",
    size=50,
    page=0,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_id: `str`<a id="project_id-str"></a>

##### search: `str`<a id="search-str"></a>

##### metadata_search: `str`<a id="metadata_search-str"></a>

##### version_status: [`VersionStatus`](./humanloop/type/.py)<a id="version_status-versionstatushumanlooptypepy"></a>

##### start_date: Union[`date`, `datetime`]<a id="start_date-uniondate-datetime"></a>


##### end_date: Union[`date`, `datetime`]<a id="end_date-uniondate-datetime"></a>


##### size: `int`<a id="size-int"></a>

##### page: `int`<a id="page-int"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`PaginatedDataLogResponse`](./humanloop/pydantic/paginated_data_log_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/logs` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.log`<a id="humanlooplog"></a>

Log a datapoint or array of datapoints to your Humanloop project.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
log_response = humanloop.log(
    body=[
        {
            "save": True,
        }
    ],
    project="string_example",
    project_id="string_example",
    session_id="string_example",
    session_reference_id="string_example",
    parent_id="string_example",
    parent_reference_id="string_example",
    inputs={},
    source="string_example",
    metadata={},
    save=True,
    source_datapoint_id="string_example",
    reference_id="string_example",
    messages=[
        {
            "role": "user",
        }
    ],
    output="string_example",
    judgment=True,
    config_id="string_example",
    config={
        "provider": "openai",
        "model": "model_example",
        "max_tokens": -1,
        "temperature": 1,
        "top_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "endpoint": "complete",
        "type": "ModelConfigRequest",
    },
    environment="string_example",
    feedback={
        "type": "string_example",
        "value": True,
    },
    created_at="1970-01-01T00:00:00.00Z",
    error="string_example",
    stdout="string_example",
    duration=3.14,
    output_message={
        "role": "user",
    },
    prompt_tokens=1,
    output_tokens=1,
    prompt_cost=3.14,
    output_cost=3.14,
    provider_request={},
    provider_response={},
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project: `str`<a id="project-str"></a>

Unique project name. If no project exists with this name, a new project will be created.

##### project_id: `str`<a id="project_id-str"></a>

Unique ID of a project to associate to the log. Either this or `project` must be provided.

##### session_id: `str`<a id="session_id-str"></a>

ID of the session to associate the datapoint.

##### session_reference_id: `str`<a id="session_reference_id-str"></a>

A unique string identifying the session to associate the datapoint to. Allows you to log multiple datapoints to a session (using an ID kept by your internal systems) by passing the same `session_reference_id` in subsequent log requests. Specify at most one of this or `session_id`.

##### parent_id: `str`<a id="parent_id-str"></a>

ID associated to the parent datapoint in a session.

##### parent_reference_id: `str`<a id="parent_reference_id-str"></a>

A unique string identifying the previously-logged parent datapoint in a session. Allows you to log nested datapoints with your internal system IDs by passing the same reference ID as `parent_id` in a prior log request. Specify at most one of this or `parent_id`. Note that this cannot refer to a datapoint being logged in the same request.

##### inputs: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="inputs-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

The inputs passed to the prompt template.

##### source: `str`<a id="source-str"></a>

Identifies where the model was called from.

##### metadata: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="metadata-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

Any additional metadata to record.

##### save: `bool`<a id="save-bool"></a>

Whether the request/response payloads will be stored on Humanloop.

##### source_datapoint_id: `str`<a id="source_datapoint_id-str"></a>

ID of the source datapoint if this is a log derived from a datapoint in a dataset.

##### reference_id: `str`<a id="reference_id-str"></a>

A unique string to reference the datapoint. Allows you to log nested datapoints with your internal system IDs by passing the same reference ID as `parent_id` in a subsequent log request.

##### messages: List[`ChatMessageWithToolCall`]<a id="messages-listchatmessagewithtoolcall"></a>

The messages passed to the to provider chat endpoint.

##### output: `str`<a id="output-str"></a>

Generated output from your model for the provided inputs. Can be `None` if logging an error, or if logging a parent datapoint with the intention to populate it later

##### judgment: Union[`bool`, `Union[int, float]`, `List[str]`, `str`]<a id="judgment-unionbool-unionint-float-liststr-str"></a>


##### config_id: `str`<a id="config_id-str"></a>

Unique ID of a config to associate to the log.

##### config: Union[`ModelConfigRequest`, `ToolConfigRequest`]<a id="config-unionmodelconfigrequest-toolconfigrequest"></a>


The model config used for this generation. Required unless `config_id` is provided.

##### environment: `str`<a id="environment-str"></a>

The environment name used to create the log.

##### feedback: Union[`Feedback`, List[`Feedback`]]<a id="feedback-unionfeedback-listfeedback"></a>


Optional parameter to provide feedback with your logged datapoint.

##### created_at: `datetime`<a id="created_at-datetime"></a>

User defined timestamp for when the log was created. 

##### error: `str`<a id="error-str"></a>

Error message if the log is an error.

##### stdout: `str`<a id="stdout-str"></a>

Captured log and debug statements.

##### duration: `Union[int, float]`<a id="duration-unionint-float"></a>

Duration of the logged event in seconds.

##### output_message: [`ChatMessageWithToolCall`](./humanloop/type/chat_message_with_tool_call.py)<a id="output_message-chatmessagewithtoolcallhumanlooptypechat_message_with_tool_callpy"></a>


The message returned by the provider.

##### prompt_tokens: `int`<a id="prompt_tokens-int"></a>

Number of tokens in the prompt used to generate the output.

##### output_tokens: `int`<a id="output_tokens-int"></a>

Number of tokens in the output generated by the model.

##### prompt_cost: `Union[int, float]`<a id="prompt_cost-unionint-float"></a>

Cost in dollars associated to the tokens in the prompt.

##### output_cost: `Union[int, float]`<a id="output_cost-unionint-float"></a>

Cost in dollars associated to the tokens in the output.

##### provider_request: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="provider_request-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

Raw request sent to provider.

##### provider_response: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="provider_response-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

Raw response received the provider.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`LogDatapointRequest`](./humanloop/type/log_datapoint_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`LogsLogResponse`](./humanloop/pydantic/logs_log_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/logs` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.logs.update`<a id="humanlooplogsupdate"></a>

Update a logged datapoint in your Humanloop project.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_response = humanloop.logs.update(
    id="id_example",
    output="string_example",
    error="string_example",
    duration=3.14,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of logged datapoint to return. Starts with `data_`.

##### output: `str`<a id="output-str"></a>

Generated output from your model for the provided inputs.

##### error: `str`<a id="error-str"></a>

Error message if the log is an error.

##### duration: `Union[int, float]`<a id="duration-unionint-float"></a>

Duration of the logged event in seconds.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`UpdateLogRequest`](./humanloop/type/update_log_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`LogResponse`](./humanloop/pydantic/log_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/logs/{id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.logs.update_by_ref`<a id="humanlooplogsupdate_by_ref"></a>

Update a logged datapoint by its reference ID.

The `reference_id` query parameter must be provided, and refers to the
`reference_id` of a previously-logged datapoint.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_by_ref_response = humanloop.logs.update_by_ref(
    reference_id="reference_id_example",
    output="string_example",
    error="string_example",
    duration=3.14,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### reference_id: `str`<a id="reference_id-str"></a>

A unique string to reference the datapoint. Identifies the logged datapoint created with the same `reference_id`.

##### output: `str`<a id="output-str"></a>

Generated output from your model for the provided inputs.

##### error: `str`<a id="error-str"></a>

Error message if the log is an error.

##### duration: `Union[int, float]`<a id="duration-unionint-float"></a>

Duration of the logged event in seconds.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`UpdateLogRequest`](./humanloop/type/update_log_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`LogResponse`](./humanloop/pydantic/log_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/logs` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.model_configs.deserialize`<a id="humanloopmodel_configsdeserialize"></a>

Deserialize a model config from a .prompt file format.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
deserialize_response = humanloop.model_configs.deserialize(
    config="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### config: `str`<a id="config-str"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`BodyModelConfigsDeserialize`](./humanloop/type/body_model_configs_deserialize.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ModelConfigResponse`](./humanloop/pydantic/model_config_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/model-configs/deserialize` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.model_configs.export`<a id="humanloopmodel_configsexport"></a>

Export a model config to a .prompt file by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
export_response = humanloop.model_configs.export(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of the model config. Starts with `config_`.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/model-configs/{id}/export` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.model_configs.get`<a id="humanloopmodel_configsget"></a>

Get a specific model config by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = humanloop.model_configs.get(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of the model config. Starts with `config_`.

#### 🔄 Return<a id="🔄-return"></a>

[`ModelConfigResponse`](./humanloop/pydantic/model_config_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/model-configs/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.model_configs.register`<a id="humanloopmodel_configsregister"></a>

Register a model config to a project.

If the project name provided does not exist, a new project will be created
automatically.

If the model config is the first to be associated to the project, it will
be set as the active model config.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
register_response = humanloop.model_configs.register(
    model="string_example",
    description="string_example",
    name="string_example",
    provider="openai",
    max_tokens=-1,
    temperature=1,
    top_p=1,
    stop="string_example",
    presence_penalty=0,
    frequency_penalty=0,
    other={},
    seed=1,
    response_format={
        "type": "string_example",
    },
    project="string_example",
    project_id="string_example",
    prompt_template="string_example",
    chat_template=[
        {
            "role": "user",
        }
    ],
    endpoint="complete",
    tools=[
        {
            "id": "id_example",
            "source": "organization",
        }
    ],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### model: `str`<a id="model-str"></a>

The model instance used. E.g. text-davinci-002.

##### description: `str`<a id="description-str"></a>

A description of the model config.

##### name: `str`<a id="name-str"></a>

A friendly display name for the model config. If not provided, a name will be generated.

##### provider: [`ModelProviders`](./humanloop/type/model_providers.py)<a id="provider-modelprovidershumanlooptypemodel_providerspy"></a>

The company providing the underlying model service.

##### max_tokens: `int`<a id="max_tokens-int"></a>

The maximum number of tokens to generate. Provide max_tokens=-1 to dynamically calculate the maximum number of tokens to generate given the length of the prompt

##### temperature: `Union[int, float]`<a id="temperature-unionint-float"></a>

What sampling temperature to use when making a generation. Higher values means the model will be more creative.

##### top_p: `Union[int, float]`<a id="top_p-unionint-float"></a>

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass.

##### stop: Union[`str`, `List[str]`]<a id="stop-unionstr-liststr"></a>


The string (or list of strings) after which the model will stop generating. The returned text will not contain the stop sequence.

##### presence_penalty: `Union[int, float]`<a id="presence_penalty-unionint-float"></a>

Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the generation so far.

##### frequency_penalty: `Union[int, float]`<a id="frequency_penalty-unionint-float"></a>

Number between -2.0 and 2.0. Positive values penalize new tokens based on how frequently they appear in the generation so far.

##### other: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="other-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

Other parameter values to be passed to the provider call.

##### seed: `int`<a id="seed-int"></a>

If specified, model will make a best effort to sample deterministically, but it is not guaranteed.

##### response_format: [`ResponseFormat`](./humanloop/type/response_format.py)<a id="response_format-responseformathumanlooptyperesponse_formatpy"></a>


The format of the response. Only type json_object is currently supported for chat.

##### project: `str`<a id="project-str"></a>

Unique project name. If it does not exist, a new project will be created.

##### project_id: `str`<a id="project_id-str"></a>

Unique project ID

##### prompt_template: `str`<a id="prompt_template-str"></a>

Prompt template that will take your specified inputs to form your final request to the provider model. NB: Input variables within the prompt template should be specified with syntax: {{INPUT_NAME}}.

##### chat_template: List[`ChatMessageWithToolCall`]<a id="chat_template-listchatmessagewithtoolcall"></a>

Messages prepended to the list of messages sent to the provider. These messages that will take your specified inputs to form your final request to the provider model. NB: Input variables within the prompt template should be specified with syntax: {{INPUT_NAME}}.

##### endpoint: [`ModelEndpoints`](./humanloop/type/model_endpoints.py)<a id="endpoint-modelendpointshumanlooptypemodel_endpointspy"></a>

Which of the providers model endpoints to use. For example Complete or Edit.

##### tools: [`ProjectModelConfigRequestTools`](./humanloop/type/project_model_config_request_tools.py)<a id="tools-projectmodelconfigrequesttoolshumanlooptypeproject_model_config_request_toolspy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ProjectModelConfigRequest`](./humanloop/type/project_model_config_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ProjectConfigResponse`](./humanloop/pydantic/project_config_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/model-configs` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.model_configs.serialize`<a id="humanloopmodel_configsserialize"></a>

Serialize a model config to a .prompt file format.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
serialize_response = humanloop.model_configs.serialize(
    body={
        "provider": "openai",
        "model": "model_example",
        "max_tokens": -1,
        "temperature": 1,
        "top_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "endpoint": "complete",
    },
    description="string_example",
    name="string_example",
    provider="openai",
    model="string_example",
    max_tokens=-1,
    temperature=1,
    top_p=1,
    stop="string_example",
    presence_penalty=0,
    frequency_penalty=0,
    other={},
    seed=1,
    response_format={
        "type": "string_example",
    },
    endpoint="complete",
    chat_template=[
        {
            "role": "user",
        }
    ],
    tools=[
        {
            "id": "id_example",
            "source": "organization",
        }
    ],
    prompt_template="{{question}}",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### description: `str`<a id="description-str"></a>

A description of the model config.

##### name: `str`<a id="name-str"></a>

A friendly display name for the model config. If not provided, a name will be generated.

##### provider: [`ModelProviders`](./humanloop/type/model_providers.py)<a id="provider-modelprovidershumanlooptypemodel_providerspy"></a>

The company providing the underlying model service.

##### model: `str`<a id="model-str"></a>

The model instance used. E.g. text-davinci-002.

##### max_tokens: `int`<a id="max_tokens-int"></a>

The maximum number of tokens to generate. Provide max_tokens=-1 to dynamically calculate the maximum number of tokens to generate given the length of the prompt

##### temperature: `Union[int, float]`<a id="temperature-unionint-float"></a>

What sampling temperature to use when making a generation. Higher values means the model will be more creative.

##### top_p: `Union[int, float]`<a id="top_p-unionint-float"></a>

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass.

##### stop: Union[`str`, `List[str]`]<a id="stop-unionstr-liststr"></a>


The string (or list of strings) after which the model will stop generating. The returned text will not contain the stop sequence.

##### presence_penalty: `Union[int, float]`<a id="presence_penalty-unionint-float"></a>

Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the generation so far.

##### frequency_penalty: `Union[int, float]`<a id="frequency_penalty-unionint-float"></a>

Number between -2.0 and 2.0. Positive values penalize new tokens based on how frequently they appear in the generation so far.

##### other: `Dict[str, Union[bool, date, datetime, dict, float, int, list, str, None]]`<a id="other-dictstr-unionbool-date-datetime-dict-float-int-list-str-none"></a>

Other parameter values to be passed to the provider call.

##### seed: `int`<a id="seed-int"></a>

If specified, model will make a best effort to sample deterministically, but it is not guaranteed.

##### response_format: [`ResponseFormat`](./humanloop/type/response_format.py)<a id="response_format-responseformathumanlooptyperesponse_formatpy"></a>


The format of the response. Only type json_object is currently supported for chat.

##### endpoint: [`ModelEndpoints`](./humanloop/type/model_endpoints.py)<a id="endpoint-modelendpointshumanlooptypemodel_endpointspy"></a>

The provider model endpoint used.

##### chat_template: List[`ChatMessageWithToolCall`]<a id="chat_template-listchatmessagewithtoolcall"></a>

Messages prepended to the list of messages sent to the provider. These messages that will take your specified inputs to form your final request to the provider model. Input variables within the template should be specified with syntax: {{INPUT_NAME}}.

##### tools: [`ModelConfigChatRequestTools`](./humanloop/type/model_config_chat_request_tools.py)<a id="tools-modelconfigchatrequesttoolshumanlooptypemodel_config_chat_request_toolspy"></a>

##### prompt_template: `str`<a id="prompt_template-str"></a>

Prompt template that will take your specified inputs to form your final request to the model. Input variables within the prompt template should be specified with syntax: {{INPUT_NAME}}.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ModelConfigsSerializeRequest`](./humanloop/type/model_configs_serialize_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/model-configs/serialize` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.projects.create`<a id="humanloopprojectscreate"></a>

Create a new project.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = humanloop.projects.create(
    name="string_example",
    directory_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

Unique project name.

##### directory_id: `str`<a id="directory_id-str"></a>

ID of directory to assign project to. Starts with `dir_`. If not provided, the project will be created in the root directory.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CreateProjectRequest`](./humanloop/type/create_project_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ProjectResponse`](./humanloop/pydantic/project_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/projects` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.projects.create_feedback_type`<a id="humanloopprojectscreate_feedback_type"></a>
![Deprecated](https://img.shields.io/badge/deprecated-yellow)

Create Feedback Type

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_feedback_type_response = humanloop.projects.create_feedback_type(
    type="string_example",
    _class="select",
    id="id_example",
    values=[
        {
            "value": "value_example",
            "sentiment": "positive",
        }
    ],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### type: `str`<a id="type-str"></a>

The type of feedback to update.

##### _class: [`FeedbackClass`](./humanloop/type/feedback_class.py)<a id="_class-feedbackclasshumanlooptypefeedback_classpy"></a>

The data type associated to this feedback type; whether it is a 'text'/'select'/'multi_select'.

##### id: `str`<a id="id-str"></a>

String ID of project. Starts with `pr_`.

##### values: List[`FeedbackLabelRequest`]<a id="values-listfeedbacklabelrequest"></a>

The feedback values to be available. This field should only be populated when updating a 'select' or 'multi_select' feedback class.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FeedbackTypeRequest`](./humanloop/type/feedback_type_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`FeedbackTypeModel`](./humanloop/pydantic/feedback_type_model.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/projects/{id}/feedback-types` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.projects.deactivate_config`<a id="humanloopprojectsdeactivate_config"></a>

Remove the project's active config, if set.

This has no effect if the project does not have an active model config set.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
deactivate_config_response = humanloop.projects.deactivate_config(
    id="id_example",
    environment="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of project. Starts with `pr_`.

##### environment: `str`<a id="environment-str"></a>

Name for the environment. E.g. 'production'. If not provided, will delete the active config for the default environment.

#### 🔄 Return<a id="🔄-return"></a>

[`ProjectResponse`](./humanloop/pydantic/project_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/projects/{id}/active-config` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.projects.delete`<a id="humanloopprojectsdelete"></a>

Delete a specific file.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
humanloop.projects.delete(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of project. Starts with `pr_`.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/projects/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.projects.delete_deployed_config`<a id="humanloopprojectsdelete_deployed_config"></a>

Remove the version deployed to environment.

This has no effect if the project does not have an active version set.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
delete_deployed_config_response = humanloop.projects.delete_deployed_config(
    project_id="project_id_example",
    environment_id="environment_id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_id: `str`<a id="project_id-str"></a>

##### environment_id: `str`<a id="environment_id-str"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/projects/{project_id}/deployed-config/{environment_id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.projects.deploy_config`<a id="humanloopprojectsdeploy_config"></a>

Deploy a model config to an environment.

If the environment already has a model config deployed, it will be replaced.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
deploy_config_response = humanloop.projects.deploy_config(
    config_id="string_example",
    project_id="project_id_example",
    environments=[
        {
            "id": "id_example",
        }
    ],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### config_id: `str`<a id="config_id-str"></a>

Model config unique identifier generated by Humanloop.

##### project_id: `str`<a id="project_id-str"></a>

##### environments: List[`EnvironmentRequest`]<a id="environments-listenvironmentrequest"></a>

List of environments to associate with the model config.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`EnvironmentProjectConfigRequest`](./humanloop/type/environment_project_config_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ProjectsDeployConfigToEnvironmentsResponse`](./humanloop/pydantic/projects_deploy_config_to_environments_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/projects/{project_id}/deploy-config` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.projects.export`<a id="humanloopprojectsexport"></a>

Export all logged datapoints associated to your project.

Results are paginated and sorts the datapoints based on `created_at` in
descending order.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
export_response = humanloop.projects.export(
    id="id_example",
    page=0,
    size=10,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of project. Starts with `pr_`.

##### page: `int`<a id="page-int"></a>

Page offset for pagination.

##### size: `int`<a id="size-int"></a>

Page size for pagination. Number of logs to export.

#### 🔄 Return<a id="🔄-return"></a>

[`PaginatedDataLogResponse`](./humanloop/pydantic/paginated_data_log_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/projects/{id}/export` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.projects.get`<a id="humanloopprojectsget"></a>

Get a specific project.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = humanloop.projects.get(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of project. Starts with `pr_`.

#### 🔄 Return<a id="🔄-return"></a>

[`ProjectResponse`](./humanloop/pydantic/project_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/projects/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.projects.get_active_config`<a id="humanloopprojectsget_active_config"></a>

Retrieves a config to use to execute your model.

A config will be selected based on the project's
active config settings.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_active_config_response = humanloop.projects.get_active_config(
    id="id_example",
    environment="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of project. Starts with `pr_`.

##### environment: `str`<a id="environment-str"></a>

Name for the environment. E.g. 'production'. If not provided, will return the active config for the default environment.

#### 🔄 Return<a id="🔄-return"></a>

[`GetModelConfigResponse`](./humanloop/pydantic/get_model_config_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/projects/{id}/active-config` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.projects.list`<a id="humanloopprojectslist"></a>

Get a paginated list of files.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = humanloop.projects.list(
    page=0,
    size=10,
    filter="string_example",
    user_filter="string_example",
    sort_by="created_at",
    order="asc",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### page: `int`<a id="page-int"></a>

Page offset for pagination.

##### size: `int`<a id="size-int"></a>

Page size for pagination. Number of projects to fetch.

##### filter: `str`<a id="filter-str"></a>

Case-insensitive filter for project name.

##### user_filter: `str`<a id="user_filter-str"></a>

Case-insensitive filter for users in the project. This filter matches against both email address and name of users.

##### sort_by: [`ProjectSortBy`](./humanloop/type/.py)<a id="sort_by-projectsortbyhumanlooptypepy"></a>

Field to sort projects by

##### order: [`SortOrder`](./humanloop/type/.py)<a id="order-sortorderhumanlooptypepy"></a>

Direction to sort by.

#### 🔄 Return<a id="🔄-return"></a>

[`PaginatedDataProjectResponse`](./humanloop/pydantic/paginated_data_project_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/projects` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.projects.list_configs`<a id="humanloopprojectslist_configs"></a>

Get an array of versions associated to your file.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_configs_response = humanloop.projects.list_configs(
    id="id_example",
    evaluation_aggregates=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of project. Starts with `pr_`.

##### evaluation_aggregates: `bool`<a id="evaluation_aggregates-bool"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ProjectsGetConfigsResponse`](./humanloop/pydantic/projects_get_configs_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/projects/{id}/configs` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.projects.list_deployed_configs`<a id="humanloopprojectslist_deployed_configs"></a>

Get an array of environments with the deployed configs associated to your project.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_deployed_configs_response = humanloop.projects.list_deployed_configs(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of project. Starts with `pr_`.

#### 🔄 Return<a id="🔄-return"></a>

[`ProjectsGetDeployedConfigsResponse`](./humanloop/pydantic/projects_get_deployed_configs_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/projects/{id}/deployed-configs` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.projects.update`<a id="humanloopprojectsupdate"></a>

Update a specific project.

Set the project's active model config by passing `active_model_config_id`.
These will be set to the Default environment unless a list of environments
are also passed in specifically detailing which environments to assign the
active config.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_response = humanloop.projects.update(
    id="id_example",
    name="string_example",
    active_config_id="string_example",
    directory_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of project. Starts with `pr_`.

##### name: `str`<a id="name-str"></a>

The new unique project name. Caution, if you are using the project name as the unique identifier in your API calls, changing the name will break the calls.

##### active_config_id: `str`<a id="active_config_id-str"></a>

ID for a config to set as the project's active deployment. Starts with 'config_'. 

##### directory_id: `str`<a id="directory_id-str"></a>

ID of directory to assign project to. Starts with `dir_`.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`UpdateProjectRequest`](./humanloop/type/update_project_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ProjectResponse`](./humanloop/pydantic/project_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/projects/{id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.projects.update_feedback_types`<a id="humanloopprojectsupdate_feedback_types"></a>
![Deprecated](https://img.shields.io/badge/deprecated-yellow)

Update feedback types.

WARNING: This endpoint has been decommissioned and no longer works. Please use the v5 Human Evaluators API instead.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_feedback_types_response = humanloop.projects.update_feedback_types(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of project. Starts with `pr_`.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/projects/{id}/feedback-types` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.sessions.create`<a id="humanloopsessionscreate"></a>

Create a new session.

Returns a session ID that can be used to log datapoints to the session.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_response = humanloop.sessions.create()
```

#### 🔄 Return<a id="🔄-return"></a>

[`CreateSessionResponse`](./humanloop/pydantic/create_session_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/sessions` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.sessions.get`<a id="humanloopsessionsget"></a>

Get a session by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_response = humanloop.sessions.get(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

String ID of session to return. Starts with `sesh_`.

#### 🔄 Return<a id="🔄-return"></a>

[`SessionResponse`](./humanloop/pydantic/session_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/sessions/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `humanloop.sessions.list`<a id="humanloopsessionslist"></a>

Get a page of sessions.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = humanloop.sessions.list(
    project_id="project_id_example",
    page=1,
    size=10,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_id: `str`<a id="project_id-str"></a>

String ID of project to return sessions for. Sessions that contain any datapoints associated to this project will be returned. Starts with `pr_`.

##### page: `int`<a id="page-int"></a>

Page to fetch. Starts from 1.

##### size: `int`<a id="size-int"></a>

Number of sessions to retrieve.

#### 🔄 Return<a id="🔄-return"></a>

[`PaginatedDataSessionResponse`](./humanloop/pydantic/paginated_data_session_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/sessions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---


## Author<a id="author"></a>
This Python package is automatically generated by [Konfig](https://konfigthis.com)
