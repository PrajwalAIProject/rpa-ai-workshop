# Tasks: PhoneDeals bot

> Reference copy. Kiro keeps its own in `.kiro/specs/phone-deals/tasks.md`. Ask Kiro to
> explain each task (Prompt 2), then build it in Studio and tick it off.

- [ ] 1. Create the Studio project `PhoneDeals` (Process, Windows, VB) in `C:\PhoneDeals`;
      install UiPath.UIAutomation.Activities and UiPath.Excel.Activities. *(Req 1)*
- [ ] 2. Add **Use Application/Browser** with the search URL. *(Req 1.1)*
- [ ] 3. Add the robot-check stop: **Check App State** + **Throw BusinessRuleException**. *(Req 1.2)*
- [ ] 4. Add **Extract Table Data**: Name, Price, Rating; one page only; output `dtRaw`. *(Req 1.3, 2.1)*
- [ ] 5. Add **Build Data Table** for `dtPhones`. *(Req 2)*
- [ ] 6. Add **For Each Row in Data Table**: clean the price, keep 1–20,000, add the row. *(Req 2.2, 2.3)*
- [ ] 7. Stop when no phone is left. *(Req 2.4)*
- [ ] 8. **Remove Duplicate Rows** and **Sort Data Table** by Price, ascending. *(Req 2.5)*
- [ ] 9. **Use Excel File** + **Write DataTable to Excel** to sheet "Phones" with headers. *(Req 3.1)*
- [ ] 10. **Log Message** with the count. *(Req 3.2)*
- [ ] 11. Run with `uip rpa run-file --file-path C:\PhoneDeals\Main.xaml`, then
      `python check_phones.py` must print PASSED. *(Req 3.3)*
