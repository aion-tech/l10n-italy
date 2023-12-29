{
    'name': "Aion Tech - Invoice - Layout PDF Alternativo",
    'summary': """Aion Tech - Invoice - Layout PDF Alternativo""",
    'author': "Aion Tech",
    'website': "https://aion-tech.it",
    'category': 'Aion Tech',
    'version': '16.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'stock',
        'ait_report_common',
        'account',
        'l10n_it_shipping_invoice',
        'l10n_it_delivery_note_base',
        'account_comment_template',
        'ait_sale_comment_template',
        'product',
        ],
    'data': [
        "reports/report.xml",
        "reports/report_invoice.xml",
        "views/account_move.xml",
    ],
    'assets': {
        'web.report_assets_common': [
            'ait_report_invoice/static/src/css/po.css',
        ],
    }
}
