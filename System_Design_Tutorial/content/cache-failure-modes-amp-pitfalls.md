# Cache Failure Modes &amp; Pitfalls

## Overview
Welcome to the module on **Cache Failure Modes &amp; Pitfalls**. This page covers the following related subtopics:

- Cache stampede / thundering herd — many requests hit DB simultaneously on cache miss
- Fix: mutex / lock around cache miss, OR probabilistic early expiry
- Cache penetration — queries for non-existent keys bypass cache
- Fix: cache null values with short TTL, OR bloom filter at cache layer
- Cache avalanche — many keys expire simultaneously, DB overwhelmed
- Hot key — one key receives disproportionate traffic (celebrity problem)

---

## Cache stampede / thundering herd — many requests hit DB simultaneously on cache miss

Detailed content for **Cache stampede / thundering herd — many requests hit DB simultaneously on cache miss** is currently being formulated. Check back soon!

## Fix: mutex / lock around cache miss, OR probabilistic early expiry

Detailed content for **Fix: mutex / lock around cache miss, OR probabilistic early expiry** is currently being formulated. Check back soon!

## Cache penetration — queries for non-existent keys bypass cache

Detailed content for **Cache penetration — queries for non-existent keys bypass cache** is currently being formulated. Check back soon!

## Fix: cache null values with short TTL, OR bloom filter at cache layer

Detailed content for **Fix: cache null values with short TTL, OR bloom filter at cache layer** is currently being formulated. Check back soon!

## Cache avalanche — many keys expire simultaneously, DB overwhelmed

Detailed content for **Cache avalanche — many keys expire simultaneously, DB overwhelmed** is currently being formulated. Check back soon!

## Hot key — one key receives disproportionate traffic (celebrity problem)

Detailed content for **Hot key — one key receives disproportionate traffic (celebrity problem)** is currently being formulated. Check back soon!

> [!NOTE]
> **Teacher's Note:** This is the *Light-Depth Baseline Version* of this tutorial. We will upgrade this page with deep-dives shortly!
