"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { DashboardShell } from "../components/DashboardShell";
import { StatusBadge } from "../components/StatusBadge";
import { Complaint, DashboardSummary, getComplaints, getDashboardSummary } from "../lib/api";

const statusColors: Record<string, string> = { NEW: "bg-blue-500", ASSIGNED: "bg-violet-500", IN_PROGRESS: "bg-amber-500", RESOLVED: "bg-emerald-500", CLOSED: "bg-slate-400" };
const priorityColors: Record<string, string> = { LOW: "bg-slate-400", MEDIUM: "bg-blue-500", HIGH: "bg-orange-500", CRITICAL: "bg-red-500" };

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [recent, setRecent] = useState<Complaint[]>([]);
  const [error, setError] = useState("");
  useEffect(() => { Promise.all([getDashboardSummary(), getComplaints({ page: 1, page_size: 5, sort_by: "created_at", sort_order: "desc" })]).then(([dashboard, complaints]) => { setSummary(dashboard); setRecent(complaints.items); }).catch((reason) => setError(reason.message)); }, []);
  const metrics = [
    ["Total complaints", summary?.total, "All customer issues", "text-brand"],
    ["New", summary?.new, "Awaiting assignment", "text-blue-600"],
    ["In progress", summary?.in_progress, "Being worked on", "text-amber-600"],
    ["Resolved", summary?.resolved, "Successfully resolved", "text-emerald-600"],
    ["Overdue", summary?.overdue, "Needs attention", "text-red-600"],
  ];
  return <DashboardShell><div className="mx-auto max-w-7xl">
    <div className="mb-8 flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
      <div><p className="mb-3 text-xs font-bold uppercase tracking-[.2em] text-brand">Overview</p><h2 className="text-3xl font-bold tracking-tight text-ink sm:text-4xl">Good morning, team.</h2><p className="mt-2 max-w-xl text-sm leading-6 text-muted">Keep a clear view of customer issues, priorities, and the work that needs attention today.</p></div>
      <Link href="/complaints/new" className="inline-flex items-center justify-center rounded-xl bg-brand px-4 py-3 text-sm font-bold text-white shadow-lg shadow-blue-200 hover:bg-blue-700">+ New complaint</Link>
    </div>
    {error && <p className="mb-5 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</p>}
    <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">{metrics.map(([label, value, hint, color]) => <article key={label as string} className="surface p-5"><div className="flex items-start justify-between"><p className="text-sm font-semibold text-muted">{label}</p><span className={`h-2.5 w-2.5 rounded-full bg-current ${color}`} /></div><p className={`mt-5 text-3xl font-bold tracking-tight ${color}`}>{value ?? "—"}</p><p className="mt-1 text-xs text-muted">{hint}</p></article>)}</section>
    <section className="surface mt-6 overflow-hidden"><div className="flex items-center justify-between border-b border-slate-100 px-5 py-5 sm:px-6"><div><h3 className="font-bold text-ink">Recent complaints</h3><p className="mt-1 text-sm text-muted">The latest customer conversations</p></div><Link href="/complaints" className="text-sm font-bold text-brand hover:text-blue-700">View all →</Link></div><div className="divide-y divide-slate-100">{recent.map((item) => <Link href={`/complaints/${item.id}`} key={item.id} className="flex flex-wrap items-center justify-between gap-3 px-5 py-4 hover:bg-slate-50 sm:px-6"><div className="min-w-0"><p className="truncate font-semibold text-ink">{item.subject}</p><p className="mt-1 text-xs text-muted">{item.customer_name} · <span className="font-semibold text-slate-400">#{item.id}</span></p></div><div className="flex items-center gap-4"><StatusBadge value={item.status} /><span className="hidden text-xs text-muted sm:block">{new Date(item.created_at).toLocaleDateString()}</span></div></Link>)}{!recent.length && <p className="p-10 text-center text-sm text-muted">{error ? "Unable to load complaints." : "No complaints yet."}</p>}</div></section>
    {summary && <section className="mt-6 grid gap-6 lg:grid-cols-2">{[["Complaints by status", summary.by_status, statusColors], ["Complaints by priority", summary.by_priority, priorityColors]].map(([title, values, colors]) => <div className="surface p-5 sm:p-6" key={title as string}><div className="flex items-center justify-between"><div><h3 className="font-bold text-ink">{title as string}</h3><p className="mt-1 text-xs text-muted">Distribution across all complaints</p></div><span className="rounded-lg bg-slate-50 px-2 py-1 text-xs font-bold text-muted">Live</span></div><div className="mt-6 space-y-4">{Object.entries(values as Record<string, number>).map(([label, value]) => <div key={label}><div className="mb-1.5 flex justify-between text-xs font-semibold text-muted"><span>{label.replace("_", " ")}</span><span>{value}</span></div><div className="h-2 rounded-full bg-slate-100"><div className={`h-2 rounded-full ${ (colors as Record<string, string>)[label] || "bg-brand" }`} style={{ width: `${summary.total ? Math.max(value ? 4 : 0, value / summary.total * 100) : 0}%` }} /></div></div>)}</div></div>)}</section>}
  </div></DashboardShell>;
}
