# Case property-management-test-cases-013: decision at 2025-09-10T10:10:00Z

**Decision:** `request_information`  |  **Risk:** routine  |  **Escalated:** no  |  **Confidence:** high

## What the system received

- Case input: `Property_Management_test_cases/013`, 24 visible event(s), history cut at the end of the supplied history

- Documents read: attachments/glazing-invoice.pdf

## Decision point

An invoice from Clearfirth Glazing has been uploaded with no amount (event-023/024), but there is no record of a visit or completion. The last contractor contact (event-021) said the glass had not arrived. Should the invoice be processed and the case closed, or verified first?

## Situation

The tenant reported a misted double-glazed kitchen pane, water around the frame, a cold kitchen and damp concerns. The landlord approved Clearfirth Glazing on condition the total is £180 inc VAT (event-010). The glass was ordered but delayed (events 018, 021) and no appointment was ever arranged; the tenant wanted to be present (event-014). Staff moved the case to post-visit documents without evidence (event-022). An invoice "Supply and fit 1 pane" was then uploaded with no amount (attachments/glazing-invoice.pdf).

## Actions taken

**DEC-001 - Landlord decision recorded:** approved_with_limit, limit £180.00: Clearfirth Glazing to supply and fit glass to the misted kitchen glazing at 8 Brackenmere Walk, on condition the total is £180 including VAT (£150 + VAT). (evidence event-010)

**MSG-001 - Email to contractor (Sella Vane)** (request_information): *8 Brackenmere Walk – kitchen glazing invoice NBL-013-INV-09: completion details and amount needed*
> Dear Sella,
>
> Thank you for invoice NBL-013-INV-09 dated 10 September 2025 for 8 Brackenmere Walk, Vellumbrook, ZZ1 1ZZ ("Supply and fit 1 pane of glass to the kitchen glazing").
>
> Before we can pass this for payment we need a few details, as our records do not show the visit taking place. When we last spoke on 2 September the glass had not yet arrived and no appointment had been arranged, and the tenant had asked to be present for the visit.
>
> Please could you confirm:
> 1. The date and time the new pane was fitted, and who gave you access to the property.
> 2. That the work is complete, the misting has cleared and the window opens, closes and locks correctly.
> 3. The invoice amount. The copy we hold shows no amount. Please send a corrected invoice showing the net amount, VAT and total. The approved price is £150 plus VAT (£180 including VAT), and we cannot authorise anything above that without first going back to the landlord.
> 4. Anything you noticed about the water gathering around the frame or any damp near the window. If the frame or seals need further attention, please let us know rather than carrying out extra work.
>
> A photo of the fitted pane would also help.
>
> Many thanks,
> Tamsin Rook
> Property Manager, Northbridge Lettings

**MSG-002 - Email to tenant (Elowen Marr)** (request_information): *8 Brackenmere Walk – has the kitchen window glass been replaced?*
> Dear Elowen,
>
> I'm writing with an update on the misted kitchen window at 8 Brackenmere Walk, Vellumbrook, ZZ1 1ZZ.
>
> The glazier has sent us paperwork saying a new pane has been fitted to the kitchen window. However, we have no record of a visit being arranged with you, and we know you wanted to be at home for it. Please could you let us know:
>
> 1. Has the glazier been to the property and replaced the glass? If so, roughly when?
> 2. If they have, has the misting between the panes cleared, and does the window still open, close and lock properly?
> 3. Is water still collecting around the frame, and have you seen any damp or mould near the window or elsewhere in the kitchen? Photos would be really helpful.
>
> If nobody has been yet, please tell us and we will arrange a date with the glazier when you can be at home. We will keep your pets in mind when we do.
>
> Thank you, and sorry for the wait on this repair.
>
> Kind regards,
> Tamsin Rook
> Property Manager, Northbridge Lettings

**ITEM-001 - Open item open**: Invoice NBL-013-INV-09 (Clearfirth Glazing, 10 Sep 2025) shows no amount and completion is unverified: there is no appointment, visit report or tenant confirmation. Do not pass it for payment or forward it to the landlord until the amount (≤ £180 inc VAT per DEC-001) and completion are confirmed.

**ITEM-002 - Open item open**: The wider concern about water around the frame, a cold kitchen and damp (event-001) has never been assessed (event-005). Confirm with the tenant after the glazing is done whether it is resolved, and raise with the landlord if not.

**NOTE-001 - Internal note** (data_quality): Invoice NBL-013-INV-09 (attachments/glazing-invoice.pdf, uploaded at event-023) shows "Amount: —", so there is no amount. There is no evidence the work was done: the last contractor contact (event-021, 2 Sep) said the glass had not arrived and no appointment was set. The tenant wanted to be present (event-014), and the event-022 status change to "awaiting post-visit documents" had no basis. Landlord approval was recorded from event-010 (conditional on a total of £180 inc VAT). The event-011 confirmation request got no visible reply, but the condition matches the quote (£150 + VAT). The invoice is held and not processed. Completion and amount have been requested from the contractor (MSG-001) and the tenant (MSG-002). The landlord will be updated once the facts are verified.

**HOLD-001 - Case put on hold** (waiting_for_contractor): waiting for Contractor: fitting date, completion confirmation and corrected invoice with amount and VAT. Tenant: confirmation of whether the glass was fitted and the current state of misting, water around the frame and damp.. Follow up 2025-09-12T10:00:00Z; if nothing arrives: Phone Sella Vane (Clearfirth Glazing) and Elowen Marr. If the work is unconfirmed, keep the invoice on hold and arrange a fitting date with the tenant present. If the invoice is above £180 inc VAT, go back to the landlord. If the records conflict, escalate to a human.

## Escalation

Not escalated.

## What failed

- none

## Next step

**agency**: Review the contractor's and tenant's replies. If completion is confirmed and the invoice is ≤ £180 inc VAT, record it and forward it to the landlord. Otherwise arrange fitting with the tenant present, or go back to the landlord or escalate. Phone both if there is no reply. (by 2025-09-12T10:00:00Z)

## Final result

`request_information`: An invoice cannot be processed without an amount, and completion has not been shown. Nothing confirms the glass arrived or that a visit took place, and the tenant, who wanted to be present, has not confirmed. So I recorded the landlord's conditional approval (DEC-001, cap £180 inc VAT, event-010) as the reference. I asked the contractor for the fitting date, access details, completion confirmation and a corrected invoice with net, VAT and total (MSG-001). I asked the tenant to confirm whether the work was done and how the misting, water around the frame and damp are now (MSG-002). The invoice and the unassessed damp concern are tracked as open items, with a hold to follow up on 12 Sep. The landlord gets no update until the facts are verified, to avoid forwarding an unverified, unpriced invoice.
