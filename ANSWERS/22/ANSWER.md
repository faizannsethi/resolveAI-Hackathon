# Case property-management-test-cases-022: decision at 2025-09-25T09:08:19Z

**Decision:** `request_information`  |  **Risk:** routine  |  **Escalated:** no  |  **Confidence:** medium

## What the system received

- Case input: `Property_Management_test_cases/022`, 31 visible event(s), history cut at the end of the supplied history

- Documents read: none

## Decision point

The tenant replied "Yes, the job is completed", but also asked whether the planned machine change is still happening. This came one day after the tenant said no replacement had been delivered. Meanwhile the landlord has arranged their own replacement but given no date, and has complained about delays.

## Situation

The washer-dryer (error E13) at 8 Brackenmere Walk was inspected by the insurer's engineer on 9 Sep. The landlord then decided on a replacement and arranged delivery, fitting and disposal themselves (event-027/029), with no date given. On 24 Sep the tenant said nothing had arrived (event-030). On 25 Sep the tenant said the "job is completed" but asked whether the change is still happening (event-031). This is contradictory, so the case cannot be closed.

## Actions taken

**MSG-001 - Email to tenant (Ari Dalen)** (request_information): *Washer-dryer at 8 Brackenmere Walk: please confirm current position*
> Dear Ari,
>
> Thank you for your email this morning about the washer-dryer at 8 Brackenmere Walk, Vellumford, ZZ1 1ZZ.
>
> Before we update our records, could you please clarify one point? You said the job is completed. However, when we spoke yesterday afternoon (24 September) you told us that no replacement machine had arrived. Could you let us know which of these is right:
>
> 1. The original washer-dryer has been repaired and is now working properly, with no E13 error; or
> 2. A new machine has now been delivered and installed; or
> 3. Nothing has changed since yesterday: the old machine is still not working and you are still waiting for the replacement.
>
> On your question about the planned washing-machine change: yes, as far as we know it is still going ahead. After the engineer's visit on 9 September, the landlord decided a replacement was needed. They have ordered a new machine and arranged for installers to deliver it, fit it and take the old unit away. We do not have a delivery date yet. We have asked the landlord for one, and we will pass on the date and time window as soon as we get it. We know you need at least three hours' notice for access, and we will make sure the installers are told.
>
> If the original machine is in fact working again, please tell us. We will then check with the landlord whether they still want to go ahead with the replacement.
>
> We are sorry for how long this has taken, and thank you for your patience.
>
> Kind regards,
> Mara Venn
> Property Manager, Northbridge Lettings

**MSG-002 - Email to landlord (Nessa Orin)** (request_information): *Replacement washing machine at 8 Brackenmere Walk: delivery and installation date*
> Dear Nessa,
>
> Thank you for arranging the replacement washing machine for 8 Brackenmere Walk, Vellumford, ZZ1 1ZZ, including delivery, fitting and removal of the old unit. We are sorry that our response felt slow. We have passed your feedback to the team, and we want to help this go smoothly from here.
>
> Where things stand:
> - We spoke to Ari yesterday (24 September). The new machine had not been delivered and there was no packaging at the property.
> - This morning Ari replied to a follow-up saying the job was "completed", but also asked whether the machine change is still happening. We have asked Ari to confirm whether anything has changed since yesterday. We will tell you as soon as we hear.
>
> To help with access, please could you send us:
> 1. The confirmed delivery and installation date and time window, once you have it.
> 2. The name and contact number of the retailer or installer, if you are happy to share them, so we can coordinate with them directly.
>
> Please also let the installers know two things. First, the current machine is integrated and fixed to the cabinet door. Second, the rear connections have not been checked because the unit has not been moved. The tenant works from home but asks for at least three hours' notice before any visit.
>
> Your email of 21 September said this was all sorted, so we have taken it that you no longer need the quote for removal and replacement you asked for earlier that day. Please tell us if you would still like one.
>
> Kind regards,
> Mara Venn
> Property Manager, Northbridge Lettings

**NOTE-001 - Internal note** (data_quality): event-031: the tenant's "Yes, the job is completed" contradicts event-030 (24 Sep: no replacement delivered, no packaging), and in the same message the tenant asks whether the machine change is still happening. Most likely this is a reply to a generic follow-up about the 9 Sep engineer visit (event-021/023), which ended with the landlord deciding on a replacement. It does not confirm that a working appliance is in place. The case is NOT treated as complete. The landlord is arranging their own replacement (event-027/029): no Northbridge contractor should be instructed and no spend is needed from us. The quote request in event-028 appears to have been superseded by event-029 ("sorted it"); MSG-002 asks the landlord to confirm. The landlord complained about response times (event-029). This is an informal complaint; it was acknowledged in MSG-002 and is tracked as an open item for property manager review. Other noise: event-023 says "825 cm" (clearly means mm); the appliance is called both a washer-dryer and a washing machine.

**ITEM-001 - Open item open**: Landlord (Nessa Orin) complained that the agency's response took too long (event-029). Acknowledged in MSG-002. Property manager to review the case handling and decide whether a fuller response is needed.

**ITEM-002 - Open item open**: Landlord-arranged replacement washing machine: delivery and installation date not yet known. Confirm the date, coordinate tenant access (3 hours' notice), then get tenant confirmation that the new machine is installed and working and the old unit removed.

**HOLD-001 - Case put on hold** (waiting_for_landlord): waiting for Tenant to clarify whether the appliance is working or the replacement has been installed (MSG-001). Landlord to provide the replacement delivery and installation date and installer contact (MSG-002).. Follow up 2025-09-29T10:00:00Z; if nothing arrives: Phone the tenant to confirm the current status of the machine. Phone or email the landlord to chase the delivery date. Update both parties.

## Escalation

Not escalated.

## What failed

- none

## Next step

**agency**: Review replies from the tenant and landlord. Pass the delivery date to the tenant (at least 3 hours' notice). If nothing arrives, phone both. Once the tenant confirms the new machine is installed and working, close the case. (by 2025-09-29T10:00:00Z)

## Final result

`request_information`: event-031 does not reliably show that the repair is complete. It contradicts event-030, and the tenant's own question implies the replacement has not happened. Closing on it would be premature. The landlord is using their own route (event-027/029), so we do not instruct a contractor. Our job is to coordinate access and confirm the outcome. I replied to the tenant to answer their question and ask them to clarify the machine's status (MSG-001). I asked the landlord for the delivery and installation date and the installer's contact, passed on the fitting and access constraints, and acknowledged the complaint (MSG-002). I opened items for the complaint and for the outstanding installation, and set a hold with follow-up on 29 Sep.
