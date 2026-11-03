import assert from "node:assert/strict";
import { createWorkspaceDefenseProject } from "../../../../../frontend/src/shared/lib/defense-project";
import { useDefenseProjectStore as projects } from "../../../../../frontend/src/shared/lib/use-defense-project-store";
import { useDefenseVariantsStore as variants } from "../../../../../frontend/src/modules/drone-defense/domain/use-defense-variants-store";
import { setAuthenticatedIdentity } from "../../../../../frontend/src/shared/lib/session-state";
import "../../../../../frontend/src/shared/lib/identity";

async function main() {
  const original = globalThis.fetch;
  try {
    for (const [name, malformed] of Object.entries({
      "empty ID": { projectId: "", enterpriseId: "E2", version: 1 },
      "missing version": { projectId: "New", enterpriseId: "E2" },
      "zero version": { projectId: "New", enterpriseId: "E2", version: 0 },
      "fractional version": { projectId: "New", enterpriseId: "E2", version: 1.5 },
      "wrong enterprise": { projectId: "New", enterpriseId: "Foreign", version: 1 },
    })) {
      setAuthenticatedIdentity(null); setAuthenticatedIdentity("synthetic-reviewer");
      const saved = { ...createWorkspaceDefenseProject(), projectId: "Existing", enterpriseId: "E1", version: 7, source: "backend" as const };
      projects.getState().acceptServerProject(saved);
      variants.setState({ ...variants.getInitialState(), activeVariantId: "Existing" }, true);
      const proposal = { ...createWorkspaceDefenseProject(), enterpriseId: "E2", projectName: "Proposed" };
      let writes = 0; let body: string | undefined; let key: string | null = null;
      globalThis.fetch = async (_input, init) => {
        assert.equal(init?.method, "POST"); writes++;
        body = init?.body as string; key = new Headers(init?.headers).get("Idempotency-Key");
        return Response.json({ name: "Proposed", ...malformed });
      };
      const result = await variants.getState().saveAsNewVariant("Proposed", proposal);
      assert.equal(result, null, name); assert.equal(writes, 1, name);
      assert.equal(projects.getState().project, saved, name);
      assert.equal(projects.getState().savedProject, saved, name);
      assert.equal(projects.getState().syncStatus, "saved", name);
      assert.equal(variants.getState().activeVariantId, "Existing", name);
      assert.equal(variants.getState().saveStatus, "error", name);
      assert.ok(key, name); assert.equal(variants.getState().workspaceCreateAttempt?.idempotencyKey, key, name);
      assert.equal(variants.getState().workspaceCreateAttempt?.body, body, name);
      console.log(JSON.stringify({ case: name, result: "PASS", writes, priorContextPreserved: true, frozenAttemptRetained: true }));
    }
  } finally { globalThis.fetch = original; }
}
void main();
