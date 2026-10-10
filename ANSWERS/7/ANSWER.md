# Case property-management-test-cases-007: decision at 2025-09-17T09:04:05Z

**Decision:** `act`  |  **Risk:** routine  |  **Escalated:** no  |  **Confidence:** high

## What the system received

- Case input: `Property_Management_test_cases/007`, 19 visible event(s), history cut at the end of the supplied history

- Documents read: none

## Decision point

The electrician (Bracken Spark Services) proposed 29 September after 15:00 (event-019). The agency needs to confirm the appointment and settle what the visit covers: the landlord approved the TV only, he is unsure the TV is his, the light has not been approved, and a door-handle issue was raised in passing.

## Situation

At 8 Vellum Court, the tenant reported a TV in the upstairs bedroom that trips the electrics and a downstairs bedroom light that flickers and pops. The landlord approved dealing with the TV (event-003) but said he doesn't remember leaving one. The light was never put to him. The tenant gave availability (event-016) and the electrician picked 29 Sept after 15:00 (event-019), which matches. The tenant also mentioned on a call that the rear-door handle has come off (event-015), but has not reported it separately.

## Actions taken

**DEC-001 - Landlord decision recorded:** approved: Electrician to attend and diagnose the reported fault with the television in the upstairs bedroom (tripping when plugged in), including checking the socket/circuit. Does NOT cover the downstairs bedroom light, the rear-door handle, or replacement/disposal of the TV. (evidence event-003)

**JOB-001 - Contractor instructed:** Bracken Spark Services (electrical, attend_diagnose_and_quote, routine), cap £120.00, authorised by landlord_decision (DEC-001)
  - MSG-001 email to contractor (Rian Sol): *New job JOB-001: electrical at 8 Vellum Court, Brindlewick, ZZ1 1ZZ*

**APT-001 - Appointment booked** for JOB-001: 2025-09-29T14:00:00Z to 2025-09-29T17:00:00Z, access: tenant_present

**MSG-002 - Email to contractor (Rian Sol)** (instruction): *Confirmed: Monday 29 September after 15:00 - 8 Vellum Court, Brindlewick (JOB-001)*
> Dear Rian,
>
> Thank you for your email. We confirm your visit to 8 Vellum Court, Brindlewick, ZZ1 1ZZ on Monday 29 September, after 15:00. The tenant has offered that slot. Please let us know an approximate arrival time if you can, so we can pass it on.
>
> Access: the tenant will be at home and will take the dog out during the visit. Please phone the tenant when you arrive rather than knocking.
>
> Scope (JOB-001):
> 1. Upstairs bedroom TV: the tenant reports it trips the electrics when plugged in. It is currently unplugged. Please test the socket and circuit, confirm whether the fault is in the TV or in the property's installation, and send us your findings. Please do not repair, remove or dispose of the TV unless we instruct you in writing. We are still confirming with the landlord who owns it.
> 2. Downstairs bedroom light (flickering and popping when switched on): we are getting the landlord's approval for this. We will confirm before the visit whether you can inspect it on the same day.
>
> Spend limit for this visit is £120 including VAT, covering attendance and diagnosis. Please send a quote with photos before doing any further chargeable work.
>
> If you find anything unsafe while on site, please make it safe and tell us straight away.
>
> Kind regards,
> Oren Pike
> Maintenance Coordinator, Northbridge Lettings

**MSG-003 - Email to tenant (Ada Pell)** (status_update): *Electrician booked Monday 29 September after 15:00 - 8 Vellum Court*
> Dear Ada,
>
> Thank you for sending your availability. The electrician, Rian Sol of Bracken Spark Services, will visit 8 Vellum Court on Monday 29 September, some time after 15:00. We have asked him to phone you when he arrives rather than knock, and we have told him you will take the dog out during the visit. If he gives us a more exact arrival time, we will pass it on.
>
> He will look at the TV fault in the upstairs bedroom. We are also arranging for him to check the downstairs bedroom light on the same visit and will confirm this before the day.
>
> Until then, for your safety:
> - Please keep the downstairs bedroom light switched off and keep using your lamp. Please don't take the fitting apart or change anything on it.
> - Please keep the TV unplugged and don't try any more fuses.
> - If you notice a burning smell, scorch marks, sparks or smoke from the light, switch or any socket, turn the power off at the fuse box (consumer unit) if it is safe to do so, and phone us straight away. If there is smoke or fire, leave the property and call 999.
>
> Two quick questions, please:
> 1. Was the TV provided with the property when your tenancy started, or does it belong to you? This decides who is responsible for it, so please don't dispose of it yet. We will confirm the next steps once we have checked.
> 2. The rear-door handle you mentioned to my colleague on the phone: please reply with a short description and a photo if you can. Also, can the rear door still be shut and locked securely? If it can't be secured, please tell us as soon as possible so we can deal with it urgently.
>
> Kind regards,
> Oren Pike
> Maintenance Coordinator, Northbridge Lettings

