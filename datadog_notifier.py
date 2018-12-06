from datadog import statsd

def notify(co2, tvoc):
    statsd.gauge('misc.office.co2', co2)
    statsd.gauge('misc.office.tvoc', tvoc)
