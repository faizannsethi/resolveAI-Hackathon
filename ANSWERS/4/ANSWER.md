# Case property-management-test-cases-004: decision at 2025-09-16T08:33:00Z

**Decision:** `wait`  |  **Risk:** routine  |  **Escalated:** no  |  **Confidence:** high

## What the system received

- Case input: `Property_Management_test_cases/004`, 23 visible event(s), history cut at the end of the supplied history

- Documents read: none

## Decision point

Tenant confirms the landlord's contractor, Dorian Wren, is due today after 10:00 to replace the front-door lock (event-023). The side issues she raised on 9 September (event-021) still had no owner.

## Situation

The front-door lock at 18 Larkspur Quay is loose and intermittent. The landlord told the agency to use his own contractor, Dorian Wren, and to stand down its locksmith, Peregrine Keyworks. Dorian attended on 9 September, found a new lock was needed and is due back today. The door can still be locked by hand but the tenant says it is getting worse. The tenant also raised a broken bedroom blind, door glazing the landlord had said he would deal with, and hot water that is too hot. None of these had been logged or raised with the landlord.

## Actions taken

**DEC-001 - Landlord decision recorded:** landlord_arranging_own_contractor: Front-door lock repair/replacement at 18 Larkspur Quay: landlord instructed agency not to use its provider and to wait for his own contractor, Dorian Wren. Agency to coordinate access and track progress only. (evidence event-011)

**ITEM-001 - Open item open**: Broken bedroom blind letting in light - raised by tenant; ownership/repair route not confirmed. Needs landlord instruction.

**ITEM-002 - Open item open**: Glazing in a door that the landlord had previously said would be addressed - status unknown; confirm with landlord whether he is arranging it and when.

**ITEM-003 - Open item open**: Hot water reported as too hot (possible scald risk) - needs landlord approval for a heating engineer to check hot water temperature/thermostat settings, or landlord's own arrangement.

**ITEM-004 - Open item open**: Confirm outcome of Dorian Wren's visit on 16 Sept 2025: lock replaced, door closes and locks properly, all keys (including tenant's spare) work, new keys supplied to tenant and agency.

**MSG-001 - Email to tenant (Nessa Vale)** (status_update): *Front-door lock visit today – 18 Larkspur Quay*
> Dear Nessa,
>
> Thank you for letting us know that Dorian Wren, the landlord's contractor, is due at 18 Larkspur Quay today (16 September) some time after 10:00.
>
> Once he has been, could you please let us know:
> - whether the lock has been replaced (or repaired);
> - whether the door now closes cleanly without catching and locks easily;
> - whether all your keys work, and how many new keys you were given (we will also need a copy for our office file).
>
> If he has not arrived by the end of today, please tell us and we will chase the landlord straight away. In the meantime, if the lock gets to the point where you cannot secure the front door at all, please contact us immediately so we can take urgent action.
>
> Your other concerns from our call on 9 September (the broken bedroom blind, the glazing in the door, and the hot water being too hot) have now been logged and we have raised them with your landlord today, asking how he wants each one dealt with. We will come back to you once we have his answer. Until the hot water has been checked, please take care at the taps: run cold water first and test the temperature before washing or bathing, to avoid any risk of scalding.
>
> Kind regards,
> Mira Sol
> Property Manager, Northbridge Lettings

**MSG-002 - Email to landlord (Tomas Elde)** (request_information): *18 Larkspur Quay – lock visit today and other repairs raised by the tenant*
> Dear Tomas,
>
> An update on the front-door lock at 18 Larkspur Quay. Nessa Vale tells us that Dorian Wren is due to attend today (16 September) some time after 10:00 to fit the new lock. On his visit on 9 September he concluded that a new lock was needed and went to get one. Nessa says the lock has got worse since then. We will confirm with Nessa once the work is done. Could you please ask Dorian to let us know when the job is complete and send us a copy of the new keys for our office file? As agreed, we have not instructed any other contractor. We assume you will settle Dorian's invoice directly; please tell us if that is not the case.
>
> On a call on 9 September Nessa also raised three other matters. Could you please tell us how you would like each one handled: either you arrange it yourself, or we obtain a price from one of our approved contractors for your approval.
> 1. Bedroom blind: broken and letting in light.
> 2. Door glazing: Nessa says you had previously said this would be dealt with. Could you confirm whether this is in hand and when it is likely to be done?
> 3. Hot water too hot: Nessa reports that the hot water is too hot. Because of the scalding risk, we recommend asking a heating engineer to check the water temperature and the boiler or cylinder thermostat settings soon. We have advised Nessa to take care in the meantime.
>
> We would be grateful for a reply by email by 19 September, so that we can update Nessa.
>
> Kind regards,
> Mira Sol
> Property Manager, Northbridge Lettings

**NOTE-001 - Internal note** (decision_rationale): Landlord is using his own contractor, Dorian Wren (event-011, event-016), recorded as DEC-001. Peregrine Keyworks was stood down (event-017). Tenant says Dorian is due today after 10:00 (event-023). Agency is not instructing anyone and will track the outcome only. The door can still be locked by hand (event-001) but the tenant says it is worse (event-020). Treated as routine/urgent rather than an emergency; tenant told to contact us at once if the door cannot be secured. Side issues from event-021 (blind, door glazing, hot water too hot) opened as ITEM-001 to ITEM-003 and raised with the landlord in MSG-002. Tenant given scald precautions in MSG-001. We have no contact details for Dorian Wren on file, so we asked the landlord to have him confirm completion. Follow up 17 Sept AM.

**HOLD-001 - Case put on hold** (waiting_for_tenant): waiting for Tenant's (or Dorian Wren's) confirmation of the outcome of today's lock visit: lock replaced, door secure, keys working. Also waiting for the landlord's instructions on the blind, door glazing and hot water temperature (requested by 19 Sept).. Follow up 2025-09-17T10:00:00Z; if nothing arrives: Phone the tenant to confirm whether Dorian attended and the lock is fixed. If he did not attend or the lock is still faulty, email and phone the landlord to chase a firm date, and escalate if the door cannot be secured. Chase the landlord on the side issues after 19 Sept if no reply.

## Escalation

Not escalated.

## What failed

- none

## Next step

**agency**: Confirm the outcome of the lock visit with the tenant. If Dorian did not attend or the lock is still faulty, chase the landlord. Chase the landlord's instructions on the blind, door glazing and hot water after 19 Sept if he has not replied. (by 2025-09-17T10:00:00Z)

## Final result

`wait`: The landlord is arranging his own contractor (event-011, event-016), so the agency must not instruct anyone. Its role is to track the work and keep everyone informed. The visit is today (event-023), so the right step is to wait for the outcome with a short follow-up. I recorded the landlord's decision (DEC-001). The tenant has had a holding reply (MSG-001) telling her what to confirm after the visit and to contact us at once if the door cannot be secured. The event-021 side issues had been left with no owner. I logged them as ITEM-001 to ITEM-003 and asked the landlord for instructions on each (MSG-002), with scald-risk advice to the tenant. ITEM-004 tracks confirmation that the lock work is done. The hold follows up tomorrow morning.