**APR-001 - Landlord approval requested** (attend_and_diagnose): Approve light inspection and fix on the day up to £150 inc VAT £150.00 (includes_vat); Inspect and quote only for the light £0.00 (includes_vat); Landlord to arrange own electrician for the light; reply due 2025-09-22T09:04:05Z
> Dear Corin,
>
> Thank you for your instruction on 5 September to deal with the TV at 8 Vellum Court, Brindlewick, ZZ1 1ZZ. Our electrician, Bracken Spark Services, will visit on Monday 29 September. On your instruction, they will test the TV and the socket/circuit to find out whether the fault is in the TV or the property's wiring. The diagnosis is capped at £120 including VAT.
>
> We need your decision on two more points, please:
>
> 1. Downstairs bedroom light. The tenant's original report also said that the downstairs bedroom ceiling light flickers and makes a popping sound when switched on. That was not part of our first request to you. A popping light can mean a loose connection or a failing fitting, so it should be checked. We have told the tenant to keep the light switched off for now, and they are using a lamp. May the electrician inspect the light on the same visit and fix it on the day if the cost is no more than £150 including VAT? Anything above that would come back to you as a quote first.
>
> 2. The TV. You mentioned you don't remember leaving a TV, and we have asked the tenant whether it came with the property. Could you confirm whether it is yours? If it is yours and turns out not to be worth repairing, would you like it disposed of, and would you want it replaced? If it isn't yours, it is the tenant's responsibility and we will not spend your money on it beyond the circuit check.
>
> Separately, the tenant has mentioned that the rear-door handle has come off. We have asked them for details and a photo, and we will come back to you with a proposal once we have them.
>
> A reply by Monday 22 September would let us confirm the full scope with the electrician before the visit.
>
> Kind regards,
> Mina Voss
> Property Manager, Northbridge Lettings

**ITEM-001 - Open item open**: Rear-door handle has come off (raised by tenant on call only, event-015/018). Awaiting tenant details/photo and confirmation the door can still be secured; then seek landlord approval for a handyman/locksmith. Escalate to urgent if the door cannot be locked.

**ITEM-002 - Open item open**: TV ownership and disposal: landlord said he does not remember leaving a TV (event-003); tenant open to it being discarded (event-015). Confirm ownership (landlord/tenant/inventory) and landlord's instruction on repair, disposal or replacement before any work beyond diagnosis.

**HOLD-001 - Case put on hold** (waiting_for_landlord): waiting for Landlord Corin Wex's decision on the downstairs bedroom light (APR-001, up to £150 inc VAT) and confirmation of TV ownership and disposal; tenant's reply on TV ownership and rear-door handle details; Bracken Spark's approximate arrival time for 29 Sept.. Follow up 2025-09-22T09:30:00Z; if nothing arrives: Phone the landlord (he had an out-of-office earlier) to get a decision on the light before the 29 Sept visit. If there is still no decision, tell the electrician the visit covers the TV/circuit only and that he may inspect and quote the light without doing any repair. Chase the tenant by SMS about the door handle and whether the door can be secured.

**NOTE-001 - Internal note** (decision_rationale): Electrician's proposed slot (event-019, 29 Sept after 15:00) matches the tenant's availability (event-016), so it has been confirmed to both parties (APT-001, JOB-001). The landlord's approval (event-003) covered the TV only, with no cap, and he was unsure he owns the TV. Recorded as DEC-001 with a £120 inc VAT diagnosis cap, and the contractor has been told not to repair or dispose of the TV. The downstairs light was never put to the landlord (event-002/005). Approval is now requested as APR-001, and the tenant has been given safety advice to keep the light off. The tenant is using a lamp (event-015), so this is routine, not an emergency. The rear-door handle was raised by phone only (event-015/018). The tenant has been asked for details and whether the door can be secured, and an open item is set. Minor data point: in the event-015 call the tenant said their partner made the original report, but event-001 is attributed to Ada Pell. This doesn't affect the decision.

## Escalation

Not escalated.

## What failed

- none

## Next step

**agency**: Check for the landlord's decision on the light and TV ownership, the tenant's reply on the door handle and the TV, and the contractor's arrival time. Phone the landlord if he hasn't replied, then confirm the final scope with Bracken Spark before 29 Sept. (by 2025-09-22T09:30:00Z)

## Final result

`act`: The proposed slot matches the tenant's availability, so we confirmed it to both the contractor and the tenant, with the access instructions about the dog and calling on arrival (MSG-002, MSG-003). The landlord's instruction in event-003 covers the TV only, with no cap. It was recorded as DEC-001 with a conservative £120 inc VAT diagnosis cap. Because ownership is unclear, the contractor must not repair or dispose of the TV without written instruction. The downstairs light was never included in a landlord request (event-002/005), so approval was requested now (APR-001, fix on the day up to £150 inc VAT), with a reply due before the visit. The same email asks him to confirm TV ownership and what to do with it. The tenant got safety advice to keep the light off and was asked who owns the TV, plus details of the door handle and whether the door can still be secured. Open items track the handle and TV ownership, and a hold with a phone-call fallback is set for 22 Sept.
