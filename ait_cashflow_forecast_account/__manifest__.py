{
    "name": "AIT - Cashflow Forecast - Account",
    "version": "16.0.1.0.0",
    "category": "Accounting",
    "summary": "AIT - Cashflow Forecast - Account",
    "author": "Aion Tech",
    "license": "LGPL-3",
    "depends": [
        "ait_cashflow_forecast",
        "account",
    ],
    "data": [
        "data/cashflow_config.xml",
        "views/account_move_views.xml",
    ],
    "post_init_hook": "post_init_hook",
}
