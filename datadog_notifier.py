from datadog import statsd

def update_co2(co2):
    statsd.gauge('misc.office.co2', co2)
