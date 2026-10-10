# Case property-management-test-cases-025: decision at 2025-09-15T11:11:18Z

**Decision:** `request_information`  |  **Risk:** routine  |  **Escalated:** no  |  **Confidence:** high

## What the system received

- Case input: `Property_Management_test_cases/025`, 22 visible event(s), history cut at the end of the supplied history

- Documents read: attachments/corrected-plumbing-invoice.pdf

## Decision point

The corrected invoice from Bracken & Vale Plumbing has arrived (event-022) and needs checking. Decide whether it can be processed and the case moved towards closure.

## Situation

The landlord approved work on the dripping kitchen tap with no price (event-003). After long delays, Bracken & Vale say they supplied and fitted a new mono kitchen tap. The corrected invoice NBL-025-INV-15 now has the right postcode, but it shows no amount, no VAT and no date of work. Nobody has confirmed the job is done: the tenant hasn't said the tap works or whether the cloudy water has cleared. The tenant's drawer report (event-012) was never answered. A separate boiler matter came up on a call (event-021), and the return of the office spare key is not confirmed.

## Actions taken

**NOTE-001 - Internal note** (data_quality): Corrected invoice NBL-025-INV-15 (attachments/corrected-plumbing-invoice.pdf, event-022) now shows the correct postcode ZZ1 1ZZ but contains NO amount, NO VAT treatment and NO date of attendance - only 'Supply and install one new mono kitchen sink tap'. It cannot be recorded or passed to the landlord for payment until those are supplied. The history never confirms the date the plumber attended (event-018 left date open) and there is no tenant confirmation that the new tap is working or whether the cloudy water persists. The landlord approved 'proceeding with the maintenance works' (event-003) without a price or limit; a full tap replacement was never priced to the landlord, so the landlord must see the amount before payment. Boiler matter raised in call event-021 is unrelated to this tap job - must not be added to this invoice; agency to check separately with the relevant engineer. Spare office key used for access (event-015/018) - return not confirmed. Safety screen 'No water' match comes from event-004 staff note ('No water sample') - false positive, no loss of supply reported. Tenant's loose drawer/snapped brackets (event-012) never answered.

**DEC-001 - Landlord decision recorded:** approved: Plumbing work to address the dripping kitchen mixer tap (and cloudy-water concern) at 18 Thistlewick Row, via Bracken & Vale Plumbing. No price or spend limit was given. (evidence event-003)

**MSG-001 - Email to contractor (Ivo Fenlock)** (request_information): *Invoice NBL-025-INV-15 – 18 Thistlewick Row, Fenmere, ZZ1 1ZZ – details needed before processing*
> Dear Ivo,
>
> Thank you for sending the corrected invoice NBL-025-INV-15 so quickly – the postcode now matches our records for 18 Thistlewick Row, Fenmere, ZZ1 1ZZ.
>
> Before we can pass it to the landlord for payment, the invoice still needs the following:
>
> 1. The amount charged, broken down into labour and parts (the tap), showing whether VAT is charged and, if so, the net, VAT and gross figures, plus your VAT number if you are VAT-registered.
> 2. The date you attended and fitted the new mono kitchen sink tap.
> 3. A short note of what you found: the cause of the drip on the old mixer tap, and anything you noticed about the tenant's report of cloudy water (for example, whether it cleared after running, or whether limescale or air in the supply was the likely cause).
> 4. Confirmation that the spare key collected from our office has been returned (or when it will be).
>
> As we discussed on the phone, any boiler work is a separate matter and should not be included on this invoice – I will check separately with the relevant engineer.
>
> If you could send these details or an updated invoice by Wednesday 17 September, we will process it promptly.
>
> Kind regards,
> Tessa Wren
> Property Manager, Northbridge Lettings

