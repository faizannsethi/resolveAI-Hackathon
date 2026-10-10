# Case property-management-test-cases-020: decision at 2025-04-12T16:42:00Z

**Decision:** `escalate`  |  **Risk:** emergency  |  **Escalated:** yes  |  **Confidence:** high

## What the system received

- Case input: `Property_Management_test_cases/020`, 25 visible event(s), history cut at the end of the supplied history

- Documents read: none

## Decision point

The tenant is back home (event-025). The socket still smells hot, there has been no inspection or isolation and no safety guidance, and the landlord has not replied to the request for electrician authority (event-024). The agency had to decide how to deal with a live electrical hazard in an occupied home with a child present.

## Situation

A kitchen counter socket at 8 Brindlewick Row has smelled hot and been warm for more than 8 hours, including with nothing plugged in. The tenant is at home with her 10-year-old son. The circuit has not been isolated. The landlord's handyman is unqualified for fixed wiring and did not get in. The landlord has not replied about an electrician. Safety advice has now been given, an emergency make-safe electrician has been instructed with a cap of £200 including VAT, the landlord has been informed, and the case has gone to the on-call manager at P1.

## Actions taken

**MSG-001 - Email to tenant (Nora Bell)** (safety_advice): *URGENT safety advice: warm kitchen socket at 8 Brindlewick Row, emergency electrician being arranged now*
> Dear Nora,
>
> Thank you for letting us know you are back home. I'm sorry you have not had clear safety guidance before now. A socket that smells hot and stays warm with nothing plugged in can mean a fault in the wiring behind it, so we are treating this as urgent. Please follow this advice now:
>
> 1. If you see smoke or flames, hear crackling or buzzing, or the smell gets stronger, get yourself and your son out of the flat straight away and call 999. Do not try to deal with it yourself.
> 2. Do not touch the socket or switch, and do not plug anything into it or into the sockets either side of it. Keep your son away from that part of the counter.
> 3. If you can do it safely, open the consumer unit (fuse box) and switch off the breaker marked for the kitchen sockets or "ring". Do not touch the socket itself to do this. If nothing is labelled and you are not sure, leave it. Please don't experiment, and don't touch the consumer unit if it is warm, damp or damaged. If you do switch off a breaker and the fridge goes off, keep the fridge door shut. Food should stay cold for several hours.
> 4. Please check that your smoke alarm is working. Press the test button.
> 5. Keep water and damp cloths away from the socket area.
>
> What happens next: we are sending an emergency electrician to make the socket safe this evening. They will check the socket, find and switch off the affected circuit if needed, and tell us what repair is required. They will not do any further repair without separate agreement. We will contact you as soon as we have an arrival time. Please reply to let us know you are at home and that it's OK to give the electrician your name and phone number so they can arrange access with you.
>
> We are also calling you now. If anything changes or gets worse, call 999 first, then let us know.
>
> Kind regards,
> Maya Chen
> Property Manager, Northbridge Lettings

**CALL-001 - Phone call to tenant (Nora Bell)** (urgent_safety); outcome: awaiting_response
> Hello Nora, this is Maya Chen from Northbridge Lettings, calling about the kitchen socket at 8 Brindlewick Row. First, some safety advice. If you see smoke or flames, hear crackling, or the smell gets stronger, take your son outside straight away and call 999. Please don't touch the socket or plug anything into it, and keep your son away from that part of the counter. If you can safely get to the fuse box, can you see a breaker labelled kitchen sockets or ring? If it's clearly labelled, please switch it off. If you're not sure, leave it, and don't touch the fuse box if it's warm or damaged. Please test your smoke alarm too. Some quick questions: Is there any smoke, scorch marks or discolouration on the socket now? Is the smell the same, stronger or weaker? Is the socket area still warm with nothing plugged in? We are sending an emergency electrician this evening to make it safe. Are you home all evening? Can I give the electrician your name and phone number so they can arrange to come in? We'll text you an arrival time. Thank you.

