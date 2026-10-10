# Case property-management-test-cases-012: decision at 2025-09-25T12:06:33Z

**Decision:** `request_information`  |  **Risk:** routine  |  **Escalated:** no  |  **Confidence:** high

## What the system received

- Case input: `Property_Management_test_cases/012`, 25 visible event(s), history cut at the end of the supplied history

- Documents read: none

## Decision point

The contractor (Edrin Moss, Keypath Repairs) says again that the window lock work is complete and promises an invoice. Nothing in the file proves the visit or the work happened.

## Situation

The tenant reported faulty sash locks and missing keys at Unit 2, 18 Brindlewick Mews. The landlord approved the agency's provider with no cap (event-003). The job moved from Hearthline Access to Keypath Repairs. On 17/09 Keypath said it had not got in and had not collected management keys. From 22/09 it has said verbally that the work was done on 19/09, but no invoice, job report or tenant confirmation exists. The tenant also mentioned bathroom mould (event-006), which has never been followed up.

## Actions taken

**MSG-001 - Email to tenant (Perrin Dall)** (request_information): *Window locks at Unit 2, 18 Brindlewick Mews: has the work been done?*
> Dear Perrin,
>
> Thank you for your patience with the window lock repairs at Unit 2, 18 Brindlewick Mews, Orellin ZZ1 1ZZ.
>
> Our contractor, Keypath Repairs, has told us that the work was finished on Friday 19 September. We have no record of the visit ourselves, so before we sign the job off, could you please let us know:
>
> 1. Did a locksmith come to the property on or around 19 September? If so, were you there, or how did they get in?
> 2. Bedroom window: does the opening sash now lock securely?
> 3. Bathroom window: does the sash now open and close properly, and do the locking buttons work without sticking?
> 4. Kitchen window: have you been given a working key for the sash lock?
> 5. Have you been given keys for all the window locks, and how many?
>
> If any of this has not been done or still isn't working, please tell us and we will get it sorted straight away. If the bedroom window still won't lock, please let us know as soon as possible, as that affects the security of your home.
>
> On our call on 9 September you also mentioned mould in the bathroom. We would like to look into this as a separate matter. Could you please tell us where the mould is (ceiling, walls, around the window?), roughly how large an area it covers, and whether anyone in the home has asthma or other breathing problems? Photos would help a lot if you can send some. In the meantime, opening the window or running the extractor fan after bathing or showering, and wiping down any condensation, will help keep it from spreading.
>
> A reply by email when you have a moment would be great. If we haven't heard back, we will check in with you again on Monday 29 September.
>
> Kind regards,
> Ilyra Venn
> Property Manager, Northbridge Lettings

**MSG-002 - Email to contractor (Edrin Moss)** (request_information): *Unit 2, 18 Brindlewick Mews: invoice and job report needed for the window lock work*
> Dear Edrin,
>
> Thank you for speaking with me today about the window lock job at Unit 2, 18 Brindlewick Mews, Orellin ZZ1 1ZZ.
>
> You mentioned the work was completed on Friday 19 September. We have no attendance record for that visit, and when we spoke on 17 September you said you had not yet collected the management keys. Before we can pass your invoice on for payment, please send the following along with it:
>
> 1. The date and time you attended, and how you got in (tenant present, management keys, or another arrangement).
> 2. A description of the work done on each window:
>    - bedroom sash: locking repaired?
>    - bathroom sash: freed so it opens, and locking buttons repaired?
>    - kitchen sash: key supplied?
> 3. Any parts fitted, and how many keys you left and with whom.
> 4. Before and after photos, if you have them.
> 5. An itemised invoice showing labour, parts and VAT (if you are VAT registered).
>
> We will check the work with the tenant, and once they confirm it, we will process the invoice. You said you would send the invoice later today. If we haven't received it with these details by Friday 26 September, we will be in touch.
>
> Kind regards,
> Ilyra Venn
> Property Manager, Northbridge Lettings

