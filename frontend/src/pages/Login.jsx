import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api/client";
import AuthLayout from "../components/AuthLayout";
import Input from "../components/ui/Input";
import Button from "../components/ui/Button";

export default function Login(){
  const nav = useNavigate();
  const [form, setForm] = useState({ username: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function onSubmit(e){
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const { data } = await api.post("/profile/login", form);
      const access = data?.access_token || data?.access || data?.token;
      const refresh = data?.refresh_token || data?.refresh;
      if (access) localStorage.setItem("access_token", access);
      if (refresh) localStorage.setItem("refresh_token", refresh);
      nav("/");
    } catch (err){
      const msg = err?.response?.data?.detail || err?.response?.data?.message || "Login failed";
      setError(String(msg));
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthLayout
      title="Welcome back"
      subtitle="Log in to access your dashboard"
      footer={<span>New here? <Link to="/signup" className="text-indigo-600 hover:underline">Create an account</Link></span>}
    >
      <form onSubmit={onSubmit} className="space-y-4">
        <Input
          label="Username"
          placeholder="yourname"
          value={form.username}
          onChange={(e)=>setForm(v=>({...v, username:e.target.value}))}
          required
        />
        <Input
          label="Password"
          type="password"
          placeholder="••••••••"
          value={form.password}
          onChange={(e)=>setForm(v=>({...v, password:e.target.value}))}
          required
        />
        {error && <div className="rounded-lg bg-red-50 text-red-700 px-3 py-2 text-sm">{error}</div>}
        <Button type="submit" className="w-full" disabled={loading}>{loading? "Signing in…" : "Sign In"}</Button>
      </form>
    </AuthLayout>
  );
}
