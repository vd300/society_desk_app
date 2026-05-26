export type Role = "ADMIN" | "RESIDENT" | "SECURITY";

export type User = {
  id: string;
  name: string;
  email: string;
  role: Role;
  is_active: boolean;
};

export type Session = {
  access_token: string;
  token_type: string;
  user: User;
};

export type StatMap = Record<string, number | string | null>;
