# Case property-management-test-cases-023: decision at 2025-02-12T16:35:00Z

**Decision:** `escalate`  |  **Risk:** urgent  |  **Escalated:** yes  |  **Confidence:** medium

## What the system received

- Case input: `Property_Management_test_cases/023`, 23 visible event(s), history cut at the end of the supplied history

- Documents read: attachments/invoice-NBL-CFM-250210-A.pdf, attachments/invoice-NBL-CFM-250210-B.pdf

## Decision point

The agency has just asked the landlord how to proceed (event-023). The contractor still cannot explain two overlapping invoices, one of which is for unauthorised and apparently undone actuator work (event-022). Meanwhile the heating repair has stalled, and the tenant has a child at home.

## Situation

Intermittent radiator heating at 7 Larkspur Fold; hot water works. Copper Finch diagnosed an actuator fault on 5 Feb under the landlord's diagnosis-only authority (£180 incl. VAT). The £372 incl. VAT replacement estimate is not approved, and the landlord's questions about it are unanswered. On 10 Feb the contractor sent invoice A (£138, matches the diagnostic quote) and invoice B (£372, claims replacement on 5 Feb). There is no authorisation or evidence for B, and the tenant has seen no contractor since 5 Feb. Neither invoice has been paid.

## Actions taken

**FIN-001 - Quote/invoice recorded:** invoice from Copper Finch Mechanical £138.00 (includes_vat, gross £138.00), payer landlord, route undecided

**FIN-002 - Quote/invoice recorded:** invoice from Copper Finch Mechanical £372.00 (includes_vat, gross £372.00), payer unknown, route undecided

**MSG-001 - Email to contractor (Petra Quill)** (chase): *7 Larkspur Fold, Orvane Heath, ZZ1 1ZZ: invoices NBL-CFM-250210-A and -B on hold*
> Dear Petra,
>
> Thank you for your email today about the heating job at 7 Larkspur Fold, Orvane Heath, ZZ1 1ZZ.
>
> So that our records are clear:
>
> 1. Invoice NBL-CFM-250210-B (£372.00 incl. VAT) is on hold and has not been accepted. The landlord authorised diagnosis only, up to £180 incl. VAT. No written authorisation was ever given for actuator supply or replacement. The tenant tells us no contractor has attended since the visit on 5 February.
> 2. Invoice NBL-CFM-250210-A (£138.00 incl. VAT) matches your diagnostic quote of 4 February. However, it is also on hold until you confirm how the two invoices relate, because invoice B repeats the attendance, diagnosis and testing charges.
>
> By 12:00 on Friday 14 February 2025, please send us:
> - written confirmation of what work was actually carried out at the property, and on which date(s);
> - whether invoice B is cancelled or withdrawn, or, if you say actuator work was done, your job notes, the parts record and the attendance record that support this;
> - a corrected or credit-noted invoice, if appropriate.
>
> Separately, please answer the questions from our email of 7 February, which the landlord needs answered before he can decide on the repair:
> - Can the actuator be repaired rather than replaced?
> - Is the part available, and how long would it take to arrive?
> - An itemised breakdown of the £372 estimate (parts, labour, testing), confirming it is the full price.
> - Would the £138 diagnostic charge be credited if the replacement goes ahead?
>
> Please do not carry out any further work at the property. No remedial work is authorised until we confirm the landlord's approval in writing.
>
> The tenant still has intermittent heating and a child lives at the property, so a prompt reply would be appreciated.
>
> Kind regards,
> Ivo Merrick
> Property Manager, Northbridge Lettings

**MSG-002 - Email to tenant (Tessa Vane)** (status_update): *Heating at 7 Larkspur Fold: update*
> Dear Tessa,
>
> Thank you for confirming on 10 February that no one has attended since the engineer's visit on 5 February, and for the update on the radiators.
>
> Where things stand: the engineer found a fault with a heating valve part (the actuator) and recommended replacing it. We have asked the landlord to decide on the repair, and we are getting some details he needs from the contractor. We will be back in touch with you by Friday 14 February. Once the repair is approved, we will contact you to agree a visit time; we know you are available after 14:00 on weekdays.
>
> In the meantime:
> - If the heating stops working altogether, or the hot water fails, please let us know straight away so we can treat it as more urgent, especially with your child at home.
> - If you use a portable heater, keep it plugged straight into a wall socket as you have been (not an extension lead), keep it clear of curtains, bedding and clothing, and do not leave it on overnight or unattended.
> - If you ever smell gas or think there may be carbon monoxide (symptoms include headaches, dizziness or nausea), leave the property and call the National Gas Emergency line on 0800 111 999 straight away.
>
> We are sorry the heating problem is taking longer than we would like to resolve.
>
> Kind regards,
> Ivo Merrick
> Property Manager, Northbridge Lettings

