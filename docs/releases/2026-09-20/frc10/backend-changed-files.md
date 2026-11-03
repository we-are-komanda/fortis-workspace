# FRC-10 backend changed files

Base: backend `4ff76c3` (accepted FRC-08). No commit or push created by this subagent.

| File | SHA-256 |
|---|---|
| `backend/cmd/app/dependencies.go` | `693e96a86fa5244a783ee315b013b6c81ffcd6a14bc464605c9e342587f70680` |
| `backend/cmd/app/frc02_access_test.go` | `f6140f5f07c8c393d87b18e0a397034291dc3261e3bfa1f3a413a4bbf4164c9f` |
| `backend/cmd/app/frc02_postgres_test.go` | `56d6d400e2426e46f0028e70bc42da9e4e3f3722decb3ea5e3a36a87639c59a9` |
| `backend/cmd/app/frc04_postgres_test.go` | `b0771394f37d86e966c51bf57b9e38342a7467fb0a476d80822f959f7b61df68` |
| `backend/cmd/app/frc10_postgres_test.go` | `d6c7024764f612d1dea391eb3815106a620f0e4651d3af1074e427fdc7855590` |
| `backend/internal/modules/budget/application/project_cost.go` | `f23cecc3b7ff8fb1cf260fcc010d176e824c19859b305a76af096ed08f7e3b49` |
| `backend/internal/modules/budget/ui/mapper.go` | `953a6855e27d16dd640172754a7cff49b845887078f8cf95f98944e42e3099b4` |
| `backend/internal/modules/report/application/commands.go` | `b4a24903b616a90e5e3f7092206a7ccb131a882fa364b86c238b674dd86fe73a` |
| `backend/internal/modules/report/application/report_service.go` | `1b2e22fb472755c9dfbbe6af85c477a5a1bfb135ea473581a46d6687680c7e80` |
| `backend/internal/modules/report/application/report_service_test.go` | `4d5a9abb4896fb774e3a6aba748710f86f873b125025848f2dbc2994a5f4859f` |
| `backend/internal/modules/report/domain/errors.go` | `014f71537bc25db32583d2aeb6ebf13ca7c80d5e2add0ca0688502dd760b4521` |
| `backend/internal/modules/report/domain/report.go` | `87ee765288e001efe99e3754c8128917f76c0b31798c04f0e317f1542e79f311` |
| `backend/internal/modules/report/domain/report_repository_interface.go` | `3fd6f5aa14b79d3b89271dff4b19e20431e432a1f414dee1753c753602aa35f9` |
| `backend/internal/modules/report/domain/vo.go` | `61c70c74f382ace17b49357363cf50df8f6f2ab38ef504c2fc00dfc0a3dfc064` |
| `backend/internal/modules/report/infrastructure/models.go` | `925a91814c2a7922af8f122fc58c34d9e0d15c842f2699d3c66e0780ad72fdf0` |
| `backend/internal/modules/report/infrastructure/report_repository.go` | `adfc289f6e860113d34d41d76fc0ff4f1993d61ae127d9d8a9d4db3bbef021e4` |
| `backend/internal/modules/report/ui/controller.go` | `91b1e68cada04e7b2a45d987e49d5f823935ae065b5d0a529de62fc7c3bcdb5c` |
| `backend/internal/modules/report/ui/controller_test.go` | `25c328cccbd382b4459dd006fe2d525fad542b42ed27f387b3b4b378a4acf8d1` |
| `backend/internal/modules/report/ui/dto.go` | `e46332ecec9d96d45126711b27760943103555f818b0f22557b984fafecc3405` |
| `backend/internal/modules/report/ui/mapper.go` | `8c0544e10a1d077610190da8305f26991e3783bf04b301168b4c3021a57dd91e` |
| `backend/internal/modules/report/ui/mapper_test.go` | `bbbc508a32099aff6ebaa5751ac0be016b9872296cb7a1e60714dbd6511594f0` |
| `backend/migrations/1789950000_issued_reports.down.sql` | `6817e528bde4bfa572b7e24768549845a31cbb4a15046675f67bd0dc0fce9041` |
| `backend/migrations/1789950000_issued_reports.up.sql` | `fef701702ffe105eb98111a244e8816c21d9c8ac737c74b6a10c496b9e090aa9` |

Responsibilities: report domain/application/repository/DTO/controller replacement; one immutable report migration; shared frozen-cost/financial-DTO reuse; DI; existing FRC02/04 fixture compatibility; unit and opt-in PostgreSQL regression cases.

Existing FRC02 in-memory access tests have no immutable revision repository. Their own-report success case is exercised by the real PostgreSQL suite; foreign/revoked access stays in the in-memory matrix. Its request helper now explicitly adds the pinned version/hideCost fields required by the new contract. Legacy migration fixtures omit the issued-report migration until project revisions exist.

Parent evidence owned here: `backend-api.md`, `backend-implementation.md`, `backend-verification.md`, this manifest, and `backend-verification-logs/`. Frontend, KB, parent shared contracts and acceptance decisions remain parent/other-agent ownership.
