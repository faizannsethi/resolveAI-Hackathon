# Case property-management-test-cases-003: decision at 2025-09-14T09:20:00Z

**Decision:** `request_information`  |  **Risk:** urgent  |  **Escalated:** no  |  **Confidence:** high

## What the system received

- Case input: `Property_Management_test_cases/003`, 23 visible event(s), history cut at the end of the supplied history

- Documents read: attachments/tap-works-invoice.pdf

## Decision point

The contractor's invoice has arrived (event-022) and been filed (event-023). Decide whether to accept or forward it, and what to do about the parts of the job it does not cover.

## Situation

Copper Finch Plumbing attended on 12/09 (event-020). Their invoice NBL-003-INV-14 (attachments/tap-works-invoice.pdf) covers only the taps: a new kitchen mixer tap, and a new brass insert and head on the bathroom hot tap. It shows a different property address (Larkspur Quay, Brindlewick) and has no amounts or VAT. There is no visit report. The rainwater through the bathroom vent and the smaller-bedroom damp were in the referral but are not mentioned. The landlord's event-004 requests (insurance check, roof-leak history) have never been actioned.

## Actions taken

**NOTE-001 - Internal note** (data_quality): Invoice review (attachments/tap-works-invoice.pdf, ref NBL-003-INV-14, dated 14/09/2025, received event-022):
1) Wrong property address: invoice states a different property (Larkspur Quay, Brindlewick) instead of Flat 4, 8-12 Juniper Mews, Vellumford. Contractor also used '8-10 Juniper Mews' on the day (event-020). Must be reissued before forwarding to landlord.
2) No amount, no line prices, no VAT information on the invoice - cannot record a financial figure or forward for payment. Not recorded via record_financial until a priced, corrected invoice arrives.
3) Scope: invoice covers taps only (new kitchen mixer tap supplied/fitted; new brass insert + chrome head on bathroom basin hot tap). Nothing on the bathroom vent rainwater ingress or smaller-bedroom damp, which were in the referral (event-008). No visit report received despite requests (event-010, event-018). Kitchen tap was replaced rather than repaired - within landlord's general 'Yes, please proceed' (event-004, no limit set), but cost unknown.
4) Landlord's event-004 requests (building insurance check; review of flat's history of repeated roof leaks) still not actioned or reported (event-005, event-012).
5) Contractor's conflicting 'job done today' (event-014) was corrected (event-015); attendance confirmed 12/09 (event-020).
Case must not be closed: tap completion unconfirmed by tenant, invoice defective, vent/damp unresolved, landlord questions unanswered.

**MSG-001 - Email to tenant (Elian Voss)** (request_information): *Your repairs at Flat 4, 8-12 Juniper Mews - taps, bathroom vent and bedroom damp*
> Dear Elian,
>
> Thank you for letting the plumber in on Friday 12 September.
>
> Gareth from Copper Finch Plumbing has told us that he fitted a new kitchen mixer tap and replaced the working parts and head of the bathroom basin hot tap. Could you confirm that both taps have stopped dripping and that the bathroom hot tap now turns off easily?
>
> The water coming through the bathroom vent in heavy rain and the damp in the smaller bedroom have not been dealt with yet, and we are following them up. To help us arrange the right next step, please could you tell us:
> - whether the plumber looked at the bathroom vent or the bedroom while he was there, and if so what he said;
> - whether water has come through the vent again since you reported it, and whether the damp patches on the bedroom ceiling and wall have got bigger;
> - whether there is any mould, and roughly how big an area it covers;
> - whether anyone in the flat has asthma or breathing problems or another health condition that damp could affect;
> - if you can, some up-to-date photos of the vent, the bedroom ceiling and the bedroom wall.
>
> In the meantime, please keep the bedroom ventilated where you can. Put a towel or container under the vent when it rains heavily. If water ever comes near a light fitting, switch or socket, do not touch it, turn off the electricity at the consumer unit if you can do so safely, and call us straight away.
>
> We are talking to the landlord about the vent and the damp. We will update you on the next steps by Tuesday 16 September.
>
> Kind regards,
> Priya Nair
> Property Manager, Northbridge Lettings

**MSG-002 - Email to contractor (Gareth Lune)** (request_information): *Invoice NBL-003-INV-14 - correction needed and visit report - Flat 4, 8-12 Juniper Mews, Vellumford*
> Dear Gareth,
>
> Thank you for attending Flat 4, 8-12 Juniper Mews, Vellumford, ZZ1 1ZZ on Friday 12 September and for sending invoice NBL-003-INV-14.
>
> Unfortunately we cannot pass the invoice to the landlord for payment as it stands:
>
> 1. The property address on the invoice is for a different property. Please reissue it showing Flat 4, 8-12 Juniper Mews, Vellumford, ZZ1 1ZZ.
> 2. The invoice shows no amounts. Please itemise labour and parts (the new kitchen mixer tap, and the brass insert and chrome head for the bathroom basin hot tap), and show the total and whether VAT is charged, with your VAT number if it applies.
>
> We also asked for a short visit report, and we still need one. Please confirm:
> - that both taps are now working properly, the drips have stopped and the bathroom hot tap now turns off easily;
> - whether you looked at the rainwater coming through the bathroom vent during heavy rain, and at the damp patches on the ceiling and wall of the smaller bedroom. Both were in our original referral. If you did, please send your findings and any photos, and tell us whether you think the cause is the roof, the vent ducting or cowl, or something else. If you think this is outside plumbing work or needs a roofer, please tell us that.
>
> Please do not carry out any further chargeable work on the vent or the damp without our written instruction. If you think further work is needed, please send a quote first.
>
> If you could reply by Tuesday 16 September, that would be very helpful.
>
> Kind regards,
> Priya Nair
> Property Manager, Northbridge Lettings

