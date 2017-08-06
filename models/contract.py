from dateutil.relativedelta import relativedelta
import logging

from openerp import api, fields, models
from openerp.addons.decimal_precision import decimal_precision as dp
from openerp.exceptions import ValidationError
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'
    
    journal_document_class_id = fields.Many2one(
        'account.journal.sii_document_class',
        'Documents Type',
        default=_default_journal_document_class_id,
        domain=_domain_journal_document_class_id,
        readonly=True,
        store=True,
        states={'draft': [('readonly', False)]})
    sii_document_class_id = fields.Many2one(
        'sii.document_class',
        related='journal_document_class_id.sii_document_class_id',
        string='Document Type',
        copy=False,
        readonly=True,
        store=True)

    turn_issuer = fields.Many2one(
        'partner.activities',
        'Giro Emisor',
        readonly=True,
        store=True,
        required=False,
        states={'draft': [('readonly', False)]},
        )
    
    
    
    def _default_journal_document_class_id(self, default=None):
        ids = self._get_available_journal_document_class()
        document_classes = self.env['account.journal.sii_document_class'].browse(ids)
        if default:
            for dc in document_classes:
                if dc.sii_document_class_id.id == default:
                    self.journal_document_class_id = dc.id
        elif document_classes:
            default = self.get_document_class_default(document_classes)
        return default


    def _domain_journal_document_class_id(self):
        domain = []
        for rec in self:
            domain = rec._get_available_journal_document_class()
        return [('id', 'in', domain)]
    
    