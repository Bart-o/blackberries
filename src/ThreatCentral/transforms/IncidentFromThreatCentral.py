#!/usr/bin/env python
# -*- coding: utf-8 -*-

from canari.maltego.utils import debug
from canari.framework import configure
from common.entities import Incident
from canari.maltego.message import Label, UIMessage
from common.client import get_incident, encode_to_utf8, ThreatCentralError

__author__ = 'Bart Otten'
__copyright__ = 'Copyright 2015, Threat Central Project'
__credits__ = []

__license__ = 'Apache 2.0'
__version__ = '1'
__maintainer__ = 'Bart Otten'
__email__ = 'bart.otten@hp.com'
__status__ = 'Development'

__all__ = [
    'dotransform'
]


@configure(
    label='Get Incident Details',
    description='Get Incident Details from Threat Central',
    uuids=['threatcentral.v2.IncidentFromThreatCentral'],
    inputs=[('Threat Central', Incident)],
    debug=False,
    remote=False
)
def dotransform(request, response, config):
    if 'ThreatCentral.resourceId' in request.fields:
        try:
            incident = get_incident(request.fields['ThreatCentral.resourceId'])
        except ThreatCentralError as err:
            response += UIMessage(err.value, type='PartialError')

        else:
            try:
                # Update Incident entity
                e = Incident(request.value)
                e.title = encode_to_utf8(incident.get('title'))
                e.resourceId = incident.get('resourceId')
                e.reportedOn = incident.get('reportedOn')
                e += Label('Reported On', incident.get('reportedOn'))

                if len(incident.get('incidentCategory', list())) is not 0:
                    e += Label('Incident Category', '<br/>'.join([encode_to_utf8(_.get('displayName'))
                                                                 for _ in incident.get('incidentCategory', list())]))

                if len(incident.get('affectedAsset', list())) is not 0:
                    e += Label('Affected Asset', '<br/>'.join([encode_to_utf8(_.get('displayName'))
                                                              for _ in incident.get('affectedAsset', list())]))

                if len(incident.get('incidentEffect', list())) is not 0:
                    e += Label('Incident Effect', '<br/>'.join([encode_to_utf8(_.get('displayName'))
                                                               for _ in incident.get('incidentEffect', list())]))

                if len(incident.get('discoveryMethod', list())) is not 0:
                    e += Label('Discovery Method', '<br/>'.join([encode_to_utf8(_.get('displayName'))
                                                                for _ in incident.get('discoveryMethod', list())]))

                if incident.get('description'):
                    e += Label('Description', '<br/>'.join(encode_to_utf8(incident.get('description')
                                                                          ).split('\n')))

                response += e

            except AttributeError as err:
                response += UIMessage('Error: {}'.format(err), type='PartialError')
            except ThreatCentralError as err:
                response += UIMessage(err.value, type='PartialError')
            except TypeError:
                return response

    return response

