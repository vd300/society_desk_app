"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { LockKeyhole, Mail } from "lucide-react";
import { apiRequest } from "@/lib/api";
import { dashboardPath, saveSession } from "@/lib/auth";
import type { Session } from "@/lib/types";

export function LoginForm() {
  const router = useRouter();
  const [email, setEmail] = useState("admin@societydesk.com");
  const [password, setPassword] = useState("password123");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const session = await apiRequest<Session>("/auth/login", {
        method: "POST",
        auth: false,
        body: JSON.stringify({ email, password }),
      });
      saveSession(session);
      router.push(dashboardPath(session.user.role));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to sign in");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form
      className="mt-8 space-y-5 rounded-lg bg-white p-6 shadow-soft ring-1 ring-ink/10"
      onSubmit={onSubmit}
    >
      <label className="block">
        <span className="text-sm font-medium text-ink">Email</span>
        <span className="mt-2 flex h-11 items-center gap-3 rounded-md border border-slate-300 bg-white px-3 focus-within:border-brand focus-within:ring-2 focus-within:ring-brand/20">
          <Mail aria-hidden="true" className="text-slate-500" size={18} />
          <input
            className="w-full border-0 bg-transparent text-sm text-ink outline-none placeholder:text-slate-400"
            name="email"
            onChange={(event) => setEmail(event.target.value)}
            type="email"
            value={email}
          />
        </span>
      </label>

      <label className="block">
        <span className="text-sm font-medium text-ink">Password</span>
        <span className="mt-2 flex h-11 items-center gap-3 rounded-md border border-slate-300 bg-white px-3 focus-within:border-brand focus-within:ring-2 focus-within:ring-brand/20">
          <LockKeyhole aria-hidden="true" className="text-slate-500" size={18} />
          <input
            className="w-full border-0 bg-transparent text-sm text-ink outline-none placeholder:text-slate-400"
            name="password"
            onChange={(event) => setPassword(event.target.value)}
            type="password"
            value={password}
          />
        </span>
      </label>

      {error ? <p className="text-sm font-medium text-rose-700">{error}</p> : null}

      <button
        className="flex h-11 w-full items-center justify-center rounded-md bg-brand text-sm font-semibold text-white transition hover:bg-teal-800 focus:outline-none focus:ring-2 focus:ring-brand focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60"
        disabled={loading}
        type="submit"
      >
        {loading ? "Signing in" : "Sign in"}
      </button>
    </form>
  );
}
