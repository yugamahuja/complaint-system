"use client";

import Link from "next/link";
import { FormEvent, useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import { DashboardShell } from "../../../components/DashboardShell";
import { StatusBadge } from "../../../components/StatusBadge";
import { assignComplaint, Complaint, getCategories, getComplaint, getEmployees, Category, Employee, transitionComplaint, updateComplaint } from "../../../lib/api";

const statuses: Complaint["status"][] = ["NEW", "ASSIGNED", "IN_PROGRESS", "RESOLVED", "CLOSED"];
const priorities: Complaint["priority"][] = ["LOW", "MEDIUM", "HIGH", "CRITICAL"];
const formatDate = (value?: string | null) => value ? new Date(value).toLocaleString() : "—";
const dateInput = (value: string) => value ? value.slice(0, 10) : "";

export default function ComplaintDetailPage() {
  const params = useParams<{ id: string }>();
  const id = params.id;
  const [complaint, setComplaint] = useState<Complaint | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionBusy, setActionBusy] = useState(false);
  const [editing, setEditing] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [form, setForm] = useState({ customer_name: "", customer_contact: "", subject: "", description: "", category_id: "", priority: "MEDIUM" as Complaint["priority"], expected_resolution_date: "" });
  const [assignee, setAssignee] = useState("");

  const load = async () => {
    setLoading(true);
    try {
      const [item, loadedCategories, loadedEmployees] = await Promise.all([getComplaint(id), getCategories(), getEmployees()]);
      setComplaint(item); setCategories(loadedCategories); setEmployees(loadedEmployees);
      setForm({ customer_name: item.customer_name, customer_contact: item.customer_contact, subject: item.subject, description: item.description, category_id: String(item.category_id), priority: item.priority, expected_resolution_date: dateInput(item.expected_resolution_date) });
      setAssignee(item.assigned_employee_id ? String(item.assigned_employee_id) : "");
      setError("");
    } catch (reason) { setError(reason instanceof Error ? reason.message : "Unable to load complaint."); }
    finally { setLoading(false); }
  };
  useEffect(() => { load(); }, [id]);
  const overdue = useMemo(() => complaint && !["RESOLVED", "CLOSED"].includes(complaint.status) && new Date(`${complaint.expected_resolution_date}T23:59:59`) < new Date(), [complaint]);
  const change = (key: keyof typeof form, value: string) => setForm((current) => ({ ...current, [key]: value }));
  const runAction = async (action: () => Promise<Complaint>, message: string) => {
    setActionBusy(true); setError(""); setSuccess("");
    try { const updated = await action(); setComplaint(updated); setSuccess(message); await load(); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Action failed."); }
    finally { setActionBusy(false); }
  };
  async function save(event: FormEvent) {
    event.preventDefault();
    await runAction(() => updateComplaint(id, { ...form, category_id: Number(form.category_id) }), "Complaint details saved.");
    setEditing(false);
  }
  if (loading) return <DashboardShell><div className="mx-auto max-w-6xl"><div className="surface animate-pulse p-8"><div className="h-4 w-32 rounded bg-slate-200" /><div className="mt-4 h-8 w-2/3 rounded bg-slate-200" /><div className="mt-3 h-4 w-1/3 rounded bg-slate-100" /></div></div></DashboardShell>;
  if (!complaint) return <DashboardShell><div className="mx-auto max-w-6xl"><p className="rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">{error || "Complaint not found."}</p><Link href="/complaints" className="mt-4 inline-block text-sm font-bold text-brand">← Back to complaints</Link></div></DashboardShell>;
  const nextStatus = statuses[statuses.indexOf(complaint.status) + 1];
  return <DashboardShell><div className="mx-auto max-w-6xl">
    <Link href="/complaints" className="text-sm font-bold text-brand hover:text-blue-700">← Back to complaints</Link>
    <div className="surface mt-5 flex flex-wrap items-start justify-between gap-5 p-5 sm:p-7"><div><p className="text-xs font-bold uppercase tracking-[.2em] text-brand">Complaint #{complaint.id}</p><h1 className="mt-2 max-w-3xl text-2xl font-bold tracking-tight text-ink sm:text-3xl">{complaint.subject}</h1><p className="mt-2 text-sm text-muted">{complaint.customer_name} · {complaint.customer_contact}</p></div><StatusBadge value={complaint.status} /></div>
    {overdue && <div className="mt-4 flex items-center gap-3 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-bold text-red-700">⚠ <span>Overdue</span><span className="font-normal text-red-600">Expected resolution {new Date(complaint.expected_resolution_date).toLocaleDateString()}</span></div>}
    {(error || success) && <p className={`mt-4 rounded-xl border p-4 text-sm ${error ? "border-red-200 bg-red-50 text-red-700" : "border-emerald-200 bg-emerald-50 text-emerald-700"}`}>{error || success}</p>}
    <div className="mt-6 grid gap-6 lg:grid-cols-[1.5fr_1fr]">
      <div className="space-y-6">
        <section className="surface p-5 sm:p-6"><h2 className="text-lg font-bold text-ink">Workflow</h2><div className="mt-5 flex flex-wrap items-center gap-2">{statuses.map((status, index) => <div key={status} className="flex items-center gap-2"><div className={`rounded-full border px-3 py-2 text-[11px] font-bold uppercase tracking-wide ${statuses.indexOf(complaint.status) >= index ? "border-brand bg-brand text-white shadow-sm shadow-blue-200" : "border-slate-200 bg-slate-50 text-muted"}`}>{status.replace("_", " ")}</div>{index < statuses.length - 1 && <span className="text-slate-300">→</span>}</div>)}</div><div className="mt-6 flex flex-wrap gap-3">{complaint.status === "NEW" && <><select value={assignee} onChange={(e) => setAssignee(e.target.value)} className="field px-3 py-2 text-sm"><option value="">Assign employee…</option>{employees.map((employee) => <option key={employee.id} value={employee.id}>{employee.name} · {employee.department}</option>)}</select><button disabled={!assignee || actionBusy} onClick={() => runAction(() => assignComplaint(id, Number(assignee)), "Complaint assigned.")} className="rounded-xl bg-brand px-4 py-2 text-sm font-bold text-white shadow-lg shadow-blue-200 disabled:opacity-50">Assign</button></>}{nextStatus && complaint.status !== "NEW" && <button disabled={actionBusy} onClick={() => runAction(() => transitionComplaint(id, nextStatus), `Moved to ${nextStatus.replace("_", " ").toLowerCase()}.`)} className="rounded-xl bg-brand px-4 py-2 text-sm font-bold text-white shadow-lg shadow-blue-200 disabled:opacity-50">Move to {nextStatus.replace("_", " ")}</button>}</div></section>
        <section className="surface p-5 sm:p-6"><div className="flex items-center justify-between"><div><h2 className="text-lg font-bold text-ink">Complaint details</h2><p className="mt-1 text-sm text-muted">Customer, issue, and timing information</p></div><button onClick={() => setEditing(!editing)} className="rounded-xl border border-slate-200 px-3 py-2 text-sm font-bold text-muted hover:bg-slate-50">{editing ? "Cancel" : "Edit details"}</button></div>{editing ? <form onSubmit={save} className="mt-5 space-y-4">{(["customer_name", "customer_contact", "subject"] as const).map((key) => <label key={key} className="block text-sm font-semibold text-ink">{key.replace("_", " ")}<input required value={form[key]} onChange={(e) => change(key, e.target.value)} className="field mt-2 w-full px-3 py-2.5" /></label>)}<label className="block text-sm font-semibold text-ink">Description<textarea required rows={5} value={form.description} onChange={(e) => change("description", e.target.value)} className="field mt-2 w-full px-3 py-2.5" /></label><div className="grid gap-4 sm:grid-cols-3"><label className="text-sm font-semibold">Category<select value={form.category_id} onChange={(e) => change("category_id", e.target.value)} className="field mt-2 w-full px-2 py-2.5">{categories.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}</select></label><label className="text-sm font-semibold">Priority<select value={form.priority} onChange={(e) => change("priority", e.target.value)} className="field mt-2 w-full px-2 py-2.5">{priorities.map((p) => <option key={p}>{p}</option>)}</select></label><label className="text-sm font-semibold">Expected resolution<input type="date" required value={form.expected_resolution_date} onChange={(e) => change("expected_resolution_date", e.target.value)} className="field mt-2 w-full px-2 py-2.5" /></label></div><button disabled={actionBusy} className="rounded-xl bg-brand px-4 py-2.5 text-sm font-bold text-white shadow-lg shadow-blue-200 disabled:opacity-50">{actionBusy ? "Saving…" : "Save changes"}</button></form> : <dl className="mt-6 grid gap-6 sm:grid-cols-2"><div><dt className="text-[10px] font-bold uppercase tracking-[.15em] text-slate-400">Customer</dt><dd className="mt-2 text-sm font-semibold leading-6 text-ink">{complaint.customer_name}<br /><span className="font-normal text-muted">{complaint.customer_contact}</span></dd></div><div><dt className="text-[10px] font-bold uppercase tracking-[.15em] text-slate-400">Category / priority</dt><dd className="mt-2 text-sm font-semibold text-ink">{complaint.category_name || `Category #${complaint.category_id}`} · {complaint.priority}</dd></div><div className="sm:col-span-2"><dt className="text-[10px] font-bold uppercase tracking-[.15em] text-slate-400">Description</dt><dd className="mt-2 whitespace-pre-wrap text-sm leading-6 text-ink">{complaint.description}</dd></div><div><dt className="text-[10px] font-bold uppercase tracking-[.15em] text-slate-400">Expected resolution</dt><dd className="mt-2 text-sm font-semibold text-ink">{formatDate(complaint.expected_resolution_date)}</dd></div><div><dt className="text-[10px] font-bold uppercase tracking-[.15em] text-slate-400">Assigned employee</dt><dd className="mt-2 text-sm font-semibold text-ink">{complaint.assigned_employee_name || employees.find((e) => e.id === complaint.assigned_employee_id)?.name || "Unassigned"}</dd></div></dl>}</section>
      </div>
      <section className="surface p-5 sm:p-6"><h2 className="text-lg font-bold text-ink">Activity timeline</h2><p className="mt-1 text-sm text-muted">A complete history of this complaint</p><div className="mt-6 space-y-5">{(complaint.activities || []).slice().sort((a, b) => +new Date(b.created_at) - +new Date(a.created_at)).map((activity) => <div key={activity.id} className="relative border-l-2 border-slate-200 pl-5"><div className="absolute -left-[7px] top-0 flex h-3 w-3 rounded-full border-2 border-white bg-brand shadow-sm" /><p className="text-sm font-bold text-ink">{activity.action.replace("_", " ")}</p><p className="mt-1 text-sm leading-6 text-muted">{activity.description}</p><p className="mt-1 text-[11px] font-semibold text-slate-400">{formatDate(activity.created_at)}{activity.performed_by ? ` · employee #${activity.performed_by}` : ""}</p></div>)}{!complaint.activities?.length && <p className="rounded-xl bg-slate-50 p-4 text-sm text-muted">No activity recorded yet.</p>}</div><dl className="mt-8 space-y-2 border-t border-slate-100 pt-5 text-sm"><div className="flex justify-between py-1"><dt className="text-muted">Created</dt><dd className="font-semibold text-ink">{formatDate(complaint.created_at)}</dd></div><div className="flex justify-between py-1"><dt className="text-muted">Updated</dt><dd className="font-semibold text-ink">{formatDate(complaint.updated_at)}</dd></div><div className="flex justify-between py-1"><dt className="text-muted">Resolved</dt><dd className="font-semibold text-ink">{formatDate(complaint.resolved_at)}</dd></div><div className="flex justify-between py-1"><dt className="text-muted">Closed</dt><dd className="font-semibold text-ink">{formatDate(complaint.closed_at)}</dd></div></dl></section>
    </div>
  </div></DashboardShell>;
}
