""" Tests for L{djed.form.interfaces.Invalid} """
from djed.testing import TestCase, BaseTestCase


class TestInvalid(BaseTestCase):

    _includes = ('djed.form',)

    def test_ctor_default(self):
        from djed.form import Invalid

        err = Invalid()
        self.assertEqual(err.msg, '')
        self.assertIsNone(err.field)
        self.assertIsNone(err.mapping)
        self.assertIsNone(err.name)
        self.assertEqual(err.errors, {})

    def test_ctor(self):
        from djed.form import Invalid

        field = object()
        serror = Invalid('suberr', name='serror')

        err = Invalid('test', field, {'1':'2'}, 'err_name', [serror])
        self.assertEqual(err.msg, 'test')
        self.assertIs(err.field, field)
        self.assertEqual(err.mapping, {'1':'2'})
        self.assertEqual(err.name, 'err_name')
        self.assertEqual(err.errors, {'serror': serror})

    def test_str(self):
        from djed.form import Invalid, Field

        f = Field(name='test')
        f.request = self.request

        err = Invalid('${val} message', f, mapping={'val': 'Error'})
        self.assertEqual(str(err), 'Error message')

    def test_str_field_no_req(self):
        from djed.form import Invalid, Field

        err = Invalid('${val} message',
                      Field(name='test'), mapping={'val': 'Error'})
        self.assertEqual(str(err), 'Error message')

    def test_str_no_field(self):
        from djed.form import Invalid

        err = Invalid('${val} message', mapping={'val': 'Error'})
        self.assertEqual(str(err), 'Error message')

    def test_str_no_request(self):
        from djed.form import Invalid
        self.config.end()

        err = Invalid('${val} message', mapping={'val': 'Error'})
        self.assertEqual(str(err), '${val} message')

    def test_get_suberror_ctor(self):
        from djed.form import Invalid

        serr = Invalid(name='test')

        err = Invalid(errors=[serr])
        self.assertIs(err['test'], serr)

    def test_get_set_suberror(self):
        from djed.form import Invalid

        err = Invalid()

        serr = Invalid()
        err['test'] = serr

        self.assertIn('test', err)
        self.assertIs(err['test'], serr)
        self.assertEqual(serr.name, 'test')


class TestNull(TestCase):

    def test_null(self):
        import djed.form

        self.assertFalse(djed.form.null)
        self.assertFalse(len(djed.form.null))
        self.assertEqual(repr(djed.form.null), '<widget.null>')
