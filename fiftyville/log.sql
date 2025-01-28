-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Let's find out about the description of the crime_scene_reports and that maybe gives us a clue
SELECT description
FROM crime_scene_reports
WHERE street = "Humphrey Street"
    AND month = 7 AND day = 28 AND year = 2023;
-- 10.15 am at the bakery 3 interviews with witnesses present at the time, all mention the bakery

-- let's find about a little bit more about those interviews
SELECT transcript,id
FROM interviews
WHERE month = 7 AND day = 28 AND year = 2023;
-- interview 160 mention probably footage of thief's car in bakery's parking lot 10 minute-range
-- interview 161 recognized the thief from earlier that morning in Leggett Street withdrawing money
-- interview 162 talked to someone in the phone planning to fly out from fiftyville the next day and the person on the phone might have purchased the ticket

-- let's see if we can find something about the transactions in the atm
SELECT account_number, transaction_type, amount
FROM atm_transactions
WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = "Leggett Street";
/* account_number | transaction_type | amount |
+----------------+------------------+--------+
| 28500762       | withdraw         | 48     |
| 28296815       | withdraw         | 20     |
| 76054385       | withdraw         | 60     |  this are the transactions that could
| 49610011       | withdraw         | 50     |  be from the thief
| 16153065       | withdraw         | 80     |
| 86363979       | deposit          | 10     |
| 25506511       | withdraw         | 20     |
| 81061156       | withdraw         | 30     |
| 26013199       | withdraw         | 35
*/

-- let's search the owner of the bank accounts in the list
SELECT name
FROM people
WHERE id IN (SELECT person_id
             FROM bank_accounts
             WHERE account_number = 28500762 OR account_number = 28296815
                OR account_number = 76054385 OR account_number = 49610011
                OR account_number = 16153065 OR account_number = 25506511
                OR account_number = 81061156 OR account_number = 26013199);
/* the suspect name:
+---------+
|  name   |
+---------+
| Kenny   |
| Iman    |
| Benista |  We can probably dicard the women but not doing it yet just in case
| Taylor  |
| Brooke  |
| Luca    |
| Diana   |
| Bruce   |
+---------+*/

-- lets look for a match between these names and the names from the cars in the parking lot
SELECT name
FROM people
WHERE license_plate IN (SELECT license_plate
                        FROM bakery_security_logs
                        WHERE month = 7 AND day = 28 AND year = 2023 AND hour = 10 AND minute BETWEEN 15 AND 25);
/* the names from the cars in the parking lot:
+---------+        +---------+
|  name   |
+---------+
| Kenny   |
| Iman    |
| Benista |  We can probably dicard the women but not doing it yet just in case
| Taylor  |
| Brooke  |
| Luca    |
| Diana   |
| Bruce   |
+---------+    The names that appear in both places are the principal suscpects at the moment:
|  name   |
+---------+     Bruce, Iman, Luca, Diana
| Vanessa |
| Barry   |
| Iman    |
| Sofia   |
| Luca    |
| Diana   |
| Kelsey  |
| Bruce   |
+---------+
*/

--Lets search for the ones that also have some relation between each other because they've had a phone call at that time
SELECT name FROM people WHERE phone_number IN
    (SELECT caller
    FROM phone_calls
    WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 120)
    OR phone_number IN
        (SELECT caller
    FROM phone_calls
    WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 120);

/* names of people in calls that could fit the mentioned in the interview of the witness
+---------+
|  name   |
+---------+
| Sean    |
| Kenny   |
| Sofia   |  this were the suspects before this query:
| Benista |    Bruce, Iman, Luca, Diana
| Taylor  |
| Anna    |  but know we have : Bruce, Diana
| Diana   |
| Kelsey  |
| Kathryn |
| Betty   |
| Arthur  |
| Peter   |
| John    |
| Bruce   |
| Terry   |
| Jason   |
| Harold  |
| Mark    |
| Carina  |
+---------+
*/

