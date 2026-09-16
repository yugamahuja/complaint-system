import { Header } from "./Header";
import { Sidebar } from "./Sidebar";

export function DashboardShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen bg-canvas">
      <Sidebar />
      <div className="min-w-0 flex-1">
        <Header />
        <main className="p-4 sm:p-6 lg:p-10">{children}</main>
      </div>
    </div>
  );
}
