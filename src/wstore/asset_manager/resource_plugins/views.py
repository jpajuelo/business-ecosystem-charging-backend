# -*- coding: utf-8 -*-

# Copyright (c) 2015 - 2016 CoNWeT Lab., Universidad Politécnica de Madrid

# This file belongs to the business-charging-backend
# of the Business API Ecosystem.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import json
from urlparse import urljoin

from django.http import HttpResponse

from wstore.store_commons.resource import Resource
from wstore.store_commons.utils.http import build_response
from wstore.store_commons.utils.http import authentication_required
from wstore.models import ResourcePlugin, Context


def get_plugin_info(plugin):
    site = Context.objects.all()[0].site
    plugin_url = urljoin(site.domain, 'api/offering/resources/plugins/' + plugin.plugin_id)
    plugin_info = {
        'id': plugin.plugin_id,
        'href': plugin_url,
        'name': plugin.name,
        'author': plugin.author,
        'version': plugin.version,
        'mediaTypes': plugin.media_types,
        'formats': plugin.formats,
        'overrides': plugin.overrides
    }
    if plugin.form:
        plugin_info['form'] = plugin.form

    return plugin_info


class PluginCollection(Resource):

    @authentication_required
    def read(self, request):
        """
        This view is used to retrieve the existing resource plugin types
        """
        # Load basic types
        result = []

        # Get resource plugins
        plugins = ResourcePlugin.objects.all()

        for plugin in plugins:
            result.append(get_plugin_info(plugin))

        mime_type = 'application/JSON; charset=UTF-8'
        return HttpResponse(json.dumps(result), status=200, mimetype=mime_type)


class PluginEntry(Resource):

    @authentication_required
    def read(self, request, plugin_id):
        try:
            plugin = ResourcePlugin.objects.get(plugin_id=plugin_id)
        except:
            return build_response(request, 404, 'Digital asset type not found')

        plugin_info = get_plugin_info(plugin)
        mime_type = 'application/JSON; charset=UTF-8'
        return HttpResponse(json.dumps(plugin_info), status=200, mimetype=mime_type)