"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import { apiRequest, patchJson, postJson } from "@/lib/api";
import { DashboardShell } from "@/components/layout/DashboardShell";
import { StatCard } from "@/components/ui/StatCard";
import { StatusBadge } from "@/components/ui/StatusBadge";

type RecordItem = Record<string, unknown>;
type SelectOption = string | { value: string; label: string };

function useApi<T>(path: string) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    setError("");
    try {
      setData(await apiRequest<T>(path));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Request failed");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, [path]);

  return { data, error, loading, reload: load };
}

function Field({
  name,
  label,
  type = "text",
  value,
  onChange,
}: {
  name: string;
  label: string;
  type?: string;
  value: string;
  onChange: (name: string, value: string) => void;
}) {
  return (
    <label className="block">
      <span className="text-xs font-semibold uppercase text-slate-500">{label}</span>
      <input
        className="mt-1 h-10 w-full rounded-md border border-slate-300 bg-white px-3 text-sm text-ink outline-none focus:border-brand focus:ring-2 focus:ring-brand/20"
        name={name}
        onChange={(event) => onChange(name, event.target.value)}
        type={type}
        value={value}
      />
    </label>
  );
}

function SelectField({
  name,
  label,
  value,
  options,
  onChange,
}: {
  name: string;
  label: string;
  value: string;
  options: SelectOption[];
  onChange: (name: string, value: string) => void;
}) {
  return (
    <label className="block">
      <span className="text-xs font-semibold uppercase text-slate-500">{label}</span>
      <select
        className="mt-1 h-10 w-full rounded-md border border-slate-300 bg-white px-3 text-sm text-ink outline-none focus:border-brand focus:ring-2 focus:ring-brand/20"
        name={name}
        onChange={(event) => onChange(name, event.target.value)}
        value={value}
      >
        {options.map((option) => {
          const value = typeof option === "string" ? option : option.value;
          const label = typeof option === "string" ? option || "Select" : option.label;
          return (
          <option key={value} value={value}>
            {label}
          </option>
          );
        })}
      </select>
    </label>
  );
}

function optionsFrom(items: RecordItem[] | null, labelKey: string): SelectOption[] {
  return [
    { value: "", label: "Select" },
    ...(items ?? []).map((item) => ({
      value: String(item.id),
      label: String(item[labelKey] ?? item.id),
    })),
  ];
}

function findLabel(items: RecordItem[] | null, id: unknown, labelKey: string) {
  const item = (items ?? []).find((entry) => entry.id === id);
  return item ? String(item[labelKey] ?? id) : String(id ?? "-");
}

function JsonList({ items }: { items: RecordItem[] }) {
  if (!items.length) {
    return <p className="rounded-lg bg-white p-5 text-sm text-slate-600 ring-1 ring-ink/10">No records yet.</p>;
  }
  return (
    <div className="overflow-hidden rounded-lg bg-white ring-1 ring-ink/10">
      <div className="divide-y divide-slate-100">
        {items.map((item) => (
          <div className="grid gap-3 p-4 text-sm md:grid-cols-4" key={String(item.id ?? JSON.stringify(item))}>
            {Object.entries(item)
              .filter(([key]) => ["id", "created_at", "updated_at"].includes(key) === false && !key.endsWith("_id"))
              .slice(0, 8)
              .map(([key, value]) => (
                <div key={key}>
                  <p className="text-xs font-semibold uppercase text-slate-500">{key.replaceAll("_", " ")}</p>
                  <div className="mt-1 break-words text-ink">
                    {key === "status" ? <StatusBadge value={String(value)} /> : String(value ?? "-")}
                  </div>
                </div>
              ))}
          </div>
        ))}
      </div>
    </div>
  );
}

function Notice({ message }: { message: string }) {
  return message ? <p className="mb-4 rounded-md bg-rose-50 px-4 py-3 text-sm font-medium text-rose-700">{message}</p> : null;
}

function FormPanel({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section className="rounded-lg bg-white p-5 shadow-sm ring-1 ring-ink/10">
      <h2 className="text-base font-semibold text-ink">{title}</h2>
      <div className="mt-4">{children}</div>
    </section>
  );
}

