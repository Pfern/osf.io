#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Populate development database with Institution fixtures."""

import logging
import sys
import urllib

import django
from modularodm import Q
django.setup()

from framework.transactions.context import TokuTransaction
from website import settings
from website.app import init_app
from website.models import Institution, Node
from website.search.search import update_institution, update_node

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

ENVS = ['prod', 'stage', 'stage2', 'test']
SHIBBOLETH_SP_LOGIN = '{}/Shibboleth.sso/Login?entityID={{}}'.format(settings.CAS_SERVER_URL)
SHIBBOLETH_SP_LOGOUT = '{}/Shibboleth.sso/Logout?return={{}}'.format(settings.CAS_SERVER_URL)


def encode_uri_component(val):
    return urllib.quote(val, safe='~()*!.\'')


def update_or_create(inst_data):
    inst = Institution.load(inst_data['_id'])
    if inst:
        for key, val in inst_data.iteritems():
            setattr(inst, key, val)
        inst.save()
        print('Updated {}'.format(inst.name))
        update_institution(inst)
        return inst, False
    else:
        inst = Institution(**inst_data)
        inst.save()
        print('Added new institution: {}'.format(inst._id))
        update_institution(inst)
        return inst, True


def main(env):
    INSTITUTIONS = []

    if env == 'prod':
        INSTITUTIONS = [
            {
                '_id': 'busara',
                'name': 'Busara Center for Behavioral Economics',
                'description': 'The <a href="http://www.busaracenter.org/">Busara Center</a> for Behavioral Economics',
                'banner_name': 'busara-banner.png',
                'logo_name': 'busara-shield.png',
                'login_url': None,
                'logout_url': None,
                'domains': [],
                'email_domains': ['busaracenter.org'],
            },
            {
                '_id': 'colorado',
                'name': 'University of Colorado Boulder',
                'description': 'This service is supported by the Center for Research Data and Digital Scholarship, which is led by <a href="https://www.rc.colorado.edu/">Research Computing</a> and the <a href="http://www.colorado.edu/libraries/">University Libraries</a>.',
                'banner_name': 'colorado-banner.png',
                'logo_name': 'colorado-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('https://fedauth.colorado.edu/idp/shibboleth')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://osf.io/goodbye')),
                'domains': [],
                'email_domains': [],
            },
            {
                '_id': 'cos',
                'name': 'Center For Open Science',
                'description': 'COS is a non-profit technology company providing free and open services to increase inclusivity and transparency of research. Find out more at <a href="https://cos.io">cos.io</a>.',
                'banner_name': 'cos-banner.png',
                'logo_name': 'cos-shield.png',
                'login_url': None,
                'logout_url': None,
                'domains': ['osf.cos.io'],
                'email_domains': ['cos.io'],
            },
            {
                '_id': 'esip',
                'name': 'Federation of Earth Science Information Partners (ESIP)',
                'description': '<a href="http://www.esipfed.org/">ESIP\'s</a> mission is to support the networking and data dissemination needs of our members and the global Earth science data community by linking the functional sectors of observation, research, application, education and use of Earth science.',
                'banner_name': 'esip-banner.png',
                'logo_name': 'esip-shield.png',
                'login_url': None,
                'logout_url': None,
                'domains': [],
                'email_domains': ['esipfed.org'],
            },
            {
                '_id': 'jhu',
                'name': 'Johns Hopkins University',
                'description': 'A research data service provided by the <a href="https://www.library.jhu.edu/">Sheridan Libraries</a>.',
                'banner_name': 'jhu-banner.png',
                'logo_name': 'jhu-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('urn:mace:incommon:johnshopkins.edu')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://osf.io/goodbye')),
                'domains': ['osf.data.jhu.edu'],
                'email_domains': [],
            },
            {
                '_id': 'ljaf',
                'name': 'Laura and John Arnold Foundation',
                'description': 'Projects listed below are for grants awarded by the Foundation. Please see the <a href="http://www.arnoldfoundation.org/wp-content/uploads/Guidelines-for-Investments-in-Research.pdf">LJAF Guidelines for Investments in Research</a> for more information and requirements.',
                'banner_name': 'ljaf-banner.png',
                'logo_name': 'ljaf-shield.png',
                'login_url': None,
                'logout_url': None,
                'domains': [],
                'email_domains': ['arnoldfoundation.org'],
            },
            {
                '_id': 'nd',
                'name': 'University of Notre Dame',
                'description': 'In <a href="https://research.nd.edu/news/64035-notre-dame-center-for-open-science-partner-to-advance-open-science-initiatives/">partnership</a> with the <a href="https://crc.nd.edu">Center for Research Computing</a>, <a href="http://esc.nd.edu">Engineering &amp; Science Computing</a>, and the <a href="https://library.nd.edu">Hesburgh Libraries</a>',
                'banner_name': 'nd-banner.png',
                'logo_name': 'nd-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('https://login.nd.edu/idp/shibboleth')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://osf.io/goodbye')),
                'domains': ['osf.nd.edu'],
                'email_domains': [],
            },
            {
                '_id': 'nyu',
                'name': 'New York University',
                'description': 'A Research Project and File Management Tool for the NYU Community: <a href="https://www.nyu.edu/research.html">Research at NYU</a> | <a href="http://guides.nyu.edu/data_management">Research Data Management Planning</a> | <a href="https://library.nyu.edu/services/research/">NYU Library Research Services</a> | <a href="https://nyu.qualtrics.com/jfe6/form/SV_8dFc5TpA1FgLUMd">Get Help</a>',
                'banner_name': 'nyu-banner.png',
                'logo_name': 'nyu-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('urn:mace:incommon:nyu.edu')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://shibboleth.nyu.edu/idp/profile/Logout')),
                'domains': ['osf.nyu.edu'],
                'email_domains': [],
            },
            {
                '_id': 'ucsd',
                'name': 'University of California San Diego',
                'description': 'This service is supported on campus by the UC San Diego Library for our research community. Do not use this service to store or transfer personally identifiable information, personal health information, or any other controlled unclassified information. For assistance please contact the Library\'s Research Data Curation Program at <a href="mailto:research-data-curation@ucsd.edu">research-data-curation@ucsd.edu</a>.',
                'banner_name': 'ucsd-banner.png',
                'logo_name': 'ucsd-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('urn:mace:incommon:ucsd.edu')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://osf.io/goodbye')),
                'domains': ['osf.ucsd.edu'],
                'email_domains': [],
            },
            {
                '_id': 'ucr',
                'name': 'University of California Riverside',
                'description': 'Policy prohibits storing PII or HIPAA data on this site, please see C&amp;C\'s <a href="http://cnc.ucr.edu/security/researchers.html">security site</a> for more information.',
                'banner_name': 'ucr-banner.png',
                'logo_name': 'ucr-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('urn:mace:incommon:ucr.edu')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://osf.io/goodbye')),
                'domains': ['osf.ucr.edu'],
                'email_domains': [],
            },
            {
                '_id': 'ugent',
                'name': 'Universiteit Gent',
                'description': None,
                'banner_name': 'ugent-banner.png',
                'logo_name': 'ugent-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('https://identity.ugent.be/simplesaml/saml2/idp/metadata.php')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://osf.io/goodbye')),
                'domains': ['osf.ugent.be'],
                'email_domains': [],
            },
            {
                '_id': 'usc',
                'name': 'University of Southern California',
                'description': 'Projects must abide by <a href="http://policy.usc.edu/info-security/">USC\'s Information Security Policy</a>. Data stored for human subject research repositories must abide by <a href="http://policy.usc.edu/biorepositories/">USC\'s Biorepository Policy</a>. The OSF may not be used for storage of Personal Health Information that is subject to <a href="http://policy.usc.edu/hipaa/">HIPPA regulations</a>.',
                'banner_name': 'usc-banner.png',
                'logo_name': 'usc-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('urn:mace:incommon:usc.edu')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://osf.io/goodbye')),
                'domains': ['osf.usc.edu'],
                'email_domains': [],
            },
            {
                '_id': 'uva',
                'name': 'University of Virginia',
                'description': 'In partnership with the <a href="http://www.virginia.edu/vpr/">Vice President for Research</a>, <a href="http://dsi.virginia.edu">Data Science Institute</a>, <a href="https://www.hsl.virginia.edu">Health Sciences Library</a>, and <a href="http://data.library.virginia.edu">University Library</a>. Learn more about <a href="http://cadre.virginia.edu">UVA resources for computational and data-driven research</a>. Projects must abide by the <a href="http://www.virginia.edu/informationpolicy/security.html">University Security and Data Protection Policies</a>.',
                'banner_name': 'uva-banner.png',
                'logo_name': 'uva-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('urn:mace:incommon:virginia.edu')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://osf.io/goodbye')),
                'domains': ['osf.virginia.edu'],
                'email_domains': [],
            },
            {
                '_id': 'vt',
                'name': 'Virginia Tech',
                'description': None,
                'banner_name': 'vt-banner.png',
                'logo_name': 'vt-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('urn:mace:incommon:vt.edu')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://osf.io/goodbye')),
                'domains': ['osf.vt.edu'],
                'email_domains': [],
            },
        ]
    if env == 'stage':
        INSTITUTIONS = [
            {
                '_id': 'cos',
                'name': 'Center For Open Science [Stage]',
                'description': 'Center for Open Science [Stage]',
                'banner_name': 'cos-banner.png',
                'logo_name': 'cos-shield.png',
                'login_url': None,
                'logout_url': None,
                'domains': ['staging-osf.cos.io'],
                'email_domains': ['cos.io'],
            },
            {
                '_id': 'nd',
                'name': 'University of Notre Dame [Stage]',
                'description': 'University of Notre Dame [Stage]',
                'banner_name': 'nd-banner.png',
                'logo_name': 'nd-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('https://login-test.cc.nd.edu/idp/shibboleth')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://staging.osf.io/goodbye')),
                'domains': ['staging-osf-nd.cos.io'],
                'email_domains': [],
            },
            {
                '_id': 'google',
                'name': 'Google [Stage]',
                'description': 'Google [Stage]',
                'banner_name': 'google-banner.png',
                'logo_name': 'google-shield.png',
                'login_url': None,
                'logout_url': None,
                'domains': [],
                'email_domains': ['gmail.com'],
            },
            {
                '_id': 'yahoo',
                'name': 'Yahoo [Stage]',
                'description': 'Yahoo [Stage]',
                'banner_name': 'yahoo-banner.png',
                'logo_name': 'yahoo-shield.png',
                'login_url': None,
                'domains': [],
                'email_domains': ['yahoo.com'],
            },
        ]
    if env == 'stage2':
        INSTITUTIONS = [
            {
                '_id': 'cos',
                'name': 'Center For Open Science [Stage2]',
                'description': 'Center for Open Science [Stage2]',
                'banner_name': 'cos-banner.png',
                'logo_name': 'cos-shield.png',
                'login_url': None,
                'logout_url': None,
                'domains': ['staging2-osf.cos.io'],
                'email_domains': ['cos.io'],
            },
        ]
    elif env == 'test':
        INSTITUTIONS = [
            {
                '_id': 'busara',
                'name': 'Busara Center for Behavioral Economics [Test]',
                'description': 'The <a href="http://www.busaracenter.org/">Busara Center</a> for Behavioral Economics',
                'banner_name': 'busara-banner.png',
                'logo_name': 'busara-shield.png',
                'login_url': None,
                'logout_url': None,
                'domains': [],
                'email_domains': ['busaracenter.org'],
            },
            {
                '_id': 'colorado',
                'name': 'University of Colorado Boulder [Test]',
                'description': 'This service is supported by the Center for Research Data and Digital Scholarship, which is led by <a href="https://www.rc.colorado.edu/">Research Computing</a> and the <a href="http://www.colorado.edu/libraries/">University Libraries</a>.',
                'banner_name': 'colorado-banner.png',
                'logo_name': 'colorado-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('https://fedauth.colorado.edu/idp/shibboleth')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://test.osf.io/goodbye')),
                'domains': [],
                'email_domains': [],
            },
            {
                '_id': 'cos',
                'name': 'Center For Open Science [Test]',
                'description': 'COS is a non-profit technology company providing free and open services to increase inclusivity and transparency of research. Find out more at <a href="https://cos.io">cos.io</a>.',
                'banner_name': 'cos-banner.png',
                'logo_name': 'cos-shield.png',
                'login_url': None,
                'logout_url': None,
                'domains': ['test-osf.cos.io'],
                'email_domains': ['cos.io'],
            },
            {
                '_id': 'esip',
                'name': 'Federation of Earth Science Information Partners (ESIP) [Test]',
                'description': '<a href="http://www.esipfed.org/">ESIP\'s</a> mission is to support the networking and data dissemination needs of our members and the global Earth science data community by linking the functional sectors of observation, research, application, education and use of Earth science.',
                'banner_name': 'esip-banner.png',
                'logo_name': 'esip-shield.png',
                'login_url': None,
                'logout_url': None,
                'domains': [],
                'email_domains': ['esipfed.org'],
            },
            {
                '_id': 'jhu',
                'name': 'Johns Hopkins University [Test]',
                'description': 'A research data service provided by the <a href="https://www.library.jhu.edu/">Sheridan Libraries</a>.',
                'banner_name': 'jhu-banner.png',
                'logo_name': 'jhu-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('urn:mace:incommon:johnshopkins.edu')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://test.osf.io/goodbye')),
                'domains': ['osf.data.jhu.edu'],
                'email_domains': [],
            },
            {
                '_id': 'ljaf',
                'name': 'Laura and John Arnold Foundation [Test]',
                'description': 'Projects listed below are for grants awarded by the Foundation. Please see the <a href="http://www.arnoldfoundation.org/wp-content/uploads/Guidelines-for-Investments-in-Research.pdf">LJAF Guidelines for Investments in Research</a> for more information and requirements.',
                'banner_name': 'ljaf-banner.png',
                'logo_name': 'ljaf-shield.png',
                'login_url': None,
                'logout_url': None,
                'domains': [],
                'email_domains': ['arnoldfoundation.org'],
            },
            {
                '_id': 'nd',
                'name': 'University of Notre Dame [Test]',
                'description': 'In <a href="https://research.nd.edu/news/64035-notre-dame-center-for-open-science-partner-to-advance-open-science-initiatives/">partnership</a> with the <a href="https://crc.nd.edu">Center for Research Computing</a>, <a href="http://esc.nd.edu">Engineering &amp; Science Computing</a>, and the <a href="https://library.nd.edu">Hesburgh Libraries</a>',
                'banner_name': 'nd-banner.png',
                'logo_name': 'nd-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('https://login-test.cc.nd.edu/idp/shibboleth')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://test.osf.io/goodbye')),
                'domains': ['test-osf-nd.cos.io'],
                'email_domains': [],
            },
            {
                '_id': 'nyu',
                'name': 'New York University [Test]',
                'description': 'A Research Project and File Management Tool for the NYU Community: <a href="https://www.nyu.edu/research.html">Research at NYU</a> | <a href="http://guides.nyu.edu/data_management">Research Data Management Planning</a> | <a href="https://library.nyu.edu/services/research/">NYU Library Research Services</a> | <a href="https://nyu.qualtrics.com/jfe6/form/SV_8dFc5TpA1FgLUMd">Get Help</a>',
                'banner_name': 'nyu-banner.png',
                'logo_name': 'nyu-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('https://shibbolethqa.es.its.nyu.edu/idp/shibboleth')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://shibbolethqa.es.its.nyu.edu/idp/profile/Logout')),
                'domains': ['test-osf-nyu.cos.io'],
                'email_domains': [],
            },
            {
                '_id': 'ucsd',
                'name': 'University of California San Diego [Test]',
                'description': 'This service is supported on campus by the UC San Diego Library for our research community. Do not use this service to store or transfer personally identifiable information, personal health information, or any other controlled unclassified information. For assistance please contact the Library\'s Research Data Curation Program at <a href="mailto:research-data-curation@ucsd.edu">research-data-curation@ucsd.edu</a>.',
                'banner_name': 'ucsd-banner.png',
                'logo_name': 'ucsd-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('urn:mace:incommon:ucsd.edu')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://test.osf.io/goodbye')),
                'domains': ['test-osf-ucsd.cos.io'],
                'email_domains': [],
            },
            {
                '_id': 'ucr',
                'name': 'University of California Riverside [Test]',
                'description': 'Policy prohibits storing PII or HIPAA data on this site, please see C&amp;C\'s <a href="http://cnc.ucr.edu/security/researchers.html">security site</a> for more information.',
                'banner_name': 'ucr-banner.png',
                'logo_name': 'ucr-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('urn:mace:incommon:ucr.edu')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://test.osf.io/goodbye')),
                'domains': ['test-osf-ucr.cos.io'],
                'email_domains': [],
            },
            {
                '_id': 'ugent',
                'name': 'Universiteit Gent [Test]',
                'description': 'Universiteit Gent [Test]',
                'banner_name': 'ugent-banner.png',
                'logo_name': 'ugent-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('https://identity.ugent.be/simplesaml/saml2/idp/metadata.php')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://test.osf.io/goodbye')),
                'domains': ['test-osf-ugent.cos.io'],
                'email_domains': [],
            },
            {
                '_id': 'usc',
                'name': 'University of Southern California [Test]',
                'description': 'Projects must abide by <a href="http://policy.usc.edu/info-security/">USC\'s Information Security Policy</a>. Data stored for human subject research repositories must abide by <a href="http://policy.usc.edu/biorepositories/">USC\'s Biorepository Policy</a>. The OSF may not be used for storage of Personal Health Information that is subject to <a href="http://policy.usc.edu/hipaa/">HIPPA regulations</a>.',
                'banner_name': 'usc-banner.png',
                'logo_name': 'usc-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('urn:mace:incommon:usc.edu')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://test.osf.io/goodbye')),
                'domains': ['test-osf-usc.cos.io'],
                'email_domains': [],
            },
            {
                '_id': 'uva',
                'name': 'University of Virginia [Test]',
                'description': 'In partnership with the <a href="http://www.virginia.edu/vpr/">Vice President for Research</a>, <a href="http://dsi.virginia.edu">Data Science Institute</a>, <a href="https://www.hsl.virginia.edu">Health Sciences Library</a>, and <a href="http://data.library.virginia.edu">University Library</a>. Learn more about <a href="http://cadre.virginia.edu">UVA resources for computational and data-driven research</a>. Projects must abide by the <a href="http://www.virginia.edu/informationpolicy/security.html">University Security and Data Protection Policies</a>.',
                'banner_name': 'uva-banner.png',
                'logo_name': 'uva-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('https://shibidp-test.its.virginia.edu/idp/shibboleth')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://test.osf.io/goodbye')),
                'domains': ['test-osf-virginia.cos.io'],
                'email_domains': [],
            },
            {
                '_id': 'vt',
                'name': 'Virginia Tech [Test]',
                'description': None,
                'banner_name': 'vt-banner.png',
                'logo_name': 'vt-shield.png',
                'login_url': SHIBBOLETH_SP_LOGIN.format(encode_uri_component('https://shib-pprd.middleware.vt.edu')),
                'logout_url': SHIBBOLETH_SP_LOGOUT.format(encode_uri_component('https://test.osf.io/goodbye')),
                'domains': ['osf.vt.edu'],
                'email_domains': [],
            },
        ]

    init_app(routes=False)
    with TokuTransaction():
        for inst_data in INSTITUTIONS:
            new_inst, inst_created = update_or_create(inst_data)
            # update the nodes elastic docs, to have current names of institutions. This will
            # only work properly if this file is the only thing changing institution attributes
            if not inst_created:
                nodes = Node.find_by_institutions(new_inst, query=Q('is_deleted', 'ne', True))
                for node in nodes:
                    update_node(node, async=False)
        for extra_inst in Institution.objects.exclude(_id__in=[x['_id'] for x in INSTITUTIONS]):
            logger.warn('Extra Institution : {} - {}'.format(extra_inst._id, extra_inst.name))


if __name__ == '__main__':
    env = str(sys.argv[1]).lower() if len(sys.argv) == 2 else None
    if env not in ENVS:
        print('An environment must be specified : {}', ENVS)
        sys.exit(1)
    main(env)
