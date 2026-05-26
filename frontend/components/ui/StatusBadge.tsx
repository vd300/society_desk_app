const tones: Record<string, string> = {
  PAID: "bg-emerald-50 text-emerald-700 ring-emerald-200",
  APPROVED: "bg-emerald-50 text-emerald-700 ring-emerald-200",
  RESOLVED: "bg-emerald-50 text-emerald-700 ring-emerald-200",
  CHECKED_IN: "bg-teal-50 text-teal-700 ring-teal-200",
  IN_PROGRESS: "bg-sky-50 text-sky-700 ring-sky-200",
  PAYMENT_SUBMITTED: "bg-amber-50 text-amber-700 ring-amber-200",
  OPEN: "bg-amber-50 text-amber-700 ring-amber-200",
  EXPECTED: "bg-amber-50 text-amber-700 ring-amber-200",
  REJECTED: "bg-rose-50 text-rose-700 ring-rose-200",
  UNPAID: "bg-rose-50 text-rose-700 ring-rose-200",
  CHECKED_OUT: "bg-slate-100 text-slate-700 ring-slate-200",
};

export function StatusBadge({ value }: { value?: string | null }) {
  if (!value) {
    return null;
  }
  return (
    <span
      className={`inline-flex rounded px-2 py-1 text-xs font-semibold ring-1 ${
        tones[value] || "bg-slate-100 text-slate-700 ring-slate-200"
      }`}
    >
      {value.replaceAll("_", " ")}
    </span>
  );
}
