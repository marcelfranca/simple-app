from flask import Flask
from flask import request
import requests

from jaeger_client import Config
from flask_opentracing import FlaskTracer
import opentracing

app = Flask(__name__)


@app.route('/')
def pull_requests():
    # Fetch a list of pull requests on the opentracing repository
    github_url = "https://api.github.com/repos/opentracing/opentracing-python/pulls"

    parent_span = flask_tracer.get_span()
    with opentracing.tracer.start_span('github-api', child_of=parent_span) as span:
        span.set_tag("http.url", github_url)
        r = requests.get(github_url)
        span.set_tag("http.status_code", r.status_code)

    with opentracing.tracer.start_span('parse-json', child_of=parent_span) as span:
        json = r.json()
        span.set_tag("pull_requests", len(json))
        pull_request_titles = map(lambda item: item['title'], json)

    return 'OpenTracing Pull Requests: ' + ', '.join(pull_request_titles)


def initialize_tracer():
    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1}
        },
        service_name='hello-world')
    return config.initialize_tracer()  # also sets opentracing.tracer


flask_tracer = FlaskTracer(initialize_tracer, True, app)
