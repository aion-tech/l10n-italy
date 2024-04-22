{
    "name": "AIT - Cashflow Forecast - Purchase",
    "version": "16.0.1.0.0",
    "category": "Accounting",
    "summary": "AIT - Cashflow Forecast - Purchase",
    "author": "Aion Tech",
    "license": "LGPL-3",
    "depends": [
        "ait_cashflow_forecast",
        "purchase",
    ],
    "data": [
        "data/cashflow_config.xml",
        "views/purchase_order_views.xml",
    ],
    "post_init_hook": "post_init_hook",
}
