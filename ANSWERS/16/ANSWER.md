# Case property-management-test-cases-016: decision at 2025-09-22T08:48:00Z

**Decision:** `escalate`  |  **Risk:** urgent  |  **Escalated:** yes  |  **Confidence:** medium

## What the system received

- Case input: `Property_Management_test_cases/016`, 17 visible event(s), history cut at the end of the supplied history

- Documents read: none

## Decision point

Review of NBL-016 (event-017). The smoke alarm is still unmounted more than six weeks after it was reported. The landlord's own electrician hasn't finished and has never been named. The tenant was recently hospitalised and asked for minimal contact. An unidentified visitor came to the door unannounced on 20 Sept (events 015–016).

## Situation

The landlord chose his own electrician on 7 Aug and promised completion by mid-August. A fitter came around 31 Aug, removed the bracket and couldn't refit the alarm. Nothing is confirmed since. The tenant was in hospital 5–11 Sept and asked not to be chased. On 20 Sept someone unannounced said they were there to "check something"; the tenant didn't let them in. The visitor hasn't been identified.

## Actions taken

**MSG-001 - Email to landlord (Ronan Vale)** (chase): *Urgent: smoke alarm still not refitted at 26 Tallowmere Close (NBL-016) – visitor identity and completion date needed*
> Dear Ronan,
>
> I am writing about the smoke alarm at 26 Tallowmere Close, Fenbarrow, ZZ1 1ZZ (our reference NBL-016), which the tenant reported on 7 August as having come away from the ceiling.
>
> Your email of 12 August said your electrician would complete the work by the following weekend. We still have no confirmation that the alarm has been refitted and tested. From what the tenant has told us, a fitter attended around the start of September, removed the old bracket, but could not refit the alarm because the new unit's box had no bracket in it. The alarm is still not mounted, so the property has been without a working, fixed smoke alarm on that level for over six weeks.
>
> Under the Smoke and Carbon Monoxide Alarm (England) Regulations, once a landlord is told an alarm is faulty they must repair or replace it. We therefore need to get this finished as a priority.
>
> Separately, on the morning of Saturday 20 September someone came to the property unannounced, said they were there to "check something", and did not give any identification. The tenant quite rightly did not let them in. Please could you tell us whether this was your electrician or someone else acting for you.
>
> Please could you reply by 5pm on Wednesday 24 September with:
> 1. The name, company and contact number of your electrician, so we can confirm who they are to the tenant before any visit.
> 2. Whether the Saturday visitor was sent by you or your electrician.
> 3. A proposed date for refitting the alarm (with the correct bracket or a replacement unit) and testing it. The tenant has recently been in hospital, so the visit needs to be agreed in advance with a named person and a time slot, and no unannounced visits please.
> 4. Written confirmation once the alarm is fixed and tested, ideally with a photo.
>
> If your electrician cannot complete the work within the next few days, please let us know whether you would like us to send one of our approved electricians to refit or replace the alarm. We would confirm the cost with you before any work goes ahead.
>
> Kind regards,
> Maya Chen
> Property Manager, Northbridge Lettings

**MSG-002 - Email to tenant (Elise Rowan)** (safety_advice): *Re: visitor on Saturday – 26 Tallowmere Close (NBL-016)*
> Dear Elise,
>
> Thank you for calling us on Saturday about the person who knocked at 26 Tallowmere Close. You were right not to let them in. Nobody should come into your home unless you have been told about the visit in advance and can check who they are.
>
> We know you asked us to keep contact to a minimum while you recover, and we will. We have now asked your landlord who the visitor was and for the name and contact details of his electrician. From now on, we will only contact you again once we have a named person and a proposed time for the alarm visit for you to agree. You do not need to arrange anything yourself.
>
> In the meantime, a few quick safety points:
> - If anyone turns up without notice, you do not have to let them in. Ask for ID and call us to check first.
> - Please do not touch any loose or exposed wires where the alarm used to be on the ceiling.
> - Check that you have a working smoke alarm on each floor, if you are able to. If you think there is a fire, get everyone out and call 999.
>
> There is no need to reply to this email. We hope your recovery is going well.
>
> Kind regards,
> Maya Chen
> Property Manager, Northbridge Lettings

