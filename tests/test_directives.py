from unittest import mock
import djed.form
from pyramid.config import Configurator
from pyramid.exceptions import ConfigurationConflictError

from djed.testing import BaseTestCase


class TestFieldset(BaseTestCase):

    _includes = ('djed.form',)

    @mock.patch('djed.form.directives.venusian')
    def test_declarative(self, m_venusian):

        @djed.form.field('my-field')
        class MyField(djed.form.Field):
            pass

        wrp, cb = m_venusian.attach.call_args[0]

        self.assertIs(wrp, MyField)

        m_venusian.config.with_package.return_value = self.config
        cb(m_venusian, 'my-field', MyField)

        self.assertIs(djed.form.get_field_factory(self.request, 'my-field'), MyField)

    def test_imperative(self):
        class MyField(djed.form.Field):
            """ """

        self.config.provide_form_field('my-field', MyField)
        self.assertIs(djed.form.get_field_factory(self.request, 'my-field'), MyField)

    def test_conflict(self):

        class MyField(djed.form.Field):
            pass

        class MyField2(djed.form.Field):
            pass

        config = Configurator()
        config.include('djed.form')
        config.provide_form_field('my-field', MyField)
        config.provide_form_field('my-field', MyField2)

        self.assertRaises(ConfigurationConflictError, config.commit)

    @mock.patch('djed.form.directives.venusian')
    def test_preview(self, m_venusian):

        class MyField(djed.form.Field):
            pass

        @djed.form.fieldpreview(MyField)
        def preview(request):
            """ """

        wrp, cb = m_venusian.attach.call_args[0]

        self.assertIs(wrp, preview)

        m_venusian.config.with_package.return_value = self.config
        cb(m_venusian, MyField, preview)

        from djed.form.directives import ID_PREVIEW
        previews = self.registry[ID_PREVIEW]

        self.assertIn(MyField, previews)
        self.assertIs(previews[MyField], preview)
        self.assertIs(djed.form.get_field_preview(self.request, MyField), preview)
