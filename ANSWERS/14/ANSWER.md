# Case property-management-test-cases-014: decision at 2025-01-14T17:08:00Z

**Decision:** `escalate`  |  **Risk:** urgent  |  **Escalated:** yes  |  **Confidence:** high

## What the system received

- Case input: `Property_Management_test_cases/014`, 19 visible event(s), history cut at the end of the supplied history

- Documents read: none

## Decision point

The contractor offered a cancellation slot for 15 Jan 09:00–11:00 that had to be booked by 17:30 (event-019). The tenant, who needs extra support, reported 10°C and asked for an update before the office closed (event-018). Nobody holds authority to spend on interim heating or transport (event-017).

## Situation

Heating failure at 7 Mallowmere Walk since this morning: radiators cold, boiler display blank, hot water still working, no gas smell. Tenant Leah Venn has a mobility impairment and the living room is down to 10°C. Her plug-in heater is unsafe and she has stopped using it. The landlord confirmed the £250 per-incident urgent-repair authority covers the £168 diagnostic (event-014). The standing authority doesn't cover a temporary heater, transport or accommodation, and the duty file has no limit for them.

## Actions taken

**DEC-001 - Landlord decision recorded:** approved_with_limit, limit £250.00: Standing urgent-repair authority for this heating failure: agency may authorise the £168 (incl. VAT) diagnostic call-out by Brackenridge Heat Services and any further repair work, provided the incident total (diagnostic, labour and parts) stays within £250 incl. VAT. Does NOT cover temporary heaters, transport or accommodation. (evidence event-014)

**JOB-001 - Contractor instructed:** Brackenridge Heat Services (gas_heating, attend_diagnose_and_quote, urgent), cap £250.00, authorised by landlord_decision (DEC-001)
  - MSG-001 email to contractor (Daniel Hart): *New job JOB-001: gas heating at 7 Mallowmere Walk, Larkfen, ZZ1 1ZZ*

**CALL-001 - Phone call to contractor (Daniel Hart)** (arrange_access); outcome: awaiting_response
> Hi Daniel, it's Maya Chen at Northbridge Lettings, calling back about 7 Mallowmere Walk, Larkfen. Please book the cancellation slot for tomorrow, Wednesday 15 January, 09:00 to 11:00, for Leah Venn's heating fault. Our job reference is JOB-001 and the full instruction is in your email now. The £168 including VAT diagnostic is authorised under the landlord's urgent-repair authority. If you can fix it on the day and the total for the incident stays within £250 including VAT, go ahead; anything above that, please make safe and send us a written quote the same day. Access: Leah must be present. Please have the engineer phone her directly at least 30 minutes before arriving and call again from outside on arrival; she needs extra time to get to the door. Please don't arrive unannounced. Nobody else at the flat can give access. I'm confirming access with Leah this evening and will let you know straight away if anything changes. Can you confirm the slot is booked and give me the engineer's name?

**APT-001 - Appointment booked** for JOB-001: 2025-01-15T09:00:00Z to 2025-01-15T11:00:00Z, access: tenant_present

**CALL-002 - Phone call to tenant (Leah Venn)** (arrange_access); outcome: awaiting_response
> Hello Leah, it's Maya Chen from Northbridge Lettings, with the update you asked for. Good news: Brackenridge Heat Services had a cancellation and we have booked their heating engineer for tomorrow, Wednesday 15 January, between 9 and 11am. The engineer will phone you directly at least 30 minutes before arriving and will call you again from outside so you have time to get to the door. They won't arrive unannounced, and I've only told them you need extra time to answer the door. Can you confirm you'll be at home and able to let them in during that window? Is the best number for them to call the one we have on file? On tonight: please keep not using that plug-in heater. Our duty manager is working on whether we can get a heater delivered or help with transport to your niece's this evening; I can't promise that yet but we'll call you back tonight either way. Have you been able to check whether your niece's entrance is step-free, and would you prefer to go there if transport can be arranged? Meanwhile, please keep to one room, close the curtains and doors, wear warm layers, use blankets and hot drinks, and use the hot water, for example a hot-water bottle, carefully. If you feel unwell, very cold or confused, call NHS 111, or 999 in an emergency. And if you ever smell gas, leave the flat, don't use switches or flames, and call 0800 111 999.

