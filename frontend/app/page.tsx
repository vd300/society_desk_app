import Link from "next/link";

export default function HomePage() {
  return (
    <main className="flex min-h-screen items-center justify-center px-6">
      <div className="w-full max-w-md rounded-lg bg-white/88 p-8 text-center shadow-soft ring-1 ring-ink/10 backdrop-blur">
        <p className="text-sm font-semibold uppercase tracking-wide text-brand">
          SocietyDesk
        </p>
        <h1 className="mt-3 text-3xl font-semibold text-ink">
          Society operations, organized.
        </h1>
        <p className="mt-4 text-sm leading-6 text-slate-600">
          A focused workspace for dues, complaints, notices, and visitors.
        </p>
        <Link
          href="/login"
          className="mt-7 inline-flex h-11 items-center justify-center rounded-md bg-brand px-5 text-sm font-semibold text-white transition hover:bg-teal-800 focus:outline-none focus:ring-2 focus:ring-brand focus:ring-offset-2"
        >
          Open login
        </Link>
      </div>
    </main>
  );
}
