# Requirements: PhoneDeals bot

> Reference copy of the spec Kiro writes in Step 1. Yours will be worded differently;
> compare the meaning, not the words. Kiro keeps its copy in `.kiro/specs/phone-deals/`.

## Introduction

A small, attended UiPath bot that lists smartphones under ₹20,000 from the first page of
amazon.in search results and saves them to Excel, so a student can compare phone prices
in one place.

## Requirement 1: Open the search results

**User story:** As a student, I want the bot to open the phone search page, so that I
don't search by hand.

Acceptance criteria:
1. WHEN the bot starts THEN it SHALL open `https://www.amazon.in/s?k=smartphone&rh=p_36%3A-2000000` in Chrome or Edge.
2. IF the page shows a robot check (CAPTCHA) THEN the bot SHALL stop with the message
   "Amazon showed a robot check. Stopping." and SHALL NOT try to get around it.
3. The bot SHALL read only the first page, and SHALL NOT log in.

## Requirement 2: Extract and clean the phones

**User story:** As a student, I want each phone's name, price and rating as clean data,
so that I can sort and filter it.

Acceptance criteria:
1. The bot SHALL extract name, price and rating for every result on the page.
2. The bot SHALL turn price text such as "₹9,499" into the whole number 9499.
3. The bot SHALL keep only phones with a price from 1 to 20,000, even if the page
   shows dearer sponsored results.
4. IF no phone is left THEN the bot SHALL stop with the message "No phones found under Rs 20,000."
5. The bot SHALL remove duplicate rows and sort by price, cheapest first.

## Requirement 3: Save to Excel

**User story:** As a student, I want the list in Excel, so that I can open and share it.

Acceptance criteria:
1. The bot SHALL write `PhonesUnder20K.xlsx`, sheet "Phones", with the header row
   Name, Price, Rating, creating the file if it does not exist.
2. The bot SHALL log how many phones it saved.
3. `python check_phones.py` SHALL print PASSED on the file the bot wrote.
