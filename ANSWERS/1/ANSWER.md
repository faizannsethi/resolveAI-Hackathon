# Case property-management-test-cases-001: decision at 2025-09-23T16:12:00Z

**Decision:** `request_information`  |  **Risk:** urgent  |  **Escalated:** yes  |  **Confidence:** high

## What the system received

- Case input: `Property_Management_test_cases/001`, 23 visible event(s), history cut at the end of the supplied history

- Documents read: attachments/bathroom-works-quotation.pdf

## Decision point

The landlord asked which quote we meant ("there are a couple"). The quote on file and the contractor's breakdown do not match, so there is no clear figure for him to approve.

## Situation

The tenant reported a recurring shower-pipe leak with damp behind the wall covering on 4 Sep. Hearthline inspected and quoted £2,370 + VAT = £2,844 (NBL-001-Q1), for cladding plus a new valve and taps. The landlord asked for an itemised breakdown. Hearthline's breakdown (£1,270 + £1,170 = £2,440 net, plus a 10% "Northbridge commission" and a 50% deposit) does not match the quote. The quote PDF also shows another property's address. The agency's vague chase (event-022) confused the landlord. No works are approved.

## Actions taken

**NOTE-001 - Internal note** (data_quality): Quote position before any approval request:
1) Only one quote is on file: Hearthline Plumbing & Bath ref NBL-001-Q1 dated 18 Sep 2025 (attachments/bathroom-works-quotation.pdf; event-016): £2,370.00 + VAT £474.00 = £2,844.00.
2) The quote PDF shows the property as 8 Wrenfold Mews, Brindlewick, not 4 Thistlewick Rise. It needs to be reissued with the correct address.
3) The breakdown in event-021 does not match the quote. Materials £1,270 + labour £1,170 = £2,440, but the quote's net figure is £2,370. The breakdown also mentions a "Northbridge commission at 10%" and a 50% deposit, without saying how either is calculated. Any commission must be explained and disclosed to the landlord. I have passed this to a human.
4) Event-022 asked the landlord to approve "the quote" without giving an amount, so the landlord was confused (event-023: "there are a couple"). He may be counting the quote and the breakdown as two quotes, or he may have a quote of his own. I have asked him.
5) Scope concern: the quote is for a cladding upgrade, but the reported fault is a recurring pipe leak (event-001). I have asked the contractor to confirm the leak source is fixed and to price an interim leak repair if possible. The leak has been ongoing since about 4 Sep, with damp behind the wall covering.
No landlord approval for the works exists yet. Event-005 authorised inspection and quote only.

**MSG-001 - Email to landlord (Orin Vale)** (status_update): *4 Thistlewick Rise – which quote: clarification on the bathroom leak works*
> Dear Orin,
>
> Thank you for your reply, and sorry our last email was unclear. It should have said which quote we meant and how much it was.
>
> For the recurring shower leak and damp wall covering at 4 Thistlewick Rise, we have one quote on file, from Hearthline Plumbing & Bath after their inspection:
>
> - Quotation ref NBL-001-Q1, dated 18 September 2025 (attached)
> - Scope: remove the existing shower screen, bath taps and shower valve; install a wall-and-riser cladding system with chrome trims; fit new bath taps and a new shower valve; refit the existing shower screen
> - Price: £2,370.00 + VAT £474.00 = £2,844.00 including VAT
>
> When you asked for an itemised breakdown, the contractor sent these figures: materials £1,270 and labour £1,170 (two people, half a day each), plus VAT at 20%. You may be counting this as a second quote. However, the figures do not add up to the original quote: £1,270 + £1,170 = £2,440 before VAT, not £2,370. The contractor's email also referred to a 10% commission to Northbridge and asked for a 50% deposit, without explaining how either is worked out. We are checking the commission internally and will tell you clearly how it affects the price, if at all. The attached PDF also shows the wrong property address.
>
> Please do not approve anything yet. We have asked Hearthline for a single corrected quotation that shows the right address, adds up properly and states the final total including VAT. We have also asked them to:
> - confirm that the work will fix the source of the leak
> - say whether the leak can be stopped with a smaller repair in the meantime, and what that would cost
>
> When we have their answer, we will send you one clear figure to approve. If you would like a second contractor to quote as well, please let us know.
>
> If you have a different quote in mind, for example one from your own contractor, please send it to us so we can compare like for like.
>
> The leak has been going on since early September and is causing damp behind the wall covering. It is worth deciding quickly once the corrected figures arrive, to limit damage to the wall and surrounding areas.
>
> Kind regards,
> Mira Sallow
> Property Manager, Northbridge Lettings

