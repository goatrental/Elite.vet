from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class VetShift(models.Model):
    """Jeden radek rozpisu: jeden den, jedna lekarka, jedna smena."""

    _name = "elite.vet.shift"
    _description = "Směna v rozpisu"
    _order = "date, type_id"

    date = fields.Date(
        string="Datum",
        required=True,
        index=True,
        default=fields.Date.context_today,
    )
    doctor_id = fields.Many2one(
        "elite.vet.doctor",
        string="Lékařka",
        ondelete="restrict",
    )
    type_id = fields.Many2one(
        "elite.vet.shift.type",
        string="Směna",
        required=True,
        ondelete="restrict",
        default=lambda self: self.env["elite.vet.shift.type"].search(
            [("is_closed", "=", False)], limit=1
        ),
    )
    is_closed = fields.Boolean(related="type_id.is_closed")
    note = fields.Char(
        string="Poznámka",
        help="Vyplňte jen u zavřeno, například: Státní svátek. Zobrazí se na webu.",
    )

    @api.depends("date", "doctor_id", "type_id")
    def _compute_display_name(self):
        for shift in self:
            if shift.type_id.is_closed:
                shift.display_name = shift.note or shift.type_id.name
            else:
                shift.display_name = "%s — %s" % (
                    shift.doctor_id.name or _("Nezadáno"),
                    shift.type_id.name or "",
                )

    @api.constrains("doctor_id", "type_id")
    def _check_doctor(self):
        for shift in self:
            if not shift.type_id.is_closed and not shift.doctor_id:
                raise ValidationError(
                    _("U směny vyberte lékařku. Bez lékařky lze uložit jen zavřeno.")
                )
