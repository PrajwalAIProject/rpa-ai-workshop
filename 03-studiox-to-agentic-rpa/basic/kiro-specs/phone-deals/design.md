# Design: PhoneDeals bot

> Reference copy. Kiro keeps its own in `.kiro/specs/phone-deals/design.md`.

## Overview

One UiPath Studio process, `Main.xaml` (Windows project, VB.NET expressions), that runs
top to bottom: open page → stop on robot check → extract table → clean and filter →
sort → write Excel → log.

## Variables

| Name | Type | Purpose |
| ---- | ---- | ------- |
| `dtRaw` | DataTable | Everything Extract Table Data reads from the page (text columns) |
| `dtPhones` | DataTable | Clean result: Name (String), Price (Int32), Rating (String) |
| `priceText` | String | One price with "₹" and commas removed |
| `price` | Int32 | That price as a number |

## Activities, in order

1. **Use Application/Browser**: Browser URL = the search URL. All steps below go inside it.
2. **Check App State**: if the CAPTCHA text "Type the characters you see" appears, **Throw**
   `New BusinessRuleException("Amazon showed a robot check. Stopping.")`.
3. **Extract Table Data** (Table Extraction wizard): columns Name, Price, Rating; one page
   only; output `dtRaw`.
4. **Build Data Table**: `dtPhones` with Name (String), Price (Int32), Rating (String).
5. **For Each Row in Data Table** over `dtRaw`:
   - **Assign** `priceText = CurrentRow("Price").ToString.Replace("₹","").Replace(",","").Trim`
   - **If** `Integer.TryParse(priceText, price) AndAlso price >= 1 AndAlso price <= 20000`
     → **Add Data Row** to `dtPhones`:
     `{CurrentRow("Name").ToString.Trim, price, CurrentRow("Rating").ToString}`
6. **If** `dtPhones.Rows.Count = 0` → **Throw** `New BusinessRuleException("No phones found under Rs 20,000.")`
7. **Remove Duplicate Rows** (`dtPhones`), then **Sort Data Table** by Price, Ascending.
8. **Use Excel File** (`PhonesUnder20K.xlsx`, Create if not exists) → **Write DataTable to
   Excel** (`dtPhones` → `Excel.Sheet("Phones")`, include headers).
9. **Log Message**: `dtPhones.Rows.Count.ToString + " phones under Rs 20,000 saved"`.

## Error handling

- Robot check or no phones: BusinessRuleException (bad input; retrying will not help).
- Page or browser problems: the activity's own error (an application exception). The
  advanced level adds retries for these.

## Testing

- Run in Studio (F5), then from the terminal: `uip rpa run-file --file-path C:\PhoneDeals\Main.xaml`.
- Check the output: `python check_phones.py` must print PASSED.
