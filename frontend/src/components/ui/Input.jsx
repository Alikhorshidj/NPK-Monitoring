export default function Input({ label, error, className = "", ...props }) {
    return (
      <label className={`block text-sm ${className}`}>
        {label && <span className="mb-1 block text-gray-700 dark:text-gray-200">{label}</span>}
        <input
          className={`w-full rounded-xl border px-3 py-2 outline-none transition focus:ring-2 focus:ring-indigo-500/50 dark:bg-neutral-900 dark:border-neutral-700`}
          {...props}
        />
        {error && <span className="mt-1 block text-xs text-red-600">{error}</span>}
      </label>
    );
  }
  