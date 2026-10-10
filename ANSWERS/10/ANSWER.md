# Case property-management-test-cases-010: decision at 2025-09-24T14:36:22Z

**Decision:** `escalate`  |  **Risk:** routine  |  **Escalated:** yes  |  **Confidence:** medium

## What the system received

- Case input: `Property_Management_test_cases/010`, 26 visible event(s), history cut at the end of the supplied history

- Documents read: none

## Decision point

The full-kitchen figures have arrived and been forwarded to the landlord (event-024/025). The cupboards-and-doors estimate is still missing. The contractor's commission/VAT basis is unresolved (event-022/023). The tenant has not been updated since 9 Sep, her offered dates have passed, and she has reported cuts from sharp edges.

## Situation

Peeling cabinet laminate with sharp edges (tenant cut several times) and doors that don't close properly at 42 Brackenveil Row. The landlord asked for two estimates. Only the full-kitchen figures have arrived: £9,260 + VAT, or £11,112 gross, including a £380 + VAT electrical estimate that is not yet confirmed. The cupboards-and-doors estimate is outstanding. A commission arrangement with the contractor was raised but not settled. No site visit has happened, and no replacement has been approved.

## Actions taken

**MSG-001 - Email to tenant (Elowen Marr)** (status_update): *Update on your kitchen cabinets – 42 Brackenveil Row*
> Dear Elowen,
>
> I'm sorry we haven't been in touch since you sent your availability. I know the 16–18 September dates went by without a visit being booked, and I apologise for that.
>
> Here is where things stand. After looking at the problem, the contractor told us that fixing the laminate properly would mean more than a simple repair. Your landlord has therefore asked for prices for a larger replacement, and we have just sent him the first estimate. We are still waiting for a second estimate and for the landlord's decision. As soon as we have it, we will arrange a visit with you. We will always agree a time in advance so the dogs can be secured.
>
> As the laminate edges have already cut you, please take care around the damaged panels until the work is done. If it helps, you could cover any lifting or sharp edges with strong tape, and keep the dogs away from damaged lower cupboards. We have also asked the landlord to approve a short visit to make the sharp edges safe in the meantime.
>
> Could you please reply with:
> 1. Some dates and times over the next two weeks when a contractor could visit (to take measurements and, if approved, to make the edges safe), and any instructions about the dogs.
> 2. Whether the damage has got any worse, or whether anyone has been hurt again since your first report. Photos of the worst edges would be very helpful.
>
> I will update you again by Monday 29 September at the latest.
>
> Kind regards,
> Nia Calder
> Property Manager, Northbridge Lettings

**MSG-002 - Email to contractor (Kellan Rook)** (chase): *42 Brackenveil Row – cupboards-and-doors estimate still needed, and site visit*
> Dear Kellan,
>
> Thank you for the full-kitchen figures for 42 Brackenveil Row, Oakhollow, ZZ1 1ZZ, which we have passed to the landlord.
>
> The landlord asked for two estimates, and we still need the second one: replacing the cupboards and doors only, keeping the existing appliances, worktops and flooring. Please send it by Friday 26 September if you can.
>
> Please also confirm the following:
> 1. Whether the figures you sent (supply £4,850, removal and fitting including tiled splashback £3,800, waste removal £230, and electrical estimate £380, all plus VAT) are your complete, final prices to the landlord. If anything could still change them, please tell us what and by how much.
> 2. Whether you need to visit the property to measure up and to confirm the electrical item before your prices are firm.
> 3. Your availability over the next two weeks for that visit. The tenant has two dogs that must be secured, so we will book the time with her in advance.
>
> Please note: no replacement work, and no other chargeable work, has been approved yet. Please do not book or order anything until we confirm the landlord's written approval.
>
> Kind regards,
> Nia Calder
> Property Manager, Northbridge Lettings

**APR-001 - Landlord approval requested** (approve_works): Approve interim make-safe of sharp laminate edges up to £150 incl. VAT £150.00 (includes_vat); Do not carry out interim make-safe; wait for replacement decision; reply due 2025-09-27T14:36:22Z
> Dear Soren,
>
> This follows my email earlier today with Alderline Joinery's full-kitchen figures for 42 Brackenveil Row, Oakhollow, ZZ1 1ZZ. Below is a summary of those figures, followed by one request.
>
> Full-kitchen figures (Alderline Joinery):
> - Supply: £4,850 + VAT
> - Removal of the old kitchen and fitting of the new one, including tiled splashback: £3,800 + VAT
> - Waste removal: £230 + VAT
> - Electrical work (estimate only, to be confirmed): £380 + VAT
> Total: £9,260 + VAT (£1,852), which comes to £11,112 including VAT. Without the electrical estimate, the total is £8,880 + VAT, or £10,656 including VAT.
> The new kitchen would include an oven, hob and chimney extractor. It would not include a microwave, washer or dryer.
>
> We have asked Alderline Joinery to:
> - send the cupboards-and-doors-only estimate you requested;
> - confirm that the figures above are final;
> - say whether they need a site visit to measure up and to confirm the electrical work.
> Please don't treat the figures above as final until we have these answers. We will send both options together for your decision. Nothing has been approved or ordered.
>
> Request: interim make-safe
> The tenant reported that the peeling laminate has sharp edges that have already cut her several times. Any replacement is likely to take some weeks. In the meantime, we recommend that the contractor removes or secures the loose, sharp laminate edges when they visit to measure up. We propose a cap of £150 including VAT for this. Anything above that would come back to you first. This would not commit you to either replacement option.
>
> Could you please reply within 72 hours to say whether you approve the interim make-safe up to £150 including VAT?
>
> Kind regards,
> Nia Calder
> Property Manager, Northbridge Lettings

