{
    'name': "Aion Tech - Invoice - Layout PDF Alternativo",
    'summary': """Aion Tech - Invoice - Layout PDF Alternativo""",
    'author': "Aion Tech",
    'website': "https://aion-tech.it",
    'category': 'Aion Tech',
    'version': '16.0.1.0.2',
    'license': 'AGPL-3',
    'depends': [
        'stock',
        'product',
        'base',
        'account',
        'l10n_it_shipping_invoice',
        'l10n_it_delivery_note_base',
        'base_comment_template',
        'ait_report_common',
        'account_comment_template',
        ],
    'data': [
        "reports/report.xml",
        "reports/report_invoice.xml",
        "views/account_move.xml",
        "views/res_config_settings.xml",
        "views/comment.xml",
    ],
    'assets': {
        'web.report_assets_common': [
            'ait_report_invoice/static/src/css/po.css',
        ],
    },
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
}
