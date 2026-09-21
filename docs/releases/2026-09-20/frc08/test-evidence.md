# FRC08 final verification

Actual [Next → Go → PostgreSQL comparison](real-integration/result.json): four checkpoints PASS, no console/page errors. A7/B3:47500000/55000000 minor, difference7500000/15.79%; currentA8 does not change the pinned response. Ordinary workspace controls and rendered cost/budget/percentage were checked. Synthetic accounting fixtures were seeded through authorized APIs; the full ordinary map/edit/report flow remains FRC13.

| Check | Observed result |
|---|---|
| Frontend focused boundary/identity/composition |26/26 PASS |
| Independent rendered comparison |20/20 PASS,0skips |
| Combined FRC03/05/06/07/08 browser regressions |76/76 PASS,0skips,exit0 |
| Full frontend frozen-copy suite |341 total:239PASS,6FAIL,96opt-inSKIP;exit1 |
| Full historical signatures |6/6 exact matches against FRC07 and original FRC02; verification-logs/baseline-signatures.json |
| TypeScript / changed14-file ESLint |PASS,exit0;final command metadata and logs in verification-logs |
| Production build |PASS,exit0,Next16.2.11,frozen dependency install reused from accepted07 |
| Source consistency |426 source/config files copied and hashed; reviewer verified no working/copy drift after final build |
| Backend full Go tests/build |PASS |
| Real PostgreSQL FRC02/03/04/05/07/08 |29 top-level+20subcases PASS,no selected skip |
| Independent backend review package checks |Four tested packages PASS,one without tests |

The full frontend suite remains non-green. Six failures are compared by complete signatures against FRC07 and original FRC02, normalizing only the absolute frontend path. Opt-in rendered tests skip in the general suite and execute explicitly in the76-case browser command. Historical tests are not silently removed or rewritten.

Exact commands, exit codes, source hashes and raw logs are in [verification-logs](verification-logs/). Backend commands and boundaries: [backend verification](backend-verification.md). Root executed browser/full/build commands because the independent agent's earlier escalation path was unavailable; reviewer independently inspected outputs and source. Round1 outputs precede the final access fix and are retained separately. Three observed frontend defects were reproduced and closed in [independent review](independent-review.md).

The isolated directory is /private/var/folders/79/mmyd13f10px_4f6vb__s9b_w0000gn/T/frc06-build-final-0oobx55m. Working user Next3000 and PostgreSQL5432 were not used. Owned Next3111, Go8092 and disposable PostgreSQL55434 supply real integration. No deployment or production evidence is inferred from local success. Raw logs preserve runner warnings/whitespace; successful build is not claimed warning-free.