**ITEM-001 - Open item open**: Invoice discrepancy. Copper Finch invoice NBL-CFM-250210-B (£372 incl. VAT) claims actuator replacement that was never authorised and is not evidenced, and it repeats charges on invoice A (£138). Need written clarification or withdrawal from the contractor, then the landlord's instruction on payment. Neither invoice is to be paid until this is resolved.

**ITEM-002 - Open item open**: Landlord's questions from event-012 are still unanswered: can the actuator be repaired, and does the £372 cover all parts, labour and testing? We need the contractor's answers (asked in events 015 and 021, and again in MSG-001) so the landlord can decide on the heating repair. Tenant with a child still has intermittent heating.

**ESC-001 - ESCALATED to human** [P3_next_working_day, financial_decision, respond within 1 working day]
  Summary: Copper Finch Mechanical attended 7 Larkspur Fold on 5 Feb to diagnose intermittent radiator heating. The landlord authorised diagnosis only, up to £180 incl. VAT. The contractor found an actuator fault and sent a £372 incl. VAT replacement estimate, which the landlord has not approved. On 10 Feb the contractor sent two invoices: A for £138, which matches the diagnostic quote, and B for £372, which claims actuator replacement on 5 Feb and repeats A's attendance, diagnosis and testing charges. There is no authorisation, completion record or parts record, and the tenant has seen no contractor since 5 Feb. When asked, the contractor could not explain the invoices (event-022). Meanwhile the heating repair has stalled for a week, and the tenant, who has a child, has intermittent heating.
  Why a human: This is a billing dispute with a contractor over an invoice for unauthorised and apparently undone work, and there may be a billing irregularity. Deciding whether to pay, part-pay or reject, and whether to keep using this contractor, is a money and liability decision beyond my authority. The heating repair has also stalled with a child in the home, so a human may want to propose a second contractor or quote to the landlord.
  Recommended: Do not pay either invoice until the contractor clarifies in writing. Invoice A (£138) looks payable once the contractor confirms invoice B is withdrawn or does not repeat its charges.; Reject invoice B unless dated attendance and parts evidence is produced. Even then, the work was never authorised.; If the contractor has not replied by 14 Feb, phone Petra Quill and consider proposing to the landlord a second heating engineer to quote for the actuator repair.; Once the landlord replies, record his decision and arrange the repair quickly, given the child at the property.

**HOLD-001 - Case put on hold** (waiting_for_landlord): waiting for Two replies. From Soren Dallow: his instruction on the repair and the invoices (event-023). From Petra Quill (Copper Finch): clarification or withdrawal of invoice B, evidence of any work, and answers to the repair-option, parts and breakdown questions, due by 12:00 on 14 Feb (MSG-001).. Follow up 2025-02-14T12:00:00Z; if nothing arrives: Phone Petra Quill and Soren Dallow. Ask the human reviewer to propose a second heating engineer's quote to the landlord. Send the tenant the promised update by end of 14 Feb, and bring the follow-up forward if the tenant reports a total loss of heating.

## Escalation

Escalated to a human: see the ESC entry above.

## What failed

- none

## Next step

**agency**: Review the landlord's and contractor's replies. If none, phone both, and ask the human reviewer to propose a second heating engineer's quote. Update the tenant by 14 Feb. (by 2025-02-14T12:00:00Z)

## Final result

`escalate`: The landlord was emailed minutes ago (event-023), so sending him another request now would duplicate it. Instead I: recorded both invoices, with A on hold and B disputed (FIN-001, FIN-002); told the contractor in writing that B is not accepted, nothing is to be paid yet and no further work is authorised, with a deadline of 12:00 on 14 Feb to clarify or withdraw B and to answer the landlord's event-012 questions (MSG-001); and gave the tenant, who has a child at home and has not been updated since 6 Feb, a status update and safety advice (MSG-002). The billing dispute and possible irregularity is a money and liability decision beyond my authority, so I escalated it without blocking routine follow-ups (ESC-001). Hold HOLD-001 follows up on 14 Feb.