**MSG-002 - Email to contractor (Ewan Rook)** (request_information): *4 Thistlewick Rise – corrected quotation needed (ref NBL-001-Q1)*
> Dear Ewan,
>
> Thank you for inspecting the bathroom at 4 Thistlewick Rise, Larkcombe, and for the breakdown. Before we can put a price to the landlord, we need a single corrected quotation. Please:
>
> 1. Reissue quotation NBL-001-Q1 with the correct property address. The current PDF shows a different property.
> 2. Give an itemised breakdown that matches the total. Your breakdown (materials £1,270 + labour £1,170 = £2,440) does not match the quote's net figure of £2,370.00. Please state the net amount, VAT and final total including VAT.
> 3. Explain the "Northbridge commission at 10%" in your email. What is it, and is it included in or added to your price? Please do not add any commission to the price unless Northbridge has agreed it in writing.
> 4. Confirm the deposit terms: is it 50% of the gross total, and when would it be due?
> 5. Confirm that the proposed works (including the new shower valve) will fix the source of the leak behind the shower. The earlier tightening did not hold.
> 6. Tell us whether the leak can be stopped or made safe with a smaller interim repair until the full works go ahead, and what that would cost. Please do not carry out any work until you have written approval.
> 7. Confirm that the office keys used for the inspection have been returned to our office.
>
> We would be grateful for your reply by 25 September 2025, as the leak is ongoing.
>
> Kind regards,
> Mira Sallow
> Property Manager, Northbridge Lettings

**MSG-003 - Email to tenant (Nessa Quill)** (status_update): *4 Thistlewick Rise – update on the shower leak*
> Dear Nessa,
>
> Here is an update on the shower leak at 4 Thistlewick Rise. Hearthline Plumbing & Bath have inspected the bathroom and quoted for the repair. We are now confirming the final details of the quote with them so the landlord can make his decision. We will update you as soon as the work is approved and ready to book.
>
> In the meantime, could you please tell us:
> - Is the leak the same, or getting worse?
> - Is any water or damp showing outside the bathroom, for example on a ceiling below, in a neighbouring room, or near light fittings or sockets?
> - Is there any mould, and if so, roughly how big an area? Photos would be very helpful.
>
> If you can, please keep shower use to a minimum and dry off any standing water. If water ever reaches light fittings, switches or sockets, do not touch them. Turn off the electricity at the consumer unit if it is safe to do so, and call us straight away.
>
> Thank you for your patience.
>
> Kind regards,
> Mira Sallow
> Property Manager, Northbridge Lettings

**ITEM-001 - Open item open**: Get a corrected Hearthline quote (correct address, breakdown that adds up, final total including VAT, deposit terms, explanation of the 10% Northbridge commission), then send ONE clear figure to the landlord for approval. The landlord's question in event-023 ("which quote?") was answered in MSG-001, but the final figure is still to be given.

**ITEM-002 - Open item open**: Confirm the office keys used for the Hearthline inspection (event-011/012) have been returned to the office.

**ESC-001 - ESCALATED to human** [P3_next_working_day, financial_decision, respond within 1 working day]
  Summary: Recurring shower-pipe leak and damp wall covering at 4 Thistlewick Rise. The only quote is Hearthline NBL-001-Q1: £2,370 + VAT = £2,844. In the itemised breakdown (event-021), the contractor quotes materials £1,270 and labour £1,170, which comes to £2,440 net and does not match the quote. He also refers to a "Northbridge commission at 10%" and asks for a 50% deposit. The landlord was confused by a vague chase (event-022/023). I have now clarified the position with him.
  Why a human: A contractor has told us a 10% "Northbridge commission" is part of his pricing. I cannot confirm whether the agency has any such arrangement or how it must be disclosed to the landlord, and this affects what we can tell him and present for approval. The 50% deposit request also needs a decision on agency policy for paying deposits.
  Recommended: Confirm internally whether any commission arrangement with Hearthline exists. If one does, make sure it is disclosed to the landlord in writing. If not, tell Hearthline to remove it.; Decide the agency position on the 50% deposit request.; When the corrected quote arrives, send the landlord a single approval request with the gross total and VAT stated.; Consider recommending a second quote or an interim leak repair, given the size of the cladding scope compared with the reported fault.

**HOLD-001 - Case put on hold** (waiting_for_contractor): waiting for Hearthline's corrected quotation (address, breakdown that adds up, total including VAT, commission and deposit explained, interim repair option). Also waiting on the landlord's answer about any other quote, internal guidance on the commission, and the tenant's update on the leak.. Follow up 2025-09-25T16:00:00Z; if nothing arrives: Phone Ewan Rook to chase the corrected quote. If it still has not arrived, recommend to the landlord a second quote from an approved plumber and/or an interim leak repair. Chase the tenant by SMS for a leak update.

## Escalation

Escalated to a human: see the ESC entry above.

## What failed

- none

## Next step

**agency**: Get Hearthline's corrected quote and the human decision on the commission, then send the landlord a single approval request with the gross figure. If nothing arrives, chase Hearthline by phone and suggest a second quote or interim repair. (by 2025-09-25T16:00:00Z)

## Final result

`request_information`: The landlord cannot make an informed decision while the figures conflict (event-016 vs event-021). Sending a formal approval request now would put an unreconciled price in front of him. So I answered his question directly (MSG-001): there is one quote, here is exactly what it covers and costs, and here are the known discrepancies. I asked him not to approve yet and whether he has a quote of his own. I asked Hearthline for a corrected, reconciled quotation and an interim leak repair option (MSG-002). The tenant has had no update since 16 Sep, so I sent her one with damp and electrical safety advice and asked her about the leak (MSG-003). The 10% "Northbridge commission" is a disclosure and policy matter outside my authority, so I escalated it to a human without blocking routine follow-up (ESC-001). Hold set to chase on 25 Sep.