**ITEM-001 - Open item open**: Identify the unannounced visitor on Sat 20 Sept (landlord's electrician, building management, or unknown). Tenant was told it had been passed to a building-management contact (event-016), but this hasn't been verified.

**ITEM-002 - Open item open**: Smoke alarm refit/test: landlord's own electrician (unnamed) has not completed. Need electrician details, an agreed date, and completion confirmation with test evidence. Statutory alarm compliance is outstanding since 7 Aug.

**NOTE-001 - Internal note** (decision_rationale): 22 Sept review. The alarm has been unmounted since 7 Aug (event-001). The landlord chose his own electrician (event-004) and promised completion by around 16-17 Aug (event-007), but it's still not done (events 010, 012, 013). The landlord has given no contractor name or confirmation. The tenant is vulnerable: hospitalised 5 Sept, discharged 11 Sept, and asked for no repeated contact (event-013, pause noted in event-014). The tenant reported an unannounced, unidentified visitor on 20 Sept (event-015). Their identity is unverified (event-016).
Actions: chased the landlord (MSG-001) for the electrician's identity, whether the visitor was theirs, a firm date and completion evidence, with a deadline of 24 Sept 17:00. I also offered our approved electrician, subject to cost approval. I sent the tenant one reply to their own call (MSG-002) with security and fire-safety advice. It promises no further contact until a named person and time are available. Do NOT chase the tenant for updates. Route everything via the landlord. We have no spending authority. The landlord is using their own contractor, so we won't instruct ours unless he approves.

**HOLD-001 - Case put on hold** (waiting_for_landlord): waiting for Landlord Ronan Vale's reply to MSG-001: electrician name/contact, whether the 20 Sept visitor was theirs, a proposed refit date, and completion confirmation.. Follow up 2025-09-24T17:00:00Z; if nothing arrives: Phone the landlord. If there's still no firm date, ask him to approve our approved electrician refitting or replacing the alarm, and escalate to the Maintenance Operations Lead as a smoke-alarm compliance matter. Don't contact the tenant except to confirm a verified visit.

**ESC-001 - ESCALATED to human** [P2_same_day, complaint_or_vulnerability, respond within 4 working hours]
  Summary: At 26 Tallowmere Close, the smoke alarm came off the ceiling on 7 Aug and is still not refitted after more than six weeks. The landlord (Ronan Vale) chose his own electrician but has never named them and missed his own completion date. The tenant (Elise Rowan) was recently in hospital and asked for minimal contact. On 20 Sept an unidentified person came to the door unannounced. The tenant says another agency contact told them it had been passed to building management, but that hasn't been verified on this file.
  Why a human: This combines a vulnerable tenant who has asked for limited contact, a statutory smoke-alarm repair that has been outstanding for a long time, and an unverified visitor to the property, which is a possible security or scam risk. A human needs to check the other agency contact and the building-management referral the tenant mentioned. They also need to decide whether to press the landlord harder on compliance, or take over the repair if he doesn't respond.
  Recommended: Check internally which colleague the tenant raised the visitor with, and what building management said; If the landlord hasn't replied by 24 Sept, phone him and get either a firm date or approval for our approved electrician; Consider a formal written reminder to the landlord of his obligations under the Smoke and Carbon Monoxide Alarm (England) Regulations if the delay continues; Contact the tenant only to propose a verified, pre-agreed visit, ideally by a single email

## Escalation

Escalated to a human: see the ESC entry above.

## What failed

- none

## Next step

**landlord**: Provide electrician details, confirm whether the 20 Sept visitor was his, and give a pre-agreed refit date. If he hasn't replied, the agency will phone him and seek approval for our approved electrician. (by 2025-09-24T17:00:00Z)

## Final result

`escalate`: The landlord is arranging his own contractor (event-004), so we can't instruct ours or spend without his approval. The right lever is a firm chase to the landlord (MSG-001). It asks for the electrician's identity, whether the visitor was his, a pre-agreed date and completion evidence by 24 Sept, cites his statutory duty to repair a reported faulty alarm, and offers our approved electrician subject to cost approval. The tenant asked for minimal contact (event-013), but they called us themselves about the visitor (event-015). So one considerate reply with security and fire-safety advice, promising no further contact until a verified visit can be proposed, is appropriate (MSG-002). The case involves vulnerability, a smoke-alarm compliance gap and an unverified visitor, and the tenant mentioned an agency contact and a building-management referral that aren't on this file. So I made a non-blocking P2 escalation for human review (ESC-001), with a hold to follow up at the landlord deadline.
