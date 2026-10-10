# Case property-management-test-cases-026: decision at 2025-03-06T16:40:00Z

**Decision:** `act`  |  **Risk:** urgent  |  **Escalated:** yes  |  **Confidence:** high

## What the system received

- Case input: `Property_Management_test_cases/026`, 20 visible event(s), history cut at the end of the supplied history

- Documents read: none

## Decision point

The contractor missed the 6 March inspection (vehicle breakdown) and offered 7 March after 13:00, subject to confirmation (event-019). The tenant asked whether the inspection is still on and whether she should keep the misdirected email with another tenant's data, and reported the stain is darker (event-020).

## Situation

The damp patch below the kitchen window near a socket is worsening, with no dripping or electrical symptoms. The landlord approved a non-intrusive inspection only (event-011). The Brindle inspection has been moved to 7 March. Separately, an unresolved data breach (event-013): another tenant's arrears details were emailed to Iris. The privacy lead has not yet decided on deletion, notification or reporting, and the possible 72-hour reporting window ends around 11:29 on 8 March.

## Actions taken

**MSG-001 - Email to tenant (Iris Bell)** (status_update): *18 Juniper Fold – damp inspection rescheduled and your question about the misdirected email*
> Dear Iris,
>
> Thank you for your email, and I am sorry the inspection at 18 Juniper Fold did not go ahead this afternoon.
>
> Inspection
> Owen Pike of Brindle Survey & Drying phoned us at 15:12 today to say his vehicle had broken down and he could not attend. He has not inspected the property yet. He has offered tomorrow, Friday 7 March 2025, after 13:00 instead. You mentioned earlier that you are usually available after 13:00 on weekdays, so we are confirming this slot with Owen now. Please reply to let us know you can give access tomorrow afternoon. If that no longer suits you, tell us and we will rearrange. As before, this is a non-intrusive inspection: Owen will not remove any trim or cut into the wall.
>
> The stain getting darker
> Thank you for telling us, and for checking for dripping and electrical symptoms. Because the patch is close to the socket under the window, please take these precautions until the inspection:
> - Avoid using that socket for high-power appliances such as kettles or heaters, if you can.
> - If you notice the socket or wall around it feeling warm, a burning smell, scorch marks, sparking or crackling, the circuit breaker tripping, or the wall around the socket becoming wet, stop using it. Do not touch it, switch off at the consumer unit if it is safe to do so, and call us straight away. If there is any smoke or fire, leave the property and call 999.
> - If you can, please send a photo of the patch as it looks today. It will help us and Owen see how it is changing.
>
> The misdirected email
> I am sorry again that this email reached you, and thank you for handling it so carefully. Please keep not forwarding, printing or sharing it. Our privacy lead is reviewing the incident. We will confirm in writing what you should do with the message by 12:00 tomorrow, Friday 7 March. Until then, please just leave it as it is.
>
> Kind regards,
> Maya Chen
> Property Manager, Northbridge Lettings
> Ref: NBL-4821

**MSG-002 - Email to contractor (Owen Pike)** (instruction): *NBL-4821 – 18 Juniper Fold – please attend Friday 7 March after 13:00 (inspection only)*
> Dear Owen,
>
> Thank you for letting us know about the breakdown. I hope the vehicle is sorted soon.
>
> Please go ahead and treat Friday 7 March 2025, after 13:00, as the rebooked slot for the non-intrusive moisture inspection at 18 Juniper Fold, Velden Quay, ZZ1 1ZZ. The tenant has said she is generally available after 13:00 on weekdays. We are reconfirming with her this evening and will tell you straight away if there is a problem with access.
>
> A reminder of the scope: the owner has approved the inspection fee only, as quoted. Please do not remove trim, cut into the wall or carry out any remedial work. Send any repair proposal to us as a separate quote for the owner to approve.
>
> Please also note: the damp patch is below the kitchen window, nearest the socket under the window. The tenant says the stain looked darker this afternoon, though there is no dripping and no visible electrical symptoms. Please check moisture readings around the socket and tell us whether you think an electrician should check it.
>
> Please confirm the slot by reply and send your findings after the visit.
>
> Kind regards,
> Maya Chen
> Property Manager, Northbridge Lettings

**MSG-003 - Email to landlord (Gareth Vale)** (status_update): *18 Juniper Fold – damp inspection moved to Friday 7 March*
> Dear Gareth,
>
> A quick update on the damp below the kitchen window at 18 Juniper Fold. Brindle Survey & Drying could not attend this afternoon because their vehicle broke down. They have offered tomorrow, Friday 7 March, after 13:00, and we are confirming that with them and the tenant.
>
> Your approval still covers the inspection fee only. No intrusive or remedial work will be done. We will send you the findings and any repair proposal separately for your approval.
>
> The tenant reports the stain looked darker this afternoon. There is still no dripping and no sign of a problem with the nearby socket. We have given her precautionary advice and asked the inspector to check moisture around the socket.
>
> Kind regards,
> Maya Chen
> Property Manager, Northbridge Lettings

