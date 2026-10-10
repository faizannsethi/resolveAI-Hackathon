# Case property-management-test-cases-017: decision at 2025-02-12T16:10:00Z

**Decision:** `wait`  |  **Risk:** routine  |  **Escalated:** no  |  **Confidence:** high

## What the system received

- Case input: `Property_Management_test_cases/017`, 19 visible event(s), history cut at the end of the supplied history

- Documents read: attachments/fire-door-quotation.pdf

## Decision point

Landlord asked whether the £186 decorating quote can be approved from the repair budget, and wants the scope and building response before booking (event-017). The building manager's reply to the scope query is pending (event-018). The tenant's question of 10 Feb (event-015) has had no reply.

## Situation

The fire-resisting flat entrance door has flaking paint and catches at the top. It latches only with a firm pull and was noted as closing slowly in last month's building check. Pale Finch quoted £186 (VAT unclear) for decorating only, valid until 28 Feb, excluding adjustment and any fire-door inspection. The landlord has not formally approved. The building manager is still to reply on the scope. Nothing is booked.

## Actions taken

**MSG-001 - Email to landlord (Elian Moss)** (status_update): *14 Lantern Mews – entrance door quotation: scope, approval and building response*
> Dear Mr Moss,
>
> Thank you for your email of 11 February about the flat entrance door at 14 Lantern Mews, Brindlewick, ZZ1 1ZZ.
>
> On your question about the repair budget: Northbridge Lettings has no authority to approve chargeable work for you. Any spend needs your clear written approval. Nothing has been booked, and as you asked, we will not book anything until the scope and the building's response have been confirmed to you.
>
> Proposed scope (Pale Finch Decorating, quotation NBL-017-Q1 dated 7 February 2025, attached)
> - Protect the work area on the flat side of the entrance door.
> - Lightly sand loose coating on the flat-side face and the visible top edge.
> - Spot-fill minor marks, then apply one undercoat and two finish coats of water-based interior paint to those areas.
> - Tidy the area afterwards.
> - Total: £186.00 including materials and labour. The quotation does not say whether VAT applies, so we will confirm this before asking for your approval. The price is valid until 28 February 2025 (the contractor reconfirmed this on 11 February).
> - Exclusions: the quotation is for decorating only. It excludes any adjustment of the door, frame or hinges, any hardware, seal or threshold work, and any fire-door inspection, certification or fire-safety opinion. Any damage found under the paint would be priced separately before work goes ahead.
>
> Building response
> The building manager, Ravi Dast, has told us the building file lists the flat entrance doors as fire-resisting doors. A common-area check last month noted this door as closing slowly, but no measurements or door-set inspection were recorded. He has asked to be consulted before any change to the door or its hardware. On 12 February we sent him the decorating scope and asked whether it needs building approval or particular materials or methods. We are waiting for his reply and will chase him if we have not heard by 14 February.
>
> Our recommendation
> Painting alone would deal with the flaking paint but not with the door catching at the top or closing slowly. Because this is a fire-resisting entrance door, it needs to close and latch fully by itself. Extra paint on the top edge where it already rubs could make the catching worse, and seals on a fire door must not be painted over. We therefore suggest:
> 1. Wait for the building manager's reply before approving the decorating.
> 2. Consider having a competent fire-door inspector or joiner (agreed with building management) assess why the door is catching and closing slowly, and quote for any adjustment. We would get that price for your approval first. You have not yet told us whether you would consider extra inspection costs, so please let us know.
>
> When we have the building manager's reply, we will send you a final scope and ask for your formal approval. The tenant has confirmed the door currently latches when pulled firmly.
>
> Kind regards,
> Maya Chen
> Property Manager, Northbridge Lettings

**MSG-002 - Email to tenant (Iona Vale)** (status_update): *14 Lantern Mews – update on your entrance door*
> Dear Ms Vale,
>
> Thank you for your message of 10 February, and for letting the decorator in on 7 February.
>
> You asked whether painting would affect the door. The decorator's proposal covers only light sanding and repainting of the flat-side face and the top edge. It would not change the door, its hardware or its seals. Because your entrance door is a fire-resisting door, we are checking with the building manager first in case the building needs particular materials or methods. We are also discussing with your landlord how to deal with the door catching at the top, which painting alone would not fix.
>
> No work has been booked. We will give you advance notice before any further visit, and we will keep to visits after 10:00 as you asked. Nobody will photograph your personal belongings.
>
> In the meantime, please make sure the door is fully closed and latched each time you use it, and do not prop it open. If it stops latching, will not close, or gets noticeably harder to close, please tell us straight away on the portal or by phone. In any fire, get out and call 999.
>
> We expect to update you again after we hear back from the building manager, which we hope will be in the next few days.
>
> Kind regards,
> Maya Chen
> Property Manager, Northbridge Lettings

**FIN-001 - Quote/invoice recorded:** quote from Pale Finch Decorating £186.00 (unknown, gross £186.00), payer landlord, route undecided

**ITEM-001 - Open item open**: Building manager (Ravi Dast) to say whether the decorating scope needs building approval or specified materials or methods, and to send any door-record information about the top-edge contact and slow closing.

**ITEM-002 - Open item open**: Fire-resisting flat entrance door catches at the top and was recorded as closing slowly. The decorating quote does not cover this. Landlord to decide whether to fund a competent fire-door or joinery inspection and quote for adjustment, coordinated with building management. No formal approval for the £186 decorating yet.

**NOTE-001 - Internal note** (decision_rationale): Safety screen 'fire' matches (event-005, 010, 011) come from wording about fire-resisting doors and fire-performance exclusions. There is no live fire or smoke, so no emergency dispatch. This is a compliance and maintenance concern: a fire-resisting flat entrance door catching at the top and recorded as closing slowly (event-013); it latches only with a firm pull (event-015). Landlord's event-017 asks whether the quote can be approved from the repair budget. That is not a clear approval, and he asked for the building response before booking. So no decision has been recorded and no job assigned. Replied to the landlord (MSG-001) and to the tenant's unanswered event-015 (MSG-002). VAT on the £186 quote is unclear; confirm with Pale Finch before the formal approval request. Household includes a family member with home-care visits (event-003): visits after 10:00 with advance notice.

**HOLD-001 - Case put on hold** (waiting_for_third_party): waiting for Reply from building manager Ravi Dast to the 12 Feb scope query (event-018), and the landlord's response to MSG-001 on next steps and extra inspection costs.. Follow up 2025-02-14T10:00:00Z; if nothing arrives: Phone and email Ravi Dast to chase the scope and door-record answer. Chase the landlord if he has not replied. Update the tenant. Then send the landlord a formal approval request (with VAT confirmed by Pale Finch) well before the quote expires on 28 Feb.

## Escalation

Not escalated.

## What failed

- none

## Next step

**agency**: Chase the building manager if he hasn't replied. Confirm VAT with Pale Finch. Send the landlord a formal approval request with the final scope, plus an option for a fire-door or joinery assessment. Update the tenant. (by 2025-02-14T10:00:00Z)

## Final result

`wait`: The landlord's message is a question, not an approval, and he asked for the building response before booking. So no decision was recorded and no job assigned. I replied to him (MSG-001): the agency has no spending authority, set out the scope and exclusions, and recommended waiting for the building manager and getting a fire-door or joinery assessment of the closing problem, since painting alone won't fix it and could make the rubbing worse. I answered the tenant's unanswered event-015 (MSG-002), confirmed advance notice and visits after 10:00, and gave door-safety advice. The building manager was only asked this morning, so I set a hold until 14 Feb with a chase planned.
