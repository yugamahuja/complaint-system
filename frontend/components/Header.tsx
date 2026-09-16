"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

export function Header() {
  const pathname = usePathname();
  return (
    <header className="sticky top-0 z-10 flex min-h-20 items-center justify-between border-b border-slate-200/80 bg-white/95 px-4 backdrop-blur sm:px-6 lg:px-10">
      <div>
        <p className="text-[11px] font-bold uppercase tracking-[.16em] text-brand">Customer experience workspace</p>
        <h1 className="mt-1 text-lg font-bold text-ink sm:text-xl">Complaint management</h1>
      </div>
      <div className="flex items-center gap-4">
        <nav className="hidden items-center gap-1 sm:flex md:hidden" aria-label="Mobile navigation">
          <Link href="/" className={`rounded-lg px-3 py-2 text-sm font-semibold ${pathname === "/" ? "bg-blue-50 text-brand" : "text-muted"}`}>Overview</Link>
          <Link href="/complaints" className={`rounded-lg px-3 py-2 text-sm font-semibold ${pathname.startsWith("/complaints") ? "bg-blue-50 text-brand" : "text-muted"}`}>Complaints</Link>
        </nav>
        <div className="hidden h-9 w-9 items-center justify-center rounded-xl bg-slate-100 text-sm font-bold text-slate-600 sm:flex">CM</div>
        <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-brand text-xs font-bold text-white sm:hidden">CC</div>
        <div className="hidden text-right sm:block">
          <p className="text-xs font-semibold text-ink">Operations team</p>
          <p className="text-[11px] text-muted">Customer support</p>
        </div>
      </div>
    </header>
  );
}
