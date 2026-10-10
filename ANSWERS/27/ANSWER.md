# Case property-management-test-cases-027: decision at 2025-09-15T16:25:18Z

**Decision:** `wait`  |  **Risk:** routine  |  **Escalated:** no  |  **Confidence:** high

## What the system received

- Case input: `Property_Management_test_cases/027`, 17 visible event(s), history cut at the end of the supplied history

- Documents read: attachments/checkout-report.pdf, attachments/move-out-works-quotation.pdf

## Decision point

The quote was forwarded to the landlord at event-014; the follow-up call at event-017 captured no decision. Should we wait, chase, or act on the quote?

## Situation

The property is vacant and being prepared for re-letting. Alderwick Property Works quoted £3,865.68 (NBL-027-Q1): one lump sum, not itemised, with VAT not stated and several checkout items left out (including the taped boiler casing and carpets). The quote went to the landlord about 2.5 hours ago and the call got no answer. Approval is required (event-015) and has not been given.

## Actions taken

**MSG-001 - Email to contractor (Iris Bell)** (request_information): *46 Fernwick Lane, Aldermead – quotation NBL-027-Q1: breakdown and scope questions*
> Dear Iris,
>
> Thank you for your quotation NBL-027-Q1 dated 15 September 2025 for the move-out works at 46 Fernwick Lane, Aldermead, ZZ1 1ZZ. We have passed it to the landlord. To help him reach a decision, please could you confirm the following:
>
> 1. A task-by-task price breakdown of the £3,865.68 total. The quotation currently shows a single "Labour & Materials" figure.
> 2. Whether £3,865.68 includes VAT, is plus VAT, or has no VAT charged.
> 3. Any exclusions or assumptions. In particular, please confirm whether the following items from the checkout report are excluded:
>    - the warped kitchen worktop and reported water ingress
>    - kitchen flooring damage, chipped living-room laminate (your quote includes a threshold)
>    - the missing bedroom curtain pole, curtains and bulbs
>    - rusting radiators other than the en-suite radiator
>    - the boiler casing held with tape (we expect this to need a Gas Safe registered engineer separately)
>    - carpet replacement
> 4. Scope checks against the checkout report:
>    - It records damage to the staircase newel posts (plural) and a bedroom door frame, plus screw damage to an upstairs uPVC window frame. Please confirm your newel post, door frame and uPVC window frame items cover all of these.
>    - Please also confirm the cause of the ceiling water damage has been checked before stain-blocking, or say whether it has been assumed.
> 5. A likely lead time once the work is approved, even if it is only approximate. The property is being prepared for re-letting.
>
> Please do not start any work until we confirm the landlord's written approval.
>
> Kind regards,
> Maya Chen
> Property Manager, Northbridge Lettings

**MSG-002 - Email to landlord (Owen Vale)** (status_update): *46 Fernwick Lane, Aldermead – move-out works quotation: points to note before you decide*
> Dear Mr Vale,
>
> I tried to call you this afternoon about the move-out works quotation I emailed earlier today for 46 Fernwick Lane, Aldermead, ZZ1 1ZZ, but couldn't get through. Here are a few points to help you decide.
>
> 1. The quotation from Alderwick Property Works (ref NBL-027-Q1, dated 15 September 2025) is for £3,865.68. It is a single "Labour & Materials" figure with no price for each task, and it does not say whether VAT is included. I have asked the contractor for a full breakdown and to confirm the VAT position.
>
> 2. The quote covers:
>    - repair to the newel post
>    - door frame screw damage
>    - filling holes in the uPVC window frames
>    - making good wall damage
>    - a new threshold and toilet-roll holder
>    - a new smoke detector
>    - rehanging the kitchen radiator
>    - two new extractor fans
>    - a new en-suite radiator
>    - stain-blocking the water-damaged ceilings
>    - reinstating the decoration
>
> 3. Several checkout items are not in this quote and would need separate pricing:
>    - the warped kitchen worktop and reported water ingress
>    - kitchen flooring and the chipped living-room laminate
>    - the curtain pole, curtains and bulbs
>    - the other rusting radiators
>    - carpet replacement, which you asked to have quoted
>    - the boiler casing, which appears to be held with tape
>
> 4. Two items are, in our view, needed before re-letting:
>    - The boiler should be inspected by a Gas Safe registered engineer.
>    - The non-working top-floor smoke detector must be working. Smoke alarms are required on each storey at the start of a tenancy.
>    I would also suggest checking the cause of the ceiling water damage before it is decorated over.
>
> Please let us know whether you would like to:
> (a) approve the £3,865.68 quotation as it stands;
> (b) wait for the itemised breakdown, which I have requested, before deciding; or
> (c) decline it, or ask for a second quote.
>
> Please also tell us whether you would like us to arrange quotes for the boiler inspection, carpets and the other items not covered. Nothing will be instructed until we have your written approval.
>
> Kind regards,
> Maya Chen
> Property Manager, Northbridge Lettings

