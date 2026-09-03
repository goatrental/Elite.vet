from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

# Pevne casy jednotlivych smen. Zamerne nejsou editovatelna pole formulare:
# klinika ma pevne smeny a kazde pole navic je jedno pole, kde se da udelat
# chyba. Stejny rozpad casu pouziva i sablona verejne stranky.
SHIFT_HOURS = {
    "am": "8:00–14:00",
    "pm": "14:00–20:00",
    "night": "20:00–8:00",
    "we": "10:00–18:00",
}


class VetShift(models.Model):
    """Jeden radek rozpisu: jeden den, jedna lekarka, jedna smena."""

    _name = "elite.vet.shift"
    _description = "Směna v rozpisu"
    _order = "date, shift_type"

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
    shift_type = fields.Selection(
        [
            ("am", "Ranní"),
            ("pm", "Odpolední"),
            ("night", "Noční"),
            ("we", "Víkendová"),
            ("closed", "Zavřeno"),
        ],
        string="Směna",
        required=True,
        default="am",
    )
    note = fields.Char(
        string="Poznámka",
        help="Vyplňte jen u zavřeno, například: Státní svátek. Zobrazí se na webu.",
    )

    @api.depends("date", "doctor_id", "shift_type")
    def _compute_display_name(self):
        labels = dict(self._fields["shift_type"].selection)
        for shift in self:
            if shift.shift_type == "closed":
                shift.display_name = shift.note or labels["closed"]
            else:
                shift.display_name = "%s — %s" % (
                    shift.doctor_id.name or _("Nezadáno"),
                    labels.get(shift.shift_type, ""),
                )

    @api.constrains("doctor_id", "shift_type")
    def _check_doctor(self):
        for shift in self:
            if shift.shift_type != "closed" and not shift.doctor_id:
                raise ValidationError(
                    _("U směny vyberte lékařku. Bez lékařky lze uložit jen „Zavřeno“.")
                )
