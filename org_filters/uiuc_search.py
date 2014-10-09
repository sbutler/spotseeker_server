"""
University of Illinois/NCSA Open Source License

Copyright (c) 2013 Board of Trustees, University of Illinois
All rights reserved.

Developed by:       CITES Software Development Group
                    University of Illinois
                    http://cites.illinois.edu                            

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal with the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

	Redistributions of source code must retain the above copyright
	notice, this list of conditions and the following disclaimers.

	Neither the names of CITES Software Development Group,
	University of Illinois, nor the names of its contributors may
	be used to endorse or promote products derived from this
	Software without specific prior written permission. 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR
ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE SOFTWARE. 
"""
import logging
import re
from spotseeker_server.org_filters.uiuc_ldap_client import get_res_street_address, get_edu_types
from spotseeker_server.models import SpotExtendedInfo
from spotseeker_server.org_filters import SearchFilter

# UIUC LDAP
LOGGER = logging.getLogger(__name__)

# TODO: Add to settings...
UIUC_REQUIRE_ADDRESS = 'uiuc_require_address'
UIUC_REQUIRE_EDUTYPE = 'uiuc_require_edutype'

class Filter(SearchFilter):
    keys = set((
        'extended_info:food_allowed',
        ))

    def filter_query(self, query):
        if 'extended_info:food_allowed' in self.request.GET:
            food_allowed = self.request.GET["extended_info:food_allowed"]
            if food_allowed:
                values = [food_allowed]
                if food_allowed == 'covered_drink':
                    values.append('any')
                query = query.filter(
                        spotextendedinfo__key="food_allowed",
                        spotextendedinfo__value__in=values
                        )

                self.has_valid_search_param = True

        if self.request.META.get('SS_OAUTH_USER', None):
            self.has_valid_search_param = True

        return query

    def filter_results(self, spots):
        """
        Remove any spots the current user can't view, based:
            - resedential address matching the regex stored in the
                extended info
            - uiucEduType matching the value stored in the extended
                info
        """

        username = self.request.META.get('SS_OAUTH_USER', None)
        if not username:
            LOGGER.info("User is not logged in. Show all spots.")
            result = spots
        else:
            # User logged in
            LOGGER.info("User is logged in. Show only spots they may access.")

            result = set()
            try:
                full_address = get_res_street_address(username)
                edutypes = get_edu_types(username)
            except:
                LOGGER.exception("Cannot get LDAP information")
                return spots

            for spot in spots: 
                add_spot = True

                try:
                    restrict_rule = spot.spotextendedinfo_set.get(
                            key=UIUC_REQUIRE_ADDRESS)
                    regex_text = restrict_rule.value
                    if re.search(regex_text, full_address, re.I):
                        LOGGER.debug("Restricted, user address matches.")
                    else:
                        LOGGER.debug("Restricted, no address match.")
                        add_spot = False
                except SpotExtendedInfo.MultipleObjectsReturned:
                    LOGGER.error("Spot %s has multiple %s values" % (spot, UIUC_REQUIRE_ADDRESS))
                    add_spot = False
                except SpotExtendedInfo.DoesNotExist:
                    # This is not a restricted spot.
                    LOGGER.debug("No restricted.")

                try:
                    restrict_rule = spot.spotextendedinfo_set.get(
                        key=UIUC_REQUIRE_EDUTYPE)
                    edutype = restrict_rule.value
                    if edutype in edutypes:
                        LOGGER.debug("Restricted, user type matches.")
                    else:
                        LOGGER.debug("Restricted, no types match.")
                        add_spot = False
                except SpotExtendedInfo.MultipleObjectsReturned:
                    LOGGER.error("Spot %s has multiple %s values" % (spot, UIUC_REQUIRE_EDUTYPE))
                    add_spot = False
                except SpotExtendedInfo.DoesNotExist:
                    # This is not a restricted spot.
                    LOGGER.debug("No restricted.")

                if add_spot:
                    result.add(spot)

        return result

