# -*- coding: utf-8 -*-

import operator
import re

from openerp import http, _
from openerp.http import request
from openerp.addons.web.controllers.main import Session


class Session(Session):

    @http.route('/web/session/change_password', type='json', auth="user")
    def change_password(self, fields):
        old_password, new_password, confirm_password = operator.itemgetter(
            'old_pwd', 'new_password', 'confirm_pwd')(
            dict(map(operator.itemgetter('name', 'value'), fields)))
        if not (old_password.strip() and new_password.strip() and confirm_password.strip()):
            return {'error': _('You cannot leave any password empty.'),
                    'title': _('Change Password')}
        if new_password != confirm_password:
            return {'error': _('The new password and its confirmation must be identical.'),
                    'title': _('Change Password')}
        length_error = len(new_password) < 8
        digit_error = re.search(r"\d", new_password) is None
        uppercase_error = re.search(r"[A-Z]", new_password) is None
        lowercase_error = re.search(r"[a-z]", new_password) is None
        symbol_error = re.search(r"[!@#$%&*,.^_`~]", new_password) is None
        if length_error or digit_error or \
                uppercase_error or lowercase_error or symbol_error:
            return {'error': _('New password is not satisfiled all the conditions.'),
                    'title': _('Error !')}
        try:
            if request.session.model('res.users').change_password(
                    old_password, new_password):
                return {'new_password': new_password}
        except Exception:
            return {
                'error': _('The old password you provided was incorrect, your password is not changed.'),
                'title': _('Change Password')
            }
        return {'error': _('Your Password was not changed.'),
            'title': _('Change Password')}