**MSG-002 - Email to tenant (Nia Calder)** (request_information): *Kitchen tap and drawer – 18 Thistlewick Row, Fenmere, ZZ1 1ZZ*
> Dear Nia,
>
> Thank you for your patience while we arranged the plumber, and sorry this took longer than it should have.
>
> Bracken & Vale Plumbing have told us they have fitted a new mono kitchen sink tap at 18 Thistlewick Row. Could you please let us know:
>
> 1. Is the new tap working properly, and has the dripping stopped?
> 2. Is the water still looking cloudy when you fill a glass? If it is, does it clear if you let the glass stand for a minute or so (which usually means harmless air bubbles), or does it stay cloudy?
> 3. Was everything left clean and tidy after the visit?
>
> On the loose top kitchen drawer with the snapped metal front brackets that you mentioned on 5 September – I am sorry we did not reply sooner. I have now asked the landlord for approval to send someone to assess and repair it, and I will be in touch to arrange a visit as soon as I hear back. If you are able to send a photo of the brackets, that would help the contractor bring the right parts.
>
> Kind regards,
> Tessa Wren
> Property Manager, Northbridge Lettings

**APR-001 - Landlord approval requested** (attend_and_diagnose): Approved maintenance contractor to attend, assess and quote for drawer repair (no work without your approval of the price); Landlord arranges own contractor for the drawer; reply due 2025-09-18T11:11:18Z
> Dear Orin,
>
> An update on the maintenance at 18 Thistlewick Row, Fenmere, ZZ1 1ZZ, following your approval on 5 August.
>
> Kitchen tap
> Bracken & Vale Plumbing have attended and supplied and fitted a new mono kitchen sink tap to replace the dripping mixer tap. They have sent an invoice (reference NBL-025-INV-15), but it does not yet show the amount or VAT, so I have asked them for a full breakdown, the date of the work, and their findings on the tenant's cloudy-water concern. I have also asked the tenant to confirm the new tap is working. I will send you the invoice with the amount for your review before anything is paid.
>
> Kitchen drawer (new item)
> The tenant, Nia Calder, has also reported that the top kitchen drawer is loose and its metal front brackets appear to have snapped. Could you let me know how you would like to proceed:
>
> 1. We send an approved maintenance contractor to assess the drawer and provide a quote. No repair would be carried out until you have approved the price. (Recommended.)
> 2. You arrange your own contractor – if so, please let me know who will contact the tenant.
>
> I would be grateful for your reply by Thursday 18 September.
>
> Kind regards,
> Tessa Wren
> Property Manager, Northbridge Lettings

**ITEM-001 - Open item open**: Invoice NBL-025-INV-15 lacks amount, VAT treatment and attendance date; obtain from Bracken & Vale, record it, and send to landlord for review before payment.

**ITEM-002 - Open item open**: Tenant confirmation that new tap works, drip stopped, and whether cloudy water persists (contractor findings also requested).

**ITEM-003 - Open item open**: Loose top kitchen drawer with snapped metal front brackets – awaiting landlord decision (APR-001) then arrange assessment/quote.

**ITEM-004 - Open item open**: Boiler matter raised in call event-021: agency to check with the relevant engineer what work was done; keep separate from this tap invoice.

**ITEM-005 - Open item open**: Confirm the agency spare key used by the plumber for access has been returned to the office.

**HOLD-001 - Case put on hold** (waiting_for_contractor): waiting for Bracken & Vale invoice amount/VAT/attendance date and findings (MSG-001); tenant completion confirmation (MSG-002); landlord decision on drawer (APR-001, due 18 Sep).. Follow up 2025-09-17T10:00:00Z; if nothing arrives: Phone Ivo Fenlock for the invoice amount/VAT and key return; SMS the tenant to check email; chase landlord by email if no reply by 18 Sep.

## Escalation

Not escalated.

## What failed

- none

## Next step

**contractor**: Provide the invoice amount and VAT breakdown, the date of work, findings on the drip and cloudy water, and confirm the key is back. Then record the invoice and send it to the landlord for review. (by 2025-09-17T10:00:00Z)

## Final result

`request_information`: The invoice can't be recorded or sent to the landlord without an amount and VAT. The landlord never saw a price for a full tap replacement (event-003), so they must review the amount before payment. Closing would be premature: there is no proof the work is done, the cloudy-water concern is open, the drawer issue is unanswered, and the key return and boiler query are loose ends. So I asked the contractor for the breakdown, the date, their findings and the key return. I asked the tenant to confirm the tap works and whether the water is still cloudy, and apologised for not answering about the drawer sooner. I asked the landlord for a decision on the drawer and updated them on the tap. I recorded the landlord's original approval (DEC-001), opened items for each loose end, and set a hold to follow up on 17 Sep.