-- lets find out if Bruce and Diana appear in the same call
SELECT
    p1.name AS caller_name,
    p2.name AS receiver_name,
    pc.duration
FROM phone_calls pc
LEFT JOIN people p1 ON pc.caller = p1.phone_number
LEFT JOIN people p2 ON pc.receiver = p2.phone_number
WHERE pc.year = 2023 AND pc.month = 7 AND pc.day = 28 AND pc.duration < 120;

-- Bruce talks to Robin for 45 s bruce calls robin
-- Bruce talks to Carl for 75s bruce is the caller
-- Diana tals to philip for 49s and diana is the caller too

-- lets see the flights that the thief could have taken
SELECT
    p.id AS person_id,
    p.name,
    p.passport_number,
    a_dest.city AS destination_city,
    f.hour
FROM flights f
JOIN passengers pa ON f.id = pa.flight_id
JOIN people p ON pa.passport_number = p.passport_number
JOIN airports a_orig ON f.origin_airport_id = a_orig.id
JOIN airports a_dest ON f.destination_airport_id = a_dest.id
WHERE a_orig.city = 'Fiftyville'
AND f.year = 2023 AND f.month = 7 AND f.day = 29
ORDER BY p.name;

/* this is the table with the names and flights that could the thief have taken
+-----------+-----------+-----------------+------------------+
| person_id |   name    | passport_number | destination_city |
+-----------+-----------+-----------------+------------------+
| 325548    | Brandon   | 7874488539      | San Francisco    |
| 458378    | Brooke    | 4408372428      | Tokyo            |
| 686048    | Bruce     | 5773159633      | New York City    |
| 423393    | Carol     | 6128131458      | Chicago          |
| 769190    | Charles   | 3915621712      | Boston           |
| 952462    | Christian | 2626335085      | Boston           |
| 750165    | Daniel    | 7597790505      | Chicago          |
| 447494    | Dennis    | 4149859587      | San Francisco    |
| 514354    | Diana     | 3592750733      | Boston           |
| 953679    | Doris     | 7214083635      | New York City    |
| 757606    | Douglas   | 3231999695      | Boston           |
| 757606    | Douglas   | 3231999695      | San Francisco    |
| 651714    | Edward    | 1540955065      | New York City    |
| 788213    | Emily     | 6263461050      | San Francisco    |
| 682850    | Ethan     | 2996517496      | Boston           |
| 788911    | Gloria    | 2835165196      | Boston           |
| 210641    | Heather   | 4356447308      | Chicago          |
| 753885    | Jennifer  | 7378796210      | San Francisco    |
| 677698    | John      | 8174538026      | Tokyo            |
| 210245    | Jordan    | 7951366683      | San Francisco    |
| 809265    | Jose      | 9183348466      | San Francisco    |
| 560886    | Kelsey    | 8294398571      | New York City    |
| 395717    | Kenny     | 9878712108      | New York City    |
| 253397    | Kristina  | 6131360461      | Boston           |
| 251693    | Larry     | 2312901747      | Tokyo            |
| 467400    | Luca      | 8496433585      | New York City    |
| 354903    | Marilyn   | 7441135547      | Chicago          |
| 619074    | Matthew   | 4195341387      | San Francisco    |
| 626361    | Melissa   | 7834357192      | Tokyo            |
| 542503    | Michael   | 6117294637      | Boston           |
| 205082    | Pamela    | 1050247273      | Tokyo            |
| 341739    | Rebecca   | 6264773605      | Chicago          |
| 710572    | Richard   | 7894166154      | Tokyo            |
| 398010    | Sofia     | 1695452385      | New York City    |
| 745650    | Sophia    | 3642612721      | Chicago          |
| 676919    | Steven    | 1151340634      | Tokyo            |
| 449774    | Taylor    | 1988161715      | New York City    |
| 660982    | Thomas    | 6034823042      | Tokyo            |
+-----------+-----------+-----------------+------------------+
*/
-- we continue to have Bruce that would have escaped to New York and Diana to Boston
-- but we have the id of both to see if they are in fact the same people from before -> Bruce id: 686048, Diana id: 514354
SELECT * FROM people
WHERE (name = 'Bruce')
   OR (name = 'Diana');