**MSG-002 - Email to tenant (Leah Venn)** (status_update): *Heating engineer booked for Wednesday 15 January, 09:00–11:00 – 7 Mallowmere Walk*
> Dear Leah,
>
> Thank you for your update this afternoon, and I'm sorry the flat has got so cold. Here is where things stand.
>
> Heating repair
> Brackenridge Heat Services had a cancellation, and we have booked their engineer to visit 7 Mallowmere Walk tomorrow, Wednesday 15 January 2025, between 09:00 and 11:00. They will look at the boiler and controller and repair it on the day if they can. If more work is needed, we will arrange it as quickly as possible.
>
> As you asked, the engineer will phone you directly at least 30 minutes before arriving and will call again from outside, so you have time to get to the door. They won't arrive unannounced. All we have told them is that you need extra time to answer the door. We haven't shared any medical details.
>
> Please reply, call or text to confirm you can let the engineer in during that window, and tell us the best number for them to call. If anything changes, let us know as soon as possible so we can tell the engineer.
>
> Tonight
> Our duty manager is looking into getting a heater delivered or helping with transport to your niece's home. I can't confirm this yet, but we will contact you again this evening either way. It would help to know whether your niece's entrance is step-free and whether you'd prefer to stay there tonight.
>
> In the meantime:
> - Please keep not using the plug-in heater whose casing was getting hot. The heating engineer has also advised against using it.
> - Try to keep to one room with the door and curtains closed. Wear warm layers, use blankets, and have hot drinks and food. You still have hot water, so a hot-water bottle filled carefully can help.
> - If you feel unwell, very cold or confused, call NHS 111, or 999 in an emergency.
> - If you ever smell gas, leave the flat, don't use switches or naked flames, and call the National Gas Emergency line on 0800 111 999.
>
> Kind regards,
> Maya Chen
> Property Manager, Northbridge Lettings

**APR-001 - Landlord approval requested** (approve_works): Authorise delivery of an oil-filled/convector heater from an approved supplier tonight, up to a limit you set; Authorise transport (taxi suitable for a tenant with limited mobility) to the tenant's niece's home tonight, up to a limit you set; Decline interim costs; reply due 2025-01-14T19:08:00Z
> Dear Owen,
>
> Thank you for confirming the £250 urgent-repair authority earlier today. Here is an update on the heating at 7 Mallowmere Walk, Larkfen, ZZ1 1ZZ, and one decision we need from you tonight.
>
> 1. Repair booked (for your information)
> Brackenridge Heat Services offered a cancellation slot, and we have booked it for tomorrow, Wednesday 15 January, 09:00–11:00. This is the fixed diagnostic call-out at £168 including VAT, authorised under your urgent-repair authority. I've told the engineer they may complete a repair on the day only if the total for the incident, including the call-out, stays within £250 including VAT. Anything above that will come back to you with a written quote.
>
> 2. Interim heating tonight: your decision needed
> Leah measured 10°C in the living room at 16:25, down from 12°C this morning. She has a mobility impairment and needs extra support. Her only plug-in heater overheats, and the heating engineer has advised her not to use it. Your urgent-repair authority doesn't cover temporary heaters, transport or accommodation, and the agency has no separate authority for these. The options are:
> - Heater delivery: our office is checking approved suppliers for a heater that can be delivered so Leah doesn't have to carry it.
> - Transport: Leah may be able to stay with her niece tonight if transport can be arranged. She is still checking whether the entrance there is step-free.
>
> Could you reply to say whether you authorise either or both, and the maximum you are happy to spend (including VAT)? Leah's temperature is falling and the office is closing, so a reply as soon as possible, ideally within the next two hours, would help a great deal. If it's easier, please phone the office.
>
> Kind regards,
> Maya Chen
> Property Manager, Northbridge Lettings

