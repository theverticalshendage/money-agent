@"
# Money Agent — Notes & Deferred Improvements

## Parser
- [ ] Refund handling: positive UPI amounts (e.g. UPI/CR/.../REFUND AMAZON) currently
      classify as 'transfer' with an awkward merchant. Consider a REFUND type, or
      using the amount sign (positive UPI = incoming/credit) for better labels.
      Deferred on Day 3 to prioritize the running-balance logic. Revisit when the
      LLM interpretation layer lands (Week 2) — refunds may be better handled there.
"@ | Out-File -FilePath NOTES.md -Encoding utf8