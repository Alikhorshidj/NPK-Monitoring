import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api/client";
import AuthLayout from "../components/AuthLayout";
import Input from "../components/ui/Input";
import Button from "../components/ui/Button";

export default function SignUp() {
  const nav = useNavigate();
  const [form, setForm] = useState({ firstname:"", lastname:"", username:"", password:"", password_confirm:"" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [ok, setOk] = useState("");

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setOk("");
    if (form.password.length < 6) return setError("Password must be at least 6 chars");
    if (form.password !== form.password_confirm) return setError("Passwords do not match");

    setLoading(true);
    try {
      const payload = { username: form.username, firstname: form.firstname, lastname: form.lastname, password: form.password, password_confirm: form.password_confirm };
//      await api.post("/profile/register", payload);
      const res = await api.post("/profile/register", payload);
      console.log("REGISTER OK:", res.status, res.data);
      setOk("Account created. You can sign in now.");
      setTimeout(()=> nav("/login"), 800);
    } catch (err) {
      console.log("REGISTER ERR:", err?.response?.status, err?.response?.data);
      const msg = err?.response?.data?.detail || err?.response?.data?.message || "Registration failed";
      setError(String(msg));
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthLayout
      title="Create your account"
      subtitle="Join and start monitoring fields"
      footer={<span>Already have an account? <Link to="/login" className="text-indigo-600 hover:underline">Sign in</Link></span>}
    >
      <form onSubmit={onSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input label="First name" placeholder="Sara" value={form.firstname} onChange={e=>setForm(v=>({...v, firstname:e.target.value}))} required />
          <Input label="Last name" placeholder="Ahmadi" value={form.lastname} onChange={e=>setForm(v=>({...v, lastname:e.target.value}))} required />
        </div>
        <Input label="Username" placeholder="yourname" value={form.username} onChange={e=>setForm(v=>({...v, username:e.target.value}))} required />
        {/* <Input label="Password" type="password" placeholder="••••••••" value={form.password} onChange={e=>setForm(v=>({...v, password:e.target.value}))} required /> */}
                <Input
                  label="Password"
                  type="password"
                  placeholder="••••••••"
                  value={form.password}
                  onChange={(e)=>setForm(v=>({...v, password:e.target.value}))}
                  required
                />
        {/* <Input label="Confirm password" type="password" placeholder="••••••••" value={form.password_confirm} onChange={e=>setForm(v=>({...v, password_confirm:e.target.value}))} required /> */}
                <Input
                  label="Password_Confirm"
                  type="password"
                  placeholder="••••••••"
                  value={form.password_confirmd}
                  onChange={(e)=>setForm(v=>({...v, password_confirm:e.target.value}))}
                  required
                />

        {error && <div className="rounded-lg bg-red-50 text-red-700 px-3 py-2 text-sm">{error}</div>}
        {ok && <div className="rounded-lg bg-emerald-50 text-emerald-700 px-3 py-2 text-sm">{ok}</div>}

        <Button type="submit" className="w-full" disabled={loading}>{loading? "Creating…" : "Create account"}</Button>
      </form>
    </AuthLayout>
  );
}