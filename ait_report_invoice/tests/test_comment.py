from odoo.tests import tagged, TransactionCase
from odoo.exceptions import UserError

@tagged('-at_install', 'post_install')
class TestBaseComment(TransactionCase):
    def setUp(self):
        super(TestBaseComment, self).setUp()
        self.invoice_line_comment = self.env['base.comment.template'].create({
            'name': 'Test line comment account.move',
            'text': 'Test line comment account.move',
            'position': 'line',
            'model_selection': 'account.move',
            'models': 'account.move',
        })

    def test_onchange_model_selection(self):
        self.invoice_line_comment.model_selection = 'account.move'
        self.invoice_line_comment._onchange_model_selection()
        self.assertEqual(self.invoice_line_comment.position, 'before_lines')
        self.assertEqual(self.invoice_line_comment.sale_order_template, False)
        self.assertEqual(self.invoice_line_comment.models, 'account.move')


    def test_create(self):
        """Test that an error is raised when trying to create a comment with empty text field"""
        with self.assertRaises(UserError):
            self.env['base.comment.template'].create({
            'name': 'Test comment',
            'text': '<p> </p>',
            'position': 'before_lines',
            'model_selection': 'account.move',
            'models': 'account.move',
        })

    def test_write(self):
        with self.assertRaises(UserError):
            self.invoice_line_comment.write({'text': '<p> </p>'})

    def test_compute_comment_template_ids(self):
        """Test that the default templates are correctly computed"""
        self.invoice_line_comment.default_on_document = True
        order = self.env['account.move'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,
        })
        self.assertIn(self.invoice_line_comment.id, order.comment_template_ids.ids)