export function AdminDashboardPage() {
  const { data, error } = useApi<Record<string, number>>("/admin/dashboard");
  return (
    <DashboardShell title="Admin Dashboard">
      <Notice message={error} />
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {Object.entries(data ?? {}).map(([key, value]) => (
          <StatCard key={key} label={key.replaceAll("_", " ")} value={value} />
        ))}
      </div>
    </DashboardShell>
  );
}

export function AdminFlatsPage() {
  const societies = useApi<RecordItem[]>("/admin/societies");
  const buildings = useApi<RecordItem[]>("/admin/buildings");
  const flats = useApi<RecordItem[]>("/admin/flats");
  const [society, setSociety] = useState({ name: "", address: "" });
  const [building, setBuilding] = useState({ society_id: "", name: "" });
  const [flat, setFlat] = useState({
    society_id: "",
    building_id: "",
    flat_number: "",
    floor_number: "1",
    maintenance_amount: "3000",
  });
  const societyOptions = useMemo(() => optionsFrom(societies.data, "name"), [societies.data]);
  const buildingOptions = useMemo(() => optionsFrom(buildings.data, "name"), [buildings.data]);
  const displayFlats = useMemo(
    () =>
      (flats.data ?? []).map((item) => ({
        society: findLabel(societies.data, item.society_id, "name"),
        building: findLabel(buildings.data, item.building_id, "name"),
        flat: item.flat_number,
        floor: item.floor_number,
        maintenance: item.maintenance_amount,
      })),
    [buildings.data, flats.data, societies.data],
  );

  async function submitSociety(event: FormEvent) {
    event.preventDefault();
    await postJson("/admin/societies", society);
    setSociety({ name: "", address: "" });
    societies.reload();
  }

  async function submitBuilding(event: FormEvent) {
    event.preventDefault();
    await postJson("/admin/buildings", building);
    setBuilding({ society_id: "", name: "" });
    buildings.reload();
  }

  async function submitFlat(event: FormEvent) {
    event.preventDefault();
    await postJson("/admin/flats", { ...flat, floor_number: Number(flat.floor_number) });
    setFlat({ society_id: "", building_id: "", flat_number: "", floor_number: "1", maintenance_amount: "3000" });
    flats.reload();
  }

  return (
    <DashboardShell title="Society Setup">
      <Notice message={societies.error || buildings.error || flats.error} />
      <div className="grid gap-4 xl:grid-cols-3">
        <FormPanel title="Society">
          <form className="space-y-3" onSubmit={submitSociety}>
            <Field label="Name" name="name" onChange={(k, v) => setSociety((s) => ({ ...s, [k]: v }))} value={society.name} />
            <Field label="Address" name="address" onChange={(k, v) => setSociety((s) => ({ ...s, [k]: v }))} value={society.address} />
            <button className="h-10 rounded-md bg-brand px-4 text-sm font-semibold text-white">Create</button>
          </form>
        </FormPanel>
        <FormPanel title="Building">
          <form className="space-y-3" onSubmit={submitBuilding}>
            <SelectField label="Society" name="society_id" onChange={(k, v) => setBuilding((s) => ({ ...s, [k]: v }))} options={societyOptions} value={building.society_id} />
            <Field label="Name" name="name" onChange={(k, v) => setBuilding((s) => ({ ...s, [k]: v }))} value={building.name} />
            <button className="h-10 rounded-md bg-brand px-4 text-sm font-semibold text-white">Create</button>
          </form>
        </FormPanel>
        <FormPanel title="Flat">
          <form className="space-y-3" onSubmit={submitFlat}>
            <SelectField label="Society" name="society_id" onChange={(k, v) => setFlat((s) => ({ ...s, [k]: v }))} options={societyOptions} value={flat.society_id} />
            <SelectField label="Building" name="building_id" onChange={(k, v) => setFlat((s) => ({ ...s, [k]: v }))} options={buildingOptions} value={flat.building_id} />
            <Field label="Flat" name="flat_number" onChange={(k, v) => setFlat((s) => ({ ...s, [k]: v }))} value={flat.flat_number} />
            <Field label="Floor" name="floor_number" type="number" onChange={(k, v) => setFlat((s) => ({ ...s, [k]: v }))} value={flat.floor_number} />
            <Field label="Maintenance" name="maintenance_amount" type="number" onChange={(k, v) => setFlat((s) => ({ ...s, [k]: v }))} value={flat.maintenance_amount} />
            <button className="h-10 rounded-md bg-brand px-4 text-sm font-semibold text-white">Create</button>
          </form>
        </FormPanel>
      </div>
      <section className="mt-6">
        <JsonList items={displayFlats} />
      </section>
    </DashboardShell>
  );
}

