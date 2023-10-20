odoo.define("odoo_bluenext.FatturapaAttachmentInTreeView", function(require) {
    "use strict";

    var core = require("web.core");
    var ListController = require("web.ListController");
    var ListView = require("web.ListView");
    var _t = core._t;
    var QWeb = core.qweb;
    var viewRegistry = require("web.view_registry");

    var FatturapaAttachmentInTreeController = ListController.extend({
        renderButtons: function() {
            this._super.apply(this, arguments);
            var self = this;
            this.$buttons.append($(QWeb.render("odoo_bluenext.import.button", this)));
            this.$buttons.on("click", ".bluenext_import_button", function() {
                self._rpc({
                    model: "fatturapa.attachment.in",
                    method: "bluenext_download_invoices_btn",
                }).then(function(res) {
                    self.reload();
                    self.displayNotification({
                        title: _t("Bluenext e-bills"),
                        message: _t(`Downloaded ${res} invoices`),
                        type: "info"
                    });
                });
            });
        },
    });

    var FatturapaAttachmentInTreeView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: FatturapaAttachmentInTreeController,
        }),
    });
    viewRegistry.add("bluenext_fattura_pa_attachment_in_list", FatturapaAttachmentInTreeView);

});
