-- Diagnostic only. No ownership assignment, cleanup, schema change or migration.
BEGIN TRANSACTION READ ONLY;

SELECT p.id AS project_id, p.enterprise_id,
       CASE WHEN p.enterprise_id IS NULL THEN 'null_enterprise' ELSE 'missing_enterprise' END AS reason
FROM defense_projects p
LEFT JOIN enterprises e ON e.id = p.enterprise_id
WHERE p.enterprise_id IS NULL OR e.id IS NULL
ORDER BY p.id;

SELECT a.id AS asset_id, a.enterprise_id,
       CASE WHEN a.enterprise_id IS NULL THEN 'null_enterprise' ELSE 'missing_enterprise' END AS reason
FROM defense_assets a
LEFT JOIN enterprises e ON e.id = a.enterprise_id
WHERE a.is_public = FALSE AND (a.enterprise_id IS NULL OR e.id IS NULL)
ORDER BY a.id;

SELECT d.id AS document_id, d.asset_id,
       CASE WHEN a.id IS NULL THEN 'missing_asset'
            WHEN a.enterprise_id IS NULL THEN 'private_parent_null_enterprise'
            ELSE 'private_parent_missing_enterprise' END AS reason
FROM defense_asset_documents d
LEFT JOIN defense_assets a ON a.id = d.asset_id
LEFT JOIN enterprises e ON e.id = a.enterprise_id
WHERE a.id IS NULL OR (a.is_public = FALSE AND (a.enterprise_id IS NULL OR e.id IS NULL))
ORDER BY d.id;

-- Public rows with NULL enterprise are valid and are intentionally not findings.
ROLLBACK;
