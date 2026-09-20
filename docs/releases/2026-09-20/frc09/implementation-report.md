# FRC-09 — CODE PASS / RUNTIME BLOCKED

Root code acceptance:2026-09-20. DATA01–10 locallyverified; production delivery not accepted. Closest task completed at the user's request to stop afterwards.

## Result

Provenance and native typed cards round-trip without lossy category/role mapping. Oldunknown sources remainunknown; knownseedlineage remainsdemo. Source labels/dates/quality and immutable documentidentity surviveAPI/storage/snapshot; server suppliesauthor/time/revision. Catalog changes use explicitpreview/apply and preserve historicalrevisions/instanceprices. Multiplependingedits accumulate; selectiondoesnotdiscardpreview; businesschanges/identity invalidate staleupdates. Unchangedsourceeditor preserves distinctcard/price provenance. Invalid importedprice remains editable and cannot silently becomezero/unknown onrename.

Documents upload actual multipartbytes into private storage and quarantine before scanner. PDF/PNG/JPEG/TXT,10MiB,signature/MIME/filename validation, serverUUIDkeys, immutableID/revision/checksum. Scannerunavailable/rejected staysclosed. Everydownload checks persistedparentaccess andintegrity; no publicURL/sourcefetch. Delete deactivateswithtransactionalaudit. Newfilenamecopycannotreplacehistoricalsources. Frontend providesupload/status/download/sourcepicker/delete withsessiongeneration guards andsafetext rendering.

Independentreview reproduced andfixed category-update corruption, previewlostduringselection/secondedit, legacyseedquality loss, distinctsource overwrite, unknownsourcepicker loss andmalformedprice/source rendering. Tests retain RED→GREEN evidence. Final typedbuild/lint/scopedOpenAPI andactualbrowser/PGflowpassed. Scope doesnotimplement later officialreport hideCostprojection (FRC10).

## Acceptance

DATA01/02/03: form/API/seedtests+actualmanagerbrowser. DATA04: frozen04snapshot+explicitrefreshstoretests. DATA05/06/07: signature/size/quarantine/service/PG/revocation/race and actualforeign404. DATA08: actualUI renders HTMLastext. DATA09: immutableID/checksum samefilenamePGchecks and browserbytes. DATA10:13nativecategory matrix, fullcardform preservation, instanceoverride preview and04losslesssnapshot.

Root freshChromium23/23 comprisescalculator10,documentpanel7,manager6. Nodefocused23/23 earlierpassed. Actualbrowser→BFF→Go→PG/privatefiles passedafterfinalintegration; checksums/metadata roundtrip,415,foreign404,deleted404,pageErrors[]. Backendrace55top+16nested, combined02/04/05/09PG27top+24nested; root independentlyranfivepackage race suite. Changedlint0, productionbuild10.1scompile+5.4stypes, Swagger2.0 scoped9pathsvalid. Detailed commands: test-evidence.md, backend-evidence.md, frontend-evidence.md, review-followup-evidence.md.

## Remaining delivery gates

APP_DOCUMENTS_ENABLED remains false by default. FRC14 must provide private persistentvolume, realClamAV scanner+clean/infected/unavailable tests, TLS, backup/retention/cleanup andownerrevocation ofexistingexternalURLs. Fakeclean scanner used inlocalbrowser is explicitly not antivirus evidence. Productionmigrations not applied.

ADR: knowledge-base/03_Architecture/ADR-0021-catalog-provenance-private-documents.md. No localcommit: sharedfiles include04/05 andunfinished06 hunks, identifiedinmanifest; thisaccepts09behavior, notentireworkspaceorrelease. No push/deploy; parentgitlinks unchanged. Userrequestedstop afterthisacceptance; resume06onlyonrequest.