export function AdminResidentsPage() {
  const residents = useApi<RecordItem[]>("/admin/residents");
  const flats = useApi<RecordItem[]>("/admin/flats");
  const societies = useApi<RecordItem[]>("/admin/societies");
  const users = useApi<RecordItem[]>("/admin/users");
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "password123",
    society_id: "",
    flat_id: "",
    phone: "",
  });

  async function submit(event: FormEvent) {
    event.preventDefault();
    const user = await postJson<RecordItem>("/auth/register", { name: form.name, email: form.email, password: form.password, role: "RESIDENT" }, false);
    await postJson("/admin/residents", { user_id: user.id, society_id: form.society_id, flat_id: form.flat_id, phone: form.phone, is_owner: true });
    residents.reload();
    users.reload();
  }

  const displayResidents = useMemo(
    () =>
      (residents.data ?? []).map((item) => {
        const user = (users.data ?? []).find((entry) => entry.id === item.user_id);
        return {
          name: user?.name ?? "-",
          email: user?.email ?? "-",
          society: findLabel(societies.data, item.society_id, "name"),
          flat: findLabel(flats.data, item.flat_id, "flat_number"),
          phone: item.phone,
          owner: item.is_owner ? "Yes" : "No",
        };
      }),
    [flats.data, residents.data, societies.data, users.data],
  );

  return (
    <DashboardShell title="Residents">
      <Notice message={residents.error || users.error} />
      <FormPanel title="Add resident">
        <form className="grid gap-3 md:grid-cols-3" onSubmit={submit}>
          {["name", "email", "password", "phone"].map((key) => (
            <Field key={key} label={key} name={key} onChange={(k, v) => setForm((s) => ({ ...s, [k]: v }))} value={String(form[key as keyof typeof form])} />
          ))}
          <SelectField label="Society" name="society_id" onChange={(k, v) => setForm((s) => ({ ...s, [k]: v }))} options={optionsFrom(societies.data, "name")} value={form.society_id} />
          <SelectField label="Flat" name="flat_id" onChange={(k, v) => setForm((s) => ({ ...s, [k]: v }))} options={optionsFrom(flats.data, "flat_number")} value={form.flat_id} />
          <button className="h-10 self-end rounded-md bg-brand px-4 text-sm font-semibold text-white">Create</button>
        </form>
      </FormPanel>
      <section className="mt-6">
        <JsonList items={displayResidents} />
      </section>
    </DashboardShell>
  );
}

export function AdminDuesPage() {
  const dues = useApi<RecordItem[]>("/dues");
  const societies = useApi<RecordItem[]>("/admin/societies");
  const flats = useApi<RecordItem[]>("/admin/flats");
  const today = new Date();
  const [form, setForm] = useState({
    society_id: "",
    month: String(today.getMonth() + 1),
    year: String(today.getFullYear()),
    due_date: today.toISOString().slice(0, 10),
  });
  const displayDues = useMemo(
    () =>
      (dues.data ?? []).map((item) => ({
        society: findLabel(societies.data, item.society_id, "name"),
        flat: findLabel(flats.data, item.flat_id, "flat_number"),
        month: item.month,
        year: item.year,
        amount: item.amount,
        status: item.status,
        due_date: item.due_date,
      })),
    [dues.data, flats.data, societies.data],
  );

  async function submit(event: FormEvent) {
    event.preventDefault();
    await postJson("/dues/generate", { ...form, month: Number(form.month), year: Number(form.year) });
    dues.reload();
  }

  return (
    <DashboardShell title="Maintenance Dues">
      <Notice message={dues.error || flats.error || societies.error} />
      <FormPanel title="Generate dues">
        <form className="grid gap-3 md:grid-cols-5" onSubmit={submit}>
          <SelectField label="Society" name="society_id" onChange={(k, v) => setForm((s) => ({ ...s, [k]: v }))} options={optionsFrom(societies.data, "name")} value={form.society_id} />
          {["month", "year", "due_date"].map((key) => (
            <Field key={key} label={key} name={key} type={key === "due_date" ? "date" : "number"} onChange={(k, v) => setForm((s) => ({ ...s, [k]: v }))} value={String(form[key as keyof typeof form])} />
          ))}
          <button className="h-10 self-end rounded-md bg-brand px-4 text-sm font-semibold text-white">Generate</button>
        </form>
      </FormPanel>
      <section className="mt-6">
        <JsonList items={displayDues} />
      </section>
    </DashboardShell>
  );
}

