# -*- coding: utf-8 -*-

import re

from openerp import api, models
from openerp.addons.auth_signup.controllers.main import AuthSignupHome
from openerp.exceptions import ValidationError
from openerp.http import request


class ChangePassword(models.AbstractModel):

    _inherit = 'change.password.user'

    @api.multi
    def check_password_validation(self):
        """
        Verify the strength of 'password'
        Returns a dict indicating the wrong criteria
        A password is considered strong if:
            atleast 8 characters long
            atleast 1 digit
            atleast 1 special character [!@#$%&*,.^_`~]
            atleast 1 uppercase letter
            atleast 1 lowercase letter
        """
        passwords = self.mapped('new_passwd')
        if not passwords:
            raise ValidationError('Password Not satisfiled all the conditions')
        for password in passwords:
            length_error = len(password) < 8
            digit_error = re.search(r"\d", password) is None
            uppercase_error = re.search(r"[A-Z]", password) is None
            lowercase_error = re.search(r"[a-z]", password) is None
            symbol_error = re.search(r"[!@#$%&*,.^_`~]", password) is None
            if length_error or digit_error or \
                    uppercase_error or lowercase_error or symbol_error:
                raise ValidationError(
                    'Password not satisfiled all the conditions')
        return True

    @api.multi
    def change_password_button(self):
        self.check_password_validation()
        return super(ChangePassword, self).change_password_button()


class AuthSignupHome(AuthSignupHome):

    def check_password_validation(self, password=''):
        length_error = len(password) < 8
        digit_error = re.search(r"\d", password) is None
        uppercase_error = re.search(r"[A-Z]", password) is None
        lowercase_error = re.search(r"[a-z]", password) is None
        symbol_error = re.search(r"[!@#$%&*,.^_`~]", password) is None
        if length_error or digit_error or \
                uppercase_error or lowercase_error or symbol_error:
            return False
        return True

    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = dict((key, qcontext.get(key)) for key in ('login', 'name', 'password'))
        assert any([k for k in values.values()]), "The form was not properly filled in."
        assert values.get('password') == qcontext.get('confirm_password'), \
            "Passwords do not match; please retype them."
        res = self.check_password_validation(qcontext.get('password'))
        assert res is True, "New password should be stong. It must contains at least one Uppercase, \
            Lowercase, Number and Special Character. Special Characters are !@#$%&*,.^_`~"
        values['lang'] = request.lang
        self._signup_with_values(qcontext.get('token'), values)
        request.cr.commit()
