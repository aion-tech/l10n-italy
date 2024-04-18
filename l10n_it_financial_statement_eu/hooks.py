#  Copyright 2023 MKT SRL
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, api


def _l10n_it_financial_statement_eu_post_init(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    fse = env["financial.statement.eu"]
    fse.financial_statement_eu_account_assoc_code("1101%", "PA.B11a", False)
    fse.financial_statement_eu_account_assoc_code("1106%", "PA.B13a", False)
    fse.financial_statement_eu_account_assoc_code("1108%", "PA.B15a", False)
    fse.financial_statement_eu_account_assoc_code("1111%", "PA.B11b", False)
    fse.financial_statement_eu_account_assoc_code("1116%", "PA.B13b", False)
    fse.financial_statement_eu_account_assoc_code("1118%", "PA.B15b", False)
    fse.financial_statement_eu_account_assoc_code("1201%", "PA.B21a", False)
    fse.financial_statement_eu_account_assoc_code("1202%", "PA.B22a", False)
    fse.financial_statement_eu_account_assoc_code("1204%", "PA.B23a", False)
    fse.financial_statement_eu_account_assoc_code("1205%", "PA.B24a", False)
    fse.financial_statement_eu_account_assoc_code("1206%", "PA.B24a", False)
    fse.financial_statement_eu_account_assoc_code("1207%", "PA.B24a", False)
    fse.financial_statement_eu_account_assoc_code("1208%", "PA.B24a", False)
    fse.financial_statement_eu_account_assoc_code("1211%", "PA.B21b", False)
    fse.financial_statement_eu_account_assoc_code("1212%", "PA.B22b", False)
    fse.financial_statement_eu_account_assoc_code("1214%", "PA.B23b", False)
    fse.financial_statement_eu_account_assoc_code("1215%", "PA.B24b", False)
    fse.financial_statement_eu_account_assoc_code("1216%", "PA.B24b", False)
    fse.financial_statement_eu_account_assoc_code("1217%", "PA.B24b", False)
    fse.financial_statement_eu_account_assoc_code("1218%", "PA.B24b", False)
    fse.financial_statement_eu_account_assoc_code("1220%", "PA.B25", False)
    fse.financial_statement_eu_account_assoc_code("130100", "PA.B32d1", False)
    fse.financial_statement_eu_account_assoc_code("1302%", "PA.B31d", False)
    fse.financial_statement_eu_account_assoc_code("1401%", "PA.C11", False)
    fse.financial_statement_eu_account_assoc_code("1404%", "PA.C11", False)
    fse.financial_statement_eu_account_assoc_code("1410%", "PA.C25a", False)
    fse.financial_statement_eu_account_assoc_code("1501%", "PA.C21a", False)
    fse.financial_statement_eu_account_assoc_code("1502%", "PA.C21a", False)
    fse.financial_statement_eu_account_assoc_code("1503%", "PA.C21a", False)
    fse.financial_statement_eu_account_assoc_code("1505%", "PA.C21a", False)
    fse.financial_statement_eu_account_assoc_code("1506%", "PA.C21a", False)
    fse.financial_statement_eu_account_assoc_code("1507%", "PA.C21a", False)
    fse.financial_statement_eu_account_assoc_code("1508%", "PA.C21a", False)
    fse.financial_statement_eu_account_assoc_code("1509%", "PA.C21a", False)
    fse.financial_statement_eu_account_assoc_code("1510%", "PA.C21a", False)
    fse.financial_statement_eu_account_assoc_code("1511%", "PA.C21a", False)
    fse.financial_statement_eu_account_assoc_code("1531%", "PA.C25a", False)
    fse.financial_statement_eu_account_assoc_code("1540%", "PA.C25a", False)
    fse.financial_statement_eu_account_assoc_code("1541%", "PA.C25a", False)
    fse.financial_statement_eu_account_assoc_code("1601%", "PA.C2Ba", False)
    fse.financial_statement_eu_account_assoc_code("1602%", "PA.C2Ba", False)
    fse.financial_statement_eu_account_assoc_code("1605%", "PA.C2Ba", False)
    fse.financial_statement_eu_account_assoc_code("1607%", "PA.C2T", False)
    fse.financial_statement_eu_account_assoc_code("1608%", "PA.C2Ba", False)
    fse.financial_statement_eu_account_assoc_code("1609%", "PA.C2Ba", False)
    fse.financial_statement_eu_account_assoc_code("1610%", "PA.C2Ba", False)
    fse.financial_statement_eu_account_assoc_code("1620%", "PA.C25a", False)
    fse.financial_statement_eu_account_assoc_code("1630%", "PA.C25a", False)
    fse.financial_statement_eu_account_assoc_code("1640%", "PA.C25a", False)
    #  accounts 1701% not present in the basic chart of accounts
    fse.financial_statement_eu_account_assoc_code("1701%", "PA.C36", False)
    fse.financial_statement_eu_account_assoc_code("1800%", "PA.C43", False)
    fse.financial_statement_eu_account_assoc_code("182%", "PA.C41", "PP.D3a")
    fse.financial_statement_eu_account_assoc_code("183001", "PP.D3a", False)
    fse.financial_statement_eu_account_assoc_code("1901%", "PA.D", "PP.E")
    fse.financial_statement_eu_account_assoc_code("1902%", "PA.D", "PP.E")
    fse.financial_statement_eu_account_assoc_code("210100", "PP.A1", False)
    #  other no standard 2101% may need to be associated with other codes
    fse.financial_statement_eu_account_assoc_code("2102%", "PP=A9", False)
    fse.financial_statement_eu_account_assoc_code("2103%", "PP=A9", False)
    fse.financial_statement_eu_account_assoc_code("2104%", "PP.B2", False)
    fse.financial_statement_eu_account_assoc_code("2105%", "PP.B2", False)
    fse.financial_statement_eu_account_assoc_code("2201%", "PP.B2", False)
    fse.financial_statement_eu_account_assoc_code("2204%", "PP.B2", False)
    fse.financial_statement_eu_account_assoc_code("2205%", "PP.B3", False)
    fse.financial_statement_eu_account_assoc_code("2211%", "PP.B3", False)
    fse.financial_statement_eu_account_assoc_code("2301%", "PP.C", False)
    fse.financial_statement_eu_account_assoc_code("2410%", "PP.D3a", False)
    fse.financial_statement_eu_account_assoc_code("2411%", "PP.D3a", False)
    fse.financial_statement_eu_account_assoc_code("2420%", "PP.D3a", False)
    fse.financial_statement_eu_account_assoc_code("2421%", "PP.D3a", False)
    fse.financial_statement_eu_account_assoc_code("2422%", "PP.D3a", False)
    fse.financial_statement_eu_account_assoc_code("2423%", "PP.D3a", False)
    fse.financial_statement_eu_account_assoc_code("2440%", "PP.D3a", False)
    fse.financial_statement_eu_account_assoc_code("2501%", "PP.D6a", False)
    fse.financial_statement_eu_account_assoc_code("2503%", "PP.D6a", False)
    fse.financial_statement_eu_account_assoc_code("2520%", "PP.D6a", False)
    fse.financial_statement_eu_account_assoc_code("2521%", "PP.D6a", False)
    fse.financial_statement_eu_account_assoc_code("2530%", "PP.D6a", False)
    fse.financial_statement_eu_account_assoc_code("2601%", "PP.DBa", False)
    fse.financial_statement_eu_account_assoc_code("2602%", "PP.DBa", False)
    fse.financial_statement_eu_account_assoc_code("2605%", "PP.DBa", False)
    fse.financial_statement_eu_account_assoc_code("2606%", "PA.C2Ba", "PP.DBa")
    fse.financial_statement_eu_account_assoc_code("2619%", "PP.DBa", False)
    fse.financial_statement_eu_account_assoc_code("2620%", "PP.DDa", False)
    fse.financial_statement_eu_account_assoc_code("2621%", "PP.DDa", False)
    fse.financial_statement_eu_account_assoc_code("2622%", "PP.DDa", False)
    fse.financial_statement_eu_account_assoc_code("2630%", "PP.DCa", False)
    fse.financial_statement_eu_account_assoc_code("2640%", "PP.DDa", False)
    fse.financial_statement_eu_account_assoc_code("2701%", "PP.E", False)
    fse.financial_statement_eu_account_assoc_code("2702%", "PP.E", False)
    fse.financial_statement_eu_account_assoc_code("2810%", "PP.DBa", False)
    fse.financial_statement_eu_account_assoc_code("2811%", "PP.DBa", False)
    fse.financial_statement_eu_account_assoc_code("2901%", "PP.DDa", False)
    fse.financial_statement_eu_account_assoc_code("2902%", "PP.DDa", False)
    fse.financial_statement_eu_account_assoc_code("2911%", "PP.DDa", False)
    fse.financial_statement_eu_account_assoc_code("2912%", "PP.DDa", False)
    fse.financial_statement_eu_account_assoc_code("2913%", "PP.DDa", False)
    fse.financial_statement_eu_account_assoc_code("2914%", "PP.DDa", False)
    fse.financial_statement_eu_account_assoc_code("2916%", "PP.DDa", False)
    fse.financial_statement_eu_account_assoc_code("2917%", "PP.DDa", False)
    fse.financial_statement_eu_account_assoc_code("2921%", "PP.DDa", False)
    fse.financial_statement_eu_account_assoc_code("2922%", "PP.DDa", False)
    fse.financial_statement_eu_account_assoc_code("2926%", "PP.DDa", False)
    fse.financial_statement_eu_account_assoc_code("2927%", "PP.DDa", False)
    fse.financial_statement_eu_account_assoc_code("2931%", "PP.DDa", False)
    fse.financial_statement_eu_account_assoc_code("2932%", "PP.DDa", False)
    fse.financial_statement_eu_account_assoc_code("3101%", "E.A1", False)
    fse.financial_statement_eu_account_assoc_code("3103%", "E.A511", False)
    fse.financial_statement_eu_account_assoc_code("3110%", "E.A511", False)
    fse.financial_statement_eu_account_assoc_code("3111%", "E.A511", False)
    fse.financial_statement_eu_account_assoc_code("3112%", "E.A511", False)
    fse.financial_statement_eu_account_assoc_code("3201%", "E.A511", False)
    fse.financial_statement_eu_account_assoc_code("3202%", "E.A511", False)
    fse.financial_statement_eu_account_assoc_code("3210%", "E.A511", False)
    fse.financial_statement_eu_account_assoc_code("3220%", "E.A511", False)
    fse.financial_statement_eu_account_assoc_code("3230%", "E.A511", False)
    fse.financial_statement_eu_account_assoc_code("3240%", "E.A511", False)
    fse.financial_statement_eu_account_assoc_code("4101%", "E.B1", False)
    fse.financial_statement_eu_account_assoc_code("4102%", "E.B1", False)
    fse.financial_statement_eu_account_assoc_code("4105%", "E.B1", False)
    fse.financial_statement_eu_account_assoc_code("4110%", "E.B2", False)
    fse.financial_statement_eu_account_assoc_code("4111%", "E.B2", False)
    fse.financial_statement_eu_account_assoc_code("4112%", "E.B2", False)
    fse.financial_statement_eu_account_assoc_code("4121%", "E.B6", False)
    fse.financial_statement_eu_account_assoc_code("4122%", "E.B6", False)
    fse.financial_statement_eu_account_assoc_code("4131%", "E.A2", False)
    fse.financial_statement_eu_account_assoc_code("4132%", "E.A2", False)
    fse.financial_statement_eu_account_assoc_code("4201%", "E.B2", False)
    fse.financial_statement_eu_account_assoc_code("4202%", "E.B2", False)
    fse.financial_statement_eu_account_assoc_code("4203%", "E.B2", False)
    fse.financial_statement_eu_account_assoc_code("4204%", "E.B2", False)
    fse.financial_statement_eu_account_assoc_code("4205%", "E.B2", False)
    fse.financial_statement_eu_account_assoc_code("4206%", "E.B2", False)
    fse.financial_statement_eu_account_assoc_code("4207%", "E.B2", False)
    fse.financial_statement_eu_account_assoc_code("4208%", "E.B2", False)
    fse.financial_statement_eu_account_assoc_code("4209%", "E.B2", False)
    fse.financial_statement_eu_account_assoc_code("4210%", "E.B2", False)
    fse.financial_statement_eu_account_assoc_code("4211%", "E.B2", False)
    fse.financial_statement_eu_account_assoc_code("4212%", "E.B2", False)
    fse.financial_statement_eu_account_assoc_code("4213%", "E.B2", False)
    fse.financial_statement_eu_account_assoc_code("4301%", "E.B3", False)
    fse.financial_statement_eu_account_assoc_code("4302%", "E.B3", False)
    fse.financial_statement_eu_account_assoc_code("4401%", "E.B41", False)
    fse.financial_statement_eu_account_assoc_code("4402%", "E.B42", False)
    fse.financial_statement_eu_account_assoc_code("4403%", "E.B43", False)
    fse.financial_statement_eu_account_assoc_code("4404%", "E.B45", False)
    fse.financial_statement_eu_account_assoc_code("4501%", "E.B51", False)
    fse.financial_statement_eu_account_assoc_code("4506%", "E.B51", False)
    fse.financial_statement_eu_account_assoc_code("4508%", "E.B51", False)
    fse.financial_statement_eu_account_assoc_code("4601%", "E.B52", False)
    fse.financial_statement_eu_account_assoc_code("4602%", "E.B52", False)
    fse.financial_statement_eu_account_assoc_code("4604%", "E.B52", False)
    fse.financial_statement_eu_account_assoc_code("4605%", "E.B52", False)
    fse.financial_statement_eu_account_assoc_code("4606%", "E.B52", False)
    fse.financial_statement_eu_account_assoc_code("4607%", "E.B52", False)
    fse.financial_statement_eu_account_assoc_code("4608%", "E.B52", False)
    fse.financial_statement_eu_account_assoc_code("4701%", "E.B9", False)
    fse.financial_statement_eu_account_assoc_code("4702%", "E.B9", False)
    fse.financial_statement_eu_account_assoc_code("4706%", "E.B9", False)
    fse.financial_statement_eu_account_assoc_code("4814%", "E.B7", False)
    fse.financial_statement_eu_account_assoc_code("4821%", "E.B7", False)
    fse.financial_statement_eu_account_assoc_code("4823%", "E.B8", False)
    fse.financial_statement_eu_account_assoc_code("4901%", "E.B9", False)
    fse.financial_statement_eu_account_assoc_code("4903%", "E.B9", False)
    fse.financial_statement_eu_account_assoc_code("4905%", "E.B9", False)
    fse.financial_statement_eu_account_assoc_code("4910%", "E.B9", False)
    fse.financial_statement_eu_account_assoc_code("4920%", "E.B9", False)
    fse.financial_statement_eu_account_assoc_code("4930%", "E.B9", False)
    fse.financial_statement_eu_account_assoc_code("4940%", "E.B9", False)
    fse.financial_statement_eu_account_assoc_code("5110%", "E.C244", False)
    fse.financial_statement_eu_account_assoc_code("5115%", "E.C244", False)
    fse.financial_statement_eu_account_assoc_code("5116%", "E.C215", False)
    fse.financial_statement_eu_account_assoc_code("5140%", "E.C23", False)
    fse.financial_statement_eu_account_assoc_code("5201%", "E.C35", False)
    fse.financial_statement_eu_account_assoc_code("5202%", "E.C35", False)
    fse.financial_statement_eu_account_assoc_code("5203%", "E.C35", False)
    fse.financial_statement_eu_account_assoc_code("5210%", "E.C35", False)
    fse.financial_statement_eu_account_assoc_code("5240%", "E.C35", False)
    fse.financial_statement_eu_account_assoc_code("7101%", "E.A511", False)
    fse.financial_statement_eu_account_assoc_code("7102%", "E.A511", False)
    fse.financial_statement_eu_account_assoc_code("7103%", "E.A511", False)
    fse.financial_statement_eu_account_assoc_code("7201%", "E.D23", False)
    fse.financial_statement_eu_account_assoc_code("7202%", "E.B9", False)
    fse.financial_statement_eu_account_assoc_code("7203%", "E.B9", False)
    fse.financial_statement_eu_account_assoc_code("7204%", "E.F5", False)
    fse.financial_statement_eu_account_assoc_code("8101%", "E_F1", False)