**FIN-001 - Quote/invoice recorded:** quote from Alderwick Property Works £3,865.68 (unknown, gross £3,865.68), payer landlord, route undecided

**ITEM-001 - Open item open**: Landlord decision outstanding on Alderwick quotation NBL-027-Q1 (£3,865.68, VAT unknown). The approval request was sent at event-014; the call at event-017 got no answer.

**ITEM-002 - Open item open**: Checkout items not covered by quote NBL-027-Q1:
- boiler casing held with tape (needs Gas Safe inspection before re-letting)
- warped kitchen worktop / water ingress
- kitchen flooring and living-room laminate
- curtain pole, curtains and bulbs
- other rusting radiators
- carpet replacement quote
Landlord to say whether separate quotes are wanted.

**ITEM-003 - Open item open**: Asked contractor (MSG-001) for: an itemised breakdown, VAT treatment, exclusions, scope confirmation (newel posts, door frame, uPVC window), whether the ceiling leak cause was checked, and lead time.

**NOTE-001 - Internal note** (decision_rationale): Quote NBL-027-Q1 (£3,865.68) went to the landlord at event-014. It is above the approval threshold (event-015). The call to the landlord at event-017 captured no decision.

Approval is NOT in place:
- The workflow note at event-002 ("approval normally in place") is not evidence.
- The job email at event-004 said the works were "agreed with the landlord", but that does not cover this specific price.

The quote is a lump sum with VAT not stated, and it omits several checkout items, including the taped boiler casing (needs a Gas Safe inspection before re-letting). Discrepancy: the checkout report says "newel posts" and "bedroom door frame", while the quote says "newel post" and "screw damage to a door frame".

No work is to be instructed until the landlord's written approval is recorded. The property is vacant and keys are at the office; no occupant safety risk at present.

**HOLD-001 - Case put on hold** (waiting_for_landlord): waiting for Owen Vale's written decision on quote NBL-027-Q1 (£3,865.68) and on whether to obtain quotes for the excluded items (boiler Gas Safe inspection, worktop, flooring, carpets, etc.). Also waiting for Alderwick's itemised breakdown and VAT confirmation.. Follow up 2025-09-17T10:00:00Z; if nothing arrives: Phone the landlord again and send a chase email. Chase Alderwick for the breakdown and VAT. If there is still no landlord response by 19 Sept, escalate to the property manager, given the re-letting timescale.

## Escalation

Not escalated.

## What failed

- none

## Next step

**agency**: Check for the landlord's decision and the contractor's breakdown. If nothing has arrived, phone and email the landlord and chase Alderwick. Record the landlord's decision before instructing any work. (by 2025-09-17T10:00:00Z)

## Final result

`wait`: The landlord only received the approval request this afternoon (event-014), so a chase is not yet due. Re-sending the approval request would duplicate it. Instead, I:
- emailed the landlord about the missed call, setting out the quote's gaps, the VAT uncertainty and the two items needed before re-letting (Gas Safe inspection of the boiler and a working smoke alarm on each storey);
- asked the contractor for an itemised breakdown, VAT treatment, exclusions and lead time.

Approval claims at event-002 and event-004 are not evidence of approval for this price. No work is instructed. A hold is set to follow up on 17 Sept.
