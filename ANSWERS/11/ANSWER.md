# Case property-management-test-cases-011: decision at 2025-06-13T15:26:00Z

**Decision:** `escalate`  |  **Risk:** urgent  |  **Escalated:** yes  |  **Confidence:** high

## What the system received

- Case input: `Property_Management_test_cases/011`, 24 visible event(s), history cut at the end of the supplied history

- Documents read: none

## Decision point

The landlord (event-022) won't consider spending beyond the quoted plumbing work until she has the likely cost and timing. The contractor (event-023) has stopped work and can't price or specify an assessment of the unidentified ceiling lining. The leak keeps recurring when the tap is used. We need to get the cost and timing information without committing any spend, and keep everyone informed.

## Situation

The leaking compression joint above the kitchen ceiling can't be reached through the hatch. A pale, fibrous-looking lining that may contain asbestos is visible and has not been disturbed. There is no survey or record of past ceiling work. The landlord approved the quoted plumbing work only and wants cost and timing before anything further. The tenant, who has a young child, has stopped using the kitchen tap. The ceiling is not sagging.

## Actions taken

**MSG-001 - Email to landlord (Ossa Fenlow)** (status_update): *16 Brindlewick Mews – kitchen ceiling leak: next steps and cost/timing to follow*
> Dear Ossa,
>
> Thank you for your email this afternoon, and for checking your records again.
>
> Understood: your approval covered the quoted plumbing work only. Nothing else has been agreed or booked, and no extra cost has been committed. To recap where things stand at 16 Brindlewick Mews, Fenbarrow, ZZ1 1ZZ:
>
> - Kellan Orve (Mossbarrow Pipe Services) came back today. Through the access hatch he could see a pale, fibrous-looking lining behind the painted ceiling board. He could not identify it and did not touch it. No drilling, cutting, sampling or removal took place, and he left with the ceiling unopened.
> - The leaking joint still cannot be reached through the hatch, so the pipe repair is still needed. Iven reported a small drip this morning when the kitchen tap was used and has now stopped using that tap. The ceiling is not sagging.
> - Kellan cannot price work involving the unidentified lining or say what assessment it needs. Until the material has been identified, we will not allow anyone to cut into the ceiling.
>
> As you asked, before you decide on any further spending we are now:
> 1. Asking an accredited asbestos surveyor for a written quote and their earliest date to identify the lining in the small area that needs opening. This would normally be a targeted survey with sampling of that area only. We are asking for the price to be shown with and without VAT.
> 2. Asking Kellan whether his existing estimate still stands if the material turns out to be safe to work on, and whether the leaking pipe can be shut off at a valve he can reach without touching the ceiling. That would stop the drip in the meantime. We will also ask for the cost of doing this, if there is one.
>
> We will send you both answers as soon as we have them, which we hope will be early next week. We will not instruct anything until you have approved it in writing.
>
> Kind regards,
> Mara Voss
> Property Manager, Northbridge Lettings

**MSG-002 - Email to contractor (Kellan Orve)** (request_information): *16 Brindlewick Mews – follow-up questions after today's paused visit (no work authorised)*
> Dear Kellan,
>
> Thank you for stopping today and for leaving the ceiling and lining untouched at 16 Brindlewick Mews, Fenbarrow, ZZ1 1ZZ.
>
> The landlord has not approved anything beyond your original quoted scope. No further work is authorised at this stage. To help her decide, could you please let us know in writing:
>
> 1. Can the leaking pipe be isolated at a valve you can reach without opening or disturbing the ceiling or the lining? Would doing so leave the property without water anywhere other than the kitchen tap? Is there any cost for this, and is that cost with or without VAT?
> 2. If a specialist survey finds the lining is safe to work on, does your existing estimate for the joint repair still stand, or would anything change?
> 3. Please send any photographs you took of the joint and of the lining seen through the hatch. We may share these with the surveyor.
>
> Please do not attend or carry out any work until we confirm in writing. If you can reply by Monday 16 June, that would be very helpful.
>
> Kind regards,
> Mara Voss
> Property Manager, Northbridge Lettings

