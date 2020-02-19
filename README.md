# DB schema

## new schema

User:
- Username(PK)
- Password 
- Name
- Phone(Unique)
- Email(Unique)
- Balance
- Photo
     
Watchlist:
- Username(FK)
- Company_id(FK)

Connections:
- Follower(Username(FK))
- Following(Username(FK))

transaction:
- transaction_id(PK)
- seller(Username(FK))
- buyer(Username(FK))
- status - {PENDING, SUCCESS, FAILED, CANCELLED}
- company_id(FK)
- cost price(i.e. selling price at that instance)
- number of shares
- time

Shares:
- Comapany_id(FK)
- Username(FK)
- Number of shares acquired
- Number of shares on sale

Company:
- Company_id(PK)
- name
- Owner(Username)(FK)
- Description
- Selling price
- *fit stats obtained by api*

Register_Event:(Performed by user)
- Username(FK)
- Event_id(FK)
- status - {Registered, Not Registered}

Events:
- Company_id(FK)
- Event_id(PK)
- name
- place
- start time
- end time
- Status - {Running, Completed, Cancelled, Upcoming}
     
* Separate Modules to be integrated later
* IF YOU HAD INVESTED CURRENCY CONVERTER(FOREX) FIND BROKER

<!-- ## models
- User
  - user ID
  - User name
  - Email
  - password

- Company
  - company Id
  - company Name
  - company type
  - unit stock price

- Stock Detail
  - Foreign key -> owning company
  - Foreign key -> owning user
  - qty  

- Transaction
  - Foreign key -> user Id
  - Foreign key -> company Id

- Notice Board
  - stores stock that are for sale
  - stock company name
  - stock qty avail for sale
  - unit stock price -->


## Stock API used
- received format
  - JSON
- Alpha Vantage
  - limitation, 5 req per min, 500 per day


## Features
- TOP GAINERS
- TOP LOSERS
- TOP ACTIVE

- GLOBAL INDICES
  - WEEKLY, MONTHLY DAILY

- EVENTS: (ONLY COMPANIES CAN CREATE)

- COMPANY:

- USER:
  -PORTFOLIO
  -WATCHLIST
  -FRIENDS/CONNECTIONS
  -CHATBOX
  
-EXTRA FEATURES:
  -IF YOU HAD INVESTED
  -CURRENCY CONVERTER(FOREX)
  -FIND BROKER  
