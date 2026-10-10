# Case property-management-test-cases-006: decision at 2025-09-18T17:42:00Z

**Decision:** `request_information`  |  **Risk:** routine  |  **Escalated:** no  |  **Confidence:** high

## What the system received

- Case input: `Property_Management_test_cases/006`, 17 visible event(s), history cut at the end of the supplied history

- Documents read: none

## Decision point

The tenant says the solar readings were already sent about two weeks ago by his wife, by phone and email. Nothing was visible against this request, and four chases have gone to the tenant.

## Situation

The landlord, Edwin Vale, asked on 3 Sept for the current solar generation readings at 14 Brindlefern Walk. This is an information request only: no fault, works or spend. The agency chased the tenant four times (events 006, 010, 013, 016). The tenant now says his wife phoned and emailed the readings about two weeks ago. They were never linked to this request, so they were probably misfiled on our side.

## Actions taken

**NOTE-001 - Internal note** (data_quality): Tenant Ivo Mercer (event-017) says his wife supplied the solar readings about two weeks ago (around 3-4 Sept) by phoning the office and by email. Nothing of this appears against this request (events 009, 012, 015 show no reply). The likely explanation is that the call or email was logged elsewhere: general inbox, another case, or under the wife's name or email address. Before asking the tenant again, the team must search the general office inbox, the call log and any records under the wife's name for 3-5 Sept. This is purely an information request. There is no fault, hazard, works or spend. The 'approved' status in event-005 does not matter here because no contractor is needed. The landlord has had no visible update since his call on 3 Sept (event-001).

**ITEM-001 - Open item open**: Search the general office inbox, the phone/call log and any misfiled correspondence (including under the tenant's wife's name or email address) for the solar generation readings the tenant says were sent around 3-5 Sept 2025. If found, link them to this case and pass them to the landlord.

**MSG-001 - Email to tenant (Ivo Mercer)** (request_information): *Solar generation readings – 14 Brindlefern Walk*
> Dear Ivo,
>
> Thank you for your reply, and I'm sorry for the repeated reminders. It sounds like your wife sent the readings promptly and they were not attached to the landlord's request on our side. We are now searching our general inbox and call records for her phone call and email from about two weeks ago, so we can pass the figures to the landlord.
>
> To help us find them quickly, could you let us know:
> - the email address your wife sent the readings from, and roughly what date; and
> - her name, in case the message was filed under it.
>
> If it is easier, a quick photo of the generation meter or inverter display (showing the kWh total) sent in reply to this email would also do. Please don't feel you have to, though, as we will look for the original first.
>
> We won't send any more reminders about this while we check. Thank you again for your help, and apologies for the trouble.
>
> Kind regards,
> Maya Chen
> Property Manager
> Northbridge Lettings

**MSG-002 - Email to landlord (Edwin Vale)** (status_update): *Update: solar generation readings – 14 Brindlefern Walk*
> Dear Edwin,
>
> Here is an update on the solar generation readings you asked for on 3 September.
>
> We asked the tenant for the current kWh reading from the generation meter or inverter display. The tenant has now told us that the readings were sent to our office, by phone and email, about two weeks ago. Unfortunately they were not linked to your request. We are now searching our inbox and call records for them, and we have also asked the tenant to send a fresh photo of the display if that is easier.
>
> I'm sorry for the delay. As soon as we have the figures, we will send them to you, and we expect to update you again by Monday 22 September at the latest. No visit or works are needed for this, so there is no cost to you.
>
> Kind regards,
> Maya Chen
> Property Manager
> Northbridge Lettings

**HOLD-001 - Case put on hold** (waiting_for_tenant): waiting for Two things: the result of the internal search of the inbox and call log for the readings the tenant's wife says she sent around 3-5 Sept (ITEM-001), and the tenant's reply with her email address, the date and her name, or a fresh photo of the meter/inverter.. Follow up 2025-09-22T10:00:00Z; if nothing arrives: If the readings are found, send them to Edwin Vale and close the case. If they are not found and the tenant hasn't replied, phone the tenant (or his wife) to take the reading over the phone or arrange a photo. Do not send any more automated chase emails. Update the landlord on 22 Sept as promised.

## Escalation

Not escalated.

## What failed

- none

## Next step

**agency**: Search the inbox and call log for the readings the tenant's wife sent (ITEM-001) and check for the tenant's reply. Send the readings to the landlord if found; otherwise phone the tenant to get the reading. (by 2025-09-22T10:00:00Z)

## Final result

`request_information`: The tenant's account (event-017) is plausible. The repeated "no reply visible" updates (009, 012, 015) only cover this request's own correspondence, so a call or email filed elsewhere would not show. Sending a fifth chase would be wrong. Instead: (1) open an internal item to search the general inbox and call log, including under the wife's name; (2) reply to the tenant with an apology, ask for details that will help find the original, offer a fresh photo as an easy fallback and promise no more reminders; (3) send the landlord his first visible update since 3 Sept, saying no cost is involved and giving a date for the next update; (4) hold until 22 Sept, then phone the tenant if the readings still haven't turned up. No contractor or landlord approval is needed, as nothing is being paid for.
