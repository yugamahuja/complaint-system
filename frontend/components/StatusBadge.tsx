export function StatusBadge({ value }: { value: string }) {
  const styles: Record<string, string> = {
    NEW: "border-blue-200 bg-blue-50 text-blue-700",
    ASSIGNED: "border-violet-200 bg-violet-50 text-violet-700",
    IN_PROGRESS: "border-amber-200 bg-amber-50 text-amber-700",
    RESOLVED: "border-emerald-200 bg-emerald-50 text-emerald-700",
    CLOSED: "border-slate-200 bg-slate-100 text-slate-600",
  };
  return <span className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-[11px] font-bold uppercase tracking-wide ${styles[value] || "border-slate-200 bg-slate-100 text-slate-600"}`}><span className="h-1.5 w-1.5 rounded-full bg-current opacity-70" />{value.replace("_", " ")}</span>;
}
