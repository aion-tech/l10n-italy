import json

from odoo import api, fields, models


class FatturapaAttachment(models.AbstractModel):
    _name = "fatturapa.attachment.mixin"

    def _post_bluenext_msg(self, msg):
        try:
            msg_body = json.dumps(msg, indent=4)
        except Exception:
            msg_body = msg
        style = "word-wrap: break-word; white-space: pre-wrap;"
        self.message_post(body=f"<pre style='{style}'>{ msg_body }</pre>")
