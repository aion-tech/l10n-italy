from odoo.tests import tagged, TransactionCase
from odoo.exceptions import UserError

@tagged('-at_install', 'post_install')
class TestBaseComment(TransactionCase):
    def setUp(self):
        super(TestBaseComment, self).setUp()
        self.base_comment_template = self.env['base.comment.template'].create({
            'name': 'Test comment',
            'text': 'Test comment',
            'position': 'line',
            'model_selection': 'sale.order',
            'models': 'sale.order',
        })
    def test_check_line_comment_for_account_move(self):
        """Test that an error is raised when trying to create a line comment for account.move"""
        with self.assertRaises(UserError):
            self.base_comment_template.model_selection = 'account.move'
            self.base_comment_template.models = 'account.move'
            self.base_comment_template.check_line_comment_for_account_move()

    def test_onchange_model_selection(self):
        self.base_comment_template.model_selection = 'account.move'
        self.base_comment_template._onchange_model_selection()
        self.assertEqual(self.base_comment_template.position, 'before_lines')
        self.assertEqual(self.base_comment_template.sale_order_template, False)
        self.assertEqual(self.base_comment_template.models, 'account.move')

        self.base_comment_template.model_selection = 'sale.order'
        self.base_comment_template._onchange_model_selection()
        self.assertEqual(self.base_comment_template.sale_order_template, 'all')
        self.assertEqual(self.base_comment_template.models, 'sale.order')

    def test_create(self):
        """Test that an error is raised when trying to create a comment with empty text field"""
        with self.assertRaises(UserError):
            self.env['base.comment.template'].create({
            'name': 'Test comment',
            'text': '<p> </p>',
            'position': 'before_lines',
            'model_selection': 'sale.order',
            'models': 'sale.order',
        })

    def test_write(self):
        with self.assertRaises(UserError):
            self.base_comment_template.write({'text': '<p> </p>'})

    def test_compute_comment_template_ids(self):
        """Test that the default templates are correctly computed"""
        self.base_comment_template.default_on_document = True
        order = self.env['sale.order'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,
        })
        self.assertIn(self.base_comment_template.id, order.comment_template_ids.ids)