-- we see in the result that there are only 2 people called like bruce diana so they are in fact unique
--lets searc for the license plate in the time the witness told us
SELECT * FROM bakery_security_logs
WHERE license_plate IN ('322W7JE', '94KL13X');
/* and now we have the time that still fits both of the suspects for the robbery
+-----+------+-------+-----+------+--------+----------+---------------+
| id  | year | month | day | hour | minute | activity | license_plate |
+-----+------+-------+-----+------+--------+----------+---------------+
| 232 | 2023 | 7     | 28  | 8    | 23     | entrance | 94KL13X       |
| 240 | 2023 | 7     | 28  | 8    | 36     | entrance | 322W7JE       |
| 261 | 2023 | 7     | 28  | 10   | 18     | exit     | 94KL13X       | exit bruce
| 266 | 2023 | 7     | 28  | 10   | 23     | exit     | 322W7JE       | exit diana
+-----+------+-------+-----+------+--------+----------+---------------+

but considering that the thief was going to take the first flight out of fiftyville , we have this table that we calculated before
where the first flight between the two is..

BRUCE!
+-----------+-----------+-----------------+------------------+------+
| person_id |   name    | passport_number | destination_city | hour |
+-----------+-----------+-----------------+------------------+------+
| 325548    | Brandon   | 7874488539      | San Francisco    | 12   |
| 458378    | Brooke    | 4408372428      | Tokyo            | 15   |
| 686048    | Bruce     | 5773159633      | New York City    | 8    | 8am
| 423393    | Carol     | 6128131458      | Chicago          | 9    |
| 769190    | Charles   | 3915621712      | Boston           | 16   |
| 952462    | Christian | 2626335085      | Boston           | 16   | vs
| 750165    | Daniel    | 7597790505      | Chicago          | 9    |
| 447494    | Dennis    | 4149859587      | San Francisco    | 12   |
| 514354    | Diana     | 3592750733      | Boston           | 16   | 4pm
*/

SELECT
    p.id AS person_id,
    p.name,
    p.passport_number,
    f.year,
    f.month,
    f.day,
    f.hour AS flight_hour,
    a_dest.city AS destination_city,
    bsl.activity,
    bsl.hour AS log_hour,
    bsl.minute AS log_minute
FROM people p
JOIN bank_accounts ba ON p.id = ba.person_id
JOIN atm_transactions at ON ba.account_number = at.account_number
JOIN passengers pa ON p.passport_number = pa.passport_number
JOIN flights f ON pa.flight_id = f.id
JOIN airports a_orig ON f.origin_airport_id = a_orig.id
JOIN airports a_dest ON f.destination_airport_id = a_dest.id
JOIN bakery_security_logs bsl ON p.license_plate = bsl.license_plate
WHERE
    p.name = 'Bruce'
    AND at.year = 2023 AND at.month = 7 AND at.day = 28
    AND f.year = 2023 AND f.month = 7 AND f.day = 29
    AND a_orig.city = 'Fiftyville'
    AND bsl.year = 2023 AND bsl.month = 7 AND bsl.day = 28
    AND bsl.hour BETWEEN 8 AND 10
    AND (bsl.activity = 'entrance' OR bsl.activity = 'exit')
ORDER BY f.hour, bsl.hour, bsl.minute;

--SO WE CAN CONFIDENTLY SAY THAT THE THIEF WAS BRUCE THAT ESCAPED TO NEW YORK CITY AND HIS ACCOMPLICE IS ROBIN.

Who the thief is: Bruce
What city the thief escaped to: New York City
Who the thief’s accomplice is who helped them escape: Robin