**MSG-003 - Email to landlord (Sella Marr)** (status_update): *Update: window lock repairs at Unit 2, 18 Brindlewick Mews*
> Dear Sella,
>
> Here is an update on the window lock repairs at Unit 2, 18 Brindlewick Mews, Orellin ZZ1 1ZZ, which you authorised on 4 September.
>
> Our contractor, Keypath Repairs, says the work was done on 19 September. We are now checking this with the tenant and have asked the contractor for a job report and an itemised invoice. We won't process the invoice until the tenant has confirmed the locks work and the keys have been handed over. When it arrives, we will send it to you with a summary of the work done.
>
> Separately, the tenant has mentioned some mould in the bathroom. We are getting more details and photos from them and will come back to you with a recommendation before any further work is arranged.
>
> Kind regards,
> Ilyra Venn
> Property Manager, Northbridge Lettings

**DEC-001 - Landlord decision recorded:** approved: Window sash lock repairs (bedroom, bathroom and kitchen sash locks and keys) by a Northbridge Lettings service provider. No spending limit or detailed scope was stated. (evidence event-003)

**ITEM-001 - Open item open**: Check that Keypath Repairs (Edrin Moss) actually finished the window lock work: they claim it was done on 19/09, but there is no attendance record and keys were not collected as of 17/09. Need the tenant's confirmation plus a job report and an itemised invoice. Then check the invoice and send it to the landlord.

**ITEM-002 - Open item open**: The tenant mentioned bathroom mould during the 09/09 call. Details, photos and any vulnerability information have been requested. Once received, assess and seek the landlord's approval for any investigation or work.

**NOTE-001 - Internal note** (data_quality): Completion claim is unverified. In event-022 (17/09), Edrin said they had tried the property three times, had not found the tenant in, had not collected management keys and could not give a date to do so. In event-023 (22/09), Edrin said the work was completed on 19/09. The tenant had asked for management-key access (event-008, event-019). There is no record of key collection, an appointment, visit notes or tenant confirmation. Do not process the invoice until the tenant confirms the work and Keypath supplies a job report. Also unresolved: Tarin Vale (Hearthline Access) said in event-016 that they had agreed a time with the tenant after the job was reassigned. Check that no second contractor attended or will invoice. Landlord approval (event-003) has no spending limit, so check the invoice for reasonableness.

**HOLD-001 - Case put on hold** (waiting_for_tenant): waiting for Two things: the tenant's confirmation that the window lock work is done (bedroom sash locks, bathroom sash opens with working buttons, kitchen key supplied) plus details of the bathroom mould; and Keypath Repairs' job report and itemised invoice, promised for today or 26/09.. Follow up 2025-09-29T10:00:00Z; if nothing arrives: Phone the tenant to confirm the work and ask about the mould. If the work isn't done or can't be confirmed, call Edrin to arrange a revisit using management keys, or reassign the job. If no invoice or job report has arrived, phone Keypath. Escalate to a human if Keypath's account and the tenant's account conflict.

## Escalation

Not escalated.

## What failed

- none

## Next step

**agency**: Review the tenant's confirmation, the mould details and Keypath's invoice and job report. If any are missing, phone the tenant or contractor. Once the work is verified, check the invoice and send it to the landlord. (by 2025-09-29T10:00:00Z)

## Final result

`request_information`: Keypath's completion claim conflicts with its own account on 17/09 (no access, keys not collected), and nothing on file supports it. We should not accept completion or process an invoice on the contractor's word alone. So I asked the tenant to confirm each window and the keys, and asked Keypath for attendance details, a job report and an itemised invoice. I also told the landlord where things stand. I recorded the approval from event-003 (no cap) and opened tracked items for the verification and the unaddressed mould. A follow-up is set for 29/09. Escalation isn't needed yet; it will be if the tenant's and contractor's accounts conflict.
