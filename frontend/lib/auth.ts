"use client";

import type { Session, User } from "./types";

const TOKEN_KEY = "societydesk_token";
const USER_KEY = "societydesk_user";

export function saveSession(session: Session) {
  localStorage.setItem(TOKEN_KEY, session.access_token);
  localStorage.setItem(USER_KEY, JSON.stringify(session.user));
}

export function getToken() {
  if (typeof window === "undefined") {
    return null;
  }
  return localStorage.getItem(TOKEN_KEY);
}

export function getUser(): User | null {
  if (typeof window === "undefined") {
    return null;
  }
  const raw = localStorage.getItem(USER_KEY);
  return raw ? (JSON.parse(raw) as User) : null;
}

export function clearSession() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

export function dashboardPath(role: User["role"]) {
  if (role === "ADMIN") {
    return "/admin/dashboard";
  }
  if (role === "SECURITY") {
    return "/security/dashboard";
  }
  return "/resident/dashboard";
}
