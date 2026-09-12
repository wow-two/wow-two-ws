# Trackers

*Last updated: 2026-09-10*

> Live operational state updated by producers and persisted nowhere.

## Location

### Folder
- must use `Trackers/` for a role folder under the domain that owns the capability.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc
- inherited documentation → [behavior](behavior.md) § *Shared rules*.

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start a concrete implementation with **Tracks**, naming the live state it tracks.
- interface starter → [language constructs](../../../lla/constructs/constructs.md) § *Behavior components*.

### Construct
- declaration and injection → [behavior](behavior.md) § *Shared rules*.

### Type name
- must suffix with `Tracker`.
- contract and implementation prefixes → [constructs](../constructs.md) § *Role and shape*.

---

## Content

- failure modes and carrier selection → [results](../../components/result.md).
- may hold mutable live state, overriding the default in
  [language constructs](../../../lla/constructs/constructs.md) § *Behavior components*.
- must keep updates safe for the lifetime and concurrency under which the tracker is registered.
- must use `Repository` when the state is persisted beyond the tracking lifecycle.
