# Frontend pages, styles ও interaction

| Page | Markup | Controller | কাজ |
| --- | --- | --- | --- |
| /login | login.html | login.js | Glass sign-in, password visibility, errors |
| / | index.html | dashboard.js | Overview metrics, recent loans, inventory snapshot |
| /books | books.html | books.js | Search, add/restock, stock reduction |
| /students | students.html | students.js | Directory, Add Member, Edit, membership status |
| /circulation | circulation.html | circulation.js | Eligible member/book issue এবং return |
| /fines | fines.html | fines.js | Outstanding fine totals ও mark paid |
| /accounts | accounts.html | accounts.js | Admin account management |
| /audit | audit.html | audit.js | Admin history filters ও field comparison |

Management pages styles.css + shared.js ব্যবহার করে। login page separate login.css/login.js ব্যবহার করে। scripts markup-এর শেষে load হয় তাই querySelector-এর elements আগে তৈরি থাকে। shared.js একটি IIFE থেকে LibraryApp object ফেরায়; page controller IIFE তার helpers destructure করে। No module bundler/React/state library।

styles.css :root tokens colors/spacing-related reusable values রাখে; header/nav, surfaces, metrics, tables, buttons, modals, forms ও responsive breakpoints আছে। Tables .table-wrap overflow-x:auto; narrow screens-এ wide member fields scroll হয়। Dialog open class toggles display, role/aria-modal/aria-hidden set হয়, Escape/backdrop/cancel close; Tab trap ও focus restoration আছে। Toast aria-live polite।

login.css multiple backgrounds: gradient overlay, pstu-library.jpg, fallback library-dashboard.png। Glass panel translucent gradient/tint, backdrop blur/saturation, border/shadow। No-backdrop-filter browser-এ darker fallback। Autofill text/background override ও Show/Hide button solid background readability বজায় রাখে। Mobile single column; short desktop viewport padding কমে। CSS query versions cache refresh করে, build hashes নয়।

login.js username trim, empty username check, AbortController 30-second timeout, single submitting flag, aria-busy এবং response payload role validation রাখে। Error message textContent; malformed JSON success response redirect হয় না। Show/Hide password type বদলায় এবং aria-pressed/aria-controls update হয়।

shared loadData coalesces overlapping refreshes and loads the complete dataset through /api/snapshot in one Oracle connection. Temporary GET failures retry once; failed loads retain old records and block changes. Recovery polling runs every five seconds, plus online/visibility events. Non-401 session lookup failures show an error instead of forcing login redirect.

Member full Edit-এর visible fields name/department/phone/email/roll/reg/status; hidden student_id endpoint target। Enable/Disable আলাদা quick action-ও থাকে। Save-এর পরে reload হওয়ায় directory ও নতুন page reads updated values দেখায়। Circulation select client-side eligibility filter করে; server final checks রাখে। Search browser state-এ হওয়ায় server read endpoint full list আনে।

The management dashboard shows available copies, active loans, members, active reservations and unpaid balances. Priorities highlight overdue returns, pending pickups and fines. The member dashboard separates catalogue, borrowing, reservations, fines and security. MemberDashboard and ReservationDesk own their views; reservations.js coordinates refresh and shared actions.
