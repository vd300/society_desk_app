"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { Building2, LogOut } from "lucide-react";
import { clearSession, getUser } from "@/lib/auth";

const nav = {
  ADMIN: [
    ["Dashboard", "/admin/dashboard"],
    ["Flats", "/admin/flats"],
    ["Residents", "/admin/residents"],
    ["Dues", "/admin/dues"],
    ["Complaints", "/admin/complaints"],
    ["Notices", "/admin/notices"],
    ["Visitors", "/admin/visitors"],
  ],
  RESIDENT: [
    ["Dashboard", "/resident/dashboard"],
    ["Dues", "/resident/dues"],
    ["Complaints", "/resident/complaints"],
    ["Notices", "/resident/notices"],
    ["Visitors", "/resident/visitors"],
  ],
  SECURITY: [
    ["Dashboard", "/security/dashboard"],
    ["Visitors", "/security/visitors"],
  ],
};

export function DashboardShell({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  const router = useRouter();
  const user = getUser();
  const links = user ? nav[user.role] : [];

  return (
    <main className="min-h-screen bg-[#f7f5f0]">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-ink/10 bg-white px-4 py-5 lg:block">
        <div className="flex items-center gap-3 px-2">
          <span className="flex size-10 items-center justify-center rounded-md bg-brand text-white">
            <Building2 size={22} />
          </span>
          <div>
            <p className="font-semibold text-ink">SocietyDesk</p>
            <p className="text-xs text-slate-500">{user?.role ?? "Workspace"}</p>
          </div>
        </div>
        <nav className="mt-8 space-y-1">
          {links.map(([label, href]) => (
            <Link
              className="block rounded-md px-3 py-2 text-sm font-medium text-slate-700 hover:bg-teal-50 hover:text-brand"
              href={href}
              key={href}
            >
              {label}
            </Link>
          ))}
        </nav>
      </aside>
      <section className="lg:pl-64">
        <header className="flex items-center justify-between border-b border-ink/10 bg-white px-5 py-4">
          <h1 className="text-xl font-semibold text-ink">{title}</h1>
          <button
            className="inline-flex size-10 items-center justify-center rounded-md text-slate-600 hover:bg-slate-100"
            onClick={() => {
              clearSession();
              router.push("/login");
            }}
            title="Sign out"
            type="button"
          >
            <LogOut size={19} />
          </button>
        </header>
        <div className="mx-auto max-w-7xl px-5 py-6">{children}</div>
      </section>
    </main>
  );
}
