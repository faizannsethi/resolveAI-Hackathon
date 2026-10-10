# Case property-management-test-cases-008: decision at 2025-06-18T12:55:00Z

**Decision:** `escalate`  |  **Risk:** emergency  |  **Escalated:** yes  |  **Confidence:** high

## What the system received

- Case input: `Property_Management_test_cases/008`, 24 visible event(s), history cut at the end of the supplied history

- Documents read: none

## Decision point

The leak into Flat 2 is still active and the ceiling bulge next to a wet light fitting is growing. The source flat (Flat 3) cannot be reached: the tenant refuses entry, the landlord has not authorised it, and the agency has no confirmed emergency-entry authority. The duty manager has said the director must decide. The agency has to decide what to do now.

## Situation

Water has been dripping through the Flat 2 bedroom ceiling light since 08:19 and the ceiling bulge is growing. The room is clear and no sparks, smoke or fallen material have been reported. An electrician is due 12:30–13:15. The plumber and the building manager could not find the source or a confirmed isolation point from Flat 2 or the communal riser. Flat 3, the suspected source, is inaccessible: Yara refuses entry until about 17:30, Niko has not authorised entry, and the agency has no confirmed authority to override the refusal.

## Actions taken

**MSG-001 - SMS to tenant (Bevin Orlo)** (safety_advice)
> Thanks Bevin. Please keep out of the bedroom with the door shut. A bulging ceiling can give way: do not push or pierce it, and do not touch the light, switches or consumer unit. If the ceiling falls, or you see sparks or smoke or smell burning, leave the room and call 999. The electrician is due by 13:15. We are working urgently on access to the flat above and will update you. Arlen, Northbridge Lettings

**MSG-002 - Email to tenant (Yara Mallow)** (request_information): *Flat 3, 8 Tallowmere Row – written details of the proposed plumbing visit, as you asked*
> Dear Yara,
>
> Thank you for speaking to Arlen at 11:48 today. As you asked, here are the details of the proposed visit to Flat 3, 8 Tallowmere Row, Ossin Vale, ZZ1 1ZZ, in writing.
>
> Why: water is still coming through the ceiling of the flat below, under your bathroom, and the ceiling there is now bulging next to a light fitting. The plumber has checked the flat below and the communal riser with the building manager, but could not find the source or a valve that can be confirmed as serving only Flat 3. We have not confirmed that the leak comes from your flat. Flat 3 is simply the most likely place to trace it from.
>
> Who: Daro Fen of Brindle Flow Plumbing.
>
> Proposed work: the first step only. Daro would trace the leak, mainly around the bathroom and its pipework, and find and turn off a safe isolation point if the leak is coming from Flat 3. He would not do any other repair without your agreement and the landlord's approval. We would explain anything further before it was done.
>
> We understand that you have not agreed to entry while you are away, and we will respect that. No key is being used and no entry to Flat 3 has been arranged. Please could you let us know, by reply or by calling Arlen, which of these you would be willing to agree to:
>
> 1. Daro attending today while you, or someone you trust, are present, if you could return earlier or nominate someone to let him in.
> 2. Daro attending as soon as you get home. We could aim to book him for about 17:30 so that there is no further delay.
> 3. In the meantime, if you know where your stopcock or the bathroom isolation valves are, please tell us. That information on its own could help.
>
> If the situation below became an immediate danger, emergency services might have to attend. If that happened, we would contact you straight away.
>
> Thank you for your help. We know this is disruptive while you are at work.
>
> Kind regards,
> Arlen Quist
> Property Manager, Northbridge Lettings

