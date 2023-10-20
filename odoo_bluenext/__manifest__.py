{
    "name": "odoo_bluenext",
    "summary": "",
    "description": "",
    "author": "Aion Tech Srl",
    "website": "https://aion-tech.it/",
    # https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    "category": "Uncategorized",
    "version": "16.0.1.0.0",
    "depends": [
        "base",
        "l10n_it_fatturapa",
        "l10n_it_fatturapa_in",
        "l10n_it_fatturapa_out",
    ],
    "installable": True,
    "application": False,
    "data": [
        "security/ir.model.access.csv",
        "data/bluenext_state_map.xml",
        "data/cron_data.xml",
        "views/res_config_settings_view.xml",
        "views/fatturapa_attachment_out_views.xml",
        "views/fatturapa_attachment_in_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "odoo_bluenext/static/src/xml/**/*",
            "odoo_bluenext/static/src/js/**/*",
        ],
    },
}