**MSG-003 - Email to landlord (Owen Vale)** (status_update): *Update: Flat 4, 8-12 Juniper Mews - taps done, vent leak and bedroom damp still outstanding*
> Dear Owen,
>
> Here is an update on the repairs at Flat 4, 8-12 Juniper Mews, Vellumford, ZZ1 1ZZ.
>
> Taps: Copper Finch Plumbing attended on Friday 12 September. According to their paperwork, they fitted a new kitchen mixer tap and replaced the brass insert and head on the bathroom basin hot tap. We are asking the tenant to confirm that both taps are now working properly. The contractor has sent an invoice, but it has the wrong property address on it and no prices, so we have asked them to reissue it. We will send you the corrected invoice once we have it. We will not process anything for payment before then.
>
> Bathroom vent and bedroom damp: the contractor's paperwork does not mention the rainwater coming through the bathroom vent or the damp in the smaller bedroom, so we have asked them for their findings. These problems look like rainwater getting in from outside, most likely through the roof or the vent outlet, rather than a plumbing fault. As the flat is in a block, the roof and outside of the building may be the responsibility of the freeholder or managing agent and covered by the buildings insurance.
>
> To follow up your request about insurance and the roof-leak history, please could you send us:
> 1. the name and contact details of the freeholder or block managing agent, if there is one;
> 2. the buildings insurance details (insurer and policy number), or confirmation of who holds the policy;
> 3. whether your lease makes you responsible for any part of the roof or the outside of the building;
> 4. any details you have of past roof leaks, such as dates, what was repaired and by whom.
>
> We are also checking our own records for earlier leak and damp reports at the flat and will send you a summary. When we hear from you, we will either report the leak to the freeholder or managing agent, or suggest a roofing and damp inspection by one of our approved contractors. We will ask for your approval of the cost before any further work is booked.
>
> Kind regards,
> Priya Nair
> Property Manager, Northbridge Lettings

**ITEM-001 - Open item open**: Corrected, priced invoice needed from Copper Finch Plumbing (NBL-003-INV-14 shows a different property address, and has no amounts or VAT). Also need the visit report and confirmation that the taps are fixed.

**ITEM-002 - Open item open**: Rainwater coming through the bathroom vent in heavy rain, and damp on the ceiling and wall of the smaller bedroom: not dealt with at the 12/09 visit. Need findings, the tenant's update and photos, and to decide who is responsible (roof, freeholder or block management) before arranging an inspection or repair.

**ITEM-003 - Open item open**: Landlord's requests in event-004: check buildings insurance cover, and review the flat's history of repeated roof leaks. We have asked the landlord for freeholder, managing agent and insurer details (MSG-003). The agency must review its own records and send the landlord a summary.

**ITEM-004 - Open item open**: Tenant to confirm that both taps are working properly after the 12/09 visit (requested in MSG-001).

**HOLD-001 - Case put on hold** (waiting_for_contractor): waiting for From Copper Finch Plumbing: a corrected, priced invoice and the visit report (MSG-002). From the tenant: confirmation that the taps are fixed, and an update and photos on the vent and damp (MSG-001). From the landlord: freeholder, managing agent and insurer details and the roof-leak history (MSG-003).. Follow up 2025-09-16T10:00:00Z; if nothing arrives: Phone Gareth Lune about the invoice and report, and phone the landlord. Give the tenant the promised update on the vent and damp. If the damp has got worse or affects a vulnerable occupant, ask the landlord to approve an urgent roofing and damp inspection, or report it to block management, and escalate to a human if the question of who is responsible stalls.

## Escalation

Not escalated.

## What failed

- send_email -> address_mismatch: Message mentions a property address that is not this case's property. Correct it, or set allow_other_addresses=true if intentional.
- send_email -> address_mismatch: Message mentions a property address that is not this case's property. Correct it, or set allow_other_addresses=true if intentional.

## Next step

**agency**: Review the replies from the contractor, tenant and landlord. Once the invoice is corrected, record it and forward it to the landlord. Decide the route for the vent and damp (block management report or landlord-approved roofing and damp inspection). Review the agency's leak history and send the landlord a summary. (by 2025-09-16T10:00:00Z)

## Final result

`request_information`: The invoice cannot be recorded or forwarded: it has the wrong address and no amounts. I asked the contractor for a reissued, itemised invoice with VAT shown and a visit report covering the vent and damp (MSG-002). Work completion has not been confirmed by anyone independent, so I asked the tenant to confirm the taps are fixed and to give an update, photos and any vulnerability details on the vent and damp (MSG-001). The landlord's insurance and history questions from event-004 were still unanswered (event-005, event-012). I updated the landlord (MSG-003) and asked for freeholder, managing agent, insurer and lease details, since a roof leak in a block is likely to be the freeholder's responsibility. I did not instruct a roofer yet because responsibility and insurance cover need settling first. Further spending will go back to the landlord for approval. Loose ends are tracked as ITEM-001 to ITEM-004, with a follow-up on 16/09. The case cannot be closed.
