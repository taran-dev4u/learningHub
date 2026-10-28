/* Hand-maintained LLD roadmap lessons. Loaded after topics.js and contentBundle.js. */
(function () {
  'use strict';
  var topics = window.topicsData;
  var bundle = window.contentBundle;
  if (!Array.isArray(topics) || !bundle) return;

  var additions = [
    {
      section: '🧭 4. Domain Modeling & Invariants', priority: 'Must know',
      subsections: [{ id: 'domain-modeling', title: 'Domain Modeling & Invariants', file: 'domain-modeling.md', concepts: [
        { title: 'Requirements to Use Cases', anchor: 'requirements-to-use-cases' },
        { title: 'Entities & Value Objects', anchor: 'entities-value-objects' },
        { title: 'Aggregates & Invariant Ownership', anchor: 'aggregates-invariant-ownership' },
        { title: 'Bounded Contexts & Vocabulary', anchor: 'bounded-contexts-vocabulary' }
      ] }]
    },
    {
      section: '🔒 5. State & Concurrency', priority: 'Must know',
      subsections: [{ id: 'state-concurrency', title: 'State & Concurrency', file: 'state-concurrency.md', concepts: [
        { title: 'State Machines & Legal Transitions', anchor: 'state-machines-legal-transitions' },
        { title: 'Atomic Operations & Race Conditions', anchor: 'atomic-operations-race-conditions' },
        { title: 'Locking, Optimistic Versions & Ownership', anchor: 'locking-optimistic-versions-ownership' },
        { title: 'Retries, Idempotency & Time', anchor: 'retries-idempotency-time' }
      ] }]
    },
    {
      section: '🔌 6. Persistence & API Boundaries', priority: 'Must know',
      subsections: [{ id: 'persistence-boundaries', title: 'Persistence & API Boundaries', file: 'persistence-boundaries.md', concepts: [
        { title: 'Repositories & Dependency Direction', anchor: 'repositories-dependency-direction' },
        { title: 'Transactions & Consistency Scope', anchor: 'transactions-consistency-scope' },
        { title: 'API Contracts, Errors & Validation', anchor: 'api-contracts-errors-validation' },
        { title: 'External Services & Failure Boundaries', anchor: 'external-services-failure-boundaries' }
      ] }]
    },
    {
      section: '🧪 10. Testing & Design Evolution', priority: 'Must know',
      subsections: [{ id: 'testing-evolution', title: 'Testing & Design Evolution', file: 'testing-evolution.md', concepts: [
        { title: 'Unit Tests for Invariants', anchor: 'unit-tests-for-invariants' },
        { title: 'Integration & Contract Tests', anchor: 'integration-contract-tests' },
        { title: 'Concurrency & Failure Tests', anchor: 'concurrency-failure-tests' },
        { title: 'Refactoring Under New Requirements', anchor: 'refactoring-under-new-requirements' }
      ] }]
    }
  ];

  bundle['domain-modeling.md'] = String.raw`# Domain Modeling & Invariants

> [!TIP]
> Follow this chapter after OOP and UML. The goal is to turn a prompt into objects that own business rules, before choosing a design pattern.

## Requirements to Use Cases

**Why it matters:** A class diagram drawn before the behavior is clear often becomes a collection of nouns with no responsibilities.

### Learn

1. Write the actors, actions, and outcomes. For a ticket system: a customer selects seats, holds them, pays, or lets the hold expire.
2. Ask which facts must always be true: one active hold per seat per show, no paid booking without a payment result, and no expired hold accepted.
3. Separate commands that change state from queries that read it. Name commands in the domain language: holdSeats, confirmBooking, releaseExpiredHold.
4. Walk one happy path and at least two failure paths before drawing classes. Each decision or state change suggests an owner.

**Practice:** For a parking lot, write use cases for entry, spot assignment, payment, and exit. Mark the rule that prevents assigning the same spot twice.

## Entities & Value Objects

**Why it matters:** Identity determines whether an object needs a lifecycle. Treating every noun as a mutable entity creates needless coupling.

### Learn

- An **entity** keeps identity as its attributes change. Booking 123 remains the same booking when its status changes.
- A **value object** is identified by its value. Money(10, USD), a date range, or a seat coordinate can usually be immutable and compared by value.
- Put validation in constructors or factories: Money must have a currency and a valid amount; a DateRange must end after it starts.
- Prefer behavior on the owner. A booking decides whether it may be canceled; a caller should not set status directly.

**Practice:** Classify Booking, Seat, Price, Address, and PaymentAttempt. Explain which identifiers must survive a process restart.

## Aggregates & Invariant Ownership

**Why it matters:** In an interview, the crucial question is often "where is this rule enforced when two requests arrive together?"

### Learn

- An **aggregate** is the smallest consistency boundary that can protect a rule in one transaction. Access its internal state through the root.
- Do not make every related object one giant aggregate. A booking and a payment can have separate lifecycles; connect them with identifiers and an explicit workflow.
- State the invariant and the owner together: "ShowInventory owns the rule that a seat has at most one active hold."
- Keep methods intention revealing: reserve(seatId, customerId, expiresAt) conveys more than setReserved(true).

**Practice:** Choose an aggregate root for a vending machine inventory. Describe how it rejects selling the last item twice.

## Bounded Contexts & Vocabulary

**Why it matters:** The same word can mean different things in different parts of a system. One universal model becomes hard to change.

### Learn

- Draw a boundary when vocabulary, rules, or ownership differ. "Order" in checkout and "order" in fulfillment may have different data and transitions.
- Use the business's words consistently in code and diagrams. If the prompt says "hold," do not call it a "booking" until payment succeeds.
- Keep a local LLD exercise focused. Show external contexts as interfaces, then explain how they interact only when asked.
- A boundary is not automatically a microservice. A modular monolith can have clear contexts and still deploy as one application.

**Practice:** Split a food delivery prompt into ordering, dispatch, and payments. Give each context one rule it owns.

### Further reading

- [Microsoft: Domain analysis and bounded contexts](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis)
- [Microsoft: Tactical domain design](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-ddd)
`;

  bundle['state-concurrency.md'] = String.raw`# State & Concurrency

> [!NOTE]
> LLD case studies such as ticket booking, elevator control, wallets, and ride matching are stateful. A clean class diagram is incomplete until legal transitions and simultaneous calls are defined.

## State Machines & Legal Transitions

**Why it matters:** Status fields are easy to write and easy to corrupt. Explicit transitions make invalid states visible.

### Learn

- List states and events. A seat hold might be AVAILABLE → HELD → CONFIRMED, or HELD → EXPIRED. CONFIRMED → AVAILABLE is not a normal timeout transition.
- Put transition guards beside the transition: confirm requires an unexpired hold and a successful payment reference.
- Make terminal states clear. Decide whether cancel is allowed after confirmation and what it changes.
- The State pattern can organize many behaviors, but a small enum plus guarded methods may be simpler. Choose by complexity, not by pattern count.

**Practice:** Draw a vending machine's states and reject dispense before payment or after stock is exhausted.

## Atomic Operations & Race Conditions

**Why it matters:** A check followed by an update is unsafe when another request can run between them.

### Learn

- Write the interleaving: A reads "seat free"; B reads "seat free"; A reserves; B reserves. Both believed they won.
- Identify the **linearization point**, the one atomic operation that decides the winner. It might be a database conditional update, unique constraint, or lock-protected in-memory transition.
- Guard the entire invariant, not just a field write. A thread-safe map alone does not make a read-then-write sequence atomic.
- Define what the loser sees: conflict, retry, alternate seat, or wait. That response is part of the design.

**Practice:** Explain how two users requesting the last parking spot receive exactly one success.

## Locking, Optimistic Versions & Ownership

**Why it matters:** Different concurrency tools fit different contention and deployment assumptions.

| Choice | Good fit | Failure or cost to discuss |
|---|---|---|
| In-process lock | One process owns all state | Does not protect another process |
| Database transaction + row lock | Shared persistent state, high contention | Waiting, deadlocks, shorter critical sections |
| Optimistic version check | Conflicts are relatively rare | Caller must retry or report a conflict |
| Unique constraint | A uniqueness invariant | Still handle the rejected write |

**Practice:** For a wallet transfer, state which record or aggregate is locked and how balance and ledger stay consistent.

## Retries, Idempotency & Time

**Why it matters:** Timeouts leave the caller unsure whether the operation happened. Blind retries can charge twice or create duplicate bookings.

### Learn

- Give a state-changing request an idempotency key. Store the key with the outcome so a retry returns the first result rather than applying a second effect.
- Define a time source and expiration rule for holds. Use an injected clock in tests; do not scatter system time calls through domain objects.
- Separate a reservation's expiry from the cleanup job. Even if cleanup is late, confirmation must reject an expired hold.
- Document retryable errors and final errors. A network timeout may warrant a status lookup; invalid input should not be retried unchanged.

**Practice:** A payment succeeds but the response is lost. Trace the retry and prove there is only one charge.

### Further reading

- [Oracle: Java concurrency utilities](https://docs.oracle.com/en/java/javase/26/core/concurrency.html)
- [Microsoft: Idempotency and retry semantics](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-implementation)
`;

  bundle['persistence-boundaries.md'] = String.raw`# Persistence & API Boundaries

> [!TIP]
> Keep the core model understandable without a database or framework. Show adapters when an exercise asks how the design would work in a real service.

## Repositories & Dependency Direction

**Why it matters:** A domain object should express rules without knowing SQL, HTTP, or a vendor SDK.

### Learn

- Define an interface around the operation the use case needs, such as findBooking(id) and save(booking). Do not expose a generic query language unless the problem needs one.
- Put the interface near the application or domain code that uses it; put SQL or storage details in an implementation outside that boundary.
- Use an in-memory implementation for a short machine-coding exercise, while preserving the same behavior contract as a persistent implementation.
- Do not hide a multi-step transaction behind unrelated repository calls. The transaction owner must be explicit.

**Practice:** Swap an in-memory BookingRepository for a SQL version without changing Booking's transition rules.

## Transactions & Consistency Scope

**Why it matters:** Saying "use a transaction" is only useful after naming which changes must commit together.

### Learn

- Write the atomic set: decrement available seats, create a hold, and record its expiry. Either all commit or none do.
- Put the transaction boundary in the application service or unit of work that coordinates repositories. Keep business rules inside the domain model.
- A database transaction cannot automatically cover a remote payment provider. Model that as a workflow with compensating or reconciliation steps.
- Explain isolation where the invariant needs it, and use constraints or conditional writes to close races.

**Practice:** A booking row commits but payment fails. Specify the resulting state and the recovery action.

## API Contracts, Errors & Validation

**Why it matters:** A caller needs stable inputs, outputs, and failure meaning; class names alone do not form a usable interface.

### Learn

- Validate syntax at the boundary and domain rules in the owner. A malformed seat ID is a request error; an already-held seat is a domain conflict.
- Name result types or error codes: NotFound, Conflict, InvalidTransition, ExpiredHold. Show which are safe to retry.
- Keep transport models separate from entities. Do not let a client set protected fields such as paymentConfirmed or inventoryCount.
- A contract should say whether an operation is idempotent and whether its result can be queried after a timeout.

**Practice:** Sketch reserveSeat(request) and its success, conflict, and validation responses.

## External Services & Failure Boundaries

**Why it matters:** Payment, notification, and identity providers can be slow or fail after the local state changes.

### Learn

- Put an interface around each external capability. The application layer orchestrates it; the domain model should not make network calls.
- Distinguish a call failure from an unknown outcome. An unknown payment outcome needs lookup or reconciliation, not immediate replay with a new request ID.
- Keep notifications out of the critical transaction when possible. A failed email should not undo a valid booking.
- In an interview, state the simplest assumption first, then show the extension for production failure handling.

**Practice:** Draw the flow for a ticket purchase when the notification provider is down.

### Further reading

- [Microsoft: Tactical domain design and application services](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-ddd)
- [Microsoft: Designing the persistence layer](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design)
- [Microsoft: Web API design](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design)
`;

  bundle['testing-evolution.md'] = String.raw`# Testing & Design Evolution

> [!NOTE]
> A machine-coding answer is easier to trust when a few focused tests demonstrate its rules. Tests also show whether the design can absorb a follow-up requirement.

## Unit Tests for Invariants

**Why it matters:** A class diagram can look correct while methods permit impossible states.

### Learn

- Test each legal transition and at least one rejected transition. For Booking, test hold → confirm and expired hold → rejected confirmation.
- Assert externally visible behavior, not private fields or the exact number of helper calls.
- Use small fake implementations of clocks and repositories to make time and state deterministic.
- Add boundary values: zero quantity, last available seat, expiry at the exact deadline, and duplicate command IDs.

**Practice:** Write three tests that prove a seat cannot be sold twice.

## Integration & Contract Tests

**Why it matters:** Unit tests cannot prove that an SQL constraint, serializer, or API adapter honors the same contract.

### Learn

- Test the repository with the real storage technology for save, reload, conflict, and rollback behavior.
- Test the API with realistic requests for validation, success, conflict, and documented error codes.
- Keep a small end-to-end path for the critical flow, rather than trying to prove every rule through the UI.
- Test an adapter against the same interface contract when implementations are swapped.

**Practice:** Persist a hold, reload it in a new application instance, and confirm that its expiry still applies.

## Concurrency & Failure Tests

**Why it matters:** A sequential test will never reveal the classic double-booking race.

### Learn

- Start two requests against one limited resource and assert exactly one succeeds. Use a barrier so both reach the contested operation together.
- Inject a failure after each important step: before commit, after commit but before response, and during the external call.
- Check final state, not only returned errors. The ledger, inventory, and booking records must agree.
- Repeat the same idempotency key and assert one effect with the same logical result.

**Practice:** Simulate a response timeout after a successful charge, then retry the purchase.

## Refactoring Under New Requirements

**Why it matters:** Interviewers often add a requirement to see where your design bends.

### Learn

- First state which existing class owns the new rule. If no owner fits, introduce one focused abstraction rather than a catch-all manager.
- Preserve existing tests while making the change. New tests should describe the added behavior.
- A design pattern is useful when it isolates a real variation point. Do not install Strategy, Factory, and Observer for hypothetical requirements.
- Revisit the diagram after the code changes; it should explain the implemented responsibilities, not an earlier sketch.

**Practice:** Add dynamic pricing to a booking design. Identify the variation point, test it, and explain what remains unchanged.

### Further reading

- [Martin Fowler: Test Pyramid](https://martinfowler.com/bliki/TestPyramid.html)
- [Martin Fowler: Unit Test](https://martinfowler.com/bliki/UnitTest.html)
`;

  function insertBefore(match, value) {
    var index = topics.findIndex(function (item) { return item.section.indexOf(match) !== -1; });
    if (index < 0) throw new Error('LLD roadmap insertion point missing: ' + match);
    topics.splice(index, 0, value);
  }
  insertBefore('Design Patterns — Creational', additions[0]);
  insertBefore('Design Patterns — Creational', additions[1]);
  insertBefore('Design Patterns — Creational', additions[2]);
  insertBefore('LLD Interview Technique', additions[3]);
  topics.forEach(function (section, index) {
    section.section = section.section.replace(/^(\D*?)\d+\.\s+/, '$1' + (index + 1) + '. ');
  });
}());
