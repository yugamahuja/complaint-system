"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navigation = [
  { label: "Overview", icon: "▦", href: "/" },
  { label: "Complaints", icon: "□", href: "/complaints" },
];

export function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="hidden w-64 shrink-0 border-r border-slate-200/80 bg-white px-5 py-7 md:block">
      <div className="mb-12 flex items-center gap-3 px-2">
        <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-brand text-sm font-bold text-white shadow-lg shadow-blue-200">
          CC
        </div>
        <div>
          <p className="text-sm font-bold text-ink">ClearCase</p>
          <p className="text-xs text-muted">Management system</p>
        </div>
      </div>
      <p className="mb-3 px-3 text-[10px] font-bold uppercase tracking-[.18em] text-slate-400">Workspace</p>
      <nav aria-label="Main navigation" className="space-y-1.5">
        {navigation.map((item) => (
          <Link
            href={item.href}
            key={item.label}
            className={`flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-semibold ${
              pathname === item.href
                ? "bg-blue-50 text-brand shadow-sm"
                : "text-slate-500 hover:bg-slate-50 hover:text-ink"
            }`}
          >
            <span className="w-5 text-center text-base">{item.icon}</span>
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
