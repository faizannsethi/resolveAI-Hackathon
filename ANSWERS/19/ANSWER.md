# Case property-management-test-cases-019: decision at 2025-09-11T06:58:16Z

**Decision:** `escalate`  |  **Risk:** routine  |  **Escalated:** yes  |  **Confidence:** high

## What the system received

- Case input: `Property_Management_test_cases/019`, 16 visible event(s), history cut at the end of the supplied history

- Documents read: attachments/remedial-works-invoice.pdf

## Decision point

Contractor invoice (£174) received for work carried out despite a quote-only instruction, with no access record, itemisation, VAT status or completion evidence.

## Situation

The six move-out items at 18 Brindle Row were approved in principle by the landlord (event-005). Alder & Finch were asked for a quote only (event-008) but say they completed the work on 9 Sep (event-013). They invoiced £174 as a single line (NBL-019-INV-11), including an unapproved variation (a new Venetian blind). How they got into the vacant property is unknown.

## Actions taken

**FIN-001 - Quote/invoice recorded:** invoice from Alder & Finch Repairs £174.00 (unknown, gross £174.00), payer landlord, route undecided

**MSG-001 - Email to contractor (Rowan Pike)** (request_information): *18 Brindle Row, Larkspur Vale, ZZ1 1ZZ - invoice NBL-019-INV-11: information needed before processing*
> Dear Rowan,
>
> Thank you for sending invoice NBL-019-INV-11 (£174.00, dated 11 September 2025) for 18 Brindle Row, Larkspur Vale, ZZ1 1ZZ.
>
> As you know from our email of 7 September, our instruction was for a quotation only, with no work to start until we had reviewed the price and issued written authority. As the work has gone ahead without that step, we cannot put the invoice forward for payment until we have the following:
>
> 1. The date and time of your visit, and exactly how you got into the property - who let you in or where the keys came from, and confirmation that any keys have been returned to our office. The previous tenant had moved out and returned his keys, and we have no record of releasing keys or arranging access, so we need this information urgently.
> 2. Who you understood had authorised the work to start.
> 3. An itemised breakdown of the £174.00, showing labour and materials for each of the six items, and in particular the new Venetian blind and the floor repair.
> 4. Whether you are VAT registered and whether £174.00 includes VAT. If you are registered, please send a VAT invoice showing your VAT number.
> 5. Before and after photographs of each item: the floor beside the fireplace and the carpet, the front lounge blind, the under-stairs cupboard handle, the kitchen blind, the toilet seat and the front-gate hinge.
> 6. An explanation of why the front lounge blind was replaced rather than repaired, and what was found with the floor (the inspection noted cracked chipboard flooring, but your invoice describes replacing a floorboard).
>
> Please reply by 5pm on Friday 12 September 2025. Once we have this, we will review it with the landlord and confirm what happens next with the invoice.
>
> Kind regards,
> Maya Chen
> Property Manager, Northbridge Lettings

**MSG-002 - Email to landlord (Ivo Marlow)** (status_update): *18 Brindle Row, Larkspur Vale, ZZ1 1ZZ - update on move-out remedial works*
> Dear Ivo,
>
> Here is an update on the remedial works at 18 Brindle Row, Larkspur Vale, ZZ1 1ZZ.
>
> After your approval on 7 September, we asked Alder & Finch Repairs for a quotation first and told them not to start any work until we had agreed a price with you. The contractor has now told us they misunderstood this and went ahead with the work, which they say they completed on 9 September. We have received their invoice NBL-019-INV-11 for £174.00. The invoice does not say whether VAT is included.
>
> The invoice lists the following work:
> - replaced the broken lounge floorboard and reinstated the carpet
> - removed the front lounge blind and supplied and fitted a new Venetian blind (the inspection had noted a repair, not a replacement)
> - refixed the under-stairs cupboard handle with new fixings
> - adjusted the kitchen blind mechanism
> - retightened the toilet seat
> - reattached the front-gate hinge with new fixings
>
> We have not paid or passed on the invoice yet. First we are asking the contractor for an itemised breakdown, their VAT status, before and after photographs, the date of the visit and how they got into the property. We are also checking our own key records. We will make sure the work has been done properly before we ask you to settle anything.
>
> We will update you once we have the contractor's reply, which we have asked for by 12 September. If you have any concerns in the meantime, including about the blind being replaced rather than repaired, please let me know.
>
> Kind regards,
> Maya Chen
> Property Manager, Northbridge Lettings

**ITEM-001 - Open item open**: Access to vacant property unexplained: contractor says work done 9 Sep but no record of key release/access arrangement (tenant returned keys 27 Aug; agency held a set). Check office key log, confirm all keys accounted for and property secure.

**ITEM-002 - Open item open**: Invoice NBL-019-INV-11 (£174, VAT unknown) for work done without quote/written authority: needs itemisation, VAT status, completion photos/verification, and landlord sign-off (incl. blind replacement variation) before payment.

**ESC-001 - ESCALATED to human** [P3_next_working_day, financial_decision, respond within 1 working day]
  Summary: Alder & Finch Repairs was instructed quote-only for six move-out items at 18 Brindle Row (event-008), with written instruction not to start work. Contractor says he misunderstood and completed the work on 9 Sep (event-013), then invoiced £174 (NBL-019-INV-11, single line, VAT status unknown, no itemisation or photos). How he got into the vacant property is unknown; tenant returned keys 27 Aug and the agency holds a set. Invoice includes a variation (new Venetian blind instead of repair). Landlord gave open approval for remedial works on 7 Sep (event-005), but no price was ever agreed.
  Why a human: The contractor did not follow a written quote-only instruction. Payment for this unauthorised work, and the variation, is a money and liability decision for a person to make. Entry to a vacant property without any recorded key release is also a security and process matter that needs a human check of the key log and possibly a site check.
  Recommended: Check office key log today and confirm all keys are accounted for and the property is secure; Review contractor's reply; if needed, arrange a quick check of the work (or rely on photos); Once the invoice is verified, send it to the landlord for sign-off, pointing out the blind replacement variation; Decide whether to remind Alder & Finch about the instruction process, or record it as a supplier performance issue

**HOLD-001 - Case put on hold** (waiting_for_contractor): waiting for Alder & Finch reply with visit date, access/key details, itemised breakdown, VAT status, before/after photos and explanation of blind replacement (MSG-001); also the human key-log check.. Follow up 2025-09-12T17:00:00Z; if nothing arrives: Phone Rowan Pike to chase; if the access question is still unanswered, ask the human reviewer to arrange a site and security check, and keep the invoice unpaid.

## Escalation

Escalated to a human: see the ESC entry above.

## What failed

- none

## Next step

**agency**: Review the contractor's reply and check the office key log; if no reply, phone Rowan Pike. Once the invoice is verified, send it to the landlord for sign-off. (by 2025-09-12T17:00:00Z)

## Final result

`escalate`: The invoice cannot be passed for payment yet. The contractor went against a written quote-only instruction (event-008), there is no itemisation, VAT status or completion evidence (event-015, invoice PDF), and the blind was replaced rather than repaired without approval. The landlord's open approval (event-005) supports work in principle but not an unchecked bill. Entry to a vacant property with no recorded key release (event-003, event-007, event-013) is a security and process concern. I recorded the invoice as unpaid with the payment route undecided, asked the contractor for the specific evidence, told the landlord honestly what has happened, opened items for the access check and the invoice check, escalated (non-blocking) for the payment decision and key-log check, and set a follow-up.
