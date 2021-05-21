import logging
import time
from jaeger_client import Config
from flask import Flask

app = Flask(__name__)


def init_jaeger_tracer(service_name='your-app-name'):
    log_level = logging.DEBUG
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)

    config = Config(
        config={  # usually read from some yaml config
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name='simple-app',
        validate=True,
    )
    return config.initialize_tracer()


@app.route('/')
def jarger_test():

    # this call also sets opentracing.tracer
    tracer = init_jaeger_tracer()

    with tracer.start_span('TestSpan') as span:
        span.log_kv({'event': 'test message', 'life': 42})

        with tracer.start_span('ChildSpan', child_of=span) as child_span:
            child_span.log_kv({'event': 'down below'})

    time.sleep(2)
    tracer.close()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