**ESC-001 - ESCALATED to human** [P1_immediate, complaint_or_vulnerability, respond within 15 minutes]
  Summary: Tenant Leah Venn at 7 Mallowmere Walk has had no central heating since this morning (boiler display blank, controller unresponsive; hot water still works; no gas smell). Living-room temperature fell from 12°C (10:10) to 10°C (16:25). She has a mobility impairment and her only plug-in heater overheats; the heating engineer advised her not to use it. Diagnostic visit now booked with Brackenridge Heat Services for 15 Jan 09:00–11:00 (£168 incl. VAT) under the landlord's £250 urgent-repair authority. Tonight she needs interim warmth: a delivered heater or transport to her niece's home. Neither is covered by any authority the agency holds. Landlord asked by email (APR-001) but he is travelling and may not reply quickly.
  Why a human: The tenant needs extra support and is in a cold home overnight. Interim measures (heater delivery, transport, accommodation) need spending authority the agent doesn't have: the duty file records no limit (event-017) and the landlord's authority excludes them (event-007). The duty manager needs to arrange a heater supplier tonight and either get the landlord's agreement by phone or decide whether the agency will fund or underwrite interim measures.
  Recommended: Before the office closes, phone Daniel Hart to confirm the 15 Jan slot is held; Phone Owen Pike for verbal agreement to a heater delivery or transport and a spending limit; record it with a note; Get a price and delivery time from an approved supplier for a heater delivered tonight (oil-filled radiator or convector); If the landlord can't be reached, decide whether the agency will fund or underwrite a heater or transport for a tenant in a cold home overnight, given her vulnerability; Call Leah back tonight with the outcome, whatever it is, as promised; check whether her niece's home is step-free and her wellbeing; If Leah can't confirm access for 15 Jan, tell Brackenridge and ask about the next earliest slot (she can't guarantee 17 Jan)

**HOLD-001 - Case put on hold** (waiting_for_tenant): waiting for Leah Venn's direct confirmation of access for 15 Jan 09:00–11:00 (CALL-002/MSG-002); Brackenridge's confirmation that the slot is held (CALL-001); landlord's decision on interim heater or transport (APR-001, due 19:08).. Follow up 2025-01-14T19:00:00Z; if nothing arrives: Phone Leah again and check on her welfare. Phone Daniel Hart to confirm the slot is held. Phone the landlord. If there is still no landlord decision, pass to the on-call manager (ESC-001) to decide on agency-funded interim measures. Tell Brackenridge immediately if Leah cannot give access.

**NOTE-001 - Internal note** (decision_rationale): Treated as an urgent repair (vulnerable tenant, 10°C, January), so the £168 diagnostic was booked under the landlord's £250 standing authority (event-014, DEC-001) before the 17:30 cut-off (event-019). The contractor's cap of £250 incl. VAT covers the whole incident; anything more needs landlord consent. The safety screen's gas match comes from Maya's own question in event-002; the tenant confirmed no gas smell (event-003), so it is not a live hazard. The suspect plug-in heater is a fire risk, but the tenant has stopped using it (event-013). Tenant asked that medical details not go to contractors (event-004); the contractor was told only 'needs extra time to answer the door'. The niece (Erin Vale) cannot give access. The tenant can't guarantee access on 17 Jan (hospital appointment), so if the 15 Jan slot falls through, rebook for another date. Interim heater or transport is outside any authority; it is with the landlord (APR-001) and on-call manager (ESC-001).

## Escalation

Escalated to a human: see the ESC entry above.

## What failed

- none

## Next step

**human_reviewer**: On-call manager: confirm the 15 Jan slot is held, get the landlord's verbal decision on a delivered heater or transport (or decide whether the agency will fund it), and call Leah back tonight with the outcome and to check her welfare. (by 2025-01-14T19:00:00Z)

## Final result

`escalate`: The early slot would be lost after 17:30, and the standard 17 Jan date clashes with the tenant's hospital appointment (event-013). So we booked it immediately under the landlord's confirmed urgent-repair authority (event-014 → DEC-001, JOB-001, APT-001, CALL-001), with a £250 incl. VAT incident cap and work above that referred for consent. Leah said she can admit someone on 15 Jan with 30 minutes' notice and a direct call (event-013). The contractor wants her direct confirmation, so we called her (CALL-002) and emailed (MSG-002) with the booking, access arrangements, warmth and safety advice, and a promise to call back tonight. Interim warmth is outside any authority (events 007, 017). We asked the landlord with a 2-hour deadline (APR-001) and escalated P1 to the on-call manager (ESC-001), because the tenant needs extra support and her home is getting colder overnight. A hold at 19:00 makes sure everything is followed up tonight.
