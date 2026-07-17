# Machine Coding & LLD Case Studies

Welcome to the ultimate test of your Low-Level Design skills. In top-tier tech interviews (like at Amazon, Uber, or Flipkart), you will be asked to do "Machine Coding". You are given a complex problem (like a Parking Lot) and 90 minutes to write working, object-oriented code.

In this masterclass, we will break down the architecture of the five most commonly asked LLD questions.

## Parking Lot Design

The Parking Lot is the "Hello World" of Low-Level Design interviews. It tests your ability to model physical entities and handle state changes.

### Core Requirements
1. The parking lot has multiple levels.
2. Each level has multiple spots (Compact, Large, Handicapped, Motorcycle).
3. Vehicles (Car, Truck, Van, Motorcycle) can park in appropriate spots.
4. The system must issue a ticket when a vehicle enters and calculate a fee when it exits.

### Architectural Breakdown
- **Enums:** `VehicleType`, `ParkingSpotType`, `TicketStatus`.
- **Entities (Models):** `Vehicle` (Abstract), `Car`, `Truck`, `ParkingLot`, `ParkingLevel`, `ParkingSpot`, `ParkingTicket`.
- **Services (Logic):** `EntryPanelService`, `ExitPanelService`, `PricingStrategy`.

> [!TIP]
> **Design Pattern Opportunity:** Use the **Strategy Pattern** for the `PricingStrategy`. Different parking lots charge differently (hourly, flat rate, weekend surge). Don't hardcode the math in the `ExitPanel`.

## Elevator System Design

The Elevator System tests your ability to handle concurrency, scheduling algorithms, and hardware-software interaction.

### Core Requirements
1. Multiple elevators in a building with multiple floors.
2. Users can press a button on a floor (Up/Down) or inside the elevator (Destination floor).
3. The system must optimally dispatch elevators to minimize wait times.

### Architectural Breakdown
- **Entities:** `ElevatorSystem`, `ElevatorCar`, `Floor`, `Door`, `Button` (Abstract), `HallButton`, `ElevatorButton`.
- **State:** Each `ElevatorCar` has a `Direction` (UP, DOWN, IDLE) and a `Status` (MOVING, STOPPED, MAINTENANCE).
- **The Algorithm:** The heart of this system is the `ElevatorDispatcher`. A common approach is the **SCAN algorithm** (the elevator keeps going up until all up requests are fulfilled, then reverses direction).

## LRU Cache Design

The Least Recently Used (LRU) Cache is heavily focused on Data Structures. It's less about OOP and more about achieving O(1) time complexity for `get()` and `put()`.

### The "Why"
A cache stores frequently accessed data in memory. When memory is full, we must evict an item. LRU evicts the item that hasn't been accessed for the longest time.

### Architectural Breakdown
You need exactly two data structures:
1. **Doubly Linked List (DLL):** Maintains the chronological order of accesses. The most recently used item is moved to the Head. The least recently used item sits at the Tail.
2. **HashMap:** Maps keys to the exact Node in the DLL. This allows us to look up a node in O(1) time and update its position without traversing the list.

## BookMyShow / Ticket Booking LLD

This problem tests your ability to handle concurrency and database locking (preventing two people from booking the same seat).

### Core Requirements
1. Users can search for movies, theaters, and shows.
2. Users can select seats and book them.
3. System must handle concurrent booking requests.

### Architectural Breakdown
- **Entities:** `Movie`, `CinemaHall`, `Show`, `Seat`, `Booking`, `Payment`.
- **Concurrency Control:** This is the most critical part. You must explain how you will lock the seats.
  - **Pessimistic Locking:** Lock the row in the database as soon as the user selects the seat. (Can cause bottlenecks).
  - **Optimistic Locking:** Allow multiple people to select the seat, but when they try to pay, check a `version` or `status` column. The first one to commit wins.

| Locking Strategy | Pros | Cons |
|------------------|------|------|
| **Pessimistic** | Guarantees the user gets the seat | Slow, locks out other users during the checkout timer |
| **Optimistic** | Fast, highly scalable | User might get rejected at the very end of checkout |

## Splitwise / Expense Sharing LLD

Splitwise tests your ability to model complex graphs and optimize transactions.

### Core Requirements
1. Users can add expenses (e.g., Alice paid $100 for Bob, Charlie, and herself).
2. Expenses can be split equally, exactly, or by percentage.
3. The system must show "Who owes who".
4. **Advanced:** Simplify debts (If A owes B $10, and B owes C $10, simplify it to A owes C $10).

### Architectural Breakdown
- **Entities:** `User`, `Expense`, `Split` (Abstract), `EqualSplit`, `ExactSplit`, `PercentSplit`.
- **Design Pattern:** The **Factory Pattern** is perfect here to generate the correct type of `Split` object based on user input.
- **The Simplification Algorithm:** This requires a graph. You calculate the net balance for every user. You put all users with a positive balance in one list, and a negative balance in another. You then greedily match the largest positive with the largest negative until all balances are zero.

> [!WARNING]
> **Common Beginner Mistake:**
> Do not try to store every single debt transaction as a permanent, immutable record if you are also running the simplification algorithm. You must differentiate between an `ExpenseRecord` (the receipt of the dinner) and the `BalanceSheet` (the current optimized debts).
