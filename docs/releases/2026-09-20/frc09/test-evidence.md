# FRC09 root verification —2026-09-20

Detailed backend/agent frontend evidence in backend-evidence.md and frontend-evidence.md. Synthetic fixtures only; no actual customer documents or external source downloads.

Root fresh Node suite23/23PASS: `rtk proxy node --import tsx --test src/modules/drone-defense/domain/asset-library-form.release.test.ts src/modules/drone-defense/infra/catalog-provenance.release.test.ts src/modules/drone-defense/infra/asset-documents-api.test.ts src/shared/lib/catalog-refresh.release.test.ts`. RED/GREEN permanent regressions cover preview invalidation by selection, accumulation, legacyseedquality, root-vs-price provenance, unknownclearing, actualbinary/session andcatalogroundtrip.

Independent Chromium panel7/7 andmanager5/5PASS (actualcomponents/store/form/API; mockedHTTPonly). Manager found selectedsource lost withunknownquality, reproducedRED thenfixedtoestimated. ExistingAPI unit9/9 is partofroot23count, not additional unique total. Optional suites require FRC09_BROWSER_TESTS=true; commands inagent evidence/testsource.

Root actual `rtk proxy node test/playwright/frc09-live.cjs` PASS: browserfileinput→NextBFF→Go→PG andrealprivatefiles; invalidPDFcontent415, TXT201, byte-exactdownload/checksum6148487623bcd9b29e80c459d9a2a2b4fc3e60eca157c304c8ef2c880d8475f4, sourcepickerestimated, sourceID/revision/checksum roundtrip, explicitpreviewapplydirty, tenantA404, delete404. Pageerrors[]. Screenshot /private/tmp/fortis-frc09-browser/source-preview.png. BrowserServer uses test-only cleanscanner; NOT production scanningevidence. Actor/sessionauthoritative, syntheticB/Aaccounts. UIicons require observedaccessible names; earlyselectorharnessfailures were corrected and finalwholeflowpassed.

Root freshGo -race withFRC09_TEST_DSN+FRC02_TEST_DSN ondisposablePG16: `go test -race -tags=unit ./internal/modules/defense_asset/... ./cmd/app -run 'Test(FRC09|FRC02Postgres|DefenseAsset|Catalog|PrivateDocumentStorage|Scanner|Document|NewDefenseAsset)' -count=1 -timeout=120s` all5packagesPASS. Independentcombined02/04/05/09PG27top+24nestedPASS;09race55top+16nestedPASS. Category/specupdate corruption reproduced thenstagedaggregatevalidation+inmemory/PGtestsGREEN. Quarantine/rollback/revocationduring scan, signature/size, unknownscanner, privatefilesystem, samefilename/newidentity tested.

OpenAPI09generatedfromannotationsandscopedtransitively9paths validatedbyroot Swagger0.36.6. ExistingwholeAPI auth/enterprise/otherresponseannotations remain owningFRC13. No productionmigration/scanner/TLS/realretention evidence claimed. Runtimegates documentedADR0021/backend evidence.

## Final root closeout

FreshcombinedChromium23/23PASS (calculator10/documentpanel7/manager6), changedlint0 and Next productionbuild `.next/frc09-build` exit0 compile10.1s/types5.4s. This supersedes intermediatefulltsc failures causedby unfinished06tests waitingforstorefields. Finalactual09live PASS project48ac3503-bd20-40f7-8e1d-a44144d8ae2e, document42b37443-2e44-4bc6-863e-09736671e9ba; sourcechecksum above. Companion05live PASS47500000minor,groups25000000/22500000. ActualUI statusbanner movedabovecolumns aftervisualinspection; final09screenshot updated.

OwnedtestBE8092 exitedPASS andcleaneditscurrent schema; Next3111 stopped, PG55434 stopped. Olderfixtureprocesses exceeded go test default10mtimeout, leavingonlysynthetic schemas inretained disposablecluster; finalrun used35m timeout andendedcleanly. No productioncleanup. Own auto-generatedtsconfig paths/formatting were removedafterverifyingtheywere theonlydifferences. Userdev3000 untouched. No finalall-release-suite claim: unfinished06 hasexplicitREDtests and03/07/08/10/13/14remainunaccepted.
