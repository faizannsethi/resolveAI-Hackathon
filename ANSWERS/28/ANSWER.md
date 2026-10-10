# Case property-management-test-cases-028: decision at 2025-09-18T14:50:04Z

**Decision:** `wait`  |  **Risk:** routine  |  **Escalated:** no  |  **Confidence:** high

## What the system received

- Case input: `Property_Management_test_cases/028`, 25 visible event(s), history cut at the end of the supplied history

- Documents read: attachments/checkout-report.pdf, attachments/provider-quotation.pdf

## Decision point

The landlord says her own contractor has finished the move-out works, and the workflow task has been dismissed. But the agency's request for the cost breakdown and her view on what the former tenant should pay (event-023) has had no reply, and nothing is set to follow it up.

## Situation

42 Mallowfen Crescent is empty. After the checkout, three items needed attention: the meter cabinet hinges, the Bedroom 1 nails and paint touch-up, and sticker residue on the front door. The landlord turned down Pineglass's £564.48 quote (event-017) and used her own company. Pineglass was stood down (event-020). On 18 Sept the landlord said the work was done (event-021). That morning the agency asked her for itemised costs and which items, if any, she thinks the former tenant should pay for (event-023). She has not replied yet, and the workflow task was dismissed (event-024/025).

## Actions taken

**DEC-001 - Landlord decision recorded:** landlord_arranging_own_contractor: Landlord declined the Pineglass Property Repairs quote (NBL-028-Q1, £564.48) for the move-out works (meter cabinet hinges, Bedroom 1 nails/paint touch-up, front door sticker residue) and arranged her own company. Landlord reported the work as completed in event-021. (evidence event-017)

**ITEM-001 - Open item open**: Awaiting landlord's itemised breakdown of costs incurred for her own contractor's move-out works, and her view on which items (if any) she considers the former tenant's responsibility, so the tenancy account/deposit can be reviewed. Requested in event-023. Any tenant recharge needs evidence (checkout report) and landlord agreement before proceeding.

**NOTE-001 - Internal note** (decision_rationale): Case not closed despite the workflow marking it complete (event-022/024). The physical works are reported complete by the landlord (event-021), but the request for cost breakdown and responsibility allocation (event-023) was sent only ~6 hours ago and is unanswered (event-025). This affects the former tenant's account/deposit, so the case stays open with a follow-up rather than relying on the dismissed workflow task. Data note: event-001 said landlord approval was 'marked as already given' for the move-out works, but the landlord expressly declined the agency quote and used her own company (event-017), so event-001 is superseded. Pineglass was stood down (event-020) before any work; no invoice expected from them, though watch for one in error. Completion evidence is the landlord's statement only (no date/photos); acceptable as the landlord owns the property and used her own contractor, but photos/invoice would support any deposit claim.

**HOLD-001 - Case put on hold** (waiting_for_landlord): waiting for Elowen Quill's reply to event-023: itemised costs for her contractor's move-out works (ideally with invoice/photos and completion date) and whether she considers any items the former tenant's responsibility.. Follow up 2025-09-22T10:00:00Z; if nothing arrives: Chase the landlord by email (and phone if needed), explaining that the tenancy account/deposit review depends on her cost breakdown and responsibility view; if she confirms no claim against the tenant, resolve the open item and close the case as resolved by landlord's own contractor.

## Escalation

Not escalated.

## What failed

- none

## Next step

**agency**: Check for the landlord's cost breakdown and her view on what the former tenant should pay. If nothing has arrived, chase her by email or phone. If she says there is no claim against the tenant, resolve ITEM-001 and close the case as resolved by her own contractor. (by 2025-09-22T10:00:00Z)

## Final result

`wait`: I didn't close the case, even though the workflow marks it complete. Whether anything is charged to the former tenant's account or deposit depends on the landlord's answer to event-023. That question was sent only about 6 hours ago, so chasing now would be too early. But nothing was set to follow it up, so it could get lost. I logged the landlord's choice to use her own contractor (DEC-001, from event-017) and opened an item for the missing breakdown (ITEM-001). I also set a follow-up for Monday 22 Sept with a planned chase. No agency contractor or spending is involved, and nobody else needs a message right now.
