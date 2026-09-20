/** Proposed cross-team DTO vocabulary. Not an implementation or proof of API support. */
export type JsonValue = null | boolean | number | string | JsonValue[] | { [key: string]: JsonValue };
export type RuntimeMode = "demo" | "workspace";
export type DataQuality = "confirmed" | "estimated" | "demo";
export type Money = { currency: "RUB"; minor: string };
export type ProjectRef = { projectId: string; projectVersion: number };
export type CalculationIdentity = ProjectRef & {
  calculationVersion: string;
  inputDataVersions: Record<string, string>;
  snapshotDigest: string;
};
export type DataProvenance = {
  sourceLabel: string;
  sourceDocumentId: string | null;
  sourceUrl: string | null;
  sourceDate: string | null;
  recordedAt: string;
  recordedBy: string;
  quality: DataQuality;
  revision: string;
};
export type Issue = {
  code: string;
  severity: "info" | "warning" | "error";
  objectIds: string[];
  message: string;
};
export type FinancialLine = {
  objectId: string;
  assetId: string;
  layerId: string;
  category: string;
  name: string;
  quantity: number;
  unitPriceMinor: string | null;
  lineTotalMinor: string | null;
  priceSource: "instance_override" | "components" | "template" | "unknown";
  provenance: DataProvenance | null;
};
export type CostGroup = {
  id: string;
  name: string;
  objectCount: number;
  unitCount: number;
  knownSubtotalMinor: string;
  totalMinor: string | null;
};
export type CostProjection = {
  identity: CalculationIdentity;
  currency: "RUB";
  lines: FinancialLine[];
  byLayer: CostGroup[];
  byType: CostGroup[];
  knownSubtotalMinor: string;
  totalMinor: string | null;
  isComplete: boolean;
  unknownPriceObjectIds: string[];
  warnings: Issue[];
};
export type BudgetConfig =
  | { budgetMode: "unlimited"; budgetLimitMinor: null }
  | { budgetMode: "limited"; budgetLimitMinor: string };
export type BudgetProjection = {
  identity: CalculationIdentity;
  config: BudgetConfig;
  spentMinor: string | null;
  remainingMinor: string | null;
  status: "within_limit" | "exceeded" | "unlimited" | "indeterminate";
};
export type BudgetUpdateRequest = BudgetConfig & { version: number };
export type BudgetCheckRequest = { version: number; projectJson: string };
export type BudgetCheckResponse = {
  basedOn: ProjectRef;
  status: "allowed" | "blocked";
  reasonCode: "within_budget" | "unlimited" | "budget_exceeded" | "price_unknown";
  projectedSpentMinor: string | null;
  projectedRemainingMinor: string | null;
};
export type SaveStatus = "loading" | "saved" | "dirty" | "saving" | "offline_draft" | "conflict" | "error";
export type SaveRequest = { name: string; enterpriseId: string; projectJson: string; version: number };
export type CompareResult = {
  enterpriseId: string;
  a: { identity: CalculationIdentity; cost: CostProjection; budget: BudgetProjection };
  b: { identity: CalculationIdentity; cost: CostProjection; budget: BudgetProjection };
  differenceMinor: string | null; // B - A; may be negative.
  differencePercent: string | null; // null when A = 0 or totals incomplete.
  warnings: Issue[];
};
export type ReportCommon = {
  reportId: string;
  identity: CalculationIdentity;
  generatedAt: string;
  title: string;
  enterprise: { id: string; name: string };
  warnings: Issue[];
  sources: DataProvenance[];
  mapSnapshotData: JsonValue; // Existing saved GIS data; no geometry calculations added here.
  mapVisibility: { layerIds: string[]; objectIds: string[]; showCoverage: boolean };
  limitations: string[];
};
export type PricedReport = ReportCommon & { hideCost: false; cost: CostProjection; budget: BudgetProjection };
export type UnpricedReport = ReportCommon & {
  hideCost: true;
  objects: Array<{ objectId: string; assetId: string; layerId: string; category: string; name: string; quantity: number; description: string }>;
};
export type ReportPayload = PricedReport | UnpricedReport;
export type ApiError = {
  error: {
    code: string;
    message: string;
    requestId: string;
    retryable: boolean;
    details?: Record<string, JsonValue>;
  };
};
export type EnterpriseRole = "admin" | "editor" | "viewer";
export type EnterprisePermission = { enterpriseId: string; role: EnterpriseRole; viewCost: boolean };
export type DemoRequestInput = {
  name: string;
  organization: string;
  email: string;
  comment: string;
  consent: true;
  consentVersion: string;
};
export type DemoRequestAccepted = { requestId: string; status: "received" };

export type AuditEvent = {
  eventId: string;
  actorId: string;
  enterpriseId: string | null;
  entityType: "session" | "membership" | "project" | "budget" | "asset_document";
  entityId: string;
  action: string;
  previousVersion: number | null;
  newVersion: number | null;
  occurredAt: string;
  requestId: string;
};
