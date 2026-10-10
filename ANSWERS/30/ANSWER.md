# Case property-management-test-cases-030: decision at 2025-09-06T18:42:00Z

**Decision:** `request_information`  |  **Risk:** urgent  |  **Escalated:** no  |  **Confidence:** high

## What the system received

- Case input: `Property_Management_test_cases/030`, 15 visible event(s), history cut at the end of the supplied history

- Documents read: none

## Decision point

The landlord, who is doing the work himself, says the smoke alarm job was completed on 31 Aug and asks for the record to be updated. He also gives details of socket fixes and a dehumidifier he provided. Decide whether to close or to verify.

## Situation

The tenant reported a beeping landing smoke alarm, which she removed, leaving a ceiling opening, and several loose sockets. The landlord chose to do the work himself. He now says it was completed on 31 Aug, that he tightened one back-bedroom socket and earlier a kitchen socket, and that he gave the tenant a dehumidifier for the bathroom. The tenant has not confirmed anything.

## Actions taken

**MSG-001 - Email to tenant (Nessa Quill)** (request_information): *8 Brindlefern Walk: please confirm the smoke alarm and socket repairs*
> Dear Nessa,
>
> The landlord, Mr Rusk, has told us that he finished the work at 8 Brindlefern Walk, Oakhollow, ZZ1 1ZZ on 31 August. Before we update the property record and close your report, please could you confirm the following:
>
> 1. Smoke alarm: has a smoke alarm been fitted again on the upstairs landing? When you press its test button, does it sound loudly? Has the beeping stopped?
> 2. Ceiling: has the opening in the ceiling where the old alarm was fitted been covered or made good?
> 3. Sockets: you told us that several plug sockets were coming away from the wall. Mr Rusk says he has tightened one socket in the back bedroom, and earlier secured one in the kitchen. Are all the sockets now firmly fixed? If any are still loose, please tell us which rooms they are in.
> 4. Bathroom: Mr Rusk says he has given you a portable dehumidifier for the bathroom. Is there any damp, condensation or mould in the bathroom or anywhere else that you would like us to look into?
>
> Photos of the new smoke alarm and of any sockets that are still loose would be very helpful.
>
> For your safety in the meantime: if any socket is loose enough to show wiring, sparks, buzzes, feels warm or has scorch marks, please stop using it, switch it off and tell us straight away. If you ever smell burning or see smoke, leave the property and call 999.
>
> Please reply by Wednesday 10 September if you can. We will then update the record or arrange anything that is still outstanding.
>
> Kind regards,
> Ivo Merrick
> Property Manager, Northbridge Lettings

**MSG-002 - Email to landlord (Tavian Rusk)** (request_information): *8 Brindlefern Walk: smoke alarm and socket work, record update*
> Dear Mr Rusk,
>
> Thank you for your emails confirming that the work at 8 Brindlefern Walk, Oakhollow, ZZ1 1ZZ was completed on 31 August, and for the details about the sockets and the dehumidifier. We have added these to the property record.
>
> We have asked Ms Quill to confirm that everything is in order. Smoke alarms are a legal requirement, so before we mark the record complete please could you also tell us:
>
> 1. Smoke alarm: what type is the new landing alarm (mains-wired or sealed battery, and is it interlinked with other alarms)? Was it tested when you fitted it, and has the ceiling opening where the old alarm was fitted been made good?
> 2. Sockets: Ms Quill reported several sockets coming away from the wall, but your email mentions only one in the back bedroom (and the kitchen socket you secured on 5 August). Were any other sockets checked? We would recommend that any socket that came away from the wall is checked by a qualified electrician, particularly the kitchen socket disturbed during the boiler work. Please also send us a copy of the current Electrical Installation Condition Report (EICR) for our compliance file if we do not already hold one.
> 3. Bathroom: could you tell us why the dehumidifier was needed? Is there a known damp, condensation or ventilation problem in the bathroom (for example, an extractor fan that is not working)? We will check with Ms Quill whether there is any mould.
> 4. Carbon monoxide: as the property has a boiler, please confirm that a working carbon monoxide alarm is fitted in the room where it is located.
>
> Once we have your reply and Ms Quill's confirmation, we will update the record and close this report, or let you know if anything is still outstanding.
>
> Kind regards,
> Ivo Merrick
> Property Manager, Northbridge Lettings

**ITEM-001 - Open item open**: Tenant to confirm that the landlord's smoke alarm replacement (landing) is fitted and works, and that the ceiling opening has been made good. The only completion claim so far is the landlord's (event-012).

**ITEM-002 - Open item open**: Loose sockets: the tenant reported several (event-005), but the landlord reports tightening only one back-bedroom socket, plus a kitchen socket on 5 Aug that came away after boiler work (event-014). Need to confirm with the tenant whether any remain loose, recommend a check by a qualified electrician, and obtain the EICR.

**ITEM-003 - Open item open**: Possible bathroom damp or condensation: the landlord gave the tenant a dehumidifier on 6 Aug (event-014). Ask the tenant whether there is damp or mould and the landlord what caused it (ventilation or extractor). Also confirm a CO alarm is fitted where the boiler is.

**NOTE-001 - Internal note** (decision_rationale): The landlord reports the smoke alarm job completed on 31 Aug (event-012) and gives socket and dehumidifier details (event-014). This is not closed yet: the only completion claim is the landlord's, and a working smoke alarm is a statutory requirement. The tenant reported several loose sockets but only one back-bedroom socket is mentioned as fixed; the kitchen socket was secured on 5 Aug, before the 20 Aug report. Note: the landlord's 5 and 6 Aug dates are earlier than the tenant's report, which is plausible but unverified. The dehumidifier suggests possible bathroom damp that was not reported in this case. Asked the tenant to confirm (MSG-001) and the landlord for alarm type, other sockets, EICR, the damp cause and the CO alarm (MSG-002). No spend involved; the landlord is using his own route, so we are not instructing a contractor.

**HOLD-001 - Case put on hold** (waiting_for_tenant): waiting for Tenant confirmation that the landing smoke alarm is refitted and working, the ceiling is made good, and the sockets are secure, plus any damp/mould. Also the landlord's answers on alarm type, the other sockets, the EICR and the CO alarm.. Follow up 2025-09-10T10:00:00Z; if nothing arrives: Phone the tenant to verify the smoke alarm works and check the sockets and damp, and chase the landlord by email. If the alarm is not working or sockets are still loose, press the landlord for a qualified electrician and escalate on compliance if he refuses.

## Escalation

Not escalated.

## What failed

- none

## Next step

**tenant**: Confirm the smoke alarm is working, the ceiling is made good, the sockets are secure, and whether there is any damp. Then the agency reviews the replies, chasing by phone if needed. (by 2025-09-10T10:00:00Z)

## Final result

`request_information`: A working smoke alarm on each storey is a statutory requirement, and the only completion evidence is the landlord's own statement (event-012). The tenant has to confirm the alarm is fitted and working before we close. The tenant reported several loose sockets (event-005), but only one recent socket fix is described (event-014), so part of the job may still be outstanding. The dehumidifier points to possible bathroom damp that has not been raised in this case. I asked the tenant to confirm, with photos, and gave her socket and fire safety advice. I asked the landlord for the alarm type, the other sockets, the EICR, the damp cause and the CO alarm, and recommended an electrician check the sockets. I opened items for each loose end and set a hold for 10 Sep. No spend is involved and the landlord is using his own route, so we are not instructing a contractor.