**MSG-002 - SMS to tenant (Nora Bell)** (safety_advice)
> Northbridge Lettings: Nora, please don't touch or use the kitchen socket. If you see smoke or flames, or the smell gets stronger, take your son out and call 999. Emergency electrician being sent this evening. Please check your email.

**JOB-001 - Contractor instructed:** Approved emergency electrician (to be allocated) (electrical, emergency_make_safe, emergency), cap £200.00, authorised by emergency_make_safe
  Emergency assessment: Kitchen socket smelling hot and staying warm with no appliance connected; possible loose or overheating fixed-wiring connection and fire risk, credibility **credible**: The tenant has given consistent, specific reports across six messages over more than 8 hours. The socket was warm to the touch after kettle use, it was still warm to a hand held near it with nothing plugged in, and a faint hot or burning smell persists on her return at 16:42. Heat with no load suggests a fault in the fixed wiring or accessory, which can lead to a fire. The circuit has not been identified or isolated, a child is present, and evening is approaching. The landlord has been asked repeatedly but has not authorised a qualified electrician, and his handyman cannot do fixed-wiring work. Making safe is proportionate and limited in scope.
  - MSG-003 email to contractor (Approved emergency electrician (to be allocated)): *New job JOB-001: electrical at 8 Brindlewick Row, Oakhollow, ZZ1 1ZZ*
  - MSG-004 email to tenant (Nora Bell): *Repair update: Approved emergency electrician (to be allocated) will be in touch*
  - MSG-005 email to landlord (Elliot Vane): *Urgent - emergency make-safe instructed at 8 Brindlewick Row, Oakhollow, ZZ1 1ZZ*

**MSG-006 - Email to landlord (Elliot Vane)** (status_update): *8 Brindlewick Row: kitchen socket still warm, emergency electrician sent to make safe only*
> Dear Elliot,
>
> Following my email at 15:02 and voicemail at 13:14, I'm writing with an update on the kitchen socket at 8 Brindlewick Row, Oakhollow, ZZ1 1ZZ.
>
> Nora returned home at 16:42. She reports that the hot smell near the counter socket is still there, more than eight hours after the first report. The socket area has been warm even with the kettle unplugged. The circuit has not been identified or switched off, and Nora's 10-year-old son is at home. Rowan attended at 13:00 but could not get in. He has confirmed he does not do fixed-wiring work and has no electrical test equipment, so he could not have made the circuit safe in any case.
>
> A socket that stays warm with nothing plugged in can mean a fault in the wiring behind it, which is a fire risk. We have not been able to reach you for a decision, so under our emergency make-safe procedure we have instructed one of our approved electricians to attend this evening. Their work is strictly limited to inspecting and making safe, for example isolating the circuit or disconnecting the faulty socket, with a cap of £200 including VAT. They will not carry out any repair beyond making safe. We will send you their report, photos and a priced quote for any permanent repair so that you can decide how to proceed, including using your own qualified electrician if you prefer.
>
> We have also given Nora safety advice. Rowan does not need to attend.
>
> If you have any concerns, please call or reply as soon as you can.
>
> Kind regards,
> Maya Chen
> Property Manager, Northbridge Lettings

**NOTE-001 - Internal note** (decision_rationale): 16:42 decision: an emergency make-safe electrician has been instructed (JOB-001, cap £200 including VAT). Reasons: the tenant's reports have been consistent for more than 8 hours: hot or burning smell, socket warm after kettle use, and still warm with nothing plugged in (events 001, 004, 008, 017, 025). The circuit has not been isolated, a 10-year-old child is present, and evening is approaching. The landlord has only authorised a general handyman (events 006, 010, 016, 021). The handyman cannot do fixed wiring and has no test equipment (events 011, 015), and he did not get in (event 023). The landlord was asked for electrician authority at 09:03 and 15:02 and called at 13:14, with no reply (events 020, 024). Doubts noted: no photo or test yet, the smell is faint and not getting stronger, and no smoke, sparking or tripping. Overall the report is credible and the hazard is current. Scope is limited to making safe, and any repair needs landlord approval. Gap fixed: no safety advice had been given before 16:42 (events 009, 025). It has now been sent by email and SMS, and a call placed (MSG-001, MSG-002, CALL-001). Landlord's SMS at event-021 ("have a look if you can get in") is not treated as key-use authority. Tenant consent to share her contact details with the electrician has been requested. Earlier consent (event-013) covered Rowan only.