**ESC-001 - ESCALATED to human** [P3_next_working_day, financial_decision, respond within 1 working day]
  Summary: Alderline Joinery (Kellan Rook) has sent full-kitchen figures for 42 Brackenveil Row: £9,260 + VAT (£11,112 gross), including a £380 + VAT electrical estimate that has not been confirmed. Before sending them, the contractor raised a 15% commission. On the call, he asked whether the old or the revised commission basis applied, whether a cap applied to a larger job, and how VAT affected the amount, and said the answers could change his quote (event-022). Staff told him to use the 'previous commission arrangement' and classify the job as before (event-023). Neither call settled the commission calculation, any cap, the VAT treatment or the total payable. The figures have been forwarded to the landlord (event-025), but the landlord has not been told whether the contractor's prices include, or are affected by, a commission payable to the agency.
  Why a human: Agreeing commission or referral-fee terms with a contractor, and deciding what to disclose to the landlord, is outside the agent's authority. The answer may change the price the landlord is asked to approve. Commission paid by contractors must be disclosed to the landlord under agency regulatory and client-money rules. A human needs to confirm the arrangement, how it applies to this job, and what the landlord is told, before any replacement quote is put up for approval.
  Recommended: Confirm the contractor commission arrangement that applies to this job (basis, cap, VAT) and write it down.; Tell Kellan Rook in writing which commission terms apply, so his final figures are firm.; Make sure any commission is disclosed to the landlord before he is asked to approve the replacement.

**ITEM-001 - Open item open**: Cupboards-and-doors-only estimate (keeping appliances, worktops and flooring), requested by the landlord in event-016, not yet received from Alderline Joinery. Chased in MSG-002, due 26 Sep.

**ITEM-002 - Open item open**: Contractor commission basis, cap and VAT treatment unresolved (event-022/023). The final payable total and disclosure to the landlord need confirming before any replacement approval is sought (ESC-001).

**ITEM-003 - Open item open**: Tenant's new visit availability and dog-access arrangements needed (the original 16–18 Sep dates have passed). Also check whether the sharp-edge injury risk is ongoing (MSG-001).

**HOLD-001 - Case put on hold** (waiting_for_landlord): waiting for Three replies: the landlord's decision on the interim make-safe (APR-001, due 27 Sep) and his view on the full-kitchen figures; the contractor's cupboards-and-doors estimate and confirmation of final figures (due 26 Sep); and the tenant's availability. The commission question is with a human (ESC-001).. Follow up 2025-09-29T09:00:00Z; if nothing arrives: Phone the landlord about APR-001, phone Kellan Rook to chase the second estimate, chase the tenant by SMS for availability, and send the tenant the promised update.

**NOTE-001 - Internal note** (decision_rationale): The full-kitchen figures (event-024) were already forwarded to the landlord in event-025. A replacement approval is not being requested yet because the cupboards-and-doors estimate is missing and the commission/VAT basis is unresolved (event-022/023, escalated in ESC-001). The tenant had not been updated since 9 Sep and her offered dates have passed, so an update and a request for availability were sent. Because the tenant reported cuts and replacement may take weeks, the landlord was asked to approve an interim make-safe capped at £150 including VAT (APR-001). The £150 cap is our proposal, not a contractor price. The event-006 approval covered the laminate-repair scope with no amount recorded, so it was not relied on to authorise spending. Arithmetic: 4850 + 3800 + 230 + 380 = £9,260 net, plus £1,852 VAT, giving £11,112 gross.

## Escalation

Escalated to a human: see the ESC entry above.

## What failed

- none

## Next step

**agency**: Review replies from the landlord (APR-001), the contractor (second estimate, final figures) and the tenant (availability). Then chase by phone if needed, and send both options to the landlord once commission is resolved under ESC-001. (by 2025-09-29T09:00:00Z)

## Final result

`escalate`: The landlord already has the full-kitchen figures (event-025), so another approval request for replacement would be premature. The second estimate he requested (event-016) is missing, and the final payable total depends on an unsettled commission basis (event-022/023). Agreeing commission terms and deciding what to disclose to the landlord are outside the agent's authority, so this went to a human as a non-blocking P3 (ESC-001). Meanwhile: the contractor was chased for the missing estimate and to confirm his prices are final (MSG-002). The tenant, who had heard nothing since 9 Sep and whose offered dates passed, got an apology, interim precautions and a request for new availability (MSG-001). Because she reported cuts and replacement could take weeks, the landlord was asked to approve an interim make-safe capped at £150 including VAT (APR-001). The follow-up hold is set for 29 Sep.