**MSG-004 - Email to agency_internal (Elena Frost)** (request_information): *Misdirected email NBL-4821 – recipient asking what to do with message; decision needed by 12:00 7 March*
> Hi Elena,
>
> Following my email of 5 March at 13:04: Iris Bell, the recipient of the misdirected appointment confirmation sent on 5 March at 11:22, emailed again today at 16:40. She asked whether she should keep the message. She confirms again that she has not forwarded it, and it is still in her inbox.
>
> I have told her to keep not sharing it and that we will give her written instructions by 12:00 on Friday 7 March. Please could you confirm by then:
> 1. Whether we should ask Iris to permanently delete the message, including from deleted items, and confirm the deletion to us in writing. Our sent copy is being preserved as you asked.
> 2. Whether and how the tenant whose name, address, arrears amount and payment arrangement were in the email should be contacted, and by whom. She has not been contacted yet.
> 3. Your assessment and decision on whether the incident needs reporting. Please note it is now more than 24 hours since we became aware on 5 March at about 11:29, so any 72-hour reporting deadline would be around 11:29 on 8 March.
>
> The maintenance job is carrying on separately.
>
> Thanks,
> Maya

**ESC-001 - ESCALATED to human** [P2_same_day, legal_or_compliance, respond within 4 working hours]
  Summary: On 5 March at 11:22, an appointment confirmation sent to tenant Iris Bell (18 Juniper Fold) also contained another tenant's name, address, rent arrears amount and payment-arrangement note (event-013). Iris reported it within minutes, has not forwarded it, and still has it in her inbox. On 6 March at 16:40 she asked whether she should keep it (event-020). The privacy lead, Elena Frost, asked for facts (event-017), and Maya supplied them (event-018). No breach assessment, deletion instruction, affected-tenant contact or reporting decision has been recorded. The separate damp inspection is being rebooked for 7 March and does not need human input.
  Why a human: A personal-data breach needs a decision from the privacy lead: whether it must be reported (the 72-hour window from awareness ends about 11:29 on 8 March), whether and how to tell the affected tenant, and what deletion instruction to give the recipient. This is outside the agent's authority. The recipient has been promised an answer by 12:00 on 7 March.
  Recommended: Privacy lead to complete the breach assessment and record the reporting decision before about 11:29 on 8 March; Send Iris the deletion instruction (draft below) by 12:00 on 7 March, once approved; Decide on contacting the affected tenant and record the rationale; Review how the content got into the template (process fix)

**ITEM-001 - Open item open**: Give Iris Bell written instructions on what to do with the misdirected email (promised by 12:00 on 7 March), once the privacy lead has decided. Get her written confirmation of deletion if she is asked to delete it.

**ITEM-002 - Open item open**: Rebooked non-intrusive damp inspection (Brindle Survey & Drying, 7 March after 13:00): get confirmation from Owen and Iris, receive the findings, and send any repair quote to Gareth Vale for separate approval (event-011).

**NOTE-001 - Internal note** (decision_rationale): Safety screen: the "sparks" match from event-009 is a negated statement. The tenant said she had NOT noticed heat, sparks or a tripped breaker, and confirmed again in event-020 that there are no visible electrical symptoms. No dripping, and the paint is cool but not wet (event-004). This is not an emergency. Damp near the socket is worsening (darker stain), so I gave precautionary electrical advice and asked for a photo (MSG-001), and asked the inspector to check moisture around the socket (MSG-002). Landlord approval (event-011) covers the inspection fee only. The fee amount is not stated in the visible history, so no FIN record was made. The data breach (event-013) was escalated to a human/privacy lead (non-blocking). I did not tell Iris to delete the email myself because the privacy lead has not decided yet.

**HOLD-001 - Case put on hold** (waiting_for_contractor): waiting for Owen Pike to confirm the 7 March after-13:00 slot; Iris Bell to confirm access; Elena Frost's privacy decision (deletion instruction promised to Iris by 12:00 on 7 March). Follow up 2025-03-07T10:00:00Z; if nothing arrives: Phone Owen to confirm attendance and Iris to confirm access. Phone Elena Frost or the duty manager to get the deletion instruction out before 12:00. If Owen cannot attend on 7 March, ask for the earliest next weekday slot after 13:00 and update the tenant and landlord.

## Escalation

Escalated to a human: see the ESC entry above.

## What failed

- none

## Next step

**agency**: Confirm the slot with Owen and access with Iris. Make sure the privacy lead's deletion instruction goes to Iris by 12:00. Chase by phone if there is no reply. (by 2025-03-07T10:00:00Z)

## Final result

`act`: The inspection is already approved and booked with Brindle (event-011, event-012), so rebooking to the offered slot needs no new approval. Iris has general weekday availability after 13:00 (event-004), so I accepted the slot with Owen and asked Iris to confirm. I updated the tenant with precautionary socket advice because the stain is darkening next to an electrical outlet, and gave the landlord a short update. The privacy question (keep or delete the email) is the privacy lead's decision and has been open more than 24 hours with no assessment (events 016-018). So I chased Elena Frost with a firm deadline, escalated non-blocking at P2 with a draft deletion instruction, and gave Iris a holding reply promising an answer by 12:00 on 7 March.