**MSG-003 - Email to landlord (Niko Pell)** (status_update): *Flat 3, 8 Tallowmere Row – leak update and access position*
> Dear Niko,
>
> Thank you for your emails this morning. As you asked to be kept updated, here is where things stand at 12:55.
>
> - Water is still coming through the ceiling of the flat below Flat 3. The ceiling there now has a growing bulge next to a light fitting. That room is being kept clear and an electrician is due by 13:15 to make the fitting safe.
> - The plumber (Daro Fen, Brindle Flow Plumbing) and the building manager checked the flat below and the communal riser. They found neither the source nor a valve that can be confirmed as serving only Flat 3. Flat 3 has not been confirmed as the source.
> - Yara is still not agreeing to entry before she returns at about 17:30. At her request, we have just sent her the plumber's details and the proposed work in writing. We have asked whether she would agree to an accompanied visit earlier, or to a visit as soon as she gets home.
> - No entry to Flat 3 has taken place or been arranged, and no key is being used. We have noted that you have not authorised forced or unaccompanied entry.
> - As you suggested, we are referring the full tenancy agreement and the question of emergency access to a senior manager at Northbridge Lettings for review. We will not take any non-routine access step without contacting you first, unless emergency services direct otherwise because of an immediate danger.
>
> If you have a copy of the full tenancy agreement to hand, please send it to us. If you know of anyone else who holds a key with Yara's agreement, please tell us that too. We will update you again once we hear from Yara or the electrician.
>
> Kind regards,
> Arlen Quist
> Property Manager, Northbridge Lettings

**ESC-001 - ESCALATED to human** [P1_immediate, legal_or_compliance, respond within 15 minutes]
  Summary: An active leak from an unknown source, probably above, is coming through the bedroom ceiling of Flat 2, 8 Tallowmere Row. Water is dripping from the ceiling light fitting and a ceiling bulge has grown over the last two hours (events 017, 023). An electrician (Runa Elt, Vellum Electrical) is due 12:30–13:15 to assess and make the fitting safe. The plumber (Daro Fen, Brindle Flow Plumbing) and the building manager (Selka Venn) found no source and no confirmed isolation point from Flat 2 or the communal riser. Tracing needs access to Flat 3. Yara Mallow, the Flat 3 tenant, refuses entry before she returns at about 17:30 and has asked that no key be used. Niko Pell, the Flat 3 landlord, has not authorised entry. The duty manager found no documented delegated authority to override the refusal and said the full tenancy agreement and a decision from the agency director are needed (event-022).
  Why a human: The case needs a decision on whether there is any lawful basis for emergency entry to Flat 3 against the tenant's stated refusal, or whether to involve emergency services if the danger becomes immediate. That is a legal and compliance decision reserved for the agency director (event-022), and the agent has no authority over it. The ceiling bulge is growing next to a wet electrical fitting, so the decision is time-critical.
  Recommended: Agency director to review the full Flat 3 tenancy agreement today and decide on any emergency-access basis. Do not use a key or force entry without that decision, and contact Niko before any non-routine access.; Get the electrician's findings as soon as the visit ends (due by 13:15) and confirm the circuit is isolated. If the ceiling collapses or there is an electrical danger, call 999 and follow their direction.; Provisionally book Daro Fen (Brindle Flow Plumbing) for about 17:30 at Flat 3, subject to Yara's consent, and phone Yara to confirm.; Confirm the spending authority and payer for the Flat 2 attendances (Flat 2 landlord or freeholder/block management), and get the Flat 3 landlord's approval for any tracing cost in Flat 3.; Consider asking Selka whether the building's insurer or freeholder procedure covers escape-of-water access.

## Escalation

Escalated to a human: see the ESC entry above.

## What failed

- none

## Next step

**human_reviewer**: Agency director/on-call manager: decide whether there is any emergency-access basis after reviewing the full Flat 3 tenancy agreement. Get the electrician's findings (due by 13:15). Call 999 if the ceiling collapses or there is an electrical danger. Follow up Yara's reply and provisionally book Daro for about 17:30, subject to her consent. (by 2025-06-18T13:15:00Z)

## Final result

`escalate`: Event-022 sends the emergency-access question to the agency director, using the full tenancy agreement. Overriding an occupant's refusal is a legal matter outside the agent's authority, so it was escalated P1 (ESC-001). Meanwhile I did what the agency can properly do now. Bevin got refreshed safety advice about the growing bulge, the wet fitting and when to call 999 (MSG-001, events 017/023). Yara's request from event-020 for the plumber's name and proposed work in writing had not been met, so I emailed her the details with consent options, including a visit at about 17:30 (MSG-002). Niko asked to be updated before any non-routine access, so I sent him a status update and asked for a copy of the agreement (MSG-003; events 006/019). I did not arrange any forced, key or unaccompanied entry, and dispatched no new contractor: the source is unconfirmed, there is no authority to enter, and no spending approval is recorded.
