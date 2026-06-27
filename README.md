LLM API Gateway

A production-minded Python project for learning how to integrate with an LLM provider safely, observably, and incrementally.

The current version establishes a reliable foundation for communicating with the OpenAI Responses API. It securely loads credentials, sends a controlled model request, handles common API failures, and reports useful metadata such as token usage and request IDs.

Current status: Initial API integration and smoke test completed.
The FastAPI gateway, automated tests, request schemas, and production features will be added incrementally during Week 3 of the AI Engineering learning path.

Project Purpose

Calling an LLM API is easy.

Building a dependable service around an LLM requires more:

secure secret management
explicit model configuration
timeout and retry handling
API error handling
token usage tracking
request tracing
logging
input and output validation
tests
clear documentation

This project is being developed to demonstrate those engineering practices step by step.

What This Project Proves

The current implementation demonstrates the ability to:

configure an LLM provider through environment variables
protect API credentials from source control
use the OpenAI Python SDK
send requests through the Responses API
separate client configuration from execution logic
define explicit timeouts and retry behavior
handle common provider and networking errors
inspect model metadata
track input, output, and total token usage
use request IDs for debugging and traceability
document current limitations honestly
Current Features
OpenAI Responses API integration
Environment-based API key management
Configurable model name
Explicit request timeout
Automatic retry configuration
Persian model response example
Token usage reporting
Request ID reporting
Handling for:
authentication and API status errors
timeouts
rate limits
network connection failures
Planned Features

The following features are intentionally not implemented yet:

FastAPI HTTP endpoint
Pydantic request and response schemas
input validation
structured logging
application-level request IDs
automated unit tests
mocked provider tests
custom retry policy
streaming responses
cost estimation
provider abstraction
authentication
rate limiting
Docker support
CI pipeline

These features will be added only when they support the current learning gate.

Architecture
User / Application
        |
        v
Python Smoke Test
        |
        v
Configured OpenAI Client
        |
        v
OpenAI Responses API
        |
        v
Model Output + Token Usage + Request ID

Current request flow:

Environment Variables
        |
        v
create_openai_client()
        |
        v
client.responses.create()
        |
        v
Response Object
        |
        +--> output_text
        +--> usage
        +--> model snapshot
        +--> request ID
Project Structure
llm-api-gateway/
├── app/
│   ├── __init__.py
│   ├── openai_client.py
│   └── smoke_test.py
├── .env.example
├── .gitattributes
├── .gitignore
├── poetry.lock
├── pyproject.toml
└── README.md
File Responsibilities
app/openai_client.py

Creates and configures the OpenAI client.

Responsibilities:

load environment variables
verify that an API key exists
configure the request timeout
configure automatic retries
app/smoke_test.py

Runs a direct request against the OpenAI Responses API.

Responsibilities:

select the configured model
send instructions and user input
print the generated response
print token usage
print the provider request ID
handle expected API failures
Requirements
Python compatible with the version declared in pyproject.toml
Poetry
An OpenAI API Platform account
A valid OpenAI API key
Active API billing or available API credits

A ChatGPT subscription and OpenAI API billing are separate services.

Installation

Clone the repository:

git clone https://github.com/mr-hosseinaskarii/llm-api-gateway.git
cd llm-api-gateway

Install dependencies:

poetry install
Environment Configuration

Copy the example environment file:

PowerShell
Copy-Item .env.example .env
macOS / Linux
cp .env.example .env

Update .env with your own API key:

OPENAI_API_KEY=your_real_api_key
OPENAI_MODEL=gpt-5.4-mini-2026-03-17
Security Rules
Never commit .env.
Never place the API key directly inside Python code.
Never expose the API key in browser-side code.
Never paste the API key into logs, screenshots, issues, or documentation.
Revoke and replace a key immediately if it is exposed.
Commit .env.example, but leave its secret value empty.

Expected .env.example:

OPENAI_API_KEY=
OPENAI_MODEL=gpt-5.4-mini-2026-03-17
Running the Smoke Test

Run the script from the project root:

poetry run python -m app.smoke_test

Example sanitized output:

INFO | HTTP Request: POST https://api.openai.com/v1/responses "HTTP/1.1 200 OK"

--- MODEL OUTPUT ---
API is a mechanism that allows software systems to communicate and exchange data or functionality.

--- METADATA ---
model: gpt-5.4-mini-2026-03-17
request_id: req_example
input_tokens: 36
output_tokens: 91
total_tokens: 127

The real request ID is intentionally not included in the repository documentation.

Token Usage

The API response reports three important values:

input_tokens

Tokens consumed by the input sent to the model, including instructions, user input, and other request context.

output_tokens

Tokens generated by the model while producing its response.

