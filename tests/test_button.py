from .base import strip, BaseTestCase, TestCase


class TestButton(BaseTestCase):

    def test_ctor(self):
        import djed.form

        btn = djed.form.Button(name='test', action_name='action',
                          actype = djed.form.AC_PRIMARY)

        self.assertEqual(btn.name, 'test')
        self.assertEqual(btn.value, 'Test')
        self.assertIsNone(btn.title)
        self.assertEqual(btn.actype, djed.form.AC_PRIMARY)
        self.assertEqual(repr(btn), '<Button "test" : "Test">')

    def test_bind(self):
        import djed.form

        btn = djed.form.Button(name='test', action_name='action',
                          actype = djed.form.AC_PRIMARY)
        params = {}
        context = object()
        request = DummyRequest()

        widget = btn.bind(request, 'test.', params, context)

        self.assertIsNot(btn, widget)
        self.assertIs(widget.context, context)
        self.assertIs(widget.request, request)
        self.assertIs(widget.params, params)
        self.assertEqual(widget.id, 'test-test')
        self.assertEqual(widget.name, 'test.test')
        self.assertEqual(widget.klass, 'btn btn-primary')

    def test_activated(self):
        import djed.form

        btn = djed.form.Button(name='test', action_name='action',
                          actype = djed.form.AC_PRIMARY)
        params = {'button.unkown': 'true'}
        context = object()
        request = DummyRequest()

        widget = btn.bind(request, 'button.', params, context)

        self.assertFalse(widget.activated())

        widget.params = {'button.test': 'true'}
        self.assertTrue(widget.activated())

    def test_render(self):
        import djed.form

        btn = djed.form.Button(name='test', action_name='action',
                           title='Title', actype = djed.form.AC_PRIMARY)
        params = {}
        context = object()
        request = self.request

        widget = btn.bind(request, 'test.', params, context)
        self.assertEqual(
            strip(widget.render().strip()),
            '<input type="submit" class="btn btn-primary" value="Test" id="test-test" name="test.test" title="Title">')

    def test_execute(self):
        import djed.form

        btn = djed.form.Button(name='test', action_name='action')

        class Test(object):
            def action(self):
                return 'Action executed'

        self.assertRaises(AttributeError, btn, object())
        self.assertEqual(btn(Test()), 'Action executed')

        btn = djed.form.Button(name='test', action=Test.action,
                          actype = djed.form.AC_PRIMARY)
        self.assertEqual(btn(Test()), 'Action executed')

        btn = djed.form.Button(name='test')
        self.assertRaises(TypeError, btn, Test())

    def test_execute_with_extract(self):
        import djed.form
        btn = djed.form.Button(name='test', action_name='action', extract=True)

        class Test(object):
            def extract(self):
                return {'k1': 'value'}, ()

            def action(self, data):
                return data

        self.assertEqual(btn(Test()), {'k1': 'value'})

    def test_execute_with_extract_with_errors(self):
        import djed.form
        btn = djed.form.Button(name='test', action_name='action', extract=True)

        class Test(object):
            def add_error_message(self, msg):
                self.msg = msg

            def extract(self):
                return {'k1': 'value'}, ('error1','error2')

        f = Test()

        self.assertIsNone(btn(f))
        self.assertEqual(f.msg, ('error1','error2'))


class TestButtons(TestCase):

    def test_ctor(self):
        import djed.form

        btn1 = djed.form.Button(name='test1', action_name='action')
        btn2 = djed.form.Button(name='test2', action_name='action')

        btns = djed.form.Buttons()
        self.assertFalse(bool(btns))

        btns = djed.form.Buttons(btn1, btn2)
        self.assertEqual(list(btns.keys()), [btn1.name, btn2.name])
        self.assertEqual(list(btns.values()), [btn1, btn2])

        btns = djed.form.Buttons(btn1)
        self.assertEqual(list(btns.keys()), [btn1.name])

        btns = djed.form.Buttons(btn2, btns)
        self.assertEqual(list(btns.keys()), [btn2.name, btn1.name])
        self.assertEqual(list(btns.values()), [btn2, btn1])

    def test_add(self):
        import djed.form

        btn1 = djed.form.Button(name='test1', action_name='action')
        btn2 = djed.form.Button(name='test2', action_name='action')

        btns = djed.form.Buttons(btn1)

        btns.add(btn2)
        self.assertEqual(list(btns.keys()), [btn1.name, btn2.name])
        self.assertEqual(list(btns.values()), [btn1, btn2])

    def test_add_duplicate(self):
        import djed.form

        btn1 = djed.form.Button(name='test1', action_name='action')
        btn2 = djed.form.Button(name='test1', action_name='action')

        btns = djed.form.Buttons(btn1)

        self.assertRaises(ValueError, btns.add, btn2)

    def test_add_action(self):
        import djed.form

        btns = djed.form.Buttons()

        btn1 = btns.add_action('Test action')

        self.assertIsInstance(btn1, djed.form.Button)
        self.assertEqual(list(btns.keys()), [btn1.name])
        self.assertEqual(list(btns.values()), [btn1])

    def test_iadd(self):
        import djed.form

        btn1 = djed.form.Button(name='test1', action_name='action')
        btn2 = djed.form.Button(name='test2', action_name='action')

        btns1 = djed.form.Buttons(btn1)
        btns2 = djed.form.Buttons(btn2)

        btns = btns1 + btns2
        self.assertEqual(list(btns.keys()), [btn1.name, btn2.name])
        self.assertEqual(list(btns.values()), [btn1, btn2])


