from bluesky.callbacks.olog import logbook_cb_factory
import readline
from collections import defaultdict

#{{- readline.get_history_item(1)}}


simple_template = """{{- start.plan_name }} ['{{ start.uid[:6] }}'] (scan num: {{ start.scan_id }})"""

manual_count_template =  """{{- start.plan_name }} ['{{ start.uid[:6] }}'] (scan num: {{ start.scan_id }}) (Measurement: {{start.Measurement}} )"""

 

count_template = """{{- start.plan_name}} :  {{start.plan_args.num}} ['{{ start.uid[:6] }}'] (scan num: {{ start.scan_id }}) (Measurement: {{start.Measurement}} )


Scan Plan
---------
{{ start.plan_type }}
{%- for k, v in start.plan_args | dictsort %}
    {{ k }}: {{ v }}
{%-  endfor %}
{% if 'signature' in start -%}
Call:
    {{ start.signature }}
{% endif %}
Metadata
--------
{% for k, v in start.items() -%}
{%- if k not in ['plan_type', 'plan_args'] -%}{{ k }} : {{ v }}
{% endif -%}


{%- endfor -%}
exposure time: TODO 
acquire  time: TODO 

"""


#single_motor_template = """{{- start.plan_name}} :  {{ start.motors[0]}} {{start.plan_args.start}} {{start.plan_args.stop}} {{start.plan_args.num}} ['{{ start.uid[:6] }}'] (scan num: {{ start.scan_id }})
single_motor_template = """{{- start.plan_name}} :  {{ start.motors[0]}}  {{'%0.3f' %start.plan_args.start|float}}    {{'%0.3f' %start.plan_args.stop|float}} {{start.plan_args.num}} ['{{ start.uid[:6] }}'] (scan num: {{ start.scan_id }})




Scan Plan
---------
{{ start.plan_type }}
{%- for k, v in start.plan_args | dictsort %}
    {{ k }}: {{ v }}
{%-  endfor %}
{% if 'signature' in start -%}
Call:
    {{ start.signature }}
{% endif %}
Metadata
--------
{% for k, v in start.items() -%}
{%- if k not in ['plan_type', 'plan_args'] -%}{{ k }} : {{ v }}
{% endif -%}


{%- endfor -%}
exposure time: TODO 
acquire  time: TODO 

"""

TEMPLATES = defaultdict(lambda: simple_template)
TEMPLATES['ct'] = count_template
TEMPLATES['count'] = count_template
TEMPLATES['manual_count'] = manual_count_template
TEMPLATES['dscan'] = single_motor_template
TEMPLATES['ascan'] = single_motor_template
TEMPLATES['ID_calibration'] = single_motor_template

from jinja2 import Template


# connect olog
from functools import partial
from pyOlog import SimpleOlogClient


# Set up the logbook. This configures bluesky's summaries of
# data acquisition (scan type, ID, etc.).

LOGBOOKS = ['Data Acquisition']  # list of logbook names to publish to
simple_olog_client = SimpleOlogClient()
generic_logbook_func = simple_olog_client.log
configured_logbook_func = partial(generic_logbook_func, logbooks=LOGBOOKS)

# This is for ophyd.commands.get_logbook, which simply looks for
# a variable called 'logbook' in the global IPython namespace.
logbook = simple_olog_client


logbook_cb = logbook_cb_factory(configured_logbook_func, desc_dispatch=TEMPLATES)

# Comment this line to turn off automatic log entries from bluesky.
RE.subscribe('start', logbook_cb)