export function AdminComplaintsPage() {
  const complaints = useApi<RecordItem[]>("/complaints");
  async function update(id: string, status: string) {
    await patchJson(`/complaints/${id}/status`, { status, admin_note: "Updated from dashboard" });
    complaints.reload();
  }
  return (
    <DashboardShell title="Complaints">
      <Notice message={complaints.error} />
      <div className="space-y-3">
        {(complaints.data ?? []).map((item) => (
          <div className="rounded-lg bg-white p-4 ring-1 ring-ink/10" key={String(item.id)}>
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <p className="font-semibold text-ink">{String(item.title)}</p>
                <p className="text-sm text-slate-600">{String(item.category)}</p>
              </div>
              <StatusBadge value={String(item.status)} />
            </div>
            <div className="mt-3 flex gap-2">
              {["IN_PROGRESS", "RESOLVED", "REJECTED"].map((status) => (
                <button className="rounded-md bg-slate-100 px-3 py-2 text-sm font-semibold text-slate-700" key={status} onClick={() => update(String(item.id), status)}>
                  {status.replaceAll("_", " ")}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </DashboardShell>
  );
}

export function AdminNoticesPage() {
  const notices = useApi<RecordItem[]>("/notices");
  const societies = useApi<RecordItem[]>("/admin/societies");
  const [form, setForm] = useState({ society_id: "", title: "", body: "", target_type: "ALL" });
  const displayNotices = useMemo(
    () =>
      (notices.data ?? []).map((item) => ({
        society: findLabel(societies.data, item.society_id, "name"),
        title: item.title,
        body: item.body,
        target: item.target_type,
        active: item.is_active ? "Yes" : "No",
      })),
    [notices.data, societies.data],
  );
  async function submit(event: FormEvent) {
    event.preventDefault();
    await postJson("/notices", form);
    setForm({ society_id: "", title: "", body: "", target_type: "ALL" });
    notices.reload();
  }
  return (
    <DashboardShell title="Notices">
      <Notice message={notices.error} />
      <FormPanel title="Publish notice">
        <form className="grid gap-3 md:grid-cols-2" onSubmit={submit}>
          <SelectField label="Society" name="society_id" onChange={(k, v) => setForm((s) => ({ ...s, [k]: v }))} options={optionsFrom(societies.data, "name")} value={form.society_id} />
          <Field label="Title" name="title" onChange={(k, v) => setForm((s) => ({ ...s, [k]: v }))} value={form.title} />
          <Field label="Body" name="body" onChange={(k, v) => setForm((s) => ({ ...s, [k]: v }))} value={form.body} />
          <SelectField label="Target" name="target_type" onChange={(k, v) => setForm((s) => ({ ...s, [k]: v }))} options={["ALL", "BUILDING"]} value={form.target_type} />
          <button className="h-10 rounded-md bg-brand px-4 text-sm font-semibold text-white">Publish</button>
        </form>
      </FormPanel>
      <section className="mt-6">
        <JsonList items={displayNotices} />
      </section>
    </DashboardShell>
  );
}

export function AdminVisitorsPage() {
  const visitors = useApi<RecordItem[]>("/visitors/logs");
  const flats = useApi<RecordItem[]>("/admin/flats");
  const displayVisitors = useMemo(
    () =>
      (visitors.data ?? []).map((item) => ({
        visitor: item.visitor_name,
        phone: item.visitor_phone,
        flat: findLabel(flats.data, item.flat_id, "flat_number"),
        purpose: item.purpose,
        visit_date: item.visit_date,
        status: item.status,
      })),
    [flats.data, visitors.data],
  );
  return (
    <DashboardShell title="Visitor Logs">
      <Notice message={visitors.error || flats.error} />
      <JsonList items={displayVisitors} />
    </DashboardShell>
  );
}

export function ResidentDashboardPage() {
  const { data, error } = useApi<Record<string, unknown>>("/resident/dashboard");
  return (
    <DashboardShell title="Resident Dashboard">
      <Notice message={error} />
      <div className="grid gap-4 md:grid-cols-2">
        <StatCard label="Current due" value={data?.current_due ? String((data.current_due as RecordItem).status) : "None"} />
        <StatCard label="Visitors today" value={Array.isArray(data?.today_visitors) ? data.today_visitors.length : 0} />
      </div>
    </DashboardShell>
  );
}

export function ResidentDuesPage() {
  const dues = useApi<RecordItem[]>("/dues/my");
  const [proof, setProof] = useState("uploads/payments/demo.png");
  async function submit(id: string) {
    const body = new FormData();
    body.set("amount", "3000");
    body.set("proof_url", proof);
    await apiRequest(`/dues/${id}/submit-payment`, { method: "POST", body });
    dues.reload();
  }
  return (
    <DashboardShell title="My Dues">
      <Notice message={dues.error} />
      <div className="mb-4 max-w-md">
        <Field label="Proof URL" name="proof" onChange={(_, value) => setProof(value)} value={proof} />
      </div>
      <div className="space-y-3">
        {(dues.data ?? []).map((due) => (
          <div className="rounded-lg bg-white p-4 ring-1 ring-ink/10" key={String(due.id)}>
            <div className="flex flex-wrap items-center justify-between gap-3">
              <p className="font-semibold text-ink">{String(due.month)}/{String(due.year)} - Rs {String(due.amount)}</p>
              <StatusBadge value={String(due.status)} />
            </div>
            <button className="mt-3 rounded-md bg-brand px-3 py-2 text-sm font-semibold text-white" onClick={() => submit(String(due.id))}>Submit payment</button>
          </div>
        ))}
      </div>
    </DashboardShell>
  );
}

export function ResidentComplaintsPage() {
  const complaints = useApi<RecordItem[]>("/complaints/my");
  const [form, setForm] = useState({ title: "", description: "", category: "OTHER", priority: "MEDIUM" });
  async function submit(event: FormEvent) {
    event.preventDefault();
    await postJson("/complaints", form);
    setForm({ title: "", description: "", category: "OTHER", priority: "MEDIUM" });
    complaints.reload();
  }
  return (
    <DashboardShell title="My Complaints">
      <Notice message={complaints.error} />
      <FormPanel title="New complaint">
        <form className="grid gap-3 md:grid-cols-2" onSubmit={submit}>
          <Field label="Title" name="title" onChange={(k, v) => setForm((s) => ({ ...s, [k]: v }))} value={form.title} />
          <SelectField label="Category" name="category" onChange={(k, v) => setForm((s) => ({ ...s, [k]: v }))} options={["PLUMBING", "ELECTRICAL", "LIFT", "CLEANING", "PARKING", "SECURITY", "OTHER"]} value={form.category} />
          <Field label="Description" name="description" onChange={(k, v) => setForm((s) => ({ ...s, [k]: v }))} value={form.description} />
          <SelectField label="Priority" name="priority" onChange={(k, v) => setForm((s) => ({ ...s, [k]: v }))} options={["LOW", "MEDIUM", "HIGH"]} value={form.priority} />
          <button className="h-10 rounded-md bg-brand px-4 text-sm font-semibold text-white">Create</button>
        </form>
      </FormPanel>
      <section className="mt-6">
        <JsonList items={complaints.data ?? []} />
      </section>
    </DashboardShell>
  );
}

export function ResidentNoticesPage() {
  const notices = useApi<RecordItem[]>("/notices/active");
  return (
    <DashboardShell title="Notices">
      <Notice message={notices.error} />
      <JsonList items={notices.data ?? []} />
    </DashboardShell>
  );
}

export function ResidentVisitorsPage() {
  const dashboard = useApi<Record<string, unknown>>("/resident/dashboard");
  const [form, setForm] = useState({ visitor_name: "", visitor_phone: "", purpose: "", vehicle_number: "", visit_date: new Date().toISOString().slice(0, 10) });
  async function submit(event: FormEvent) {
    event.preventDefault();
    await postJson("/visitors/expected", form);
    dashboard.reload();
  }
  return (
    <DashboardShell title="My Visitors">
      <Notice message={dashboard.error} />
      <FormPanel title="Expected visitor">
        <form className="grid gap-3 md:grid-cols-3" onSubmit={submit}>
          {Object.keys(form).map((key) => (
            <Field key={key} label={key} name={key} type={key === "visit_date" ? "date" : "text"} onChange={(k, v) => setForm((s) => ({ ...s, [k]: v }))} value={String(form[key as keyof typeof form])} />
          ))}
          <button className="h-10 self-end rounded-md bg-brand px-4 text-sm font-semibold text-white">Add</button>
        </form>
      </FormPanel>
      <section className="mt-6">
        <JsonList items={(dashboard.data?.today_visitors as RecordItem[]) ?? []} />
      </section>
    </DashboardShell>
  );
}

export function SecurityDashboardPage() {
  const { data, error } = useApi<Record<string, unknown[]>>("/security/dashboard");
  return (
    <DashboardShell title="Security Dashboard">
      <Notice message={error} />
      <div className="grid gap-4 md:grid-cols-2">
        <StatCard label="Expected today" value={data?.expected_visitors_today?.length ?? 0} />
        <StatCard label="Checked in" value={data?.checked_in_visitors?.length ?? 0} />
      </div>
    </DashboardShell>
  );
}

export function SecurityVisitorsPage() {
  const visitors = useApi<RecordItem[]>("/visitors/today");
  const flats = useApi<RecordItem[]>("/visitors/flats");
  const [form, setForm] = useState({ flat_id: "", visitor_name: "", visitor_phone: "", purpose: "", vehicle_number: "" });
  async function walkIn(event: FormEvent) {
    event.preventDefault();
    await postJson("/visitors/walk-in", form);
    visitors.reload();
  }
  async function action(id: string, actionName: "check-in" | "check-out") {
    await postJson(`/visitors/${id}/${actionName}`, {});
    visitors.reload();
  }
  return (
    <DashboardShell title="Gate Visitors">
      <Notice message={visitors.error} />
      <FormPanel title="Walk-in visitor">
        <form className="grid gap-3 md:grid-cols-3" onSubmit={walkIn}>
          <SelectField label="Flat" name="flat_id" onChange={(k, v) => setForm((s) => ({ ...s, [k]: v }))} options={optionsFrom(flats.data, "flat_number")} value={form.flat_id} />
          {["visitor_name", "visitor_phone", "purpose", "vehicle_number"].map((key) => (
            <Field key={key} label={key} name={key} onChange={(k, v) => setForm((s) => ({ ...s, [k]: v }))} value={String(form[key as keyof typeof form])} />
          ))}
          <button className="h-10 self-end rounded-md bg-brand px-4 text-sm font-semibold text-white">Check in</button>
        </form>
      </FormPanel>
      <div className="mt-6 space-y-3">
        {(visitors.data ?? []).map((visitor) => (
          <div className="rounded-lg bg-white p-4 ring-1 ring-ink/10" key={String(visitor.id)}>
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <p className="font-semibold text-ink">{String(visitor.visitor_name)}</p>
                <p className="text-sm text-slate-600">
                  {findLabel(flats.data, visitor.flat_id, "flat_number")} · {String(visitor.purpose)}
                </p>
              </div>
              <StatusBadge value={String(visitor.status)} />
            </div>
            <div className="mt-3 flex gap-2">
              <button className="rounded-md bg-slate-100 px-3 py-2 text-sm font-semibold text-slate-700" onClick={() => action(String(visitor.id), "check-in")}>Check in</button>
              <button className="rounded-md bg-slate-100 px-3 py-2 text-sm font-semibold text-slate-700" onClick={() => action(String(visitor.id), "check-out")}>Check out</button>
            </div>
          </div>
        ))}
      </div>
    </DashboardShell>
  );
}
