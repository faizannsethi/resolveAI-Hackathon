# Case property-management-test-cases-015: decision at 2025-09-25T08:34:11Z

**Decision:** `wait`  |  **Risk:** routine  |  **Escalated:** yes  |  **Confidence:** medium

## What the system received

- Case input: `Property_Management_test_cases/015`, 21 visible event(s), history cut at the end of the supplied history

- Documents read: attachments/move-out-inspection-report.pdf, attachments/property-preparation-quotation.pdf

## Decision point

Event-021 is a staff instruction to wait three more working days for the separate major maintenance to finish before the sanitation work is booked. The question is whether to wait, book the contractor, or deal with the loose ends first.

## Situation

The property is vacant. Brindlewick quoted £665 (NBL-015-Q1) for cleaning, waste removal and garden clearance. The landlord approved it only if the cost is recovered from the deposit, but the deposit is £650 and in dispute. Her later 'approved quote' (event-016) does not say which quote she meant. The work is on hold until the separate major maintenance is finished. No visit is booked. A prospective tenant wanted to move in on 28 Sep.

## Actions taken

**NOTE-001 - Internal note** (decision_rationale): Position at 25/09/2025: Per staff instruction (event-021), the sanitation/waste/garden work is held for 3 more working days (to Tue 30/09/2025) until the separate major maintenance is completed. No job has been formally instructed or booked with Brindlewick in this system.
Unresolved points that prevent treating the £665 quote (NBL-015-Q1, attachments/property-preparation-quotation.pdf) as unconditionally approved:
1. Landlord approval (event-008, repeated event-010) was conditional on recovering the cost from the former tenants' deposit. Deposit held is £650 (event-011), less than the £665 quote alone, and the claim is going through the deposit process, so recovery cannot be guaranteed. The condition cannot be met in advance.
2. The landlord's 'approved quote' (event-016) does not say which quote it refers to. It may be the separate major maintenance quote (outstanding at event-015) rather than NBL-015-Q1.
3. Scope mismatch: the quote includes carpet shampooing (Bedroom 1, stairs, landings), which is not in the inspection report, and it does not cover making good the disturbed soil in the rear garden (attachments/move-out-inspection-report.pdf). The landlord's request (event-007) did not list these items.
4. Timing: a prospective tenant wanted to move in on 28/09/2025 (event-015). The 3-working-day wait ends after that date, so the move-in date needs checking.
Event-009 told the contractor the quote was approved without mentioning the condition. Event-012 then put the work on hold, so no work has been carried out.
No landlord decision recorded yet because of points 1 and 2.

**MSG-001 - Email to landlord (Nessa Quill)** (request_information): *18 Thistlevaunt Lane – post-tenancy preparation: update and two points to confirm*
> Dear Ms Quill,
>
> Here is an update on the post-tenancy preparation at 18 Thistlevaunt Lane, Orvelune, ZZ1 1ZZ, and two points we need you to confirm.
>
> Current position
> The cleaning, waste removal and garden clearance by Brindlewick Turnover Services has not been booked yet. The separate major maintenance has to be finished before the cleaning can go ahead, so we are holding the booking for now. We expect to update you by Tuesday 30 September 2025.
>
> 1. Which quote did you approve?
> On 17 September you sent "approved quote". Could you confirm which quote you meant: the separate maintenance quote, or the Brindlewick property preparation quote (reference NBL-015-Q1, £665.00)?
>
> 2. The condition on the £665 preparation quote
> On 8 September you approved the £665 quote on condition that the cost is recovered from the former tenants' deposit. The deposit held is £650. We are claiming the full deposit through the deposit protection process, but the outcome is decided by that process, so we cannot promise in advance that any particular amount will be recovered. Please confirm whether you are happy for this work to go ahead whatever the outcome of the deposit claim, or tell us if you would like a different approach.
>
> Scope of the quote
> So that you approve exactly what is in it, quote NBL-015-Q1 covers:
> - degreasing the oven, hob and extractor
> - treating kitchen grease and bathroom limescale
> - removing rubbish
> - general sanitation of the remaining areas
> - carpet shampooing in Bedroom 1, the stairs and the landings (this was not listed in the move-out inspection report)
> - weeding, cutting the grass and tidying the rear garden
>
> The quote does not cover making good the soil in the rear garden, which the inspection noted had been disturbed by digging. Please tell us if you would like us to ask Brindlewick to add this. The quote does not show whether VAT is included in the £665.00, so we will confirm that with the contractor.
>
> We will not book any work until we have your confirmation.
>
> Kind regards,
> Northbridge Lettings

**ITEM-001 - Open item open**: Landlord to confirm (a) which quote 'approved quote' (event-016) referred to, (b) whether the £665 preparation work (NBL-015-Q1) may go ahead whatever the outcome of the deposit claim, and (c) the scope (carpet shampooing is included; making good the disturbed soil is not). Asked in MSG-001.

**ITEM-002 - Open item open**: Separate major maintenance must be completed before the sanitation work can be booked (event-021). Confirm its completion date, then get dates from Brindlewick (promised at event-019, not yet received).

**ESC-001 - ESCALATED to human** [P2_same_day, conflicting_information, respond within 4 working hours]
  Summary: The preparation work at 18 Thistlevaunt Lane (Brindlewick quote NBL-015-Q1, £665) is on hold, per your instruction at event-021, until the separate major maintenance is finished (about 3 working days, to 30/09/2025). Three things need a human decision: (1) a prospective tenant wanted to move in on 28/09/2025 (event-015), which is before the hold ends and before any cleaning or maintenance is booked; (2) the landlord approved the £665 only if it is recovered from the deposit (events 008 and 010), but the deposit is £650 and in dispute (event-011), so that condition cannot be guaranteed; (3) the landlord's 'approved quote' (event-016) does not say which quote it means.
  Why a human: The move-in date clash and the deposit dispute are tenancy, legal and money matters outside my authority. The landlord's conditional approval cannot be treated as firm approval to spend.
  Recommended: Confirm with the prospective tenant whether the 28 Sep move-in is going ahead, and agree a later date if needed; Handle the deposit claim through the scheme; do not promise the landlord a recovery amount; Once the landlord gives unconditional approval and the maintenance date is known, record the decision and book Brindlewick

**HOLD-001 - Case put on hold** (waiting_for_third_party): waiting for Completion of the separate major maintenance (staff instruction at event-021 to wait 3 working days), plus the landlord's reply to MSG-001 on which quote she approved and the deposit condition.. Follow up 2025-09-30T09:00:00Z; if nothing arrives: Check with Mira Venn on maintenance completion; phone landlord Nessa Quill to chase confirmation; once both confirmed, record landlord decision and ask Brindlewick (Elian Wren) for a firm slot.

## Escalation

Escalated to a human: see the ESC entry above.

## What failed

- none

## Next step

**agency**: Confirm that the separate maintenance is finished and chase the landlord's reply to MSG-001. If she approves unconditionally, record the decision and get a firm slot from Brindlewick. (by 2025-09-30T09:00:00Z)

## Final result

`wait`: I followed the staff instruction to hold until 30/09/2025 (event-021) rather than booking Brindlewick. The approval cannot be treated as firm: it depends on recovering the cost from the deposit (events 008 and 010), which cannot be guaranteed while the claim is in dispute (event-011), and the 'approved quote' message (event-016) does not say which quote it means. So I recorded no landlord decision and assigned no job. I emailed the landlord to clear up both points and to confirm the scope: carpet shampooing is in the quote, and making good the disturbed soil is not. I raised a non-blocking escalation for the 28 Sep move-in clash and the deposit dispute, and set a hold with a follow-up.
