#!/usr/bin/env python

from canari.maltego.utils import debug
from canari.framework import configure
from common.entities import Case, TTP
from canari.maltego.message import UIMessage
from common.client import get_case, encode_to_utf8, ThreatCentralError

__author__ = 'Bart Otten'
__copyright__ = 'Copyright 2015, Threat Central'
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
    label='Get linked TTPs',
    description='Get linked TTPs from Threat Central',
    uuids=['threatcentral.v2.CaseToTTP'],
    inputs=[('Threat Central', Case)],
    debug=False,
    remote=False
)
def dotransform(request, response, config):

    if 'ThreatCentral.resourceId' in request.fields:
        try:
            case = get_case(request.fields['ThreatCentral.resourceId'])
        except ThreatCentralError as err:
            response += UIMessage(err.value, type='PartialError')
        else:
            try:
                # Show linked TTP's
                if len(case.get('tacticsTechniquesAndProcedures', list())) is not 0:
                    for ttp in case.get('tacticsTechniquesAndProcedures'):
                        if ttp.get('tcScore'):
                            weight = int(ttp.get('tcScore'))
                        else:
                            weight = 1

                        e = TTP(encode_to_utf8(ttp.get('title')), weight=weight)
                        e.title = encode_to_utf8(ttp.get('title'))
                        e.resourceId = ttp.get('resourceId')
                        response += e

            except AttributeError as err:
                response += UIMessage('Error: {}'.format(err), type='PartialError')
            except ThreatCentralError as err:
                response += UIMessage(err.value, type='PartialError')
            except TypeError:
                return response

    return response
