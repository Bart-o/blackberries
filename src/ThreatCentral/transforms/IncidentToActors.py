#!/usr/bin/env python

from canari.maltego.utils import debug
from canari.framework import configure
from common.entities import Actor, Incident
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
    label='Get linked Actors',
    description='Get linked Actors from Threat Central',
    uuids=['threatcentral.v2.IncidentToActors'],
    inputs=[('Threat Central', Incident)],
    debug=False,
    remote=False
)
def dotransform(request, response, config):

    if 'ThreatCentral.resourceId' in request.fields:

        try:
            incidents = get_incident(request.fields['ThreatCentral.resourceId'])
        except ThreatCentralError as err:
            response += UIMessage(err.value, type='PartialError')

        else:
            try:
                # Show linked actors
                if len(incidents.get('actors', list())) is not 0:
                    for actor in incidents.get('actors'):
                        notes = list()
                        if actor.get('tcScore'):
                            weight = int(actor.get('tcScore'))
                        else:
                            weight = 1

                        if actor.get('name'):
                            e = Actor(encode_to_utf8(actor.get('name')), weight=weight)
                            e.name = encode_to_utf8(actor.get('name'))
                            e.actor = encode_to_utf8(actor.get('name'))
                        elif actor.get('title'):
                            e = Actor(encode_to_utf8(actor.get('title')), weight=weight)

                        e.title = encode_to_utf8(actor.get('title'))
                        e.resourceId = actor.get('resourceId')
                        if actor.get('organization'):
                            e.organization = encode_to_utf8(actor.get('organization'))
                        if actor.get('aliases'):
                            e.aliases = actor.get('aliases')
                        if actor.get('country'):
                            e.country = encode_to_utf8(actor.get('country', dict()).get('displayName'))
                        if actor.get('score'):
                            e.score = actor.get('score')

                        if actor.get('links'):
                            e += Label('Links', '<br/>'.join(['<a href="{}">{}</a>'.format(_.get('href'),
                                                                                           _.get('href'))
                                                              for _ in actor.get('links')]))
                        if actor.get('hyperlinks'):
                            e += Label('Hyperlinks', '<br/>'.join(['<a href="{}">{}</a>'.format(_.get('url'),
                                                                                                _.get('title'))
                                                                  for _ in actor.get('hyperlinks')]))

                        if actor.get('title'):
                            e += Label('Title', encode_to_utf8(actor.get('title')))
                        if actor.get('resourceId'):
                            e += Label('ResourceID', actor.get('resourceId'))

                        if actor.get('aliases'):
                            e += Label('Aliases', '<br/>'.join([encode_to_utf8(_) for _ in actor.get('aliases', '')]))
                        if actor.get('description'):
                            e += Label('Description', '<br/>'.join(encode_to_utf8(actor.get('description', '')
                                                                                  ).split('\n')))

                        if actor.get('country'):
                            e += Label('Country', encode_to_utf8(actor.get('country', dict()).get('displayName')))
                        if actor.get('organization'):
                            e += Label('Organization', encode_to_utf8(actor.get('organization')))
                        if actor.get('types'):
                            e += Label('Types', '<br/>'.join([encode_to_utf8(_.get('displayName'))
                                                              for _ in actor.get('types')]))

                        if actor.get('motivations'):
                            e += Label('Motivations', '<br/>'.join([encode_to_utf8(_.get('displayName'))
                                                                    for _ in actor.get('motivations')]))

                        if actor.get('intendedEffects'):
                            e += Label('Intended Effects', '<br/>'.join([encode_to_utf8(_.get('displayName'))
                                                                         for _ in actor.get('intendedEffects')]))

                        if actor.get('sophistication'):
                            e += Label('Sophistication', actor.get('sophistication', dict()).get('displayName'))

                        if actor.get('socialMediaText'):
                            e += Label('Social Media', '<br/>'.join(encode_to_utf8(actor.get('socialMediaText',
                                                                                             '')).split('\n')))

                        if actor.get('moreInfo'):
                            e += Label('More Info', '<br/>'.join(encode_to_utf8(actor.get('moreInfo', '')
                                                                                ).split('\n')))

                        if actor.get('score'):
                            e += Label('Score', actor.get('score'))

                        response += e

            except AttributeError as err:
                response += UIMessage('Error: {}'.format(err), type='PartialError')
            except ThreatCentralError as err:
                response += UIMessage(err.value, type='PartialError')
            except TypeError:
                return response

    return response
