# Case property-management-test-cases-009: decision at 2025-09-10T18:20:00Z

**Decision:** `request_information`  |  **Risk:** routine  |  **Escalated:** no  |  **Confidence:** high

## What the system received

- Case input: `Property_Management_test_cases/009`, 20 visible event(s), history cut at the end of the supplied history

- Documents read: attachments/forwarded-document.pdf

## Decision point

Tenant reports "All jobs was done" by landlord's contractor Richard (report promised, not received); landlord forwarded a gas safety record with no message that turns out to be for a different property.

## Situation

Landlord Dorian Pike chose to handle the bedroom window repair himself (inspection, then his own contractor Richard, parts ordered per event-018). Tenant now says work is done (event-020), but has not specifically confirmed the window seals, and no contractor report has arrived. Landlord's forwarded LGSR (event-019, forwarded-document.pdf) is for 8 Thistledown Mews, Vellumby, not 24 Bramblewick Lane.

## Actions taken

**DEC-001 - Landlord decision recorded:** landlord_arranging_own_contractor: Bedroom window not closing/sealing at 24 Bramblewick Lane: landlord inspected personally and arranged his own contractor (Richard) for the repair. Agency not instructing a contractor or incurring cost. (evidence event-014)

**NOTE-001 - Internal note** (data_quality): Event-019: landlord forwarded a Landlord Gas Safety Record (attachments/forwarded-document.pdf, ref NBL-009-GSR-25, engineer Rellan Voss, inspection 8 Sept 2025, outcome satisfactory) but the record is for 8 Thistledown Mews, Vellumby – NOT 24 Bramblewick Lane. Do not file it as this property's gas safety record. Asked landlord to clarify and supply the correct record for 24 Bramblewick Lane if the property has gas appliances. Also note event-011 EICR forward – property/content not verified in this file. Event-020: tenant says "All jobs was done" via landlord's contractor Richard (no surname/company known); no contractor report received yet and tenant has not specifically confirmed the bedroom window now closes and seals. Not closing until window confirmed and report received.

**MSG-001 - Email to tenant (Elena Voss)** (request_information): *Bedroom window – 24 Bramblewick Lane: thank you, quick confirmation please*
> Dear Elena,
>
> Thank you for letting us know that the work has been done at 24 Bramblewick Lane, and for explaining that Richard said he would send a report – that's no problem at all.
>
> So that we can close the repair properly, could you please confirm:
> 1. The bedroom window now closes fully and seals, with no gap or draught, and the handle locks it shut.
> 2. Whether anything else was left outstanding or needs a return visit (for example, if any part is still on order).
>
> If you are able to send a quick photo of the window closed, that would be helpful but is not essential.
>
> We have not yet received Richard's report, so we are also asking Mr Pike for it. Once we have your confirmation and the report, we will close the request. If the window is still not sealing properly, just tell us and we will take it up with the landlord straight away.
>
> Kind regards,
> Maya Chen
> Property Manager, Northbridge Lettings

**MSG-002 - Email to landlord (Dorian Pike)** (request_information): *24 Bramblewick Lane – bedroom window completion, and gas safety record query*
> Dear Mr Pike,
>
> Bedroom window: Elena Voss has told us this evening that the work at 24 Bramblewick Lane has been completed by your contractor, Richard, and that he said he would send a report. Could you please forward Richard's report (or a brief note of what was done and whether any parts are still outstanding) so we can update the property file? We have also asked the tenant to confirm the window now closes and seals properly. As you arranged this work directly, we understand any invoice is being handled between you and Richard – please let us know if that is not the case.
>
> Gas safety record: thank you for forwarding the Landlord Gas Safety Record this morning. However, the record you sent (reference NBL-009-GSR-25, inspection date 8 September 2025) is for 8 Thistledown Mews, Vellumby, not 24 Bramblewick Lane. We have not filed it against this property. Could you please check whether it was sent in error and, if 24 Bramblewick Lane has gas appliances, send us the current gas safety record for this address?
>
> Kind regards,
> Maya Chen
> Property Manager, Northbridge Lettings

**ITEM-001 - Open item open**: Gas safety record forwarded by landlord (event-019, forwarded-document.pdf) relates to 8 Thistledown Mews, not 24 Bramblewick Lane. Need landlord to confirm and supply correct LGSR for this property if gas appliances present.

**ITEM-002 - Open item open**: Completion of bedroom window repair: need tenant confirmation that window closes/seals and the landlord's contractor (Richard) report.

**HOLD-001 - Case put on hold** (waiting_for_landlord): waiting for Tenant confirmation that the bedroom window now closes and seals; landlord to forward contractor Richard's report and clarify/supply the correct gas safety record for 24 Bramblewick Lane.. Follow up 2025-09-15T10:00:00Z; if nothing arrives: Chase landlord by phone (he prefers calls) and tenant by SMS/email nudge; if the tenant confirms the window is fixed but no report arrives, consider closing the window repair with the tenant's confirmation while keeping the gas record query open/escalating to a human for compliance follow-up.

## Escalation

Not escalated.

## What failed

- none

## Next step

**agency**: Review tenant confirmation and contractor report; chase landlord by phone and tenant by SMS if no reply; close window repair once confirmed; keep gas record query open until resolved. (by 2025-09-15T10:00:00Z)

## Final result

`request_information`: The tenant's message is ambiguous ("all jobs") and the promised contractor report is outstanding, so closing now would be premature. Asked tenant to confirm the window closes/seals and nothing remains outstanding; asked landlord for Richard's report and flagged that the gas safety record he sent relates to another address, requesting the correct record for this property if applicable. Recorded the landlord-own-contractor route (event-014) so no agency contractor/spend is involved. Opened items for completion and the gas record mismatch, and set a hold to follow up on 15 Sept.
