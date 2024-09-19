from .test_cases import ComponentTransactionCase


class TestPartnerBankListener(ComponentTransactionCase):
    def test_create_mandate_in_partner_bank_creation(self):
        partner = self.browse_ref("mandate_partner_bank_creation.res_partner_1_demo")
        previous_mandate_count = partner.mandate_count

        self.env["res.partner.bank"].create(
            {"acc_number": "ES1000492352082414205416", "partner_id": partner.id}
        )
        partner._compute_mandate_count()

        self.assertEqual(partner.mandate_count, previous_mandate_count+1)

    def test_not_create_mandate_in_partner_bank_creation_if_partner_is_not_customer(self):  # noqa
        partner = self.browse_ref("base.res_partner_4")
        previous_mandate_count = partner.mandate_count
        self.env["res.partner.bank"].create(
            {"acc_number": "ES1000492352082414205416", "partner_id": partner.id}
        )
        partner._compute_mandate_count()

        self.assertEqual(partner.mandate_count, previous_mandate_count)

