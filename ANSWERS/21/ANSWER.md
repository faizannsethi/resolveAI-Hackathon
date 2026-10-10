# Case property-management-test-cases-021: decision at 2025-05-16T16:05:00Z

**Decision:** `request_information`  |  **Risk:** routine  |  **Escalated:** no  |  **Confidence:** high

## What the system received

- Case input: `Property_Management_test_cases/021`, 21 visible event(s), history cut at the end of the supplied history

- Documents read: none

## Decision point

The landlord says his plumber fixed the hot water on 14 May, but this is second-hand: it comes from a text the plumber sent him. The tenant has not answered our voicemail or email of 15 May. The letterbox fault the tenant raised on 13 May has not been followed up. Decide whether to close, chase or escalate.

## Situation

The tenant reported no hot water and no power to the boiler on 6 May. The landlord chose to use his own contractor. The tenant said twice that nothing had been done, and the landlord's plumber missed one expected visit. On 15 May the landlord said his plumber attended on 14 May and fixed it, but gave no work details. The tenant has not confirmed. Separately, the tenant reported on 13 May that the letterbox isn't working; this is still open and not assessed.

## Actions taken

**MSG-001 - Email to tenant (Iris Vale)** (request_information): *17 Wrenfold Quay – is your hot water working again? Also your letterbox*
> Dear Iris,
>
> I'm following up on my voicemail and email of 15 May about the hot water at 17 Wrenfold Quay, Larkhollow, ZZ1 1ZZ.
>
> Your landlord tells us his plumber came on 14 May and fixed the problem. Before we close the repair, we need to hear from you. Could you please reply to confirm:
>
> 1. Is the hot water now working at the taps and in the shower?
> 2. Does the boiler have power and is it working normally?
> 3. If anything still isn't right, please tell us what is happening (for example, what the boiler display shows) and we will take it up straight away.
>
> You also told us on 13 May that your letterbox isn't working. You don't need to make a separate report: we have logged it on this case. To help us arrange the right repair, could you please tell us:
> - Is it the letterbox in your own front door or a communal/building post box?
> - What is wrong with it (for example, the flap is stuck, broken, won't close, or post can't be delivered)?
> - If you can, please send a photo.
>
> If nothing has been fixed, or you have no hot water again, please call or email us as soon as you can. We will call you on Monday 19 May if we haven't heard from you by then.
>
> Kind regards,
> Maya Chen
> Property Manager, Northbridge Lettings

**MSG-002 - SMS to tenant (Iris Vale)** (nudge_check_email)
> Hi Iris, Northbridge Lettings here. Is the hot water at 17 Wrenfold Quay working again? Please reply or check our email. We've also asked about your letterbox. Thanks, Maya

**MSG-003 - Email to landlord (Ravi Sethi)** (request_information): *17 Wrenfold Quay – hot water repair details and a letterbox issue*
> Dear Ravi,
>
> Thank you for letting us know on 15 May that your plumber attended 17 Wrenfold Quay, Larkhollow, ZZ1 1ZZ on 14 May and fixed the hot water.
>
> We have asked Iris to confirm that the hot water and boiler are now working. We have not heard back from her yet and have chased her again today. We will keep the repair open until she confirms.
>
> For our records, could you please send a short description of what your plumber found and did? For example: the cause of the loss of power to the boiler, whether any electrical work was done, and any report or invoice reference. The original report was that the boiler had no power, so it would help to know if this was an electrical fault and whether any follow-up is needed.
>
> Separately, on 13 May Iris told us the letterbox at the property isn't working. We have asked her for details and a photo and will pass them on when we get them. Please let us know whether you would like to deal with this through your own contractor, or would like Northbridge Lettings to arrange a quote for you to approve. We won't instruct anyone without your agreement.
>
> Kind regards,
> Maya Chen
> Property Manager, Northbridge Lettings

**ITEM-001 - Open item open**: Tenant has not yet confirmed hot water and boiler power are restored after the landlord's plumber visited on 14 May. The only evidence of a fix is the landlord passing on a text from his plumber (event-018). Get the plumber's work description from the landlord.

**ITEM-002 - Open item open**: Letterbox not working, reported by the tenant on 13 May (event-017). Not yet assessed. Need details and a photo from the tenant, and the landlord's preferred route (own contractor or agency quote). No spend without landlord approval.

**NOTE-001 - Internal note** (decision_rationale): The case cannot be closed yet. The only evidence that the hot water was fixed is the landlord passing on a text from his plumber (event-018). The tenant has not confirmed: we left a voicemail and sent an email on 15 May (events 019 and 020) with no reply. Over 6–15 May the tenant reported three times that nothing had been done (events 012 and 017), so tenant confirmation is needed before we close. We chased the tenant today by email and SMS, and asked the landlord for the plumber's work details. The letterbox issue (event-017) had not been followed up: it is now logged, we have asked the tenant for details, and we have told the landlord and asked his preferred route. No spend has been authorised. Contact the tenant only: the household member does not speak English (event-003). This is the landlord-managed route (events 007 and 010). Event-015 gave conditional permission for an agency contractor, but it is now superseded by the landlord's report of a fix. If the tenant says hot water is still off, phone the landlord the same day to get an agency contractor approved. Follow up Mon 19 May: call the tenant if there is still no reply.

**HOLD-001 - Case put on hold** (waiting_for_tenant): waiting for Tenant to confirm that hot water and boiler power are restored, and to send letterbox details and a photo. Also waiting for the landlord's plumber work description and his preferred route for the letterbox.. Follow up 2025-05-19T10:00:00Z; if nothing arrives: Phone the tenant (Iris Vale only) to confirm the hot water status and get letterbox details. If the hot water is still not working, phone the landlord the same day to get approval for an agency heating/electrical contractor. If the tenant still can't be reached, write again and do not close. Chase the landlord for the plumber's details.

## Escalation

Not escalated.

## What failed

- none

## Next step

**agency**: Check for replies from the tenant and landlord. If the tenant hasn't replied, phone her. If she says hot water is still off, phone the landlord the same day for approval of an agency contractor. Once she confirms it's fixed, deal with the letterbox through the landlord's chosen route. (by 2025-05-19T10:00:00Z)

## Final result

`request_information`: We can't close yet. The only evidence of a fix is the landlord's account of a text from his plumber (event-018), and on this case the tenant had already reported more than once that nothing had happened (events 012 and 017). The tenant hasn't replied since event-020, about 31 hours ago, so a second chase by email and SMS is reasonable. Phoning the landlord is not needed: he has given his update. We asked him for the plumber's work details because the original fault was no power to the boiler, which could be electrical. The letterbox issue (event-017) was promised a follow-up but never logged, so it is now tracked and both parties have been told. No spend has been authorised. We are holding until Monday morning, then phoning the tenant.
