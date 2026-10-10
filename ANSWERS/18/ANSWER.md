# Case property-management-test-cases-018: decision at 2025-09-11T14:30:00Z

**Decision:** `request_information`  |  **Risk:** urgent  |  **Escalated:** no  |  **Confidence:** medium

## What the system received

- Case input: `Property_Management_test_cases/018`, 19 visible event(s), history cut at the end of the supplied history

- Documents read: none

## Decision point

The landlord-arranged rat proofing visit (8 Sep) did not happen, and the agency's repeated wait periods for a landlord update have expired with no response (event-018). We need to decide how to move the stalled works forward.

## Situation

The tenant reported rats in the kitchen at 14 Mosswold Crescent on 14 Aug. The landlord chose to arrange the work himself (event-007). The pest treatment visits appear to have finished on 7 Sep (event-014). The separate contractor expected on 8 Sep to seal the openings did not come (event-017). Since 18 Aug the landlord has sent no update in writing and has not confirmed completion or provided a pest report. The agency's internal waits have lapsed twice (events 013, 015, 016, 018).

## Actions taken

**CALL-001 - Phone call to landlord (Gareth Vale)** (chase_response); outcome: awaiting_response
> Hello Mr Vale, this is Northbridge Lettings calling about the rat problem at 14 Mosswold Crescent, Brindlewick. We understand from Ms Rowan that your pest controller made what was expected to be the final visit on Sunday 7 September and removed their equipment. However, the contractor she expected on Monday 8 September to seal the openings by the kitchen sink and wall did not attend, and we have had no update from you since. Until those openings are sealed, the rats could come back in. Please could you tell us: 1) who is doing the proofing work and their contact details; 2) the new date for the visit; 3) whether the pest controller has given you a written report or completion note, and if so, could you send us a copy; 4) whether you would like Northbridge Lettings to arrange the proofing instead, in which case we would get a quote for you to approve first. We would like a date by tomorrow, Friday 12 September, so we can keep the tenant updated. Thank you.

**MSG-001 - Email to landlord (Gareth Vale)** (chase): *14 Mosswold Crescent – rat proofing visit missed: date and contractor details needed*
> Dear Mr Vale,
>
> I'm following up on the rat problem at 14 Mosswold Crescent, Brindlewick, ZZ1 1ZZ. You are arranging this work yourself, as agreed on 18 August. We have also just tried to reach you by phone.
>
> Ms Rowan has told us:
> - Your pest controller attended on Sunday 7 September and removed their equipment. She understood this to be the final treatment visit.
> - She was expecting a separate contractor on Monday 8 September to seal the openings by the kitchen sink and wall, but nobody came.
>
> We have had no update from you since then. Until the entry points are sealed, the rats are likely to come back, so we would like to get the proofing work booked quickly.
>
> By tomorrow, Friday 12 September, please could you let us know:
> 1. Who is doing the proofing work, and the new date for their visit.
> 2. What exactly they will be doing (for example, sealing the openings under the sink or working on the wall area, and any outside openings near the drain).
> 3. Whether the pest controller has given you a written report or completion note. If so, please send us a copy for the property file.
> 4. Once the proofing is done, please confirm it to us so we can check with the tenant and close the matter.
>
> If you would prefer Northbridge Lettings to arrange the proofing instead, just say so. We would get a quote for you to approve before any work goes ahead.
>
> Ms Rowan works during the day and has asked to be contacted by phone to arrange access. Please ask your contractor to call her in advance.
>
> Kind regards,
> Tara Wren
> Property Manager, Northbridge Lettings

**CALL-002 - Phone call to tenant (Elise Rowan)** (status_update); outcome: awaiting_response
> Hello Ms Rowan, this is Tara from Northbridge Lettings calling about the rats at 14 Mosswold Crescent. I'm sorry the contractor didn't turn up on Monday to seal the openings. We have chased Mr Vale today by phone and email. We've asked him for the contractor's details and a new date, and for a reply by tomorrow, Friday 12 September. We'll call you as soon as we hear. A few quick questions: Have you seen any rats or signs of them, such as droppings, gnawing or noises, inside the house since pest control removed their equipment on Sunday? If so, where, and could you send us a photo? Has the landlord or any contractor been in touch with you about a new date? Meanwhile, please keep food, including your dog's food, in sealed containers, and keep the dog away from the area under the sink. If a contractor calls you to arrange a visit, please let us know the date. Thank you.

**ITEM-001 - Open item open**: Landlord-arranged proofing of the rat entry points (under the kitchen sink, the wall area and possibly the outside drain openings) is not confirmed as complete. The proofing visit expected on 8 Sep did not happen. Still needed: the contractor's name, a new date, confirmation of completion and the pest control report.

**NOTE-001 - Internal note** (decision_rationale): The landlord is arranging his own contractors (event-007). We have had nothing in writing from him since 18 Aug. Treatment visits appear finished (event-014), but the proofing visit on 8 Sep did not happen (event-017). Two extra wait periods have now expired with no response (event-013, event-016, event-018). Waiting passively again is not appropriate. Today we called the landlord on 07700 900184 and left a voicemail script, and sent him an email asking for a reply by Fri 12 Sep with the contractor's details, a new date, the scope of work, the pest report, or a choice to have the agency arrange the proofing (subject to a quote and his approval). We also called the tenant, who prefers phone, with an update and safety and food-storage advice. We asked her about current rat activity and whether any contractor has been in touch. Scope conflict: event-010 says openings beneath the sink, event-014 says opening or working on the wall area, and event-001 mentions outside openings near the drain. The landlord has been asked to clarify. We will not instruct an agency contractor: the landlord is using his own and has not approved any spend. If there is no response by the follow-up, escalate to a human property manager, because a landlord repair obligation is now stalled (rats in a home with a dog).

**HOLD-001 - Case put on hold** (waiting_for_landlord): waiting for Mr Vale's reply (call or email) with the proofing contractor's details, a rearranged date and scope, and the pest control report, or his request that the agency arrange the proofing. Also the tenant's answer on current rat activity.. Follow up 2025-09-12T15:00:00Z; if nothing arrives: Call the landlord again. If there is still no date or engagement, escalate to a human property manager (P2), because the landlord-arranged proofing has stalled, the previous waits have expired and rats are a risk to the tenant's health. Call the tenant to update her.

## Escalation

Not escalated.

## What failed

- none

## Next step

**agency**: Check for the landlord's reply and the tenant's answer. If the landlord has not responded, call him again and escalate to a human property manager (P2). Update the tenant by phone. (by 2025-09-12T15:00:00Z)

## Final result

`request_information`: The landlord is using his own contractors, so the agency must not instruct one or spend money. Further passive waiting is not justified: two wait periods have expired and the proofing visit was missed. The right step is an active chase by phone, which the landlord asked for in event-004, and by email. We have asked for the contractor's details, a new date, the scope of work and the pest report by Fri 12 Sep, and offered agency-arranged proofing subject to a quote and his approval. The tenant prefers phone contact (event-017), so we called her with an update, food-storage advice and questions about current rat activity. We opened an open item to track completion and set a short hold. If the landlord still does not engage, the case will be escalated to a human.