**MSG-003 - Email to tenant (Iven Rell)** (status_update): *16 Brindlewick Mews – kitchen ceiling leak update*
> Dear Iven,
>
> Thank you for letting Kellan in again today, and for telling us about this morning's drip.
>
> As explained earlier, Kellan stopped before opening the ceiling because there is a lining behind the ceiling board that has not been identified yet. The next step is to get a specialist to identify it safely before anyone cuts into the ceiling. We are now getting prices and dates and will update you early next week once the visit is agreed. We are also asking Kellan whether the leaking pipe can be shut off somewhere that doesn't involve the ceiling, to stop the drip in the meantime.
>
> Until then, please:
> - Keep not using the kitchen tap. Do not open the hatch, touch the ceiling, or drill, fix or hang anything on that part of the ceiling.
> - If there is any drip, put a container or towel underneath it and keep your child away from that area.
> - Contact us straight away if the dripping becomes steady, the stain or crack gets bigger, the ceiling starts to sag or bulge, or water reaches any light, socket or appliance. If water gets near electrics, switch off the electricity at the consumer unit if it is safe to do so. If the ceiling looks like it might come down, keep everyone out of the kitchen and phone us at once. In an emergency where anyone is in danger, call 999.
>
> If not having the kitchen tap is causing you real difficulty, please let us know so we can take this into account.
>
> Kind regards,
> Mara Voss
> Property Manager, Northbridge Lettings

**ITEM-001 - Open item open**: Landlord (event-022) needs the likely cost and timing of a specialist assessment of the unidentified ceiling lining before she will consider any spend. We still need an accredited asbestos surveyor's quote and earliest date, plus Kellan's answers on interim isolation and whether his repair estimate still stands, before going back to her for a decision.

**ESC-001 - ESCALATED to human** [P2_same_day, legal_or_compliance, respond within 4 working hours]
  Summary: The kitchen ceiling leak at 16 Brindlewick Mews has been traced to a compression joint above the ceiling (event-009). The joint cannot be reached through the hatch. The landlord approved only the quoted plumbing scope (event-013). On today's return visit, Kellan Orve (Mossbarrow Pipe Services) saw a pale, fibrous-looking, unidentified lining behind the ceiling board and stopped before drilling or cutting (events 017, 018, 023). Nothing was disturbed. There is no survey or record of past ceiling work (events 006, 013, 022). The landlord has confirmed that further spending needs the cost and timing first (event-022). The leak recurs whenever the kitchen tap is used, so the tenant has stopped using it. A young child lives in the flat.
  Why a human: The lining may contain asbestos, which brings duties under the asbestos regulations. A suitably accredited asbestos surveyor (a UKAS-accredited survey or sampling firm) needs to be sourced and asked for a quote. No such firm appears in the case and none is on our usual trade list here. The agency must also make sure no trade disturbs the material until it has been identified. A human should pick the surveyor and check the compliance approach before the landlord is asked to approve the cost.
  Recommended: Get a written quote and earliest available date from a UKAS-accredited asbestos surveying firm for a targeted survey and sampling of the roughly 30 cm area of kitchen ceiling to be opened, with prices shown with and without VAT. Share Kellan's photos if he sends them.; Send the quote, the timing and Kellan's answers to Ossa Fenlow and ask for written approval using request_landlord_approval.; If isolating the pipe is possible at nil or minimal cost, put that to the landlord as an interim step so the leak stops wetting the unidentified material.; Keep the tenant updated by Monday 16 June. Escalate urgently if the drip worsens, the ceiling sags, or water reaches electrics.

**HOLD-001 - Case put on hold** (waiting_for_third_party): waiting for An accredited asbestos surveyor's quote and earliest date (being sourced via the human escalation), and Kellan Orve's reply to MSG-002 on interim isolation, his estimate and photos. Both are needed so we can give the landlord the cost and timing she asked for in event-022.. Follow up 2025-06-16T10:00:00Z; if nothing arrives: Phone Kellan to chase his answers, and check with the human reviewer whether the surveyor has quoted. Update the landlord and tenant on progress. Act immediately if the tenant reports the leak getting worse or the ceiling sagging.

## Escalation

Escalated to a human: see the ESC entry above.

## What failed

- none

## Next step

**human_reviewer**: Get a quote and earliest date from an accredited asbestos surveyor for a targeted survey of the ceiling area. Then send it, with Kellan's answers, to the landlord for written approval. (by 2025-06-16T10:00:00Z)

## Final result

`escalate`: Nothing can go ahead until the lining has been identified (events 017, 018, 023). The landlord has made clear that any extra spending needs cost and timing first (event-022). Kellan can't provide those, so the agency has to get a quote from an accredited asbestos surveyor. No such firm appears in the case, and the matter has compliance implications, so I escalated the sourcing and compliance check to a human at P2 without blocking automation. Meanwhile I replied to the landlord confirming nothing has been committed and setting out what comes next. I asked Kellan about isolating the pipe in the meantime, whether his estimate still stands, and for photos. I sent the tenant an update with safety advice. I opened a tracked item for the landlord's request and set a hold to follow up on Monday 16 June. No spending or appointment was authorised.
