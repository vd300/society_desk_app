export function StatCard({ label, value }: { label: string; value: string | number | null }) {
  return (
    <div className="rounded-lg bg-white p-5 shadow-sm ring-1 ring-ink/10">
      <p className="text-sm text-slate-600">{label}</p>
      <p className="mt-2 text-3xl font-semibold text-ink">{value ?? "-"}</p>
    </div>
  );
}