total_tokens

The total reported token usage for the request.

total_tokens = input_tokens + output_tokens

Token usage is important because it affects:

API cost
latency
prompt size
context-window usage
monitoring
model-selection decisions

This project currently reports token usage but does not yet calculate monetary cost.

Model Alias and Snapshot

A model alias may point to a specific dated model snapshot.

For example:

Requested alias:
gpt-5.4-mini

Resolved snapshot:
gpt-5.4-mini-2026-03-17

Using an alias can provide access to newer default versions over time.

Using a dated snapshot provides greater reproducibility because the application is pinned to a specific model version.

This project currently uses a dated snapshot to reduce unexpected behavioral changes during development and testing.

Error Handling

The smoke test handles several common failure categories.

Timeout
The model provider did not respond within the configured timeout.

Handled with:

openai.APITimeoutError
Rate Limit or Quota
The provider rejected the request because of rate limits or unavailable quota.

Handled with:

openai.RateLimitError
Connection Failure
The application could not connect to the provider.

Handled with:

openai.APIConnectionError
Provider API Error
The provider returned an HTTP error such as 400, 401, 404, or 500.

Handled with:

openai.APIStatusError

The status code and provider request ID are logged when available.

Request IDs and Debugging

Each successful or failed provider request may include a request ID.

Example:

req_example

A request ID can help:

correlate application logs
identify a specific failed request
investigate provider-side errors
communicate clearly with provider support
trace failures in larger systems

A request ID is not a replacement for application logging. A production system should store it alongside its own request ID, timestamp, model, latency, token usage, and result status.

Example Failure Encountered

During initial setup, the API returned:

401 Unauthorized

The request successfully reached the provider, but authentication failed because the API key was invalid.

Resolution:

A new API key was created.
The local .env file was updated.
The request was executed again.
The API returned 200 OK.

This demonstrates why authentication errors should be handled explicitly rather than treated as generic application failures.

Testing

Automated tests have not been implemented yet.

Upcoming tests will cover:

missing API key behavior
client configuration
model configuration
provider error mapping
successful response parsing
token usage extraction
mocked API responses

Real API calls should not be required for normal unit tests because they:

cost money
depend on external network access
may be rate-limited
can produce nondeterministic output
make the test suite slower

Provider calls will therefore be mocked in the automated test suite.

Current Limitations
The project is currently a command-line smoke test, not a complete HTTP gateway.
There is no FastAPI endpoint yet.
User input is currently hard-coded.
Model output is not validated.
There is no structured output schema.
There is no persistent logging.
There is no latency measurement.
Monetary cost is not calculated.
There are no automated tests yet.
There is no fallback model.
There is no provider abstraction.
There is no authentication or rate limiting.
The application currently supports only OpenAI.
Planned Development Stages
Stage 1 — Provider Smoke Test

Secure API key loading

OpenAI Responses API request

Timeout configuration

Retry configuration

Token usage reporting

Request ID reporting

Basic error handling

Stage 2 — Application Service

Extract provider-call logic into a reusable service

Accept dynamic user input

Return an internal response model

Add structured application logging

Stage 3 — FastAPI Gateway

Create a FastAPI application

Add a health endpoint

Add an LLM generation endpoint

Add Pydantic schemas

Map provider errors to safe HTTP responses

Stage 4 — Testing

Unit-test configuration

Mock OpenAI responses

Test timeout and provider failures

Test missing or invalid output

Add regression tests

Stage 5 — Production Foundation

Dockerize the application

Add rate limiting

Add authentication

Add latency and cost tracking

Add CI

Add operational documentation

Engineering Principles

This project follows several rules:

Secrets must never enter source control.
External provider failures must be expected.
Model responses must not be trusted blindly.
Token usage must be visible.
Models must be selected based on requirements, not hype.
Small, tested increments are preferred over large unfinished systems.
Documentation must describe the real project state.
A successful API call is only the beginning of AI Engineering.
What This Project Is Not

This project is currently not:

a complete production gateway
a RAG system
an AI agent
a multi-provider platform
a fine-tuned model
a LangChain application
a frontend chatbot
a complete LLMOps system

Those features are intentionally outside the current scope.

Learning Outcomes

By building this project, the developer practices:

LLM API integration
secret management
environment configuration
provider error handling
timeout and retry awareness
token usage interpretation
request tracing
model version awareness
documentation discipline
incremental AI system development

No license has been selected yet.

Until a license is added, reuse and redistribution rights are not explicitly granted.

Author

Developed as part of a structured AI Engineering learning path.

Target roles:

Junior AI Engineer
AI Backend Developer
LLM Application Developer
Python AI Engineer
Applied AI Engineer