# Ciphers

*Last updated: 2026-09-10*

> Encryption and decryption under a cryptographic contract.

## Location

### Folder
- must use `Ciphers/` for a role folder under the domain that owns the capability.

### File
- file rules → [one type, one file](../../mla.md).

---

## Declaration

### Type doc
- inherited documentation → [behavior](behavior.md) § *Shared rules*.

#### [Summary](../../../lla/notation/documentation/summary.md)
- must start a concrete implementation with **Encrypts**, naming the protected value and decryption capability.
- interface starter → [language constructs](../../../lla/constructs/constructs.md) § *Behavior components*.

### Construct
- declaration and injection → [behavior](behavior.md) § *Shared rules*.

### Type name
- must suffix with `Cipher`.
- contract and implementation prefixes → [constructs](../constructs.md) § *Role and shape*.

---

## Content

- failure modes and carrier selection → [results](../../components/result.md).
- static eligibility → [constructs](../constructs.md) § *Static or instance*.
