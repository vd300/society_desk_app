import { Building2 } from "lucide-react";
import { LoginForm } from "@/components/LoginForm";

export default function LoginPage() {
  return (
    <main className="grid min-h-screen grid-cols-1 lg:grid-cols-[1.05fr_0.95fr]">
      <section className="flex items-center px-6 py-10 sm:px-10 lg:px-16">
        <div className="w-full max-w-md">
          <div className="flex items-center gap-3">
            <div className="flex size-11 items-center justify-center rounded-md bg-brand text-white">
              <Building2 aria-hidden="true" size={24} />
            </div>
            <div>
              <p className="text-xl font-semibold text-ink">SocietyDesk</p>
              <p className="text-sm text-slate-600">Maintenance management</p>
            </div>
          </div>

          <h1 className="mt-10 text-3xl font-semibold text-ink">
            Sign in to your society desk
          </h1>
          <p className="mt-3 text-sm leading-6 text-slate-600">
            Admin, resident, and security teams share one organized workspace.
          </p>

          <LoginForm />
        </div>
      </section>

      <section className="hidden bg-ink px-12 py-10 text-white lg:flex lg:items-end">
        <div className="max-w-lg">
          <div className="grid grid-cols-2 gap-3">
            {["Dues", "Complaints", "Notices", "Visitors"].map((item) => (
              <div
                className="rounded-lg border border-white/15 bg-white/10 p-5 backdrop-blur"
                key={item}
              >
                <p className="text-sm font-semibold">{item}</p>
                <div className="mt-8 h-2 rounded-full bg-coral" />
              </div>
            ))}
          </div>
          <p className="mt-8 text-4xl font-semibold leading-tight">
            One calm workspace for admins, residents, and security.
          </p>
        </div>
      </section>
    </main>
  );
}