**ESC-001 - ESCALATED to human** [P1_immediate, safety_emergency, respond within 15 minutes]
  Summary: At 8 Brindlewick Row, a kitchen counter socket has had a hot or slightly burning smell and has felt warm since about 08:14. It has stayed warm with the kettle unplugged, and the smell is still present at 16:42. The tenant, Nora Bell, is at home with her 10-year-old son. No circuit has been isolated and no one has inspected the socket. The landlord, Elliot Vane, only authorised his general handyman, who cannot do fixed wiring and could not get in. The landlord has not replied to requests for electrician authority (09:03, 13:14 voicemail, 15:02). At 16:42 the agency sent the tenant safety advice (email, SMS, call) and instructed an emergency make-safe electrician (JOB-001, make-safe only, cap £200 including VAT). The landlord has been informed.
  Why a human: This is a live electrical fire risk in an occupied home with a child, after a day without safety advice or inspection. A human needs to make sure an approved electrician is actually allocated and attends this evening. That may need phone calls out of hours. They should also confirm the tenant has had the advice, and handle the landlord, who has been unresponsive and may object to the cost.
  Recommended: Phone the approved electrician list now and confirm someone is allocated, with an arrival time tonight; Phone Nora to confirm she has the safety advice, her current condition, her consent to share contact details, and the arrival time; If no electrician can attend within about 4 hours, ask Nora to switch off the kitchen socket circuit, or the main switch if she can do so safely, and tell her to call 999 if the condition gets worse; Keep trying to reach Elliot Vane by phone; record any reply with record_landlord_decision; After make-safe, send the electrician's report and quote to the landlord for approval of the permanent repair

**HOLD-001 - Case put on hold** (waiting_for_contractor): waiting for Emergency electrician (JOB-001) to confirm an arrival time this evening. Also waiting for the tenant to reply on her current condition and consent to share contact details, and for any reply from the landlord.. Follow up 2025-04-12T18:00:00Z; if nothing arrives: Phone the electrician list and the tenant directly. If no electrician is confirmed, ask the tenant to isolate the circuit or main switch if safe, repeat the 999 advice, and push the human escalation for an alternative contractor.

## Escalation

Escalated to a human: see the ESC entry above.

## What failed

- none

## Next step

**agency**: On-call manager to confirm an electrician arrival time tonight, phone the tenant (safety check, consent to share contact details, arrival time), and keep trying the landlord. Agency follow-up at 18:00 under HOLD-001. (by 2025-04-12T18:00:00Z)

## Final result

`escalate`: The tenant's reports have been consistent and specific all day (events 001, 004, 008, 017, 025): a hot smell, and warmth even with no load, which suggests a fault in the fixed wiring and a fire risk. A child is present and no circuit has been isolated. The file shows no safety advice was ever given (events 009, 025), so advice went out at once by email, SMS and phone call, including the 999 advice. The landlord authorised only a general handyman (events 006, 016, 021). The handyman cannot do fixed-wiring work, has no test equipment, and did not inspect (events 011, 015, 023). The landlord was asked three times about an electrician with no answer (events 005, 020, 024), so waiting longer was not acceptable. Under the emergency make-safe exception, a qualified electrician has been instructed for make-safe only, with a modest cap. Any permanent repair goes back to the landlord for approval. The case was escalated at P1, without blocking automation, so that a human can make sure the electrician actually attends this evening and can deal with the unresponsive landlord.
