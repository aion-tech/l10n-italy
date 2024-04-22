{
    "name": "AIT - Cashflow Forecast - Sale",
    "version": "16.0.1.0.0",
    "category": "Accounting",
    "summary": "AIT - Cashflow Forecast - Sale",
    "author": "Aion Tech",
    "license": "LGPL-3",
    "depends": [
        "ait_cashflow_forecast",
        "sale",
    ],
    "data": [
        "data/cashflow_config.xml",
        "views/sale_order_views.xml",
    ],
    "post_init_hook": "post_init_hook",
}