class TestButtonDecorator(TestCase):

    def test_decorator(self):
        import djed.form

        class MyForm(object):
            @djed.form.button('Test button', title='Test button title')
            def handler(self):
                """ """

        self.assertEqual(len(MyForm.buttons), 1)

        btn = list(MyForm.buttons.values())[0]
        self.assertEqual(btn.value, 'Test button')
        self.assertEqual(btn.title, 'Test button title')
        self.assertEqual(btn.action_name, 'handler')
        self.assertFalse(btn.extract)

    def test_decorator_buton2(self):
        import djed.form

        class MyForm(object):
            @djed.form.button2('Test button', title='Test button title')
            def handler(self):
                """ """

        self.assertEqual(len(MyForm.buttons), 1)

        btn = list(MyForm.buttons.values())[0]
        self.assertEqual(btn.value, 'Test button')
        self.assertEqual(btn.title, 'Test button title')
        self.assertEqual(btn.action_name, 'handler')
        self.assertTrue(btn.extract)

    def test_decorator_multiple(self):
        import djed.form

        class MyForm(object):
            @djed.form.button('Test button')
            def handler1(self):
                """ """
            @djed.form.button('Test button2')
            def handler2(self):
                """ """

        self.assertEqual(len(MyForm.buttons), 2)

        btn1 = list(MyForm.buttons.values())[0]
        btn2 = list(MyForm.buttons.values())[1]
        self.assertEqual(btn1.action_name, 'handler1')
        self.assertEqual(btn2.action_name, 'handler2')

    def test_create_id(self):
        import binascii
        from djed.form.button import create_btn_id

        self.assertEqual(create_btn_id('Test'), 'test')
        self.assertEqual(create_btn_id('Test title'),
                         binascii.hexlify('Test title'.encode('utf-8')))


class TestActions(TestCase):

    def _makeOne(self, form, request):
        from djed.form.button import Actions
        return Actions(form, request)

    def test_ctor(self):
        request = DummyRequest()
        form = DummyForm()
        inst = self._makeOne(form, request)
        self.assertEqual(inst.form, form)
        self.assertEqual(inst.request, request)

    def test_update(self):
        import djed.form

        request = DummyRequest()
        tform = DummyForm()

        def disabled(form):
            return False

        res = {}
        def action1(form):
            res['action1'] = True
        def action2(form):
            res['action2'] = True

        btn1 = djed.form.Button(name='test1', action=action1)
        btn2 = djed.form.Button(name='test2', action=action2, condition = disabled)
        tform.buttons = djed.form.Buttons(btn1, btn2)

        actions = self._makeOne(tform, request)
        actions.update()

        self.assertEqual(list(actions.keys()), [btn1.name])
        self.assertEqual(actions[btn1.name].name, 'djed.form.buttons.test1')

        actions.execute()
        self.assertEqual(res, {})

        params = {'djed.form.buttons.test1': 'true',
                  'djed.form.buttons.test2': 'true'}
        tform.params = params
        actions.update()
        actions.execute()
        self.assertEqual(res, {'action1': True})


class DummyRequest(object):
    def __init__(self):
        self.params = {}
        self.cookies = {}


class DummyForm(object):
    prefix = 'djed.form.'
    params = {}
    def __init__(self):
        self.buttons = {}
    def form_params(self):
        return self.params
