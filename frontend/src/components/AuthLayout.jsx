import { Link } from "react-router-dom";

export default function AuthLayout({ title, subtitle, children, footer }) {
  return (
    <div className="min-h-screen grid md:grid-cols-2 bg-gradient-to-br from-indigo-50 to-white dark:from-neutral-950 dark:to-neutral-900">
      {/* Left panel */}
      <div className="flex items-center justify-center p-6 order-2 md:order-1">
        <div className="w-full max-w-md">
          <div className="mb-8 text-center">
            <h1 className="text-2xl font-bold tracking-tight text-neutral-900 dark:text-white">{title}</h1>
            {subtitle && (
              <p className="mt-2 text-sm text-neutral-600 dark:text-neutral-300">{subtitle}</p>
            )}
          </div>
          <div className="rounded-2xl border bg-white/80 backdrop-blur p-6 shadow-sm dark:bg-neutral-950 dark:border-neutral-800">
            {children}
          </div>
          {footer && <div className="mt-4 text-sm text-neutral-600 dark:text-neutral-300 text-center">{footer}</div>}
        </div>
      </div>

      {/* Right hero */}
      <div className="relative overflow-hidden order-1 md:order-2">
        <div className="absolute inset-0 -z-10">
          <div className="absolute -top-24 right-8 h-72 w-72 rounded-full bg-indigo-400/20 blur-3xl" />
          <div className="absolute -bottom-24 left-8 h-80 w-80 rounded-full bg-purple-400/20 blur-3xl" />
        </div>
        <div className="h-full w-full flex items-center justify-center p-8">
          <div className="max-w-md text-center">
            <div className="mx-auto mb-6 h-16 w-16 rounded-2xl bg-indigo-600/90" />
            <h2 className="text-3xl font-semibold text-neutral-900 dark:text-white">NPK Monitoring</h2>
            <p className="mt-2 text-neutral-600 dark:text-neutral-300">
              note.
            </p>
            {/* <div className="mt-6 text-xs text-neutral-500">© {new Date().getFullYear()} NPK</div> */}
          </div>
        </div>
      </div>
    </div>
  );
}